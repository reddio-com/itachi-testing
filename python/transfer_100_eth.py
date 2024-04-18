from functions import Itachi
import time

import threading

def transfer_and_print_balance(itachi, from_account, to_account, amount, times):
    for _ in range(times):
        itachi.transfer(from_account=from_account, to_account=to_account, amount=amount)
        from_balance = itachi.get_eth_balance(address=from_account.address)
        to_balance = itachi.get_eth_balance(address=to_account.address)
        print("Transfering amount: ", amount, " from ", str(hex(from_account.address)), " to ", str(hex(to_account.address)))
        print("Current balance: ", "from: ", from_balance, " to: ", to_balance)

if __name__ == "__main__":
    itachi = Itachi()
    private_key1 = 0x050953649BfFC4878db6CfBe46E52f89812eD7Cdcf0B1AadDed3BFBA859BB681
    private_key2 = 0x050953649BfFC4878db6CfBe46E52f89812eD7Cdcf0B1AadDed3BFBA859BB682
    address1, priv = itachi.create_argent_account_no_deploy(private_key=private_key1)
    address2, priv = itachi.create_argent_account_no_deploy(private_key=private_key2)

    itachi.transfer_eth_multi(1*10**18,[address1,address2])

    account1, _ = itachi.deploy_argent_account(address1, private_key1)
    account2, _ = itachi.deploy_argent_account(address2, private_key2)

    # One account is transferred 100 times to another, 1 ETH each time, the last balance is reduced by 100 ETH
    thread1 = threading.Thread(target=transfer_and_print_balance, args=(itachi, account1, account2, 10*10**18, 100))

    thread1.start()

    thread1.join()

    account1_balance = itachi.get_eth_balance(address=account1.address)
    print(f"account1 balance: {account1_balance}")
    account2_balance = itachi.get_eth_balance(address=account2.address)
    print(f"account2 balance: {account2_balance}")

    time.sleep(10)

    account1_balance = itachi.get_eth_balance(address=account1.address)
    print(f"account1 balance: {account1_balance}")
    account2_balance = itachi.get_eth_balance(address=account2.address)
    print(f"account2 balance: {account2_balance}")
