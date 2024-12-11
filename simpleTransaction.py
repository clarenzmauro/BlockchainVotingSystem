from web3 import Web3

# Connect to the blockchain (ganache rpc server)
rpcServer = input("RPC server: ")
web3 = Web3(Web3.HTTPProvider(rpcServer))

# accounts
user_account = input("Enter your address: ")
user_key = input("Enter your private keys: ")
receiver = input("Enter the receiver address: ")
sendAmount = input("Enter how much you want to send: ")
account1 = user_account
account2 = receiver
private_keys = user_key

# for verification
nonce = web3.eth.get_transaction_count(account1)

# build a tx
tx = {
    'nonce': nonce,
    'to': account2,
    'value': web3.to_wei(sendAmount, 'ether'),
    'gas': 2000000,
    'gasPrice': web3.to_wei('50', 'gwei')
}

# sign
signed_tx = web3.eth.account.sign_transaction(tx, private_keys)

# send
tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

# tx hash / receipt
print("Transaction successful! Transaction hash: " + str(web3.to_hex(tx_hash)) + " Block number: " + str(web3.eth.block_number))