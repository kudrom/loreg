import json, csv, re, sys


# votes is a list with all the initial votes
def sainte_lague(votes, limit):
    # aux is a list of lists that will store the current state
    aux = []
    s = 1
    maxis = []
    seats = []

    # Initialize the aux structure
    for vote in votes:
        aux.append([vote])
        seats.append(0)

    while(limit > 0):
        # The maximum values of a party are stored at the head of the list
        maxis = list(map(lambda x: x[0], aux))
        maximum = max(maxis)
        index = maxis.index(maximum)
        del aux[index][0]
        seats[index] += 1

        i = 0
        for vote in votes:
            aux[i].append(vote / (2*s + 1))
            i += 1

        s += 1
        limit -= 1
    
    return seats

if __name__ == "__main__":
    votes = []
    nombres = []
    years = []
    with open("poblacion.csv") as csvfile:
        poblacion = csv.reader(csvfile)
        for row in poblacion:
            if row[0] == "":
                for year in row[1:]:
                    years.append(year)
                    votes.append([])
            else:
                nombres.append(row[0])
                i = 1
                for aux in votes:
                    aux.append(int(row[i]))
                    i += 1

    i = 0
    csvfile = open("350-1.csv", "w")
    writer = csv.writer(csvfile)
    for year in votes:
        seats = sainte_lague(year, 298)
        final = list(map(lambda x: x + 1, seats))
        if i == 0:
            writer.writerow(["Year"] + nombres)
        writer.writerow([years[i]] + final)
        i += 1
    csvfile.close()
    
    i = 0
    csvfile = open("350-2.csv", "w")
    writer = csv.writer(csvfile)
    for year in votes:
        seats = sainte_lague(year, 248)
        final = list(map(lambda x: x + 2, seats))
        final[-1] -= 1
        final[-2] -= 1
        if i == 0:
            writer.writerow(["Year"] + nombres)
        writer.writerow([years[i]] + final)
        i += 1
    csvfile.close()

    i = 0
    csvfile = open("400-1.csv", "w")
    writer = csv.writer(csvfile)
    for year in votes:
        seats = sainte_lague(year, 348)
        final = list(map(lambda x: x + 1, seats))
        if i == 0:
            writer.writerow(["Year"] + nombres)
        writer.writerow([years[i]] + final)
        i += 1
    csvfile.close()

    i = 0
    csvfile = open("400-2.csv", "w")
    writer = csv.writer(csvfile)
    for year in votes:
        seats = sainte_lague(year, 298)
        final = list(map(lambda x: x + 2, seats))
        final[-1] -= 1
        final[-2] -= 1
        if i == 0:
            writer.writerow(["Year"] + nombres)
        writer.writerow([years[i]] + final)
        i += 1
    csvfile.close()
