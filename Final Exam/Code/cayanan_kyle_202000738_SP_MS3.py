#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#imports
import copy
import heapq
from collections import defaultdict

#create resistor class
class R_class:
    def __init__(self, resistor_name, start_node, end_node, resistance):
        #first three inputs can stay as strings
        self.name = resistor_name
        self.node1 = start_node
        self.node2 = end_node
        
        #resistor in Ohms needs to be converted to float
        self.weight = float(resistance)
        
def R_input(n_resistors, input_debug=None):
    #declare initial dictionary
    R_dictionary={}
    
    #declare initial key list
    R_keylist=[]
    
    #declare initial vertex list
    V_list=[]
    
    #declare loop counter
    r_count = 0
    
    #repeat loop for every input of R
    while r_count < n_resistors:   
        #input split the resistor values
        #take the input as string
        #INPUT DEBUG
        if (input_debug==None):
            name, N1, N2, W = map(str, input().split())
        else:
            name, N1, N2, W = input_debug[r_count]
        
        #enter the name(key) into a list
        #R_keylist+=[name]
        R_keylist.append(name)
        
        #enter the nodes into the vertex list
        #V_list+=[N1,N2]
        V_list.append(N1)
        V_list.append(N2)
        
        #create a resistor object
        R_temporary = R_class(name,N1,N2,W)
        
        
        #enter the class into a dictionary using deepcopy
        R_dictionary[name] = copy.deepcopy(R_temporary)
        
        #iterate r_count
        r_count+=1
        
    
    #convert the list of nodes into a set, then back into a list
    V_return = list(set(V_list))
    
    
    return R_dictionary, R_keylist, V_return
    #final output:
    #R_dictionary = Dictionary of R_classes
    #R_keylist = List of Resistor Names(Keys)
    #V_return = List of Nodes

####################################
# Modified MinHeap
###################################

#Observe: MinHeap functions rely almost exclusively on the value entry
#The "key" entry can be any data type such as "string" and it will not affect its functionality

#Conclusion: changed key input from "int" to "str"
class MinHeap:
    def __init__(self) -> None:
        self.size = 0
        self.keys = [None]  # other elements start at index 1
        self.values = [None]
    
    def __str__(self) -> str:
        return f"keys: {self.keys}, values: {self.values}"

    #change append item to string
    def add(self, item: str, value: int) -> None:
        self.keys.append(item)
        self.values.append(value)
        self.size += 1
        
        idx = self.size
        parent_idx = idx//2
        while (idx > 1) and (self.values[parent_idx] > value):
            self._swap_nodes(parent_idx, idx)
            idx = parent_idx
            parent_idx = idx//2

    def _swap_nodes(self, idx1: int, idx2: int):
        # Swap keys
        self.keys[idx1], self.keys[idx2] = self.keys[idx2], self.keys[idx1]

        # Swap values
        self.values[idx1], self.values[idx2] = self.values[idx2], self.values[idx1]

    def get_smallest(self) -> int:
        """Return the key of the Node with smallest value"""
        return self.keys[1]

    def remove_smallest(self) -> int:
        """Remove and return the key of Node with smallest value"""
        key_of_min = self.keys[1]
        end_key = self.keys.pop()
        end_value = self.values.pop()
        self.size -= 1

        if self.size:
            self.keys[1] = end_key
            self.values[1] = end_value

        # Reorder the heap to fix order
        self._reorder_heap_from_root()
        
        return key_of_min

    def _reorder_heap_from_root(self):
        parent_idx = 1
        while True:
            right_idx = parent_idx*2 + 1
            left_idx = parent_idx*2

            # Get index with minimum value among parent and children
            min_idx = parent_idx
            if left_idx <= self.size:
                if self.values[left_idx] < self.values[min_idx]:
                    min_idx = left_idx
            if right_idx <= self.size:
                if self.values[right_idx] < self.values[min_idx]:
                    min_idx = right_idx
            
            # If parent already minimum value, heap already ok.
            # Otherwise, swap and continue
            if min_idx == parent_idx:
                break
            self._swap_nodes(min_idx, parent_idx)
            parent_idx = min_idx
####################################
# Modified Graph
####################################

class GraphUndirected:
    
    #modify the graph to use dictionaries instead of only lists
    def __init__(self, vertex_list):
        #name change
        #no longer needed
        #dont remove just in case issues
        self.vertex_list = vertex_list
        
        #no change
        self.num_edges = 0
        
        #add the nodes into the main "adj_list" dictionary
        #for vertex in vertex_list:
        #    #each vertex will be added as a dictionary
        #    self.adj_list[vertex] = {}
        #    
        #    for neighbor in vertex_list:
        #        #each neighbor will point to an empty list
        #        self.adj_list[vertex][neighbor] = []
        
        
        #OPTIMIZE 1.1 : GraphClass defaultdict
        
        #######################################
        # Change: use defaultdicts
        #######################################
        
        #declare all the default values to be used
        empty_return = lambda: []
        
        #adj_list: nested default dict with value "[]"
        self.adj_list= defaultdict(lambda: defaultdict(empty_return))
                
        
        #Optimize 2.0: convert to set
        #did not change variable name to avoid issues
        
        #new init variable
        self.resistor_list=set()
                
    
    #no changes to this function
    def __str__(self) -> str:
        return f"adj: {self.adj_list}"
    
    #change function to append()
    def add_edge(self, v: str, w: str, weight: str):
        #explanation:
        #the weight of the nodes must be a linked list in order to accomodate parallel connections
        #the standard list in python must either use "+[value]" or .append(value)
        self.adj_list[v][w].append(weight)
        self.adj_list[w][v].append(weight)
        self.num_edges += 1
    
        #change function to append()
        
        #new action: add to resistor list
        self.resistor_list.add(weight)
        
    #################################
    #New Function: remove edge
    #################################
    def remove_edge(self, v: str, w: str):
        #get the list of resistors via deepcopy
        R_out = copy.deepcopy(self.adj_list[v][w])
        #get the number of resistors
        R_count = len(R_out)
        
        #delete/reset the nodes to empty list
        self.adj_list[v][w]=[]
        self.adj_list[w][v]=[]
        
        #remove the number of edges based on how many resistors were removed
        self.num_edges -= R_count
        
        #remark: empty list will always have a length of zero (0) so no need to perform self.has_edge()
        
        return R_out
    
    #################################
    #New Function: remove resistor
    #################################
    def remove_resistor(self, Resistor):
        #removes the resistor from self.resistor_list
        #purpose: to check which resistors are processed WITHOUT ruining the circuit
        self.resistor_list.remove(Resistor)
    
    #################################
    #New Function: peek edge
    #################################
    def peek_edge(self, v: str, w: str):
        #take a peek of the resistor(s) INSIDE two nodes
        R_out = self.adj_list[v][w]
        
        return R_out
    
    #################################
    #New Function: peek resistors
    #################################
    def peek_resistors(self, a, b):
        #take a peek at all the resistors AROUND two nodes
        resistors = []
        
        #get adjacent nodes
        neighbors_a = self.adj(a)
        neighbors_b = self.adj(b)
        
        #process both sides
        for w in neighbors_a:
            if(w==b):
                pass
            #else
            temp = self.peek_edge(a,w)
            resistors+=temp
        for w in neighbors_b:
            if(w==a):
                pass
            #else
            temp = self.peek_edge(b,w)
            resistors+=temp
            
            
        #return the list of resistors
        return resistors
        
    
    #modified to accomodate implementation
    #observe: this version of graph already has a full dictionary for every neighbor
    #therefore: return adj_list[v] will return the entire list of neighbors
    #solution: check every list and make sure they are not empty
    def adj1(self, v: str):
        #declare empty list
        adj_vertex = []
        
        #OPTIMIZE 3.0: list comprehension
        
        #check each vertex one by one
        for neighbor in self.vertex_list:
            #if the node is the input, then skip
            if neighbor==v:
                pass
            
            #get the list of the target neighbor
            #check its len() to determine if it contains any resistors (e.x.) len(["R1", "R2"]) = 2
            #weight_check = len(self.adj_list[v][neighbor])
            
            #if list is not empty, add to return list
            #if weight_check > 0:
            #    adj_vertex+=[neighbor]
            
            #change: just check if not empty

            if self.adj_list[v][neighbor] != []:
                #adj_vertex+=[neighbor]
                adj_vertex.append(neighbor)
                
            #repeat for all neighbors
        
        return adj_vertex # returns vertices adjacent to v
    def adj(self, v: str):
        adj_vertex=[]
        
        #because of default
        
        for w in self.adj_list[v]:
            if(self.adj_list[v][w]!=[]):
                adj_vertex.append(w)
        
        return adj_vertex # returns vertices adjacent to v
    
    #modified to accomodate dictionaries
    def has_edge(self, v:str, w:str) -> bool:
        #if the node is the input, then skip
        if v==w:
            pass

        #get the list of the target neighbor
        #check its len() to determine if it contains any resistors (e.x.) ["R1", "R2"]
        weight_check = len(self.adj_list[v][w])

        #if list is not empty, then there is an edge
        if weight_check > 0:
            return True
        #else, return false
        return False

#############################################
#class Edge:
#    def __init__(self, src, dest, cost):
#        self.src = src
#        self.dest = dest
#        self.cost = cost
#############################################
#replaced by class R_class:
#############################################
####################################
# Path Validity
####################################

#check validity of path
#branches are invalid path for series

def branch_check(v,w,graph):
        #skip self check
        if v==w:
            pass
    
        #check length of linked list
        #redefine weight_check: a branch exists when a node has at least 3 connections to ALL its neighbors
        
        weight_check = 0
        
        #get the total number of resistors in all neighbors
        for neighbor in graph.adj_list[v]:
            weight_check += len(graph.adj_list[v][neighbor])

        #if resistors are greater than 2, then there is a branch in the path
        if weight_check > 2:
            return True
        
        #else return False
        return False
    
#this is meant to check if there is a branch between the node itself
# "why does this matter?" 
#because: it is possible that only one side of the resistor has branches while the other side is still series
def shallowbranch_check(v,w,graph):
        #skip self check
        if v==w:
            pass

        #check length of linked list
        weight_check = len(graph.adj_list[v][w])

        #if list is greater than 1, then there is a branch within the resistor nodes
        if weight_check > 1:
            return True
        
        #else return False
        return False

#checks the validity of path
#Vdd and GND are end nodes
#Vdd and GND is still possible, but all paths out of it are now infinite
def node_check(v,w,graph):
        #the node to itself is an "invalid path"
        if v==w:
            return True
        
        #if Vdd, then next node is infinity
        if(v=="Vdd"):
            return True
        
        #if GND, then next node is infinity
        if(v=="GND"):
            return True
        
        #else return False
        return False


def path_check(v,w,graph, enable=1):
    branch = branch_check(v, w, graph) #check if there are more than three paths into the node
    node = node_check(v, w, graph) #check if the current node is Vdd or GND
    
    #if either of the invalid paths are triggered, return False
    if(branch):
        return False
    
    if(node and enable==1):
        return False
    
    #else return True
    return True


#remarks:
#djikstra already checks for neighbor nodes, so no need to add an if-case for (start==end)
#however, I still added it just in case
####################################
#Modified Dejikstra Path
####################################

#modify for exclusive resistor use
class Dijkstra:
    
    #change initial vertex to voltage, Vdd
    def __init__(self, graph: GraphUndirected, init_v="Vdd", enable=1):
        #initial variables
        self.graph = graph #undirected resistor graph
        self.source = init_v #this is now a string
        
        #new variable
        #this enable integer will allow certain functions to run
        #example: if the starting node is Vdd, then the next node should not be infinity
        self.enable=enable
        
        #important for algorithm variables
        
        #OPTIMIZE 1.2: default dictionaries for djikstra
        
        #######################################################
        # MAJOR CHANGE: defaultdict optimization
        #######################################################
        
        #declare default values to be used
        infinite_return = lambda: float('inf')
        none_return = lambda: None
        false_return = lambda: False

        
        
        #declare each dictionary with their default value
        self.dist_to = defaultdict(infinite_return)
        self.edge_to = defaultdict(none_return)
        self.is_marked = defaultdict(false_return)
                
        ######################################################
        ######################################################
        
        #no change needed
        self.dist_to[init_v] = 0
        
        #DONE: modify the function
        self.shortest_path(self.graph)

    #change this function
    #check branches instead of smallest weight
    def shortest_path(self, graph: GraphUndirected):
        
        #DONE: modify MinHeap() to be str compatible OR replace entirely
        #conclusion: no changes needed because MinHeap is independent from "key"
        pq = MinHeap()
        pq.add(self.source, 0)  # Set distance to source as 0

        # Set distance to other vertices to be inf in PQ
        #modify to access vertex_list
        
        ###############################################################
        #MAJOR CHANGE: only check neighbors --> then modify scan()
        ###############################################################
        for v in graph.adj(self.source):
            if v != self.source:
                #add the key string as infinite float
                pq.add(v, float('inf'))
        
        #no change needed
        p1 = pq.remove_smallest()
        
        #DONE: modify scan() function
        self.scan(graph, pq, p1, self.enable)
        
        #no change needed
        #while loop simply iterates through all nodes
        while pq.size > 0:
            p1 = pq.remove_smallest()
            if self.is_marked[p1]:
                continue
            self.scan(graph, pq, p1)
    
    #modify to check for branching paths
    def scan(self, graph: GraphUndirected, pq: MinHeap, point: str, enable=1):
        #mark check
        self.is_marked[point] = True
        
        #modify to for loop to match the implemented version
        #get each neighbor in the adjacency list
        for neighbor in graph.adj(point): #recall: adj() returns a list of adjacent dictionary keys
            
            #check mark status
            if self.is_marked[neighbor]:
                continue
                
            #perform validity check
            #def path_check(v,w,graph):
            valid = path_check(point, neighbor, graph, enable) #recall: path_check verifies Vdd, GND, and branching paths
            
            #if valid==True, that means there are no branches, VDD, or GND
            #if valid==False, that means an invalid path was found
            
            #modify if case to check for valid paths instead of caring about smaller weight
            if(valid):
                ####################################################
                #Major Change: add adjacent nodes of neighbor to pq
                ####################################################
                for v in graph.adj(neighbor):
                    
                    #make sure that you dont re-add already visited locations
                    if self.is_marked[v]==False:
                        #add the key string as infinite float
                        pq.add(v, float('inf'))
                        
                
                #before: in the past, Djikstra would visit every node regardless if it is impossible to visit
                #now: djikstra will only visit its neighbors, and the neighbors of its neighbors
                
                #conslusion: djikstra will now traverse VALID paths only
                
                #let distance = 1 if path is valid
                #no need to add
                self.dist_to[neighbor] = 1 
                
                #no change
                self.edge_to[neighbor] = point
                
                #same as dist_to[neighbor]
                #just let it be 1
                pq.add(neighbor, 1)

    def get_shortest_path(self, dest):
        #starting vertex (ex) "Vdd"
        start = self.source
        
        #change: transferred the infinite return case to the beginning in order to reduce runtime
        
        #if there is no path, return None
        #print(self.dist_to[dest])
        if(self.dist_to[dest]==float('inf')):#if None is returned, then it is not in Series
            return None, None
        
        
        #target destination vertex (ex) "GND"
        end = dest
        
        #declare empty path list
        path = []
        
        #no changes needed
        while end is not None:  # Check if end is not None
            path.append(end)
            end = self.edge_to[end]
        
        #no changes needed
        path.append(start)
        path.reverse()
        


        return self.dist_to[dest], path

####################################
# Parallel Check
####################################

def Parallel(start, end, graph, dictionary):
    #declare parallel variable
    parallel = 0
    
    #call the resistor objects
    R1 = dictionary[start]
    R2 = dictionary[end]
    
    #declare the nodes to be compared
    node11 = R1.node1
    node21 = R2.node1
    node12 = R1.node2
    node22 = R2.node2
    
    #first check: starting nodes are equal
    if(node11==node21 and node12==node22):
        parallel = 1
        
    #second check: opposite nodes are equal
    if(node12==node21 and node11==node22):
        parallel = 1
    
    #final check, return True if either checks are satisfied
    if(parallel==1):
        return True
    #else return False
    return False
####################################
# Series Check
####################################

def Series(start, end, graph, dictionary):
    #call the resistor objects
    R1 = dictionary[start]
    R2 = dictionary[end]
    
    node11 = R1.node1
    node21 = R2.node1
    node12 = R1.node2
    node22 = R2.node2

    #OPTIMIZE 4.0: redundant checking

    #autofail check#1: branching
    #autofail check#2: cornered by Vdd and GND 
    if(shallowbranch_check(node11,node12,graph) or shallowbranch_check(node21,node22,graph) or VG_check(node11,node12) or VG_check(node12,node22)):
        return False
    
    ################
    # NEW
    ################
    
    #autofail check#3: branched on either side of the target resistors
    #if a single resistor is cornered by branches, then it is automatically impossible to have a series connection
    #remark: branch_check only checks one node actually, but I already wrote too much code 
    #I might accidentally break all my functions if I try to remove the second node in branch_check(v,w,graph)
    
    #R1 check
    if(branch_check(node11,node12,graph) and shallowbranch_check(node12,node12,graph)):
        return False
    
    #R2 check
    if(branch_check(node21,node22,graph) and shallowbranch_check(node22,node21,graph)):
        return False
    
    #algorithm check: start must not be Vdd or GND
    #justification: autofail#2 guarantees that at least one node in R1 will not be GND or Vdd
    
    #test check for node11
    if(node11!="Vdd" and node11!="GND"):
        #path finder route 1: node11 to node21, then validity of node21 to node22
        if(Series_Pathing(node11,node21,node22,graph)):
            #print("route1")
            return True
        #path finder route 2: node11 to node22, then validity of node22 to node21
        if(Series_Pathing(node11,node22,node21,graph)):
            #print("route2")
            return True
    
    #test check for node12
    if(node12!="Vdd" and node12!="GND"):
        #path finder route 3: node12 to node21, then validity of node21 to node22
        if(Series_Pathing(node12,node21,node22,graph)):
            #print("route3")
            return True
        #path finder route 4: node12 to node22, then validity of node22 to node21
        if(Series_Pathing(node12,node22,node21,graph)):
            #print("route4")
            return True

    #else return False
    return False

#remarks:
#pathing might become useful for simplifying series summation later in milestone 2
#however, for now I am planning to use for loops

####################################
# Series Pathing
####################################
def Series_Pathing(n1,n2,n3,graph):
    
    #create modified Djikstra Object using R1 as the init_v
    Pathing = Dijkstra(graph, n1, 0) #recall def __init__(self, graph: GraphUndirected, init_v="Vdd"):
    
    #only allow pathing if the destination is not Vdd or GND
    #declare series_check1 and series_check2
    series_check1=None
    series_check2=None
    
    
    if(n2!="Vdd" and n2!="GND"):
        #find a path from n1 to n2
        series_check1, series_path1 = Pathing.get_shortest_path(n2)
        branch1 = branch_check(n2,n3,graph) #then check for branching
    
    if(n3!="Vdd" and n3!="GND"):
        series_check2, series_path2 = Pathing.get_shortest_path(n3)
        branch2 = branch_check(n3,n2,graph) #then check for branching

    #path is true if and only if, there is a path and there is no branching between the pair
    if(series_check1!=None and branch1==False):
        return True
    if(series_check2!=None and branch2==False):
        return True
    
    #else return False
    return False

####################################
# Autofail Condition: Vdd and GND
####################################
def VG_check(n1,n2):
    if(n1=="Vdd" and n2=="GND"):
        return True
    if(n1=="GND" and n2=="Vdd"):
        return True
    
    #else
    return False
####################################
# Resistor Check
####################################

def Resistor_check(start, end, graph, dictionary):
    
    #first check parallel
    #if parallel is returned True, then return the parallel statement
    if(Parallel(start, end, graph, dictionary)):
        return("PARALLEL")
        
    #if series is returned True, then return series
    if(Series(start, end, graph, dictionary)):
        return("SERIES")
    
    #if none of the checks are true, then it will be neither
    return("NEITHER")
########################################
# Milestone 2 exclusive functions
########################################
########################################
# Parallel Detection
########################################

#Pull as in: pull the resistors out of the original graph


def Parallel_Pull(resistor_name, target_graph, dictionary, destination_graph=None):
    #call the resistor object
    R0 = dictionary[resistor_name]
    
    #declare nodes
    nodeA=R0.node1
    nodeB=R0.node2
    
    #perform a shallow branch check
    #if it is returned TRUE, then the resistor is parallel with someone 
    enable = shallowbranch_check(nodeA, nodeB, target_graph)
        
    #declare variables to be returned
    R_list = []
    R_eq = float(0)
    R_nodes = [nodeA,nodeB]
    
    #if enabled, perform solving
    if(enable):
        #pop the parallel resistors
        #Resistors = target_graph.remove_edge(nodeA,nodeB)
        
        #change: get the resistors instead of popping them
        Resistors = target_graph.peek_edge(nodeA,nodeB)
        
        #change: you're not allowed to pop the resistors to prevent false positives on NEITHERS
        #instead: just remove them from the resistor list
        for component in Resistors:
            target_graph.remove_resistor(component) #def remove_resistor(self, Resistor):
            
        #add the components of Req
        for r in Resistors:
            resistor = dictionary[r]
            ohms = dictionary[r].weight
            R_eq+= 1/ohms
        
        #finalize Req
        R_eq = (R_eq)**(-1)
        
        #modify R_list
        R_list+=Resistors
        
        #finally: modify the resistance of R0
        R0.weight = copy.deepcopy(R_eq)
        
        #add to destination graph
        #destination_graph.add_edge(nodeA,nodeB,R0.name)
        
        #remark: R0 will be the name of the resistor in the destination graph
    
    
    #finally, return all the relevant values
    return enable, R_list, R_eq, R_nodes


    #explanation: 
    #if enable is False, that means there is no parallel connection
    #additionally, R_list and R_eq will be empty
########################################
# Series Detection
########################################

#Series Pull will contain a recursive helper function

def Series_Pull(resistor_name, target_graph, dictionary, destination_graph=None):
    #purpose of dict_enable: only modify the dictionary during the top level recursion
    
    #call the resistor object
    R0 = dictionary[resistor_name]
    
    #declare nodes
    nodeA=R0.node1
    nodeB=R0.node2
    
    #declare nodes list
    node_list = []
    
    #declare variables to be returned
    R_heap = [] #list that will be used to order resistors in ascending order
    R_temp = set([R0.name])#set that will contain all processed resistors so far
    R_list = []#final output list
    R_eq = float(0)#total resistance so far
    enable = False
    check = False

    ################################################################################
    # Change: only perform series checking on neighbors
    ################################################################################
    
    #perform initial series check
    #recall: def neighbor_init(Rsource:str, R_temp:set, target_graph, dictionary):
    #recall: return check(Bool), r_out(List)
    
    #check if the resistor has series neighbors
    enable, R_neighbor = neighbor_init(R0.name, R_temp, target_graph, dictionary)
    
    #if enable is true, then perform series_pull on its neighbors    
    #now process the neighbors
    if(enable):
        
        #process the one or two resistors in series with the main resistor
        for Rn in R_neighbor:
            #turn ON the while loop
            check = True
            
            #let the current resistor (Rc) be the initial neighbor(Rn)
            Rc = Rn
            
            while(check):
                
                #check if the current resistor has any series neighbors   
                check, Rc = neighbor_loop(Rc, R_temp, target_graph, dictionary)
                    
                #if there is at least one series neighbor, check==True, Rc= {Series Neighbor}
                #the while loop will repeat and process {Series Neighbor}
                    
                #if there are no series neighbors, check==False and Rc==None
                #the while loop will break and move on to the second resistor in R_neighbor
                
                
    #progress so far:
    #initial resistor (R0) added to set()
    #initial neighbors (R0 left side) and (R0 right side) added to set()
    #neighbor of neighbors added to set()
    
    #next steps:
    #(1) arrange resistor names in ascending order
    #(2) add resistor values into total resistance
    #(3) remove all resistor names from resistor list
            

    #now process all the series resistor names
    if(enable):
        
        ################################################################################################
        #process every series resistor found
        #recall: every resistor in R_temp is already confirmed to be series
        for R1 in R_temp:
            #recall: def series_process(R1, node_list, R_heap, R_eq, target_graph, dictionary):
            R_eq = series_process(R1, node_list, R_heap, R_eq, target_graph, dictionary)

            #purpose: 
            #(a) add R1 nodes to node_list
            #(b) add R1 name to R_heap
            #(c) add R1 resistance to R_eq
            #(d) remove R1 name from graph resistor_list
            
        ################################################################################################            
        #next: process the nodes
        final_nodes=[]

        #for loop to look for the start node and end node of the chain of series resistors
        for node in node_list:
            #add the node to the final list
            if(node not in final_nodes):
                final_nodes.append(node)

            #if the node is found again, that means it is not in the edge of the series
            #delete it
            elif(node in final_nodes):
                final_nodes.remove(node)

        ################################################################################################
        #next: organize the resistors in increasing order
        
        #OPTIMIZE 2.2: finalized the sorting for R_list
        
        #add the sorted resistor names to the final list
        #recall: {tuple at index 1} = Resistor Name
        
        popsize = len(R_heap) #length of the minheap list
        R_pop = None #variable that will hold onto popped touple
        
        for i in range(popsize):
            #pop the touple
            R_pop = heapq.heappop(R_heap)
            
            #at the resistor name from index=1 into the final R_list
            R_list.append(R_pop[1])
            
        ################################################################################################
        #for Milestone 3: 
        #(1) delete all the resistor edges from the graph
        #(2) add the final resistance to the new graph
        #    target_graph.add_edge(final_nodes[0],final_nodes[1],R0.name)
        #(3) change the value in the dictionary to match the newly added resistor
        #    R0.node1=final_nodes[0]; R0.node1=final_nodes[1]; R0.weight=float(R_eq)
        return True, R_list, R_eq, final_nodes
    
    final_nodes=[]
    #finally, return all the relevant values
    return False, R_list, R_eq, final_nodes


    #explanation: 
    #if enable is False, that means there is no series connection
    #additionally, R_list and R_eq will be empty
    
##################################
# Helper Functions for Series Pull
##################################

#check each neighbor of the MAIN resistor
#adds series resistors to the R_tempt set()
def neighbor_init(Rsource:str, R_temp:set, target_graph, dictionary):
    #get neighboring resistors
    #recall: def peek_resistors(self, a, b):
    neighbors = target_graph.peek_resistors(dictionary[Rsource].node1, dictionary[Rsource].node2)

    #declare empty variables
    r_out = []
    check = False

    for R1 in neighbors:
        #skip if not in resistor list
        if(R1 not in target_graph.resistor_list):
            #because already processed
            continue

        #skip if already in R_temp
        if(R1 in R_temp):
            #because already processed
            continue

        if(Series(Rsource, R1, target_graph, dictionary)):#recall: def Series(start, end, graph, dictionary):
            #set to True permanently
            check = True

            #add to set
            R_temp.add(R1)

            #add to output return
            r_out.append(R1)

        #else nothing happens

    return check, r_out

#modified version of neighbor_init()
#guaranteed to only return one series resistor at a time
#proof:there can only be two series neighbors at one time;  function ignores the already processed resistor in the line
def neighbor_loop(Rsource:str, R_temp:set, target_graph, dictionary):
    #get neighboring resistors
    #recall: def peek_resistors(self, a, b):
    neighbors = target_graph.peek_resistors(dictionary[Rsource].node1, dictionary[Rsource].node2)

    #declare empty variables
    r_out = None
    check = False

    for R1 in neighbors:
        #skip if not in resistor list
        if(R1 not in target_graph.resistor_list):
            #because already processed
            continue

        #skip if already in R_temp
        if(R1 in R_temp):
            #because already processed
            continue

        if(Series(Rsource, R1, target_graph, dictionary)):#recall: def Series(start, end, graph, dictionary):
            #set to True permanently
            check = True

            #add to set
            R_temp.add(R1)

            #add to output return
            r_out = R1

        #else nothing happens
    return check, r_out


#add the series resistor to the total list
def series_process(R1, node_list, R_heap, R_eq, target_graph, dictionary):

    #add R1 nodes to nodelist
    #node_list+=[dictionary[R1].node1, dictionary[R1].node2]
    node_list.append(dictionary[R1].node1)
    node_list.append(dictionary[R1].node2)

    #OPTIMIZE 2.1: changed R_list into R_heap in order to perform sorting on the phonetics via string concatenation
    # string="R123" ; string[1:] = "123"

    #add R1 name to the minheap
    heapq.heappush(R_heap,(int(R1[1:]),R1))
    
    #add R1 resistance to final output
    R_eq += dictionary[R1].weight

    #remove R1 name from resistor list
    target_graph.remove_resistor(R1) #def remove_resistor(self, Resistor):
    
    return R_eq

########################################
# Final Function
########################################
def Resistor_Pull(graph, dictionary, destination_graph=None):
    #create main output list
    R_process = []
    
    #DEBUG
    count=0
    
    #check every resistor in the dictionary
    for R in dictionary:
        #debug string
        #print(f'count{count} start')
        
        #if R exists in the resistor_list: then it has not been popped yet
        #why popping: to prevent duplicates from being processed
        if(R in graph.resistor_list):
            
            #process R
            allow, string, integer = Get_Topology(R, graph, dictionary)
            
            #if a topology is detected, add to list
            if(allow):
                #R_process+=[string]
                R_process.append(string)
        
        #debug string
        #print(f'count{count} done')
        count+=1
            #else, nothing happens
    
    #return the final list
    return R_process
                

########################################
# Topology Helper Function
########################################
def Get_Topology(resistor, graph, dictionary, destination_graph=None):
    #declare variables
    allow = False
    R_list = []
    R_eq = float(0)
    R_nodes=[]
    
    #recall output format: Bool, List of Resistors, Equivalent Resistance
    ################################
    #call parallel processing
    ################################
    #then return if True
    allow, R_list, R_eq, R_nodes = Parallel_Pull(resistor, graph, dictionary)
    if(allow):        

        
        #convert the data into the required string format: [R1, R2, R3] 1000
        output_list = [R_list, R_eq, 'Parallel', R_nodes]
        return True, output_list, R_nodes
    
    
    ################################
    #call series processing
    ################################
    
    #then return if true
    allow, R_list, R_eq, R_nodes = Series_Pull(resistor, graph, dictionary)
    if(allow):
        #identical to parallel if-case
        R_eq = int(R_eq)

        R_first = int(R_list[0][1:])
        
        output_list = [R_list, R_eq, 'Series', R_nodes]

        return True, output_list, R_nodes
    
    ################################
    #neither processing
    ################################

    return allow, None, None
    #where allow==False

########################################
# String Output Helper Function
########################################

def print_helper(rlist, requivalent):
    test = rlist
    out = "["
    oot = str(requivalent)
    for i in range(len(test)-1):
        uut = test[i]
        out+= uut
        out+=", "

    out+=test[-1]
    out+="]"
    out+=" "+oot
    return(out)

#comment out debug code
#eyo = print_helper(['R1', 'R2', 'R3'], 1000)
#print(eyo)
#resistor and queries
#change: only resistors

R = int(input())

#R = number of resistors

#call the resistor processing function
#return a dictionary, keylist, and vertex list

#for debugging
R_lister=None

R_dict, R_keys, R_nodes = R_input(R,R_lister)

#DEBUG
#print("Input Finished")

#create the resistor graph
Resistor_graph = GraphUndirected(R_nodes)

#print("Graph Creation Finished")

#create holder graph for when resistors are popped
#Holder_graph = copy.deepcopy(Resistor_graph)

#add the resistors as edges to the graph
for resistor in R_keys:
    Resistor_graph.add_edge(R_dict[resistor].node1,R_dict[resistor].node2,R_dict[resistor].name)

#print("Edge Addition Finished")
    
#call the grouping function
#recall: def Resistor_Pull(graph, dictionary, destination_graph==None):

#recall
#self.num_edges == number of resistors inside a graph
R_total = float(0)

#debug
loop=1

while(Resistor_graph.num_edges!=1):
    loop+=1
    group = Resistor_Pull(Resistor_graph, R_dict)

    #observe: I did not put a test case for if "group" is empty
    #reason: It is physically impossible for all resistors to be "Neither" unless Wye Delta

    for i in group:
        #recall group element format: [ [R1, R2] , 2000 ,'Series' , [nodea,nodeb]]
        
        #get main resistor
        MainName=i[0][0]
        MainResistor=R_dict[MainName]
        
        #get group elements
        TotalResistors=i[0]
        TotalResistance=i[1]
        topology=i[2]
        nodes=i[3]

        if(topology=='Parallel'):
            #remove resistors from graph
            #recall: def remove_edge(self, v: str, w: str):
            Resistor_graph.remove_edge(nodes[0],nodes[1])
            
            #modify dictionary weight
            MainResistor.weight=TotalResistance
            
            #add the main resistor back into the graph
            Resistor_graph.add_edge(MainResistor.node1,MainResistor.node2,MainResistor.name)
            
        if(topology=='Series'):
            #remove all resistors from graph
            for reseries in TotalResistors:
                #recall: def remove_edge(self, v: str, w: str):
                Resistor_graph.remove_edge(R_dict[reseries].node1,R_dict[reseries].node2)
            
            #modify dictionary weight
            MainResistor.weight=TotalResistance
            
            #modify dictionary nodes
            MainResistor.node1=nodes[0]
            MainResistor.node2=nodes[1]
            
            #add the main resistor back into the graph
            Resistor_graph.add_edge(MainResistor.node1,MainResistor.node2,MainResistor.name)
        
        R_total=TotalResistance
        #repeat until only 1 resistor left


print(int(R_total))

#references

# EEE121 Week 11 Lecture Guide for Dijkstra Algorithm
# https://colab.research.google.com/drive/1st36PdGYt3yGefdThVqxTpOuhMz8E19I?usp=sharing

# Stackoverflow how to use defaultdict lambda
# https://stackoverflow.com/questions/8419401/python-defaultdict-and-lambda

