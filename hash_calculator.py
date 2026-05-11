#***********************************************************************************************************************
# Program name:         hash_calculator.py
# Description:          Generates a SHA-256 output for a message or a file
# Author:               Thierry Perroud
# Creation date:        27.04.2026
# Modified by:          Thierry Perroud
# Modification date:    11.05.2026
# Version:              1.1
#***********************************************************************************************************************
#***********************************************************************************************************************
# Imports
#***********************************************************************************************************************
import hashlib


#***********************************************************************************************************************
# Functions
#***********************************************************************************************************************
def main():
    """
    Main function of the program

    :return: None
    """
    ### Welcome ###
    print(f"Bienvenue dans Hash Calculator !\n")

    ### Option ###
    print(f"Choisissez une option : \n")
    print(f"[1] Hacher un texte\n")
    print(f"[2] Hacher un fichier\n")

    ### User input ###
    choice = ask_for_int_choice()

    ### Hash text ###
    clear_result = ""
    hash_result = ""
    if choice == 1:
        clear_result, hash_result = hash_text()

    ### Hash file ###
    else:
        clear_result, hash_result = hash_file()

    ### Save hash ###
    print(f"Voulez-vous sauvegarder le résultat du hash ? \n")

    ### Option ###
    print(f"[1] Sauvegarder\n")
    print(f"[2] Ne pas sauvegarder\n")

    ### User choice ###
    choice = ask_for_int_choice()

    ### Save ###
    if choice == 1:
        save_hash(clear_result, hash_result)

def ask_for_int_choice():
    """
    Asks user for an integer choice and validates input

    :return: An int (1 or 2)
    """
    user_choice = input(f"votre choix : ")

    while user_choice != "1" and user_choice != "2":
        print(f"\nVous devez choisir une option entre 1 et 2 !\n")

        user_choice = input("votre choix : ")

    return int(user_choice)


def hash_text():
    """
    Asks user for text and hashes it

    :return: SHA-256 hashed text
    """
    ### User text ###
    text = input(f"\nEntrez le texte à hacher : ")

    ### SHA-256 hash ###
    hashed_text = hashlib.sha256(text.encode("utf-8")).hexdigest()

    ### Output ###
    print(f"SHA-256 : {hashed_text}\n")

    return text, hashed_text


def hash_file():
    """
    Asks user for a file and hashes it

    :return: SHA-256 hashed file
    """
    ### User file path input ###
    filepath = input(f"\nEntrez le chemin du fichier à hacher: ")

    try:
        ### SHA-256 hash ###
        with open(filepath, "rb") as file:
            file_data = file.read()
            hashed_file = hashlib.sha256(file_data).hexdigest()

        ### Output ###
        print(f"SHA-256 : {hashed_file}\n")

        return filepath, hashed_file

    except FileNotFoundError:
        print(f"\n[ERREUR] Le fichier n'existe pas.")
        return filepath, None




def save_hash(text, hashed_text):
    # TODO
    print(f"Fonctionnalité non implémentée.")
    pass


#***********************************************************************************************************************
# Program
#***********************************************************************************************************************
if __name__ == '__main__':
    main()