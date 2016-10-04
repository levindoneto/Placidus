#!/usr/bin/python
# coding: UTF-8
import csv
from src.main.bitUtils import bitVectorUtils as classBit
from src.main.data import bitList as classBitList
from BitVector import BitVector
import time
'''Global Variables'''
switch_info  = 0
match_info   = 1
dst_info     = 2
action_info  = 3
visited_info = 4


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

'''
print classBitList.theSwitchList[0]
print classBitList.switchList[0]
print classBitList.ruleList[0]
print classBitList.dstList[0]
print classBitList.actionList[0]
'''
def make_graph(diffSwitches, Switch_rule, Match, Destination, Action): # Type of all parameters -> List of BitVectors
    graph = {}                              # __INIT the graph network topology
    for switch in range(len(diffSwitches)): # Iterations = Number of rules in the network topology
        rulesInTheSwith = []                # Format: [[Switch0, Match0, Destination0, Action0],[Switch1, Match1, Destionation1, Action1],...] -> BitVector Elements
                                            # __init__ the list each switch

        for ruleVertice in range(len(Destination[switch])):
            rulesInTheSwith.append([])      # Each list of that contains informations about one rule
            ''' Access the position ruleVertice of rulesInTheSwitch (Dynamic allocation) and
                add switch of the rule, getting a lists of information in this way:
                information->switch->ruleVertice
            '''
            rulesInTheSwith[ruleVertice].append(Switch_rule[switch][ruleVertice])
            rulesInTheSwith[ruleVertice].append(Match[switch][ruleVertice])
            rulesInTheSwith[ruleVertice].append(Destination[switch][ruleVertice])
            rulesInTheSwith[ruleVertice].append(Action[switch][ruleVertice])
            #rulesInTheSwith[ruleVertice].append(visited[switch][ruleVertice])

        graph.update({classBit.makeBitVector(switch):rulesInTheSwith}) # Update at graph with Sw : rule_list->rule_information->(match, dst, action)
        switch += 1  # For the switch to start at one
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

''' This method given a package, search this package in a network topology
	(graph of rules).
    @:parameter : BV package(list[match, dst]), BV graph
    @:return    : BV Graph '''
def graphSearch(package, network_topology):
    switches   = network_topology.values()
    print type(switches)
    match_info = 1  # Position of match in the node rule
    # Searching package->match at the list of rules of all switches
    for s in range(len(switches)):
        for r in range(len(switches[s])):
            if (package[0] in switches[s][match_info]):
                print package[0]
                print switches[s][match_info]
                print "\n\nPackage founded in somewhere"
                print "This was founded in the line ", r, "\n\n"
    print len(switches[3])
    print "There are ", len(switches), " switches in the network topology", "\n"
    print len(switches[1])