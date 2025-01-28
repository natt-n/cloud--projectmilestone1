import csv

keysSaved = False
rowDict = {}
keys = []

with open('Labels.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:

        #save the keys
        if(not keysSaved):
            keys = row
            keysSaved = True
            continue

        #save row into a dictionary
        i = 0
        for key in keys:
            rowDict[key] = row[i]
            i += 1
            print(key + ":" + rowDict[key])

        break #will only print the result of first line
