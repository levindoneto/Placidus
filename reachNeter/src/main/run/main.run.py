#!/usr/bin/python
# coding: UTF-8
import csv
from src.main.bitUtils import bitVectorUtils as classBit
from src.main.data import bitList as classBitList
from BitVector import BitVector
import time
csvData = "../data/data.csv"


allow = classBit.makeBitVector(1)
deny = classBit.makeBitVector(0)

swinc = 0    # Switch counter (for csv file)

# Parsing CSV (Regras)
auxMatchKey = BitVector(size=0) # __init__ BitVect
rule_index = 0
with open(csvData, "rb") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='\'')
    for row in spamreader:   #Linha a linha do csv
        info_index = 0           # Indice
        classBitList.bitList.append([])

        for ind in range(len(row)):          # Coluna a coluna do csv
            ''' FAZER NESSE MODELO O ACTION
            # Catch action informations and put this in a specific list
            n = 0
            for rule_id in range(len(classBitList.bitList)):
                classBitList.actionList.append(classBitList.bitList[n][-1])                           # <<<< NAO VAI TER MAIS ESSE LANCE DE PEGAR O ULTIMO COM -1
                n += 1
            '''

            row[info_index] = classBit.stringToIntFormated(row[info_index])  # String -> Int
            row[info_index] = classBit.makeBitVector(row[info_index])        # Int -> BitVector
            classBitList.bitList[rule_index].append(row[info_index])         # Add in the list the BitVectors

            #adicionar mais uma coluna com o switch, talvez algo antes, que mexa direto no arquivo de maneira separada

            info_index += 1
        #if (len(classBitList.bitList[rule_index]) == 0):
            #print "swinc++"

        rule_index += 1
a=0
swinc = 1
for rule_index in range(len(classBitList.bitList)):
    if (len(classBitList.bitList[rule_index]) == 0):
        swinc += 1
    classBitList.bitList[rule_index].insert(-1, classBit.makeBitVector(swinc))  # Penultimate position in the list with informations about a rule <- swinc

print "\n\n\n", classBitList.bitList[1][6]


indexBV_rule = 0
# Catch match informations and put this in a specific list
for rule_id in classBitList.bitList:                  # Rule by rule
    auxPredicate = BitVector(size=0)
    for info_id in rule_id[0:-3]:                     # -1: action, -2: switch  [information a information of a rule]
        auxPredicate += info_id                       # Forming a BitVector mask predicate
    classBitList.bitList[indexBV_rule] = auxPredicate # list_rules(list of informations) <- list_rules(BV predicate mask)
    indexBV_rule += 1
'''

start = time.time()  #__init time

if (testePack in classBitList.bitList):
    index_testePack = classBitList.bitList.index(testePack)
    if (classBitList.actionList[index_testePack] == allow):
        print "Package pass"
    elif (classBitList.actionList[index_testePack] == deny):
        print "Package does not pass"
else:
    print "Package not found"
print type(testePack)


end = time.time()
#print (end - start), "seconds"
'''
'''
# Creating a package list
lista_regras = [1,2,42,9007199254740992,4,2,806,3]
lista_regras = classBit.makeTest(lista_regras)
print "\n\n", lista_regras, "\n\n"
'''
