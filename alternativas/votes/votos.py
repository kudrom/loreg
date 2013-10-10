import json, csv, re, sys


years = ["1977", "1979", "1982", "1986", "1989", "1993", "1996", "2000", "2004", "2008", "2011"]
if __name__ == "__main__":
    regex = re.compile(r".+\((.+)\)")
    for year in years:
        final = {}
        with open("{}.csv".format(year), "r") as csvfile:
            resultados = csv.reader(csvfile)
            for row in resultados:
                if row[3] == "Censo" and row[0] == "":
                   censo = row[-3]
                elif row[0] != "" and row[1] != "":
                    if row[3] != "Blancos" and row[3] != "Censo" and row[3] != "Votantes" and row[3] != "Nulos" and row[3] != "V&aacute;lidos":
                         id = int(row[1]) - 1
                         v = int(row[-3])
                         if row[3] != "Otros":
                             partido = re.match(regex, row[3]).group(1)
                         if partido not in final:
                             final[partido] = {"pv": [0]*52}
                         final[partido]["pv"][id] = v
        
        # Add the census with empty pv to avoid both the paint in the congress and the break of the API
        final["census"] = {"pv": [0]*52, "n": censo}
        with open("{}.json".format(year), "w") as jsonfile:
            json.dump(final, jsonfile, indent=4)
