import json
max_lat = min_lat = max_lon = 0
min_lon = 100

with open("provincias.json", "r") as provincias:
    loaded = json.loads(provincias.read())
    for provincia in loaded:
        coords = provincia["coordinates"]
        for coord in coords:
            for both in coord:
                max_lat = max([max_lat, both[0]])
                min_lat = min([min_lat, both[0]])
                max_lon = max([max_lon, both[1]])
                min_lon = min([min_lon, both[1]])

print(max_lat, min_lat)
print(max_lon, min_lon)