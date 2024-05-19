import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def moving_average(a, n=3):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

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

# Définir les couleurs pour les graphes
colors = ['red', 'green', 'blue', 'cyan', 'magenta', 'yellow', 'black', 'orange', 'purple', 'brown', 'pink']

# Parcourir les fichiers
for i, file in enumerate(files):
    # Lire les données à partir du fichier CSV
    data = pd.read_csv(r'C:\ecriture\ExportDuctus\JV\\' + file, delimiter='\t', encoding='ISO-8859-1', on_bad_lines='skip')

    # Remplacer les virgules par des points dans les chaînes de caractères
    data['T (s)'] = data['T (s)'].str.replace(',', '.').astype(float)
    data['Aabs F (cm/s/s)'] = data['Aabs F (cm/s/s)'].str.replace(',', '.').astype(float)

    # Extraire les colonnes du temps et de l'accélération
    t = data['T (s)']
    a = data['Aabs F (cm/s/s)']

    # Extraire les colonnes de position X et Y
    x = data['PosX (cm)'].str.replace(',', '.').astype(float)
    y = data['PosY (cm)'].str.replace(',', '.').astype(float)

    # Calculer la distance parcourue entre chaque paire de points consécutifs
    distances = [0] * len(x)
    for j in range(1, len(x)):
        dx = x[j] - x[j-1]
        dy = y[j] - y[j-1]
        distances[j] = (dx**2 + dy**2)**0.5

    # Calculer la vitesse à chaque point
    v = [0] * len(t)
    for j in range(1, len(t)):
        v[j] = distances[j] / (t[j] - t[j-1])

    # Convertir les unités de vitesse de cm/s en m/s
    v = [v_i / 100 for v_i in v]

    # Définir la taille de la fenêtre de lissage (entre 600 et 2000)
    n = 600

    # Calculer la moyenne mobile pour la vitesse
    v_smooth = moving_average(np.array(v), n=n)  # Ajustez la valeur de n pour régler le degré de lissage

    # Calculer la moyenne mobile pour l'accélération
    a_smooth = moving_average(np.array(a), n=n)  # Ajustez la valeur de n pour régler le degré de lissage

    # Tracer le graphique de la vitesse en fonction du temps (lissé)
    plt.plot(t[n-1:], v_smooth, color=colors[i])

    # Tracer le graphique de l'accélération en fonction du temps (lissé)
    plt.plot(t[n-1:], a_smooth, color=colors[i])

# Ajouter les légendes, les titres et les grilles
plt.figure(1)
plt.xlabel('Temps (s)')
plt.ylabel('Vitesse (m/s)')
plt.title('Vitesse en fonction du temps (lissée)')
plt.grid()
plt.legend(files)

plt.figure(2)
plt.xlabel('Temps (s)')
plt.ylabel('Accélération (cm/s²)')
plt.title('Accélération en fonction du temps (lissée)')
plt.grid()
plt.legend(files)

plt.show()
