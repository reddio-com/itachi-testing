from functions import Itachi
import time
import threading

if __name__ == "__main__":
    itachi = Itachi()
    accounts_count = 5000
    each_batch = 20
    eth_transfer_batch = 200
    batches = int(accounts_count/each_batch)
    eth_transfer_batches = int(accounts_count/eth_transfer_batch)
    private_key_list = []
    account_list = [None] * accounts_count
    private_key_start = 0x050953649BfFC4878db6CfBe46E52f89812eD7Cdcf0B1AadDed3BFBA859B0001

    start_time = time.time()
    for i in range(accounts_count):
        private_key_list.append(private_key_start + i)
    address_list = []
    for private_key in private_key_list:
        account, priv = itachi.create_argent_account_no_deploy(private_key=private_key)
        address_list.append(account)
    
    print("Create accounts took: ", time.time() - start_time , " seconds")

    to_account_address = address_list[0]
    
    start_time = time.time()
    
    for batch in range(eth_transfer_batches):
        print("Transfer 1 ETH all accounts, batch:", batch, "/", eth_transfer_batches)
        start = batch*eth_transfer_batch
        end = (batch+1)*eth_transfer_batch
        itachi.transfer_eth_multi(1*10**18,address_list[start:end])
    
    print("Transfer 1000 ETH all accounts took: ", time.time() - start_time , " seconds")

    balance = itachi.get_eth_balance(to_account_address)
    print(f"to_account balance: {balance}")

    def deploy_account(i):
        print("Deploying account: ", i+1, "/", accounts_count)
        account, _ = itachi.deploy_argent_account(address_list[i], private_key_list[i])
        account_list[i] = account
    
    # Deploy accounts in batch
    start_time = time.time()
    for batch in range(batches):
        threads = []
        for i in range(each_batch):
            thread = threading.Thread(target=deploy_account, args=(batch*each_batch+i,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()
    
    print("Deployed all accounts, took: ", time.time() - start_time , " seconds")

    to_account = account_list[0]
    transfer_from_account_list = account_list[1:]

    def transfer(account):
        print("Transfer from account: "+hex(account.address)+" to account: "+hex(to_account.address)+" amount: 1 ETH")
        itachi.transfer_no_wait(account, to_account, 1*10**18,1)

    threads = []
    for account in transfer_from_account_list:
        thread = threading.Thread(target=transfer, args=(account,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
    
    start_time = time.time()
    # Check the balance of the to_account
    balance = itachi.get_eth_balance(to_account_address)
    print(f"to_account balance: {balance}")

    valid_accounts_count = sum(x is not None for x in transfer_from_account_list)

    expect_value = 1000*10**18 + valid_accounts_count*10**18
    print(f"expect_value: {expect_value}")

    while balance != expect_value:
        balance = itachi.get_eth_balance(to_account_address)
        print("Current balance: ", balance)
        time.sleep(0.2)
    
    end_time = time.time()
    print("All transactions accepted on L2, took: ", end_time - start_time , " seconds")
    print("TPS:", accounts_count/(end_time - start_time))