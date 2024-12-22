import os
import re
import string
import sys

# Fonction pour récupérer le nom du dossier
def get_argvs():
    if len(sys.argv) != 2:  # Vérifier s'il y a le nombre correct d'arguments
        print("Nombre d'arguments est invalide")
        exit()
    return sys.argv[1]

# Fonction pour récupérer les médicaments à partir des fichiers HTML
def fetch_meds(folder):
    alphabet_list = string.ascii_uppercase  # Liste des alphabets en majuscule
    list_of_meds = []
    info = {letter: 0 for letter in alphabet_list}  # Dictionnaire pour les statistiques

    for letter in alphabet_list:
        file_path = os.path.join(folder, f"vidal-Sommaires-Substances-{letter}.htm")
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                file_text = file.read()
                occurences = re.findall(r'(<a href="Substance/.+\.htm">)(.+?)(</a>)', file_text)
                info[letter] = len(occurences)  # Mettre à jour le nombre d'entités
                list_of_meds.extend([occurence[1] for occurence in occurences])

    return list_of_meds, info

# Fonction pour générer le fichier "subst.dic"
def generate_dictionary(list_of_meds):
    with open('subst.dic', 'w', encoding="utf-16le") as dictionnaire:
        dictionnaire.write("\ufeff")  # Écrire le BOM
        for med in list_of_meds:
            dictionnaire.write(f"{med},.N+subst\n")

# Fonction pour générer le fichier "infos1.txt"
def generate_stats(info):
    with open("infos1.txt", "w") as stats:
        total = 0
        for letter, count in info.items():
            stats.write(f"{letter} : {count}\n")
            total += count
            print(f"{letter} : {count}")  # Afficher dans la console
        stats.write(f"Total : {total}\n")
        print(f"Total : {total}")  # Afficher le total dans la console

if __name__ == "__main__":
    folder = get_argvs()  # Récupérer le nom du dossier

    list_of_meds, info = fetch_meds(folder)  # Récupérer la liste des médicaments

    generate_dictionary(list_of_meds)  # Générer le fichier subst.dic

    generate_stats(info)  # Générer le fichier infos1.txt
    