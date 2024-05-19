import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Lire les données à partir d'un fichier CSV
data = pd.read_csv(r'C:/ecriture/ExportDuctus/JV/QWG50.csv', delimiter='\t', encoding='ISO-8859-1', on_bad_lines='skip')

# Remplacer les virgules par des points dans les chaînes de caractères
data['T (s)'] = data['T (s)'].str.replace(',', '.').astype(float)
data['Aabs F (cm/s/s)'] = data['Aabs F (cm/s/s)'].str.replace(',', '.').astype(float)

# Extraire les colonnes du temps et de l'accélération
t = data['T (s)']
a = data['Aabs F (cm/s/s)']

# Afficher quelques valeurs des listes t et a
print("Temps (s) :", t[:5])
print("Accélération (cm/s²) :", a[:5])

# Extraire les colonnes de position X et Y
x = data['PosX (cm)'].str.replace(',', '.').astype(float)
y = data['PosY (cm)'].str.replace(',', '.').astype(float)

# Calculer la distance parcourue entre chaque paire de points consécutifs
distances = [0] * len(x)
for i in range(1, len(x)):
    dx = x[i] - x[i-1]
    dy = y[i] - y[i-1]
    distances[i] = (dx**2 + dy**2)**0.5

# Calculer la vitesse à chaque point
v = [0] * len(t)
for i in range(1, len(t)):
    v[i] = distances[i] / (t[i] - t[i-1])

# Convertir les unités de vitesse de cm/s en m/s
v = [v_i / 100 for v_i in v]

def moving_average(a, n=3):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

# Définir la taille de la fenêtre de lissage (de base n=10 fonctionne, avec 200 c'est très lisible)
n = 200

# Calculer la moyenne mobile pour la vitesse
v_smooth = moving_average(np.array(v), n=n)  # Ajustez la valeur de n pour régler le degré de lissage

# Calculer la moyenne mobile pour l'accélération
a_smooth = moving_average(np.array(a), n=n)  # Ajustez la valeur de n pour régler le degré de lissage

# Afficher quelques valeurs de la liste v
print("Vitesse (m/s) :", v[:5])

# Tracer le graphique de la vitesse en fonction du temps (lissé)
plt.plot(t[n-1:], v_smooth)
plt.xlabel('Temps (s)')
plt.ylabel('Vitesse (m/s)')
plt.title('Vitesse en fonction du temps (lissée)')
plt.grid()
plt.show()

# Tracer le graphique de l'accélération en fonction du temps (lissé)
plt.plot(t[n-1:], a_smooth)
plt.xlabel('Temps (s)')
plt.ylabel('Accélération (cm/s²)')
plt.title('Accélération en fonction du temps (lissée)')
plt.grid()
plt.show()
