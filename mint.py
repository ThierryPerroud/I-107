#***********************************************************************************************************************
# Program name:         mint.py
# Description:          Mints metadata containing an image URL to make it as an NFT
# Author:               Thierry Perroud
# Creation date:        01.06.2026
# Modified by:          -
# Modification date:    -
# Version:              1.0
#***********************************************************************************************************************
from dotenv import load_dotenv
from web3 import Web3
import json
import os

# Adresse et clé privée de l'expéditeur
load_dotenv()
private_key = os.getenv("PRIVATE_KEY")

# Connexion au nœud Ethereum
w3 = Web3(Web3.HTTPProvider("http://10.229.43.182:8545"))  # Remplacez par l'URL de votre nœud
assert w3.is_connected(), "Échec de la connexion au nœud Ethereum"

URI =  "https://raw.githubusercontent.com/ThierryPerroud/I-107/refs/heads/master/NFT_metadata.json"

# Adresse et ABI du contrat déployé
contract_address = "0x9A8C8E2EB8F6fA1Bd7EF9161417F64E48bf54225"
second_contract_address = "0x54b7226b364a90D1B7D5Acb403C9d7B360E2b3b2"
third_contract_address = "0xb5913CF61fcbc543375FCba1A00BB6aB1fd093c0"
thierry_perroud_contract_address = "0x49b392B337Fd6953d04A2F7F9D6E2fa566FE7BB7"
deployer_address = "0xdc6EdB5D91E1e26A80eCAC4cF4BAB6936b25A011"
recipient_address = "0xdc6EdB5D91E1e26A80eCAC4cF4BAB6936b25A011"

sender_address = w3.to_checksum_address(deployer_address)

'''
# Charger l'ABI du contrat (contrat prof)
with open("./SimpleMintContract.abi", "r") as abi_file:
    contract_abi = json.load(abi_file)
'''

# Charger l'ABI du contrat (contrat Thierry)
with open("./PerroudThierryContract.abi", "r") as abi_file:
    contract_abi = json.load(abi_file)

# Charger le contrat
nft_contract = w3.eth.contract(address=thierry_perroud_contract_address, abi=contract_abi)

# Étape 1 : Mint du token
nonce = w3.eth.get_transaction_count(sender_address)
valueEth = 0.05
mint_txn = nft_contract.functions.mint(URI).build_transaction({
    "chainId": 32383,  # ID de votre blockchain privée ou testnet
    "gas": 2000000,
    "gasPrice": w3.to_wei("10", "gwei"),
    "value": w3.to_wei(valueEth, "ether"),  # Prix du mint défini dans le contrat
    "nonce": nonce
})

signed_mint_txn = w3.eth.account.sign_transaction(mint_txn, private_key)

try:
    # Fait un test avant pour savoir si tout est en ordre, si c'est bon ça passe sinon 
    # ça leve l'exception
    mint_check = nft_contract.functions.mint(URI).call({
        "from": sender_address,
        "value": w3.to_wei(valueEth, "ether")  # Prix du mint défini dans le contrat
    })


    mint_tx_hash = w3.eth.send_raw_transaction(signed_mint_txn.raw_transaction)
    print(f"Transaction de mint envoyée : {mint_tx_hash.hex()}")

    # Attendre la confirmation
    mint_receipt = w3.eth.wait_for_transaction_receipt(mint_tx_hash)
    print(f"Transaction de mint confirmée dans le bloc {mint_receipt.blockNumber}")
except Exception as e:
    print(f"Une erreur est survenue : {str(e)}")

# Récupérer le tokenId (assume que c'est totalSupply après mint)
token_id = nft_contract.functions.totalSupply().call()
print(f"Token ID minté (c'est totalSupply) : {token_id}")

