from web3 import Web3
import json

INFURA_URL = "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"
PRIVATE_KEY = "your_private_key"
TOKEN_ADDRESS = "0xYourTokenContract"
SENDER_ADDRESS = "0xYourWalletAddress"

w3 = Web3(Web3.HTTPProvider(INFURA_URL))

# ERC20 ABI snippet for transfer function
with open('erc20_abi.json') as f:
    erc20_abi = json.load(f)

token_contract = w3.eth.contract(address=TOKEN_ADDRESS, abi=erc20_abi)

def send_tokens(addresses, amounts):
    nonce = w3.eth.getTransactionCount(SENDER_ADDRESS)
    for i, to_address in enumerate(addresses):
        tx = token_contract.functions.transfer(to_address, amounts[i]).buildTransaction({
            'nonce': nonce + i,
            'gas': 70000,
            'gasPrice': w3.toWei('50', 'gwei')
        })
        signed_tx = w3.eth.account.signTransaction(tx, private_key=PRIVATE_KEY)
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(f"Sent to {to_address}, tx hash: {tx_hash.hex()}")

if __name__ == "__main__":
    # Example usage
    recipients = ["0xAddr1", "0xAddr2"]
    amounts = [1000 * 10**18, 500 * 10**18]  # token decimals = 18
    send_tokens(recipients, amounts)
