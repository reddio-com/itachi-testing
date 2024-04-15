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
    account1, priv = itachi.create_argent_account(private_key=private_key1)
    account2, priv = itachi.create_argent_account(private_key=private_key2)

    # 一账号往另外一个账号转账 100 次，每次 1 eth, 最后余额减少 100 eth
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
