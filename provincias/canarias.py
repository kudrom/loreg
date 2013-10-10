import json
with open("provincias_sin_canarias.json", "r") as provincias:
    loaded = json.loads(provincias.read())
    dumped = []
    for provincia in loaded:
        if provincia["name"] == "Santa cruz de tenerife" or provincia["name"] == "Las palmas":
            coords = provincia["coordinates"]
            for coord in coords:
                for both in coord:
                    both[0] += 18;
                    both[1] += 7.5;
        dumped.append(provincia)

with open("provincias.json", "w") as provincias:
    json.dump(dumped, provincias, sort_keys=True)
