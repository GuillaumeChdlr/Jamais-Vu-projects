import matplotlib.pyplot as plt
import pandas as pd

# Lire les données à partir d'un fichier CSV
data = pd.read_csv(r'C:\ecriture\ExportDuctus\JV\QWG016.csv', delimiter='\t', encoding='ISO-8859-1', on_bad_lines='skip')

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




# Afficher quelques valeurs de la liste v
print("Vitesse (m/s) :", v[:5])

# Tracer le graphique de la vitesse en fonction du temps
plt.plot(t, v)
plt.xlabel('Temps (s)')
plt.ylabel('Vitesse (m/s)')
plt.title('Vitesse en fonction du temps')
plt.grid()
plt.show()

# Tracer le graphique de l'accélération en fonction du temps
plt.plot(t, a)
plt.xlabel('Temps (s)')
plt.ylabel('Accélération (cm/s²)')
plt.title('Accélération en fonction du temps')
plt.grid()
plt.show()
