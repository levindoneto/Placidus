#!/usr/bin/python
# coding: UTF-8

ruleList      = []  # __init__ of BitVectorList, the lsb is a action bit # Match
matchList     = []  # This list contains informations about matches of all rules
switchMatch   = []  # This list is used for to link match and switches of network topology
dstList       = []  # This list contains only information about destination of packages in the network
actionList    = []  # This list contains only information about actions of predicates with the same index of the match informations
switchList    = []  # This list contains only information about switches according the network topology {switch : rule}
theSwitchList = []  # List of switches in the network topology
visitedList   = []  # List that saves the flag about a node, 1:visited  0:not visited
route_action  = []  # List that contais the route of the package in the action view
route_switch  = []  # List that contais the route of the package in the switch view
