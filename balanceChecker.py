from web3 import Web3

# Connect to the blockchain (ganache rpc server)
rpcServer = input("RPC server: ")
web3 = Web3(Web3.HTTPProvider(rpcServer))

# gets an input from the user then continues to check for balance after entry
user_address = input("Enter the address: ")
balance = web3.eth.get_balance(user_address)
balance = web3.from_wei(balance, 'ether')

print("The user has: " + str(balance) + " voting power in his/her account.")