import json
from web3 import Web3

# Connect to the blockchain (ganache rpc server)
rpcServer = input("RPC server: ")
web3 = Web3(Web3.HTTPProvider(rpcServer))

# voter identification
web3.eth.default_account = web3.eth.accounts[0]

# contract call

# edit this per contract
vAdress = input("Input voting address: ")
abi = json.loads('[{"inputs":[{"internalType":"string[]","name":"_candidateNames","type":"string[]"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"candidates","outputs":[{"internalType":"string","name":"name","type":"string"},{"internalType":"uint256","name":"voteCount","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_candidateIndex","type":"uint256"}],"name":"getCandidate","outputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getCandidateCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_candidateIndex","type":"uint256"}],"name":"vote","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"voters","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"}]')
voting_address = web3.to_checksum_address(vAdress)

# variable for contract
contract = web3.eth.contract(address=voting_address, abi=abi)

# for displaying results
print(contract.functions.getCandidate(0).call())
print(contract.functions.getCandidate(1).call())