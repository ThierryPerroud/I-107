#***********************************************************************************************************************
# Program name:         enableContract.py
# Description:          Enables/Disables the Smart Contract
# Author:               Thierry Perroud
# Creation date:        07.06.2026
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

thierry_perroud_contract_address = "0x49b392B337Fd6953d04A2F7F9D6E2fa566FE7BB7"
deployer_address = "0xdc6EdB5D91E1e26A80eCAC4cF4BAB6936b25A011"
recipient_address = "0xdc6EdB5D91E1e26A80eCAC4cF4BAB6936b25A011"

sender_address = w3.to_checksum_address(deployer_address)

# Charger l'ABI du contrat
with open("./PerroudThierryContract.abi", "r") as abi_file:
    contract_abi = json.load(abi_file)

# Charger le contrat
nft_contract = w3.eth.contract(address=thierry_perroud_contract_address, abi=contract_abi)

enable = nft_contract.functions.toggleIsMintEnabled().build_transaction({
    "from": sender_address,
    "nonce": w3.eth.get_transaction_count(sender_address)
})

signed_enable = w3.eth.account.sign_transaction(enable, private_key)

try:
    # Fait un test avant pour savoir si tout est en ordre, si c'est bon ça passe sinon
    # ça leve l'exception
    mint_check = nft_contract.functions.toggleIsMintEnabled().call({
        "from": sender_address
    })

    enable_tx_hash = w3.eth.send_raw_transaction(signed_enable.raw_transaction)
    print(f"Transaction de toggle : {enable_tx_hash.hex()}")

    # Attendre la confirmation
    enable_receipt = w3.eth.wait_for_transaction_receipt(enable_tx_hash)
    print(f"Transaction de toggle confirmée dans le bloc {enable_receipt.blockNumber}")

except Exception as e:
    print(f"Une erreur est survenue : {str(e)}")