import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

# Chargement des donnees de taille de pupille a partir du fichier 'FilteredPupilData.txt'
with open('FilteredPupilData.txt', 'r') as f:
    lines = f.readlines()
pupil_data = [line.strip().split(' --> ') for line in lines]
pupil_data = [(float(time), sizes) for time, sizes in pupil_data if 'None' not in sizes]

# Calcul de la taille moyenne de la pupille a chaque instant
avg_pupil_sizes = [(time, sum(map(float, sizes.split(', ')))/2) for time, sizes in pupil_data]

# Trace des donnees originales
plt.figure(figsize=(12, 8))
plt.subplot(2, 2, 1)
plt.plot([time/60 for time, _ in avg_pupil_sizes], [size for _, size in avg_pupil_sizes])
plt.title('Donnees Originales')
plt.xlabel('Temps (minutes)')
plt.ylabel('Taille Moyenne de la Pupille')

# Determination de la periode de base (0 a 2 minutes dans cet exemple)
baseline_period = (0, 2*60)
baseline_data = [size for time, size in avg_pupil_sizes if baseline_period[0] <= time <= baseline_period[1]]
baseline_avg = sum(baseline_data) / len(baseline_data)

# Application de la correction de la ligne de base et suppression de la periode de base
corrected_pupil_sizes = [(time, size - baseline_avg) for time, size in avg_pupil_sizes if time > baseline_period[1]]

# Trace des donnees apres correction de la ligne de base
plt.subplot(2, 2, 2)
plt.plot([time/60 for time, _ in corrected_pupil_sizes], [size for _, size in corrected_pupil_sizes])
plt.title('Apres Correction de la Ligne de Base')
plt.xlabel('Temps (minutes)')
plt.ylabel('Taille Moyenne de la Pupille (Correction de la Ligne de Base)')

# Sous-echantillonnage des donnees
downsample_rate = 10  # Changez cette valeur pour ajuster le nombre de points sur le graphique
downsampled_pupil_sizes = corrected_pupil_sizes[::downsample_rate]

# Trace des donnees apres sous-echantillonnage
plt.subplot(2, 2, 3)
plt.plot([time/60 for time, _ in downsampled_pupil_sizes], [size for _, size in downsampled_pupil_sizes])
plt.title('Apres Sous-echantillonnage')
plt.xlabel('Temps (minutes)')
plt.ylabel('Taille Moyenne de la Pupille (Correction de la Ligne de Base)')

# Application du filtre Savitzky-Golay pour lisser les donnees
yhat = savgol_filter([size for _, size in downsampled_pupil_sizes], 51, 3)  # taille de la fenetre 51, ordre du polynome 3

# Trace des donnees apres le filtre Savitzky-Golay
plt.subplot(2, 2, 4)
plt.plot([time/60 for time, _ in downsampled_pupil_sizes], yhat)
plt.title('Apres Filtre Savitzky-Golay')
plt.xlabel('Temps (minutes)')
plt.ylabel('Taille Moyenne de la Pupille (Correction de la Ligne de Base)')

# Affichage du graphique
plt.tight_layout()
plt.show()
