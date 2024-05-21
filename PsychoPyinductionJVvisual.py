from psychopy import visual, core, event, gui
import random
import pandas as pd
import time
import os

# Créer une boîte de dialogue pour demander l'ID du participant
myDlg = gui.Dlg(title="Expérience de Guix")
myDlg.addText('''Veuillez entrer votre identifiant anonyme, qui se construit de la manière suivante : 
    Votre jour de naissance, suivi des deux premières lettres du prénom de votre mère et de votre père (sans accents), 
    Ex : si vous êtes né.e le 22 août 2000 et que vos parents s’appellent Corinne et Jérôme, votre identifiant est 22COJE''')
myDlg.addField('Identifiant:')
myDlg.addField('Age (2 chiffres):')
myDlg.addText('Informations supplémentaires (NE PAS TOUCHER)')
myDlg.addField('Grating Ori:',45)
myDlg.addField('Sujets:', choices=["Expérience", "Crêpe"])
ok_data = myDlg.show()  # Afficher la boîte de dialogue et attendre OK ou Annuler

if myDlg.OK:  # ou si ok_data n'est pas None
    participant_id = ok_data[0]
else:
    print('Utilisateur annulé')

# Liste des mots et non-mots
mots = ["CHIEN", "FEMME"]
non_mots = ["MORLU", "CAPPA"]
mots_ecart = ["B    I    L     L   E", "R    O    U    L    E"]
non_mots_ecart = ["V    I    N    T    E", "M    Y    L    L    E"]

# Mélange des listes
random.shuffle(mots)
random.shuffle(non_mots)
random.shuffle(mots_ecart)
random.shuffle(non_mots_ecart)

# Création de la liste combinée
combined_list = mots + non_mots + mots_ecart + non_mots_ecart
random.shuffle(combined_list)

# Création de la fenêtre
win = visual.Window([1500, 900], color='black')

# Création du DataFrame pour stocker les résultats
df = pd.DataFrame(columns=["IDparticipant", "Stimulus", "Temps de reponse", "Reponse"])

# Boucle sur les mots et non-mots
for stimulus in combined_list:
    # Affichage de la croix de fixation
    fixation = visual.TextStim(win, text='+', color='white')
    fixation.draw()
    win.flip()
    core.wait(3)

    # Affichage du stimulus
    text = visual.TextStim(win, text=stimulus)
    text.draw()
    win.flip()

    # Enregistrement du temps de début
    start_time = time.time()

    # Attente de 30 secondes
    clock = core.Clock()
    response_time = None
    response = 'NON'
    while clock.getTime() < 3:
        keys = event.getKeys(['space'])
        if keys:
            response_time = clock.getTime()
            response = 'JV'
            # Enregistrement de la réponse
            df = df.append({"IDparticipant": participant_id, "Stimulus": stimulus, "Temps de reponse": response_time, "Reponse": response}, ignore_index=True)
                
        text.draw()  # Redessiner le stimulus à chaque itération pour qu'il reste à l'écran (non perceptible)
        win.flip()
    if response_time is None:
        response_time = 3
        # Enregistrement de la réponse
        df = df.append({"IDparticipant": participant_id, "Stimulus": stimulus, "Temps de reponse": response_time, "Reponse": response}, ignore_index=True)

    # Effacer l'écran
    win.flip()

# Afficher "fin de l'expérience"
text = visual.TextStim(win, text='Fin de l\'expérience')
text.draw()
win.flip()
core.wait(3)

win.close()

# Vérifier si le fichier existe déjà
if os.path.isfile('resultats.xlsx'):
    # Si le fichier existe, lire les données existantes pour pas les écraser
    df_existing = pd.read_excel('resultats.xlsx')
    # Ajouter les nouvelles données aux données existantes
    df = pd.concat([df_existing, df])

# Exporter le DataFrame au format Excel
df.to_excel('resultats.xlsx', index=False)
