import json
from web3 import Web3
import tkinter as tk
from tkinter import messagebox

def show_candidates():
    # Get user inputs
    rpc_server = 'http://192.168.100.10:7545'
    voting_address = '0x64AFF1523F197B1873620e4d224A392EeEd572c7'

    try:
        # Connect to the blockchain (ganache rpc server)
        web3 = Web3(Web3.HTTPProvider(rpc_server))

        # Load contract ABI
        abi = json.loads('[{"inputs":[{"internalType":"string[]","name":"_candidateNames","type":"string[]"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"candidates","outputs":[{"internalType":"string","name":"name","type":"string"},{"internalType":"uint256","name":"voteCount","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_candidateIndex","type":"uint256"}],"name":"getCandidate","outputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getCandidateCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_candidateIndex","type":"uint256"}],"name":"vote","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"voters","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"}]')

        # Create contract object
        contract = web3.eth.contract(address=voting_address, abi=abi)

        # Get candidate count
        candidate_count = contract.functions.getCandidateCount().call()

        # Display candidates
        candidate_list.delete(1.0, tk.END)
        for i in range(candidate_count):
            candidate_name, vote_count = contract.functions.getCandidate(i).call()
            candidate_list.insert(tk.END, f"Candidate {i + 0}: {candidate_name}, Votes: {vote_count}\n")

    except Exception as e:
        # Show error message
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


def vote():
    # Get user inputs
    rpc_server = 'http://192.168.100.10:7545'
    user_account = account_entry.get()
    user_key = key_entry.get()
    voting_address = '0x64AFF1523F197B1873620e4d224A392EeEd572c7'
    user_vote = vote_entry.get()

    try:
        # Connect to the blockchain (ganache rpc server)
        web3 = Web3(Web3.HTTPProvider(rpc_server))

        # Voter identification
        web3.eth.default_account = user_account

        # Load contract ABI
        abi = json.loads(
            '[{"inputs":[{"internalType":"string[]","name":"_candidateNames","type":"string[]"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"candidates","outputs":[{"internalType":"string","name":"name","type":"string"},{"internalType":"uint256","name":"voteCount","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_candidateIndex","type":"uint256"}],"name":"getCandidate","outputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getCandidateCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_candidateIndex","type":"uint256"}],"name":"vote","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"voters","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"}]')

        # Create contract object
        contract = web3.eth.contract(address=voting_address, abi=abi)

        # Check if user has already voted
        has_voted = contract.functions.voters(user_account).call()

        if has_voted:
            messagebox.showerror("Error", "You have already voted!")
        else:
            # Vote for candidate
            tx_hash = contract.functions.vote(int(user_vote)).transact({"from": user_account, "privateKey": user_key})

            # Wait for transaction to be mined
            tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

            # Check if transaction was mined
            if tx_receipt['status'] == 1:
                # Get block number and transaction index
                block_number = tx_receipt['blockNumber']
                transaction_index = tx_receipt['transactionIndex']

                # Show success message with block number and transaction index
                messagebox.showinfo("Success",
                                    f"Your vote has been recorded!\nBlock Number: {block_number}\nTransaction Hash: {tx_hash.hex()}")

                # Update candidate list
                show_candidates()
                
            else:
                messagebox.showerror("Error", "Transaction failed")

    except Exception as e:
        # Show error message
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


root = tk.Tk()
root.title("Blockchain Voting System")

candidate_list = tk.Text(root, height=10, width=40)
candidate_list.grid(row=0, column=0, columnspan=3)

vote_label = tk.Label(root, text="Vote for Candidate:")
vote_label.grid(row=1, column=0)
vote_entry = tk.Entry(root)
vote_entry.grid(row=1, column=1)

account_label = tk.Label(root, text="Your Account:")
account_label.grid(row=2, column=0)
account_entry = tk.Entry(root)
account_entry.grid(row=2, column=1)

key_label = tk.Label(root, text="Your Private Key:")
key_label.grid(row=3, column=0)
key_entry = tk.Entry(root, show='*')  # Use show attribute to display '*' instead of actual characters
key_entry.grid(row=3, column=1)

vote_button = tk.Button(root, text="Vote", command=vote)
vote_button.grid(row=4, column=0, columnspan=2)

show_candidates_button = tk.Button(root, text="Show Candidates", command=show_candidates)
show_candidates_button.grid(row=5, column=0, columnspan=2)

root.mainloop()