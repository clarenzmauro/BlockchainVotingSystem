import json
from web3 import Web3

# Connect to the blockchain (ganache rpc server)
rpcServer = input("RPC server: ")
web3 = Web3(Web3.HTTPProvider(rpcServer))

# account

# inputs
user_account = input("Enter your address: ")
user_key = input("Enter your private keys: ")
# main variables for accounts
account1 = user_account
private_keys = user_key
# voter identification
web3.eth.default_account = account1

# contract call

# edit this per contract
vAdress = input("Input voting address: ")
abi = json.loads('[{"inputs":[{"internalType":"string[]","name":"_candidateNames","type":"string[]"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"candidates","outputs":[{"internalType":"string","name":"name","type":"string"},{"internalType":"uint256","name":"voteCount","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_candidateIndex","type":"uint256"}],"name":"getCandidate","outputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getCandidateCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_candidateIndex","type":"uint256"}],"name":"vote","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"voters","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"}]')
voting_address = web3.to_checksum_address(vAdress)

# variable for contract
contract = web3.eth.contract(address=voting_address, abi=abi)

# for listing the candidates
candidate_count = contract.functions.getCandidateCount().call()
for i in range(candidate_count):
    # Call the getCandidate() function with the candidate index
    candidate_name, _ = contract.functions.getCandidate(i).call()
    print(f"Candidate {i + 0}: {candidate_name}")

# for voting
user_vote = input("Who do you want to vote? Input the Candidate Number: ")
tx_hash = contract.functions.vote(int(user_vote)).transact()

web3.eth.wait_for_transaction_receipt(tx_hash)

print("Vote successful! Transaction hash:" + str(web3.to_hex(tx_hash)) + " Block number: " + str(web3.eth.block_number))