import csv
from io import StringIO
import xml.etree.ElementTree as ET

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
                obj[keys[i]] = row[i]
            obj["counter"] = current_line
            csv_content.append(obj)
            
        return csv_content

    def xml(self, file_name_or_string):
        root = None
        if file_name_or_string.endswith(".xml"):
            tree = ET.parse('country_data.xml')
            root = tree.getroot()
        else:
            it = ET.iterparse(StringIO(file_name_or_string))
            for _, el in it:
                prefix, has_namespace, postfix = el.tag.partition('}')
                if has_namespace:
                    el.tag = postfix # strip all namespaces
            root = it.root
        # Usage:
        # for child in root:
        #    print(child.tag)
        #    print(child.attrib)
        return root

    
    def text(self, file_name, delimiter="\n"):
        textFile = open(file_name,"r").read()
        return textFile.split(delimiter)
        
