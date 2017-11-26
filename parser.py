from __future__ import print_function
import csv
import sys
import re
from execute import Execute
from utils import Utils
from filereader import FileReader

class Parser:
    def __init__(self):
        self.utils = Utils()
        self.execute = Execute()
        self.filereader = FileReader()

    def parse_query(self, query, dictionary):
        if query:
            query = self.utils.spaces_rem(query)
        keywords = ["from", "select", "distinct", "where"]
        parsedquery = {}
        d = tuple()
        for k in keywords:
            if k in query and k == "from":
                parsedquery[k] = query.split(k)
            elif k == "select" and k in parsedquery["from"][0].strip():
                parsedquery['select'] = self.utils.spaces_rem(parsedquery["from"][0].strip().split('select')[1])
            elif k == "distinct" and k in parsedquery['select']:
                parsedquery[k] = self.utils.spaces_rem(parsedquery['select'].strip().split('distinct')[1])
                distinct = True
            elif k == "distinct" and k not in parsedquery['select']:
                parsedquery[k] = self.utils.spaces_rem(parsedquery['select'])
                distinct = False
            elif k == "where":
                parsedquery['where'] = self.utils.spaces_rem(parsedquery['from'][1]).split('where')
                tableNames = [self.utils.spaces_rem(x) for x in
                              self.utils.spaces_rem(parsedquery['where'][0]).split(',')]
                self.filereader.check_tables(tableNames, dictionary)
            else:
                sys.exit("No" + k + "Clause")
        parsedquery['distinct'] = self.utils.spaces_rem(parsedquery["distinct"])
        parsedquery['distinct'] = [self.utils.spaces_rem(x) for x in parsedquery["distinct"].split(',')]

        if distinct:
            for a in parsedquery['distinct']:
                if '(' in a or ')' in a:
                    d_att = a.split('(')[1][:-1]
                    if d_att:
                        parsedquery['distinct'][parsedquery['distinct'].index(a)] = d_att
                        break
            aggregation = ""

            x = self.filereader.add_tableName([d_att], tableNames, dictionary)
            d = (x[0], True)

        aggr_func = ""
        temp = []
        for a in parsedquery['distinct']:
            if '(' in a or ')' in a:
                print(a)
                aggr_func = a
            else:
                temp.append(a)
        parsedquery['distinct'] = temp

        if aggr_func:
            if '.' not in aggr_func:
                print(aggr_func)
                parsedquery['distinct'] = [self.utils.spaces_rem(aggr_func).split('(')[1][:-1]]
                parsedquery['distinct'] = self.filereader.add_tableName(parsedquery['distinct'], tableNames, dictionary)
                aggr_func = self.utils.spaces_rem(aggr_func).split('(')[0] + '(' + parsedquery['distinct'][0] + ')'

        parsedquery['distinct'] = self.filereader.add_tableName(parsedquery['distinct'], tableNames, dictionary)
        parsedquery['distinct'] = self.utils.check_attributes(parsedquery['distinct'], tableNames, dictionary)

        if len(parsedquery['where']) > 1:
            conditions = self.utils.spaces_rem(parsedquery['where'][1])
        else:
            conditions = ""
        self.execute.run(dictionary, tableNames, parsedquery['distinct'], conditions, d, aggr_func)
