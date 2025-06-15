import pandas as pd

# Bounding box coordinates 
# Define the bounding box coordinates
# Default set to area in near Brussels, Belgium;
LEFT = 3.68
RIGHT = 3.70
BOTTOM = 51.02
TOP = 51.04

input_file = '' # Specify the path to your CSV file here
df = pd.read_csv(input_file)

min_lon = df['longitude'].min()
max_lon = df['longitude'].max()
min_lat = df['latitude'].min()
max_lat = df['latitude'].max()

print(f'Data bounding box:')
print(f'  Left (min lon):   {min_lon}')
print(f'  Right (max lon):  {max_lon}')
print(f'  Bottom (min lat): {min_lat}')
print(f'  Top (max lat):    {max_lat}')

# Check if coordinates are within the bounding box
in_bounds = df[(df['longitude'] >= LEFT) & (df['longitude'] <= RIGHT) & (df['latitude'] >= BOTTOM) & (df['latitude'] <= TOP)]

print(f'Number of points within bounds: {len(in_bounds)}')
print('\nSample of points within bounds:')
print(in_bounds.head()) 