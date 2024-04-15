from functions import Itachi
from starknet_py.net.client_models import TransactionExecutionStatus, TransactionStatus, Call
import time

if __name__ == "__main__":
    itachi = Itachi()
    private_key1 = 0x050953649BfFC4878db6CfBe46E52f89812eD7Cdcf0B1AadDed3BFBA859BB681
    private_key2 = 0x050953649BfFC4878db6CfBe46E52f89812eD7Cdcf0B1AadDed3BFBA859BB682
    account1, priv = itachi.create_argent_account(private_key=private_key1)
    account2, priv = itachi.create_argent_account(private_key=private_key2)

    account1_balance = itachi.get_eth_balance(address=account1.address)
    print(f"account1 balance: {account1_balance}")
    account2_balance = itachi.get_eth_balance(address=account2.address)
    print(f"account2 balance: {account2_balance}")

    # One account transfers 1 ETH to another account 1000 times, with the balance decreasing by 1000 ETH in the end.
    # Calculate time interval to AcceptedOnL2
    times = 100
    amount = 10*10**18
    from_account = account1
    to_account = account2

    tx_hash_list = []
    for i in range(times):
        print("Sending transaction: ", i+1)
        tx_hash = itachi.transfer_no_wait(from_account=from_account, to_account=to_account, amount=amount, nonce=i+1)
        print("Tx hash: ", hex(tx_hash))
        tx_hash_list.append(tx_hash)
    
    print("All transactions sent")
    start_time = time.time()
    for tx_hash in tx_hash_list:
        receipt_status = itachi._client.get_transaction_status_sync(tx_hash)
        status = receipt_status.finality_status
        while status != TransactionStatus.ACCEPTED_ON_L2:
            receipt_status = itachi._client.get_transaction_status_sync(tx_hash)
            status = receipt_status.finality_status
        print("Tx: ", hex(tx_hash), " status: ", status)
    end_time = time.time()
    print("All transactions accepted on L2")
    print("Time: ", end_time - start_time)

    account1_balance = itachi.get_eth_balance(address=account1.address)
    print(f"account1 balance: {account1_balance}")
    account2_balance = itachi.get_eth_balance(address=account2.address)
    print(f"account2 balance: {account2_balance}")

    time.sleep(10)

    account1_balance = itachi.get_eth_balance(address=account1.address)
    print(f"account1 balance: {account1_balance}")
    account2_balance = itachi.get_eth_balance(address=account2.address)
    print(f"account2 balance: {account2_balance}")