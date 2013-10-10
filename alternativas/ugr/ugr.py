import json, csv, re, sys
from collections import OrderedDict
results = {}
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
    
    "GIL": "#FF9232",
    "VERDES": "#307F15",
    "LV-E": "#4ED302",
    "LV-LV": "#4ED302",
    "RUIZ-MATEOS": "#307F15",
    "PTE-UC": "#FFF602",
    "PTE": "#FFF602",
    "PST": "#2DCEAE",
    "MUC": "#FFF602",
    "PRD": "#2DCEAE",
    "PCC": "#BF264F",
    "FN": "#4C4C4C",
    "PSOE-H": "#B71D58",
    "ORT": "#BF264F",
    "ERFN": "#4C4C4C",
    "MC-OIC": "#2DCEAE",
    "BNPG": "#BF264F",
    "FDC-EDC": "#FFF602",
    "FDI": "#BC258C",
    "ASDCI": "#16706E",
    "AET": "#606614",
    "AN18": "#2EEAD4",
}
if len(sys.argv) == 2:
    year = sys.argv[1]
    with open("{}.csv".format(year)) as csvfile:
        resultados = csv.reader(csvfile)
        for row in resultados:
            # Initialize the results
            if row[0] == "id":
                parties = row
                for i in range(3, len(row)):
                    results[row[i]] = {"n": 0, "pn": [0]*52, "color": colors[row[i]]}
            elif row[0] != "Total":
                for i in range(3, len(row)):
                    if row[i] != "":
                        id = int(row[0])
                        results[parties[i]]["pn"][id - 1] = int(row[i])
            # Last line
            else:
                for i in range(3, len(row)):
                    results[parties[i]]["n"] = int(row[i])
    final_ord = OrderedDict(sorted(results.items(), key=lambda x: x[1]["n"]))
    with open("{}.json".format(year), "w") as jsonfile:
        json.dump(final_ord, jsonfile, indent=4)
else:
    print("Pasa el año de las elecciones como parámetro")