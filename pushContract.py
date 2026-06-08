#***********************************************************************************************************************
# Program name:         pushContract.py
# Description:          Python script to push a Smart Contract into the blockchain
# Author:               Thierry Perroud
# Creation date:        07.06.2026
# Modified by:          -
# Modification date:    -
# Version:              1.0
#***********************************************************************************************************************
from web3 import Web3
from dotenv import load_dotenv
import os
import json

load_dotenv()

file_name = "PerroudThierryContract"
w3 = Web3(Web3.HTTPProvider("http://10.229.43.182:8545"))

if not w3.is_connected():
    raise Exception("Erreur : Impossible de se connecter au nœud Ethereum")

private_key = os.getenv("PRIVATE_KEY")
deployer_address = "0xdc6EdB5D91E1e26A80eCAC4cF4BAB6936b25A011"
sender_address = w3.to_checksum_address(deployer_address)

with open(file_name + ".abi", "r") as abi_file:
    contract_abi = json.load(abi_file)

with open(file_name + ".bin", "r") as bin_file:
    contract_bytecode = "0x" + bin_file.read().strip()

SimpleNFT = w3.eth.contract(abi=contract_abi, bytecode=contract_bytecode)
nonce = w3.eth.get_transaction_count(sender_address)

transaction = SimpleNFT.constructor(sender_address).build_transaction({
    "chainId": 32383,
    "gas": 3000000,
    "gasPrice": w3.to_wei("20", "gwei"),
    "nonce": nonce,
})

try:
    signed_tx = w3.eth.account.sign_transaction(transaction, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    print(f"Contrat déployé à l'adresse : {tx_receipt.contractAddress}")

except Exception as e:

    print(f"Une erreur est survenue : {str(e)}")