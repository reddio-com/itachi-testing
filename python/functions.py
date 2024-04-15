
import time
import random
from pathlib import Path

from starknet_py.net.full_node_client import FullNodeClient
from starknet_py.contract import Contract
from starknet_py.net.account.account import Account
from starknet_py.net.signer.stark_curve_signer import KeyPair
from starknet_py.net.client_models import TransactionExecutionStatus, TransactionStatus, Call
from starknet_py.hash.address import compute_address
from starknet_py.net.client_errors import ClientError

from abi import ERC20_ABI

FULLNODE_URL = "http://127.0.0.1:9091/v0_6"
CHAIN_ID = 0x534e5f474f45524c49

ETH_ADDRESS = 0x49d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7
AA_ADDRESS = 0x4

class Itachi(object):
    def __init__(self):
        self._client = FullNodeClient(node_url=FULLNODE_URL)
        self._chain = 0x534e5f474f45524c49
        self._eth_contract = Contract(
            address=ETH_ADDRESS,
            provider=self._client,
            cairo_version= 0,
            abi = ERC20_ABI,
        )
        self._account = Account(
            client=self._client,
            address=AA_ADDRESS,
            key_pair=KeyPair(12, 34),
            chain=self._chain,
        )
        self.account = Account(
            client=self._client,
            address=AA_ADDRESS,
            key_pair=KeyPair(12, 34),
            chain=self._chain,
        )
    
    def wait_for_transaction_sync(self, tx):
        while True:
            try:
                receipt = self._client.wait_for_tx_sync(tx)
                return receipt
            except ClientError as e:
                if 'Internal Error' in str(e):
                    continue
                else:
                    raise e  # If it's another error, raise it.

    def get_eth_balance(self, address=AA_ADDRESS):
        eth_balance = self._eth_contract.functions["balanceOf"].call_sync(address)[0]
        return eth_balance

    def get_latest_block(self):
        block = self._client.get_block_sync(block_number="latest")
        return block

    def transfer_eth_multi(self, amount = 5000*10**18, recipients = [0x050953649BfFC4878db6CfBe46E52f89512eD7Cdcf0B1AadDed3BFBA859BB678]):
        calls = []
        for recipient in recipients:
            calls.append(self._eth_contract.functions["transfer"].prepare_call(recipient, amount))
        
        nonce = self.get_nonce()
        transaction_resp = self._account.execute_v1_sync(calls=calls, max_fee=int(1e18),nonce=nonce)
        tx_hash = transaction_resp.transaction_hash
        receipt_status = self._client.get_transaction_status_sync(tx_hash)
        status = receipt_status.finality_status
        while status != TransactionStatus.ACCEPTED_ON_L2:
            receipt_status = self._client.get_transaction_status_sync(tx_hash)
            status = receipt_status.finality_status

        receipt = self._client.get_transaction_receipt_sync(tx_hash)
        return receipt
    
    def transfer_eth(self, amount = 5000*10**18, recipient = 0x050953649BfFC4878db6CfBe46E52f89512eD7Cdcf0B1AadDed3BFBA859BB678):
        calls = [
            self._eth_contract.functions["transfer"].prepare_call(recipient, amount),
        ]
        nonce = self.get_nonce()
        transaction_resp = self._account.execute_v1_sync(calls=calls, max_fee=int(1e18),nonce=nonce)
        tx_hash = transaction_resp.transaction_hash
        receipt_status = self._client.get_transaction_status_sync(tx_hash)
        status = receipt_status.finality_status
        while status != TransactionStatus.ACCEPTED_ON_L2:
            receipt_status = self._client.get_transaction_status_sync(tx_hash)
            status = receipt_status.finality_status

        receipt = self._client.get_transaction_receipt_sync(tx_hash)
        return receipt

    def transfer(self, from_account, to_account, amount):
        calls = [
            self._eth_contract.functions["transfer"].prepare_call(to_account.address, amount),
        ]

        transaction_response = from_account.execute_v1_sync(calls=calls, max_fee=int(1e18))
        tx_hash = transaction_response.transaction_hash
        receipt_status = self._client.get_transaction_status_sync(tx_hash)
        status = receipt_status.finality_status
        while status != TransactionStatus.ACCEPTED_ON_L2:
            time.sleep(0.5)
            receipt_status = self._client.get_transaction_status_sync(tx_hash)
            status = receipt_status.finality_status

        receipt = self._client.get_transaction_receipt_sync(tx_hash)
        return receipt

    def transfer_no_wait(self, from_account, to_account, amount,nonce):
        calls = [
            self._eth_contract.functions["transfer"].prepare_call(to_account.address, amount),
        ]
        transaction_response = from_account.execute_v1_sync(calls=calls, max_fee=int(1e18),nonce=nonce)
        tx_hash = transaction_response.transaction_hash
        return tx_hash
    
    def get_nonce(self):
        nonce = self._account.get_nonce_sync()
        return nonce
    
    def generate_private_key(self):
        private_key = random.randint(0, 2**251)
        return private_key
    
    def create_argent_account_no_deploy(self,private_key = 0x050953649BfFC4878db6CfBe46E52f89812eD7Cdcf0B1AadDed3BFBA859BB687,  class_hash = 0x1a736d6ed154502257f02b1ccdf4d9d1089f80811cd6acad48e6b6a9d1f2003, salt = 0x03Db4f4fAd96e5444BDC1D0286f42948763AF1B7BdB7873c08D28CB5129d4aac):
        key_pair = KeyPair.from_private_key(private_key)
        constructor_args = [key_pair.public_key,0x0]
        address = compute_address(
            salt=salt,
            class_hash=class_hash,
            constructor_calldata=constructor_args,
        )
        return address, private_key
    
    def deploy_argent_account(self, address, private_key, class_hash = 0x1a736d6ed154502257f02b1ccdf4d9d1089f80811cd6acad48e6b6a9d1f2003, salt = 0x03Db4f4fAd96e5444BDC1D0286f42948763AF1B7BdB7873c08D28CB5129d4aac):
        key_pair = KeyPair.from_private_key(private_key)
        constructor_args = [key_pair.public_key,0x0]
        account_deployment_result = Account.deploy_account_v1_sync(
            address=address,
            class_hash=class_hash,
            salt=salt,
            key_pair=key_pair,
            client=self._client,
            chain=self._chain,
            constructor_calldata=constructor_args,
            max_fee=int(1e17),
        )
        # Wait for deployment transaction to be accepted
        while True:
            try:
                account_deployment_result.wait_for_acceptance_sync()
                break
            except ClientError as e:
                if 'Internal Error' in str(e):
                    continue
                else:
                    raise e  # If it's another error, raise it.
        # From now on, account can be used as usual
        account = account_deployment_result.account
        print("private key:", str(hex(private_key)),"Address:", hex(account.address))
        return account, private_key

    def create_argent_account(self,private_key = 0x050953649BfFC4878db6CfBe46E52f89812eD7Cdcf0B1AadDed3BFBA859BB687,  class_hash = 0x1a736d6ed154502257f02b1ccdf4d9d1089f80811cd6acad48e6b6a9d1f2003, salt = 0x03Db4f4fAd96e5444BDC1D0286f42948763AF1B7BdB7873c08D28CB5129d4aac):
        key_pair = KeyPair.from_private_key(private_key)
        constructor_args = [key_pair.public_key,0x0]
        address = compute_address(
            salt=salt,
            class_hash=class_hash,
            constructor_calldata=constructor_args,
        )
        print("Address: ", hex(address))

        # receipt = self.transfer_eth(recipient=address,amount = 1000*10**18)

        # if receipt.execution_status != TransactionExecutionStatus.SUCCEEDED:
        #     print("Transfer ETH failed due to status"+ str(receipt.execution_status))
        #     print("Transaction hash: "+ str(receipt.transaction_hash))
        #     print("Reason: "+ str(receipt.revert_reason))
        #     return

        account_deployment_result = Account.deploy_account_v1_sync(
            address=address,
            class_hash=class_hash,
            salt=salt,
            key_pair=key_pair,
            client=self._client,
            chain=self._chain,
            constructor_calldata=constructor_args,
            max_fee=int(1e17),
        )
        # Wait for deployment transaction to be accepted
        while True:
            try:
                account_deployment_result.wait_for_acceptance_sync()
                break
            except ClientError as e:
                if 'Internal Error' in str(e):
                    continue
                else:
                    raise e  # If it's another error, raise it.

        # From now on, account can be used as usual
        account = account_deployment_result.account
        print("private key:", str(hex(private_key)),"Address:", hex(account.address))
        return account, private_key
    
    def declare_class(self, address, key, class_file="data/cool_sierra_contract_class.json", casm_file="data/cool_compiled_class.casm"):
        account = Account(
            client=self._client,
            address=address,
            key_pair=KeyPair.from_private_key(key=key),
            chain=self._chain,
        )
        declare_result = Contract.declare_v2_sync(
            account=account,
            compiled_contract=Path(class_file).read_text(),
            compiled_contract_casm=Path(casm_file).read_text(),
            max_fee=int(1e16),
        )
        time.sleep(10)
        declare_result.wait_for_acceptance_sync()

        print("class hash", hex(declare_result.class_hash))
        return declare_result
    
    def deploy_contract(self, address, key, class_file="data/cool_sierra_contract_class.json", casm_file="data/cool_compiled_class.casm"):
        declare_result = self.declare_class(address, key, class_file, casm_file)

        deploy_result = declare_result.deploy_sync(
            max_fee=int(1e16)
        )
        time.sleep(10)

        deploy_result.wait_for_acceptance_sync()

        contract = deploy_result.deployed_contract
        print("contract address", hex(contract.address))
        return hex(declare_result.class_hash), hex(contract.address)
    
    def test_transfer_eth(self):
        amount = 5000*10**18

        recipient = 0x050953649BfFC4878db6CfBe46E52f89512eD7Cdcf0B1AadDed3BFBA859BB678
        recipient_eth_balance_before = self.get_eth_balance(address=recipient)
        sender_eth_balance_before = self.get_eth_balance(address=AA_ADDRESS)

        receipt = self.transfer_eth(amount, recipient)
        if receipt.execution_status != TransactionExecutionStatus.SUCCEEDED:
            print("Transfer failed due to status")
            return

        recipient_eth_balance_after = self.get_eth_balance(address=recipient)
        sender_eth_balance_after = self.get_eth_balance(address=AA_ADDRESS)
        nonce_after = self.get_nonce()

        recipient_eth_balance_delta = recipient_eth_balance_after - recipient_eth_balance_before
        sender_eth_balance_delta = sender_eth_balance_before - sender_eth_balance_after

        recipient = hex(recipient)
        tx = hex(receipt.transaction_hash)
        print(f"Eth balance delta: {recipient_eth_balance_delta} of recipient: {recipient} after transaction: {tx}")
        print(f"Eth balance delta: {sender_eth_balance_delta} of sender: {AA_ADDRESS} after transaction: {tx}")
        if recipient_eth_balance_delta == amount and sender_eth_balance_delta == amount:
            print("Transfer successful")
        else:
            print("Transfer failed")
    
    def test_nonce(self):
        nonce = self.get_nonce()
        print(f"Nonce: {nonce}")
        amount = 5000*10**18
        recipient = 0x050953649BfFC4878db6CfBe46E52f89512eD7Cdcf0B1AadDed3BFBA859BB678
        receipt = self.transfer_eth(amount, recipient)
        if receipt.execution_status != TransactionExecutionStatus.SUCCEEDED:
            print("Transfer failed due to status")
            return
        
        nonce_after = self.get_nonce()
        print(f"Nonce after: {nonce_after}")
        if nonce_after == nonce + 1:
            print("Nonce test successful")
        else:
            print("Nonce test failed")

    def test_create_argent_account(self):
        self.create_argent_account()
    
    def test_declare_class(self):
        private_key = self.generate_private_key()
        address, key = self.create_argent_account(private_key)
        declare_result = self.declare_class(address, key)
    
    def test_deploy(self):
        private_key = self.generate_private_key()
        address, key = self.create_argent_account(private_key)
        class_hash, contract_address = self.deploy_contract(address, key)
        print(f"class hash: {class_hash}, contract address: {contract_address}")

if __name__ == "__main__":
    itachi = Itachi()
    itachi.create_argent_account()
    # balance = itachi.get_eth_balance(AA_ADDRESS)
    # print(balance)
    # itachi.transfer_eth()
    # print(itachi.get_eth_balance(AA_ADDRESS))
    # print(itachi.get_eth_balance(0x050953649BfFC4878db6CfBe46E52f89512eD7Cdcf0B1AadDed3BFBA859BB678))
    # itachi.test_transfer_eth()
    # itachi.test_nonce()
    # itachi.test_deploy()