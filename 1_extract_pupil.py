# Importation du module json pour manipuler les donnees JSON
import json

# Definition de la fonction extract_data qui prend en entree le nom du fichier de donnees et le nom du fichier de sortie
def extract_data(gazedata, outputfile):
    # Ouverture du fichier de donnees en mode lecture
    with open(gazedata, 'r') as file:
        # Lecture de toutes les lignes du fichier
        lines = file.readlines()

    # Initialisation d'une liste vide pour stocker les donnees extraites
    data = []
    # Parcours de chaque ligne du fichier
    for line in lines:
        # Conversion de la ligne (chaîne de caractères) en objet JSON
        json_line = json.loads(line)
        # Extraction du timestamp
        timestamp = json_line['timestamp']
        # Extraction de la taille de la pupille de l'oeil gauche, si elle existe
        left_pupil = json_line['data']['eyeleft'].get('pupildiameter') if 'eyeleft' in json_line['data'] else None
        # Extraction de la taille de la pupille de l'oeil droit, si elle existe
        right_pupil = json_line['data']['eyeright'].get('pupildiameter') if 'eyeright' in json_line['data'] else None
        # Ajout du tuple (timestamp, taille de la pupille de l'oeil gauche, taille de la pupille de l'oeil droit) a la liste de donnees
        data.append((timestamp, left_pupil, right_pupil))

    # Ouverture du fichier de sortie en mode ecriture
    with open(outputfile, 'w') as file:
        # Parcours de chaque element de la liste de donnees
        for item in data:
            # ecriture de l'element dans le fichier de sortie sous le format "timestamp --> taille de la pupille de l'oeil gauche, taille de la pupille de l'oeil droit"
            file.write(f"{item[0]} --> {item[1]}, {item[2]}\n")

# Appel de la fonction extract_data avec le nom du fichier de donnees et le nom du fichier de sortie
extract_data('gazedata', 'sortie.txt')
