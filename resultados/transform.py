import json, csv, re, sys
from collections import OrderedDict

final = {}
censo = 0
colors = {
    "PP": "#009FE0",
    "CP": "#009FE0",
    "AP-PDP": "#009FE0",
    "AP": "#009FE0",
    "CD": "#009FE0",
    "PSOE": "#FE0002",
    "CDS": "#AB2DBC",
    "UCD": "#FF843D",
    
    "CiU": "#F98E07",
    "ERC": "#BFBA35",
    "EC-FED": "#186F89",
    "IC-V": "#42C470",
    "PDC": "#D3AB26",

    "BNG": "#7BBAD8",
    "FAC": "#AA386D",
    "CG": "#7BBAD8",
    
    "IU": "#AA1111",
    "IU-LV": "#4ED302",
    "IU-EUiA": "#4ED302",
    "PCE": "#AA1111",
    
    "UPyD": "#E2017B",
    
    "EAJ-PNV": "#1E813C",
    "PNV": "#1E813C",
    "AMAIUR": "#1C5268",
    "EA": "#8343A0",
    "EA-EUE": "#8343A0",
    "GBAI": "#707070",
    "Na-Bai": "#707070",
    "NA-Bai": "#707070",
    "HB": "#5B5B5B",
    "EE": "#00BB02",
    "EE-IE": "#00BB02",
    
    "CC-NC-PNC": "#3F1DA5",
    "CC-PNC": "#3F1DA5",
    "CC": "#3F1DA5",
    "AIC": "#3F1DA5",
    "UPC": "#3F1DA5",
    
    "COMPROMIS-Q": "#F26D21",
    
    "ChA": "#A54560",
    "PAR": "#AD484A",
    "CAIC": "#B5B5B5",
    "PA": "#383838",
    "CA": "#383838",
    "PSA-PA": "#D132CB",
    "UV": "#2B70AD",
    "UPN": "#66D6D4",
    
    "UN": "#1E1E1E",
    "PSP-US": "#C15DC0",
    "UC-DCC": "#E57F37",
    "CIC": "#31560E",
    
}
census = 0
pcensus = []
valid = 0
if len(sys.argv) == 2:
    year = sys.argv[1]
    # Regular expression to extract the acronym of the political parties
    regex = re.compile(r".+\((.+)\)")
    with open("raw/{}.csv".format(year), "r") as csvfile:
        resultados = csv.reader(csvfile)
        for row in resultados:
            # The census is used to calculate the % of votes
            if row[3] == "Censo":
                censo = int(row[4])
                if row[0] == "":
                    census = censo
                elif row[1] != "":
                    pcensus.append(censo)
            # National results
            elif row[0] == "":
                if row[3] == "V&aacute;lidos":
                    valid = int(row[-3])
                elif row[3] == "Votantes":
                    final["Abstención+Nulos"] = {"v": (100 - float(row[-2])) / 100, "pv": [], "color": "#D5D5D5"}
                elif row[3] == "Nulos":
                    final["Abstención+Nulos"]["v"] += int(row[-3]) / censo
                elif row[3] == "Blancos":
                    final[row[3]] = {"v": int(row[-3]) / censo, "pv": [], "color": "white"}
                    acc = int(row[-3])
                else:
                    v = int(row[-3])
                    n = int(row[-1])
                    if n != 0:
                        partido = re.match(regex, row[3]).group(1)
                        # I initialize the pv and pn to 0 in order to avoid skipping provinces 
                        # in political parties where the party hasn't gathered any vote 
                        final[partido] = {"v": v / censo, "n": n, "pv": [0]*52, 
                                          "pn": [0]*52, "color": colors[partido]}
                        acc += v
                    else:
                        final["Sin representacion"] = {"v": (valid - acc) / censo, "color": "#42EFFF", "pv": [0]*52}
            # Provincial results, exclude the autonomical
            elif row[1] != "":
                if row[3] == "Votantes":
                    final["Abstención+Nulos"]["pv"].append((100 - float(row[-2])) / 100)
                elif row[3] == "Nulos":
                    final["Abstención+Nulos"]["pv"][-1] += int(row[-3]) / censo
                elif row[3] == "Blancos":
                    final[row[3]]["pv"].append(int(row[-3]) / censo)
                    acc = int(row[-3])
                elif row[3] == "V&aacute;lidos":
                    valid2 = int(row[-3])
                elif row[3] != "Otros":
                    id = int(row[1]) - 1
                    n = int(row[-1])
                    v = int(row[-3])
                    partido = re.match(regex, row[3]).group(1)
                    # The political party has representation so acumulate their votes
                    if n != 0:
                        acc += v
                    try:
                        final[partido]["pv"][id] = v / censo
                        final[partido]["pn"][id] = n
                    except KeyError as e:
                        print(e)
                else:
                    final["Sin representacion"]["pv"][id] = (valid2 - acc) / censo
    final_ord = OrderedDict(sorted(final.items(), key=lambda x: x[1]["n"] if "n" in x[1].keys() else 2000))
    final_ord["census"] = {"total" :census, "provinces": pcensus}
    final_ord["valid"] = valid
    with open("{}.json".format(year), "w") as jsonfile:
        json.dump(final_ord, jsonfile, indent=4)
else:
    print("Pasa como argumento el año de elecciones")