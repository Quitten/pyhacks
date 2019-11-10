import csv

class Parser:
    def __init__(self, verbose = False):
        self.verbose = verbose

    def csv(self, file_name, delimiter=",", quotechar="\""):
        csvFile = open(file_name, "r")
        spamreader = csv.reader(csvFile, delimiter=delimiter, quotechar=quotechar)
        current_line = 0
        csv_content = []

        keys = []
        for row in spamreader:
            current_line = current_line + 1
            if current_line == 1:
                keys = row
                continue
            obj = {}

            if len(keys) != len(row):
                raise Exception("Malformed CSV file key length != row length")
            for i in range(len(keys)):
                if row[i] != "":
                    obj[keys[i]] = row[i]
            obj["counter"] = current_line
            csv_content.append(obj)
        return csv_content
    
    def text(self, file_name, delimiter="\n"):
        textFile = open(file_name,"r").read()
        return textFile.split(delimiter)
        