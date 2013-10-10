import json
with open("provincias_old.json", "r") as provincias:
    loaded = json.loads(provincias.read())
    dumped = []
    for provincia in loaded:
        coords = provincia["coordinates"]
        final_coords = []
        for coord in coords:
            new_coord = []
            for both in coord.split(" "):
                lat = round(float(both.split(",")[0]), 4)
                lon = round(float(both.split(",")[1]), 4)
                new_coord.append([lat, lon])
            final_coords.append(new_coord)
        dumped.append({
            "id": provincia["id"],
            "name": provincia["nombre"],
            "community": provincia["comunidad"],
            "coordinates": final_coords
        })
with open("provincias_sin_canarias.json", "w") as provincias:
    json.dump(dumped, provincias, sort_keys=True)
