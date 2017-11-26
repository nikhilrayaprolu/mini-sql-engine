from __future__ import print_function
import csv
import sys
import re
from utils import Utils

class FileReader:
    def __init__(self):
        self.utils = Utils()

    def readFile(self, tName, fileData):
        if tName:
            with open(tName, 'rb') as f:
                reader = csv.reader(f)
                if reader:
                    for row in reader:
                        fileData.append(row)

    def create_table_signatures(self, filename, dictionary):
        with open(filename, 'rb') as f:
            flag = 0
            for line in f:
                if flag == 1:
                    tableName = line.strip()
                    dictionary[tableName] = []
                    flag = 0
                    continue
                if line.strip() == "<begin_table>":
                    flag = 1
                    continue
                if not line.strip() == '<end_table>':
                    dictionary[tableName].append(tableName + "." + line.strip())

    def add_tableName(self, attributes, tableNames, dictionary):
        for a in attributes:
            self.utils.spaces_rem(a)
            if "." not in a:
                self.utils.spaces_rem(a)
                found = 0
                for key in tableNames:
                    for v in dictionary[key]:
                        if a == v.split('.')[1]:
                            attributes[attributes.index(a)] = v
                            found = 1
                            break
                    if found:
                        break
        return attributes

    def check_tables(self, tableNames, dictionary):
        for t in tableNames:
            try:
                d = dictionary[t]
            except:
                sys.exit("Table not found error")
