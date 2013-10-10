import json, csv
from math import floor
from collections import OrderedDict

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
    "UFV": "#BF264F",
    "UEC": "#BF264F",
    "PSM-EN-EU-EV-ERC": "#ccc",
    "PSM-IV-EXM-EQUO": "#e37",
    "SSP-SxTF-EQUO": "#ccd",
    "PACMA": "#dcd",
    "Eb": "#FFF602",
    "PRC": "#f3a",
    "EQUO": "#345",
    "PxC": "#2171B2",
    "Otros": "#A88326"
}

def hare(votes, limit):
    total = sum([value for _, value in votes.items()])
    quota = total / limit

    seats = {}
    rests = {}
    current = seat = 0
    while current < limit and len(votes) > 0:
        key, maximum = max(votes.items(), key=lambda x: x[1])
        seat = min(floor(maximum / quota), limit - current)
        seats[key] = seat
        rests[key] = maximum % quota
        current += seat
        del votes[key]

    while current < limit:
        key, maximum = max(rests.items(), key=lambda x: x[1])
        del rests[key]
        seats[key] += 1
        current += 1

    return seats

# votes is a list with all the initial votes
def dhont(votes, limit):
    # aux is a list of lists that will store the current state
    aux = []
    votess = []
    parties = []
    final = {}
    s = 1
    maxis = []
    seats = []

    # Initialize the aux structure
    for party, vote in votes.items():
        aux.append([vote])
        votess.append(vote)
        parties.append(party)
        seats.append(0)

    while(limit > 0):
        # The maximum values of a party are stored at the head of the list
        maxis = list(map(lambda x: x[0], aux))
        maximum = max(maxis)
        index = maxis.index(maximum)
        del aux[index][0]
        seats[index] += 1

        i = 0
        for vote in votess:
            aux[i].append(vote / s)
            i += 1
        s += 1
        limit -= 1

    i = 0
    for party in parties:
        final[party] = seats[i]
        i += 1
    return final

if __name__ == "__main__":
    combinations = [(hare, "350-1"), (hare, "350-2"), (hare, "400-1"), (hare, "400-2"),
                    (dhont, "350-1"), (dhont, "400-1"), (dhont, "400-2")]
    years = ["1979", "1977", "1982", "1986", "1989", "1993", "1996", "2000", "2004", "2008", "2011"]

    for comb in combinations:
        with open("circunscripciones/" + comb[1] + ".csv") as csvcircuns:
            cir = csv.reader(csvcircuns)
            circuns = []
            for i in cir:
                circuns.append(i)

            for year in years:
                circ = list(filter(lambda x: x[0] == year, circuns))
                circ = circ[0][1:]

                with open("votes/{}.json".format(year)) as jsparties:
                    # parties -> {"name_party": {"pv": [...]}, ...} 
                    parties = json.load(jsparties)
                    census = int(parties["census"]["n"])

                    # final -> {"name_party": {"pn": [], "n": #}, ...} one for each combination-year
                    final = {}
                    for party in parties.keys():
                        if party != "census":
                            final[party] = {"pn": [0]*52, "n": 0, "color": colors[party], "v": 0}

                    for province in range(52):
                        votes = {}
                        for party, obj in parties.items():
                            if obj["pv"][province] > 0:
                                votes[party] = obj["pv"][province]
                                final[party]["v"] += obj["pv"][province]
                        seats = comb[0](votes, int(circ[province]))

                        # Dump the province-results to the national-results for each year
                        for party, seat in seats.items():
                            final[party]["pn"][province] = seat
                            final[party]["n"] += seat

                    for party, obj in final.items():
                        obj["v"] /= census
                    final_ord = OrderedDict(sorted(final.items(), key=lambda x: x[1]["n"]))
                    # Store it in the correct file
                    with open("{}-{}/{}.json".format(comb[0].__name__, comb[1], year), "w") as jsfinal:
                        json.dump(final_ord, jsfinal, indent=4)
