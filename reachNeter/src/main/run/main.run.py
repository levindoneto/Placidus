#!/usr/bin/python
# coding: UTF-8
import csv
from src.main.bitUtils import bitVectorUtils as classBit
from src.main.data import bitList as classBitList
from src.main.bitUtils import bfsGraphs as ClassBFS
from BitVector import BitVector
import time
csvData = "../data/arquivoDados.csv"

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
        classBitList.matchList.append([])

        for ind in range(len(row)):          # Coluna a coluna do csv
            row[info_index] = classBit.stringToIntFormated(row[info_index])  # String -> Int
            row[info_index] = classBit.makeBitVector(row[info_index])        # Int -> BitVector
            classBitList.matchList[rule_index].append(row[info_index])       # Add in the list the BitVectors

            #adicionar mais uma coluna com o switch, talvez algo antes, que mexa direto no arquivo de maneira separada

            info_index += 1
        #if (len(classBitList.bitList[rule_index]) == 0):
            #print "swinc++"

        rule_index += 1

predicate=0
swinc = 1
classBitList.theSwitchList.append(classBit.makeBitVector(swinc))
for rule_index in range(len(classBitList.matchList)):
    if (len(classBitList.matchList[rule_index]) == 0): # Row == None
        predicate+=1
        swinc+=1
        classBitList.dstList.append(None)
        classBitList.switchList.append(None)
        classBitList.actionList.append(None)
        classBitList.theSwitchList.append(classBit.makeBitVector(swinc)) # Add a different switch in the network topology

    else:
        classBitList.dstList.append(classBitList.matchList[predicate][6])
        classBitList.switchList.append(classBit.makeBitVector(swinc))
        classBitList.actionList.append(classBitList.matchList[predicate][-1])
        #classBitList.bitList[rule_index].insert(-1, classBit.makeBitVector(swinc))  # Penultimate position in the list with informations about a rule <- swinc
        predicate+=1


indexBV_rule = 0
# Catch match informations and put this in a specific list
for rule_id in classBitList.matchList:                  # Rule by rule
    auxPredicate = BitVector(size=0)
    for info_id in rule_id[0:-1]:                     # [information a information of a rule]
        auxPredicate += info_id                       # Forming a BitVector mask predicate
    classBitList.matchList[indexBV_rule] = auxPredicate # list_rules(list of informations) <- list_rules(BV predicate mask)
    indexBV_rule += 1


grafo = ClassBFS.make_graph(classBitList.theSwitchList, classBitList.switchList, classBitList.matchList, classBitList.dstList, classBitList.actionList) #test

'''
print classBitList.matchList[0]
print classBitList.actionList[0]
print classBitList.dstList[0]
print classBitList.switchList[0]
'''
"TESTE BFS"

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

# Creating a package list
lista_regras = [1,2,42,1,9007199254740992,4,2,806,3]
lista_regras = classBit.makeTest(lista_regras)
print "\n\n", lista_regras, "\n\n"

print lista_regras[0], lista_regras[1]
