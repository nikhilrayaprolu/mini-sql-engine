
from __future__ import print_function
import csv
import sys
import re
class Utils:
    def __init__(self):
        pass

    def spaces_rem(self, q):
        if q:
            return (re.sub(' +', ' ', q)).strip()
        else:
            return ""

    def parse_condition(self, condition):
        if condition:
            x = condition.split("=")
            L = []
            t = self.spaces_rem(x[0]).split('.')[0]
            L.append(t)
            t = self.spaces_rem(x[1]).split('.')[0]
            L.append(t)
            t = self.spaces_rem(x[0]).split('.')[1]
            L.append(t)
            t = self.spaces_rem(x[1]).split('.')[1]
            L.append(t)
        return tuple(L)

    def print_aggr(self, tof, res, schema, agg_att):
        l = []
        if tof:
            for r in res:
                l.append(int(r[schema.index(agg_att)]))
            self.spaces_rem(tof)
            if tof and tof == "avg":
                print("Avg of " + agg_att)
                print(sum(l) / len(l))
            elif tof == "sum":
                print("Sum of " + agg_att)
                print(sum(l))
            elif tof == "min":
                print("min of " + agg_att)
                print(min(l))

            elif tof == "max":
                print("max of " + agg_att)
                print(max(l))
            else:
                sys.exit("Unknown aggregate function")

    def rem_via_constants(self, resultant_data, const_conditions, schema, dictionary, tableNames):
        new = []
        if resultant_data:
            for data in resultant_data:
                # print (data)
            #    print(data)
                s = self.evaluate(data, const_conditions, dictionary, schema, tableNames)
                # print(s)
                if len(s):
                    if eval(s):
                        if data:
                            new.append(data)
            resultant_data = new
        return (resultant_data, schema)


    def evaluate(self, data, const_conditions, dictionary, schema, tableNames):
        #print(const_conditions)
        const_conditions = re.sub('=', ' = ', const_conditions)
        const_conditions = re.sub('> = ', ' >= ', const_conditions)
        const_conditions = re.sub('< =', ' <= ', const_conditions)

        #print(const_conditions)
        const_conditions = self.spaces_rem(const_conditions)
        const_conditions = const_conditions.split(" ")
        string = ""
        relational = ['and', 'or']
        if const_conditions[0].lower() in relational:
            self.spaces_rem(const_conditions)
            const_conditions.pop(0)
        lhs = True
        #print(const_conditions)
        for i in const_conditions:
            if i == "=":
                string += i * 2
            elif i ==">" or i=="<" or i=="<=" or i==">=":
                string += i
            elif i.lower() == 'and' or i.lower() == 'or':
                string += ' ' + i.lower() + ' '
                relational = ['and', 'or']
            elif i and lhs:
                lhs = False
         #       print(i)
                if i.split('.')[0] not in dictionary.keys() and ('.' in i):
                    relational = ['and', 'or']
                    sys.exit("No table found by name" + i.split('.')[0])
                else:
                    try:
                        i = self.add_tableName([i], tableNames, dictionary)
          #              print(i)
                        string += data[schema.index(i[0])]
                    except:
                        string = ""
            else:
                lhs = True
           #     print(i)
                string += i
        #print(string)
        return string

    def add_tableName(self, attributes, tableNames, dictionary):
        for a in attributes:
            self.spaces_rem(a)
            if "." not in a:
                self.spaces_rem(a)
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

    def check_attributes(self, attributes, tablenames, dictionary):
        try:
            if attributes:
                if attributes[0] == "*":
                    attributes = dictionary[tablenames[0]]
                else:
                    for a in attributes:
                        self.spaces_rem(a)
                        present = False
                        for key, value in dictionary.items():
                            if a in value:
                                self.spaces_rem(a)
                                if present:
                                    sys.exit("Ambigious case for attibute " + a)
                                present = True
                                break
                        if not present:
                            sys.exit("Attribute " + a + " not present")
        except:
            sys.exit("Attribute not found")
        return attributes
