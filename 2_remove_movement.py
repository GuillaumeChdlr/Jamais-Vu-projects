import json
import numpy as np
import scipy.signal

# Ajoutez les fonctions ici
def calculate_magnitude(data):
    return np.sqrt(data[0]**2 + data[1]**2 + data[2]**2)

def filter_outliers(data, m=2):
    return data[abs(data - np.mean(data)) < m * np.std(data)]

def low_pass_filter(data, cutoff_frequency, fs=1.0):
    nyquist_frequency = 0.5 * fs
    normal_cutoff = cutoff_frequency / nyquist_frequency
    b, a = scipy.signal.butter(1, normal_cutoff, btype='low', analog=False)
    return scipy.signal.lfilter(b, a, data)

# Load data
with open('imudata', 'r') as f:
    lines = f.readlines()

data = [json.loads(line) for line in lines if json.loads(line)['type'] == 'imu']

# Calculate magnitudes
accel_magnitudes = [calculate_magnitude(d['data']['accelerometer']) for d in data if 'accelerometer' in d['data']]
gyro_magnitudes = [calculate_magnitude(d['data']['gyroscope']) for d in data if 'gyroscope' in d['data']]

# Definissez la frequence de coupure et la frequence d'echantillonnage
cutoff_frequency = 0.1  # Vous pouvez ajuster cette valeur en fonction de vos besoins
sampling_frequency = 1.0  # Vous pouvez ajuster cette valeur en fonction de vos besoins

# Appliquez les filtres ici
accel_magnitudes = low_pass_filter(filter_outliers(np.array(accel_magnitudes)), cutoff_frequency, sampling_frequency)
gyro_magnitudes = low_pass_filter(filter_outliers(np.array(gyro_magnitudes)), cutoff_frequency, sampling_frequency)

# Calculate averages
accel_avg = np.mean(accel_magnitudes)
gyro_avg = np.mean(gyro_magnitudes)

# Identify periods of excessive movement
excessive_movement_periods = []
start_time = None
for d, accel_mag, gyro_mag in zip(data, accel_magnitudes, gyro_magnitudes):
    if accel_mag > accel_avg and gyro_mag > gyro_avg:
        if start_time is None:
            start_time = d['timestamp']
    else:
        if start_time is not None:
            end_time = d['timestamp']
            excessive_movement_periods.append((start_time, end_time))
            start_time = None

# Write excessive movement periods to file
with open('MouvementParasite.txt', 'w') as f:
    for start_time, end_time in excessive_movement_periods:
        f.write(f"{start_time} - {end_time}\n")
