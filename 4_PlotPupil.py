import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

# Load pupil size data
with open('FilteredPupilData.txt', 'r') as f:
    lines = f.readlines()
pupil_data = [line.strip().split(' --> ') for line in lines]
pupil_data = [(float(time), sizes) for time, sizes in pupil_data if 'None' not in sizes]

# Calculate average pupil size at each timestamp
avg_pupil_sizes = [(time, sum(map(float, sizes.split(', ')))/2) for time, sizes in pupil_data]

# Determine baseline period (0 to 2 minutes in this example)
baseline_period = (0, 2*60)
baseline_data = [size for time, size in avg_pupil_sizes if baseline_period[0] <= time <= baseline_period[1]]
baseline_avg = sum(baseline_data) / len(baseline_data)

# Apply baseline correction
corrected_pupil_sizes = [(time, size - baseline_avg) for time, size in avg_pupil_sizes]

# Filter data to start from 2 minutes
corrected_pupil_sizes = [(time, size) for time, size in corrected_pupil_sizes if time > 2*60]

# Downsample data to reduce the number of points on the plot
downsample_rate = 10
downsampled_pupil_sizes = corrected_pupil_sizes[::downsample_rate]

# Apply Savitzky-Golay filter to smooth the data
yhat = savgol_filter([size for _, size in downsampled_pupil_sizes], 51, 3)

# Create plot
times = [time for time, _ in downsampled_pupil_sizes]
plt.plot(times, yhat)
plt.xlabel('Time')
plt.ylabel('Average Pupil Size (Baseline Corrected)')
plt.show()
