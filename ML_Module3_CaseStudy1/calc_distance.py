# Write a program to find the distance between two locations when their latitude
# and longitudes are given.
#  Hint: Use the math module.

import math

def haversine(lat1, lon1, lat2, lon2):
    # Radius of Earth in kilometers
    R = 6371.0  

    # Convert degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Differences
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Distance in kilometers
    distance = R * c
    return distance

# Example: Distance between Bangalore and Delhi
lat1, lon1 = 12.9716, 77.5946   # Bangalore
lat2, lon2 = 28.7041, 77.1025   # Delhi

dist = haversine(lat1, lon1, lat2, lon2)
print(f"Distance: {dist:.2f} km")

# Example input:
# Latitude and Longitude of Bangalore: 12.9716, 77.5946
# Latitude and Longitude of Delhi: 28.7041, 77.1025 
# Distance: 1743.17 km
# Example input:
# Latitude and Longitude of Bangalore: 12.9716, 77.5946
# Latitude and Longitude of Delhi: 28.7041, 77.1025
# Distance: 1743.17 km