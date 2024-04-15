from functions import Itachi

if __name__ == "__main__":
    itachi = Itachi()
    private_key1 = 0x050953649BfFC4878db6CfBe46E52f89812eD7Cdcf0B1AadDed3BFBA859BB681
    account1, priv = itachi.create_argent_account(private_key=private_key1)

    # Declare 同一个合约，第一次 delcare 成功，后面的全部失败
    itachi.declare_class(address=account1.address, key=private_key1)
    itachi.deploy_contract(address=account1.address, key=private_key1)