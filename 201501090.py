from __future__ import print_function
import csv
import sys
import re

from filereader import FileReader
from parser import Parser
from utils import Utils


class MainClass:
    def __init__(self):
        self.utils = Utils()
        self.filereader = FileReader()
        self.parser = Parser()
        pass

    def main(self):
        Tables_map = {}
        self.filereader.create_table_signatures("metadata.txt", Tables_map)
        query = str(sys.argv[1])
        if query:
            self.parser.parse_query(query, Tables_map)
        else:
            print("No query")


if __name__ == "__main__":
    main = MainClass()
    main.main()
