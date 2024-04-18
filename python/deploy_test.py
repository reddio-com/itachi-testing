from functions import Itachi
from starknet_py.net.client_models import TransactionExecutionStatus, TransactionStatus, Call
import time

if __name__ == "__main__":
    itachi = Itachi()
    private_key1 = 0x050953649BfFC4878db6CfBe46E52f89812eD7Cdcf0B1AadDed3BFBA859BB681
    address, _ = itachi.create_argent_account_no_deploy(private_key=private_key1)
    itachi.transfer_eth_multi(1000*10**18,[address])

    # Check balance
    account1_balance = itachi.get_eth_balance(address=address)
    print(f"account1 balance: {account1_balance}")

    account, priv = itachi.deploy_argent_account(address, private_key1)
    print(f"account: {account}")

    class_hash, contract_address, contract = itachi.deploy_contract(address=account.address, key=private_key1,class_file="data/testing_origin.contract_class.json",casm_file="data/testing_origin.compiled_contract_class.json")

    calls = [
        contract.functions['set_value'].prepare_call(1),
    ]
    nonce = account.get_nonce_sync()
    transaction_resp = account.execute_v1_sync(calls=calls, max_fee=int(1e18),nonce=nonce)
    tx_hash = transaction_resp.transaction_hash
    print(f"tx_hash: {tx_hash}")