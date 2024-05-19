import pandas as pd

# Définir les noms des fichiers
files = [
    "QWG111.csv",
    "QWG020.csv",
    "QWG023.csv",
    "QWG038.csv",
    "QWG050.csv",
    "QWG055.csv",
    "QWG072.csv",
    "QWG077.csv",
    "QWG095.csv",
    "QWG101.csv",
    "QWG110.csv"
]

# Créer un dictionnaire pour stocker les noms de fichiers et les vitesses moyennes correspondantes
mean_speeds = {}

# Parcourir les fichiers
for i, file in enumerate(files):
    # Lire les données à partir du fichier CSV
    data = pd.read_csv(r'C:\ecriture\ExportDuctus\JV\\' + file, delimiter='\t', encoding='ISO-8859-1', on_bad_lines='skip')

    # Remplacer les virgules par des points dans les chaînes de caractères
    data['Vabs F (cm/s)'] = data['Vabs F (cm/s)'].str.replace(',', '.').astype(float)

    # Calculer la vitesse moyenne
    mean_speed = data['Vabs F (cm/s)'].mean()

    # Convertir les unités de vitesse de cm/s en m/s
    mean_speed = mean_speed / 100

    # Ajouter le nom du fichier et la vitesse moyenne au dictionnaire
    mean_speeds[file] = mean_speed

# Créer un DataFrame à partir du dictionnaire
mean_speeds_df = pd.DataFrame(list(mean_speeds.items()), columns=['File', 'Mean Speed (m/s)'])

# Exporter le DataFrame dans un fichier CSV
mean_speeds_df.to_csv('C:/ecriture/ExportDuctus/JV/mean_speeds.csv', index=False)
    