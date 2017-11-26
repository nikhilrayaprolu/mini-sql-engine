from __future__ import print_function
import csv
import sys
import re
from utils import Utils
from filereader import FileReader

class Join:
    def __init__(self):
        self.utils = Utils()
        self.filereader = FileReader()

    def join(self, dictionary, tableNames, const_conditions, join_conditions):
        database = {}
        visited = {}
        for t in tableNames:
            visited[t] = False
            database[t] = []
            self.filereader.readFile(t + ".csv", database[t])
            # print database
        Jc = self.get_join_conditions(dictionary, join_conditions)
        remove_attribs = []
        i = 1
        for t in tableNames:
            self.utils.spaces_rem(t)
            if i == 1:
                resultant_data = database[t]
                visited[t] = True
                schema = dictionary[t]
                i = 0
            else:
                for key, value in visited.items():
                    if visited[key]:
                        try:
                            join_attribs = Jc[(t, key)]
                        except:
                            join_attribs = None
                        if join_attribs:
                            remove_attribs.append(t + '.' + join_attribs[0])
                            resultant_data, schema = self.join_tables(resultant_data, database[t], key, t, schema,
                                                                      join_attribs[1], join_attribs[0], dictionary)
                        else:
                            resultant_data, schema = self.join_tables(resultant_data, database[t], key, t, schema, None,
                                                                      None,
                                                                      dictionary)

        if const_conditions:
            if "=" in const_conditions:
                if len(const_conditions):
                    resultant_data, schema = self.utils.rem_via_constants(resultant_data, const_conditions, schema,
                                                                    dictionary,
                                                                    tableNames)

        for r in remove_attribs:
            try:
                schema.remove(r)
            except:
                print("No such attribute present")

        return resultant_data, schema

    def get_join_conditions(self, dictionary, join_conditions):
        Jc = {}
        if join_conditions:
            for j in join_conditions:
                j = self.utils.spaces_rem(j)
                c = self.utils.parse_condition(j)
                if c:
                    Jc[(c[0], c[1])] = (c[2], c[3])
                    Jc[(c[1], c[0])] = (c[3], c[2])
        return Jc

    def join_tables(self, resultant_data, table_data, table1, table2, schema, r_att, t_att, dictionary):
        if schema:
            if r_att and t_att:
                h = {}
                new = []
                old = []
                i = schema.index(table1 + "." + r_att)

                for idx, row in enumerate(resultant_data):
                    h[row[i]] = idx
                if t_att:
                    i = dictionary[table2].index(table2 + "." + t_att)
                if resultant_data:
                    for row in table_data:
                        if h.has_key(row[i]):
                            new.append(resultant_data[h[row[i]]] + row)
                    resultant_data = new

            else:
                new = []
                if resultant_data:
                    for r in resultant_data:
                        for t in table_data:
                            new.append(r + t)
                    resultant_data = new
            schema += dictionary[table2]

        return (resultant_data, schema)
