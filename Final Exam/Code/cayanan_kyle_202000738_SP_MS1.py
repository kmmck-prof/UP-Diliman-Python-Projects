#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#imports
import copy
#create resistor class
class R_class:
    def __init__(self, resistor_name, start_node, end_node, resistance):
        #first three inputs can stay as strings
        self.name = resistor_name
        self.node1 = start_node
        self.node2 = end_node
        
        #resistor in Ohms needs to be converted to float
        self.weight = float(resistance)
        
def R_input(n_resistors):
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
        #iterate r_count
        r_count+=1
        
        #input split the resistor values
        #take the input as string
        name, N1, N2, W = map(str, input().split())
        
        #enter the name(key) into a list
        R_keylist+=[name]
        
        #enter the nodes into the vertex list
        V_list+=[N1,N2]
        
        #create a resistor object
        R_temporary = R_class(name,N1,N2,W)
        
        
        #enter the class into a dictionary using deepcopy
        R_dictionary[name] = copy.deepcopy(R_temporary)
        
    
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
        self.vertex_list = vertex_list
        
        #no change
        self.num_edges = 0
        
        #changed to a dictionary
        #to minimize user errors: the name of adj_list was not changed
        self.adj_list = {}
        
        #add the nodes into the main "adj_list" dictionary
        for vertex in vertex_list:
            #each vertex will be added as a dictionary
            self.adj_list[vertex] = {}
            
            for neighbor in vertex_list:
                #each neighbor will point to an empty list
                self.adj_list[vertex][neighbor] = []
                
    
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
    
    #modified to accomodate implementation
    #observe: this version of graph already has a full dictionary for every neighbor
    #therefore: return adj_list[v] will return the entire list of neighbors
    #solution: check every list and make sure they are not empty
    def adj(self, v: str):
        #declare empty list
        adj_vertex = []
        
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
                adj_vertex+=[neighbor]
                
            #repeat for all neighbors
        
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
        
        #######################################################
        # MAJOR CHANGE: combine all three for loops into one
        #######################################################
        
        #modify dist_to into a dictionary
        self.dist_to = {}
        self.edge_to = {}
        self.is_marked = {}
        for i in graph.vertex_list:
            self.dist_to[i] = float('inf')
        
        #initialize edges as NONE
            self.edge_to[i] = None
            
        #initialize markings as FALSE
        for i in graph.vertex_list:
            self.is_marked[i] = False
        
        ######################################################
        ######################################################
        
        #no change needed
        self.dist_to[init_v] = 0
        
        #TODO: modify the function
        self.shortest_path(self.graph)

    #change this function
    #check branches instead of smallest weight
    def shortest_path(self, graph: GraphUndirected):
        
        #TODO: modify MinHeap() to be str compatible OR replace entirely
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
        
        #TODO: modify scan() function
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
   
    #autofail check#1: branching
    #if there is a branch between a single resistor's two nodes, then it is automatically neither 
    if(shallowbranch_check(node11,node12,graph) or shallowbranch_check(node21,node22,graph)):
        return False
    
    #autofail check#2: cornered by Vdd and GND
    #if a single resistor is cornered by these two circuit points, it is automatically neither
    if(VG_check(node11,node12) or VG_check(node12,node22)):
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
#resistor and queries
R, Q= map(int, input().split())

#R = number of resistors
#Q = number of queries


#call the resistor processing function
#return a dictionary, keylist, and vertex list
R_dict, R_keys, R_nodes = R_input(R)

#create the resistor graph
Resistor_graph = GraphUndirected(R_nodes)

#add the resistors as edges to the graph
for resistor in R_keys:
    Resistor_graph.add_edge(R_dict[resistor].node1,R_dict[resistor].node2,R_dict[resistor].name)
#perform queries
Q_count = 0
while Q_count<Q:
    #increment
    Q_count+=1

    #map the string keys
    Key1, Key2 = map(str, input().split())

    #call the checker function
    #recall: Resistor_check(start, end, graph, dictionary):
    Path = Resistor_check(Key1, Key2, Resistor_graph, R_dict) 

    print(Path)
    
#references
# EEE121 Week 11 Lecture Guide for Dijkstra Algorithm
# https://colab.research.google.com/drive/1st36PdGYt3yGefdThVqxTpOuhMz8E19I?usp=sharing

