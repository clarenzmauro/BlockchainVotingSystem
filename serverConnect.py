from web3 import Web3

# Connect to the blockchain (ganache rpc server)
rpcServer = input("RPC server: ")
web3 = Web3(Web3.HTTPProvider(rpcServer))

# Check if connected to the blockchain
if web3.is_connected():
    print("Connected to the blockchain.")
else:
    print("Not connected to blockchain.")

# Check the block number
print("Total number of blocks in the blockchain:", web3.eth.block_number)