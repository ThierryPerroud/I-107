#***********************************************************************************************************************
# Program name:         placer_pdf.py
# Description:          Places a hashed PDF file, with its access path into the blockchain
# Author:               Thierry Perroud
# Creation date:        11.05.2026
# Modified by:          -
# Modification date:    -
# Version:              1.0
#***********************************************************************************************************************
from web3 import Web3
import os
from dotenv import load_dotenv
import json

# ==========================================================
# CONFIGURATION
# ==========================================================
load_dotenv()

# URL RPC de la blockchain privée CPNV
RPC_URL = "http://10.229.43.182:8545"

# Adresse du compte expéditeur
SENDER_ADDRESS = "0xdc6EdB5D91E1e26A80eCAC4cF4BAB6936b25A011"

# Addresse du compte récipient
RECEIVER_ADDRESS = "0x0000000000000000000000000000000000000000"

# Clé privée
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

# ==========================================================
# CONNEXION À LA BLOCKCHAIN
# ==========================================================
w3 = Web3(Web3.HTTPProvider(RPC_URL))

if w3.is_connected():
    print("✅ Connecté à la blockchain")

else:
    print("❌ Connexion échouée")
    exit()

# ==========================================================
# ENVOI DE FICHIER
# ==========================================================

def envoyer_fichier(data):
    """
    Construit, signe et envoie une transaction
    """
    transaction = {
        "nonce": w3.eth.get_transaction_count(SENDER_ADDRESS),
        "from": SENDER_ADDRESS,
        "to": RECEIVER_ADDRESS,
        "value": w3.to_wei(0, "ether"),
        "gas": 24000,
        "gasPrice": w3.eth.gas_price,
        "chainId": w3.eth.chain_id,
        "data": w3.to_hex(text=data)
    }

    # Signature de la transaction
    signed_tx = w3.eth.account.sign_transaction(transaction, PRIVATE_KEY)

    # Envoi sur le réseau
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

    return tx_hash.hex()

# ==========================================================
# PROGRAMME PRINCIPAL
# ==========================================================
def main():
    # Récupération des données (lien vers PDF + hash, en tant que dict)
    with open("data.json") as file:
        data = json.load(file)

    # Transformation du dict en string JSON
    data_dump = json.dumps(data)

    # Placement du chemin + hash dans la Blockchain
    try:
        tx_hash = envoyer_fichier(data_dump)

        print(f"Transaction envoyée vers {RECEIVER_ADDRESS}")
        print(f"Hash : {tx_hash}")

    except Exception as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    main()