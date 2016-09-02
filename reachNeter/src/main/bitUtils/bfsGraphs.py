#!/usr/bin/python
# coding: UTF-8
import csv
from src.main.bitUtils import bitVectorUtils as classBit
from src.main.data import bitList as classBitList
from BitVector import BitVector
import time
csvData = "../data/data.csv"

def generate_edges(graph):
    edges = []
    for node in graph:
        for neighbour in graph[node]:
            edges.append((node, neighbour))

    return edges

def find_isolated_nodes(graph):
    """ returns a list of isolated nodes. """
    isolated = []
    for node in graph:
        if not graph[node]:
            isolated += node
    return isolated

''' Convert a list of rules and others informations in a graph
    @:parameter : BV Lists: switches, match, destination, action
    @:return    : BV Graph '''
def make_graph(diffSwitches, Switch_rule, Match, Destination, Action): # Type of all parameters -> List of BitVectors
    graph = {}
    for i in range(len(diffSwitches)):
        i+=1          # For the switch to start at one
        ruleID = [] # Format: [[Match0, Destination0, Action0],[Match1, Destionation1, Action1],...] -> BitVector Elements
                      # __init__ the list each switch
        for j in range(len(Switch_rule)):
            ruleID.append([])               # Sublist
            ruleID[j].append(Match[j])
            ruleID[j].append(Destination[j])
            ruleID[j].append(Action[j])
        graph.update({classBit.makeBitVector(i):ruleID})
    return graph

class NetQueue: # just an implementation of a queue
	def __init__(self):
		self.holder = []

	def enqueue(self,val):
		self.holder.append(val)

	def dequeue(self):
		val = None
		try:
			val = self.holder[0]
			if len(self.holder) == 1:
				self.holder = []
			else:
				self.holder = self.holder[1:]
		except:
			pass

		return val

	def IsEmpty(self):
		result = False
		if len(self.holder) == 0:
			result = True
		return result

#print(find_isolated_nodes(graph))

def BFS(graph,start,end,q):
	temp_path = [start]
	
	q.enqueue(temp_path)
	
	while q.IsEmpty() == False:
		tmp_path = q.dequeue()
		last_node = tmp_path[len(tmp_path)-1]
		print tmp_path
		if last_node == end:
			print "VALID_PATH : ",tmp_path
		for link_node in graph[last_node]:
			if link_node not in tmp_path:
				new_path = []
				new_path = tmp_path + [link_node]
				q.enqueue(new_path)
