from __future__ import print_function
import csv
import sys
import re
from utils import Utils
from filereader import FileReader
from join import Join
class Execute:
    def __init__(self):
        self.utils = Utils()
        self.filereader = FileReader()
        self.join = Join()


    def run(self, dictionary, tableNames, attributes, conditions, d, aggr_func):
        conditions = re.sub(' ?= ?', '=', conditions)
        self.utils.spaces_rem(conditions)
        conditions = [self.utils.spaces_rem(c) for c in conditions.split(" ")]
        if len(conditions[0]):
            resultant_data = []
            join_conditions = []
            const_conditions = ""
            for c in conditions:
                self.utils.spaces_rem(c)
                RHS = ""
                x = c.split("=")
                try:
                    RHS = x[1]
                    RHS = self.utils.spaces_rem(RHS)
                except:
                    RHS = ""
                if '.' in RHS:
                    join_conditions.append(c)
                if '.' not in RHS:
                    const_conditions += " " + c + " "
            if const_conditions:
                const_conditions = self.utils.spaces_rem(const_conditions)

            resultant_data, schema = self.join.join(dictionary, tableNames, const_conditions, join_conditions)
            const_conditions = self.utils.spaces_rem(const_conditions)
            if resultant_data:
                self.print_result(resultant_data, attributes, schema, d, aggr_func)

        elif len(tableNames) > 1:
            resultant_data, schema = self.join.join(dictionary, tableNames, None, None)
            if resultant_data:
                self.print_result(resultant_data, attributes, schema, d, aggr_func)

        else:
            resultant_data = []
            schema = dictionary[tableNames[0]]
            self.filereader.readFile(tableNames[0] + ".csv", resultant_data)
            if resultant_data:
                self.print_result(resultant_data, attributes, schema, d, aggr_func)

    def print_result(self, resultant_data, attributes, schema, d, aggr_func):
        if len(d):
            i = 1
            if attributes:
                for a in attributes:
                    if i == 1:
                        print(a, end="")
                        i = 0
                    else:
                        print("," + a, end="")
                print("\n")
            h = {}
            if resultant_data:
                for idx, row in enumerate(resultant_data):
                    try:
                        if h[row[schema.index(d[0])]]:
                            continue
                    except:
                        h[row[schema.index(d[0])]] = idx
            if h:
                for key, value in h.items():
                    i = 1
                    for col in attributes:
                        data = resultant_data[value]
                        if i == 1:
                            i = 0
                            print(data[schema.index(col)], end="")
                        else:
                            print("," + data[schema.index(col)], end="")
                    print("\n")

        elif aggr_func:
            param = self.utils.spaces_rem(aggr_func).split('(')[0]
            type_of_func = self.utils.spaces_rem(param).lower()
            param2 = self.utils.spaces_rem(aggr_func).split('(')[1][:-1]
            self.utils.print_aggr(type_of_func, resultant_data, schema, self.utils.spaces_rem(param2))

        else:
            i = 1
            if attributes:
                for a in attributes:
                    if i == 1:
                        print(a, end="")
                        i = 0
                    else:
                        print("," + a, end="")
                print("\n")
                if resultant_data:
                    for data in resultant_data:
                        i = 1
                        for col in attributes:
                            if i == 1:
                                print(data[schema.index(col)], end="")
                                i = 0
                            else:
                                print("," + data[schema.index(col)], end="")
                        print("\n")


