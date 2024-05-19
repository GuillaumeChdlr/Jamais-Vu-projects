# Load excessive movement periods
with open('MouvementParasite.txt', 'r') as f:
    lines = f.readlines()
excessive_movement_periods = [tuple(map(float, line.strip().split(' - '))) for line in lines]

# Load pupil size data
with open('sortie.txt', 'r') as f:
    lines = f.readlines()
pupil_data = [line.strip().split(' --> ') for line in lines]
pupil_data = [(float(time), sizes.split(', ')) for time, sizes in pupil_data]

# Filter pupil size data
filtered_pupil_data = []
for time, sizes in pupil_data:
    if not any(start_time <= time <= end_time for start_time, end_time in excessive_movement_periods):
        # Handle 'None' pupil sizes
        if sizes.count('None') == 2:
            continue  # Skip this line if both pupil sizes are 'None'
        elif sizes.count('None') == 1:
            sizes = [size if size != 'None' else sizes[1 - sizes.index(size)] for size in sizes]  # Replace 'None' with the other pupil size
        filtered_pupil_data.append((time, sizes))

# Write filtered pupil size data to file
with open('FilteredPupilData.txt', 'w') as f:
    for time, sizes in filtered_pupil_data:
        f.write(f"{time} --> {', '.join(sizes)}\n")
