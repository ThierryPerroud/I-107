#***********************************************************************************************************************
# Program name:         recuperer_pdfs.py
# Description:          Gets every PDF files that were placed into the blockchain
# Author:               Thierry Perroud
# Creation date:        26.05.2026
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

# Addresse 0 de la blockchain
BLOCKCHAIN_ADDRESS = "0x0000000000000000000000000000000000000000"

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
# LECTURE DES ADRESSES
# ==========================================================

def lire_adresses(fichier):
    """
    Lire les adresses Ethereum depuis un fichier texte

    Retourne une liste d’adresses
    """
    adresses = []

    with open(fichier, "r") as f:
        data = json.load(f)

    for adresse, name in data.items():
        # Vérifier que l’adresse est valide
        if w3.is_checksum_address(adresse):
            adresses.append(adresse)

    return adresses

# ==========================================================
# RECUPERER LES PDF
# ==========================================================
def recuperer_pdfs(adresse):
    """
    Récupère les liens et hash vers le fichier .pdf en scannant les 100 derniers blocs avec l'adresse d'expéditeur de
    chaque élève, et l'adresse du récipient 0x000... de la blockchain.
    """
    latest_block = w3.eth.block_number

    for block_num in range(latest_block - 100, latest_block):
        block = w3.eth.get_block(block_num, full_transactions=True)

        for tx in block.transactions:
            if tx["from"] == adresse and tx["to"] == BLOCKCHAIN_ADDRESS:
                print(tx["input"])

# ==========================================================
# PROGRAMME PRINCIPAL
# ==========================================================
def main():
    adresses = lire_adresses("adresses.json")

    for adresse in adresses:
        try:
            recuperer_pdfs(adresse)

        except Exception as e:
            print(f"Erreur : {e}")


if __name__ == "__main__":
    main()