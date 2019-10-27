import csv

class Parser():
    def __init__(self, verbose = False):
        self.verbose = verbose

    def csv(self, fileName, delimiter=",", quotechar="\""):
        csvfile = open(fileName, 'r')
        spamreader = csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar)
        currentLine = 0
        csvContent = []

        keys = []
        for row in spamreader:
            currentLine = currentLine + 1
            if currentLine == 1:
                keys = row
                continue
            obj = {}

            if len(keys) != len(row):
                raise Exception("Malformed CSV file key length != row length")
            for i in range(len(keys)):
                if row[i] != "":
                    obj[keys[i]] = row[i]
            obj["counter"] = currentLine
            csvContent.append(obj)
        return csvContent