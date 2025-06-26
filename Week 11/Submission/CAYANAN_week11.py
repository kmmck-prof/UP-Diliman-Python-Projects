#!/usr/bin/env python
# coding: utf-8

# In[4]:


#classes and imports

#from loguru import logger
#from typing import List
#import numpy as np

####################################################
# minheap class
####################################################
class MinHeap:
    def __init__(self) -> None:
        self.size = 0
        self.keys = [None]  # other elements start at index 1
        self.values = [None]
    
    def __str__(self) -> str:
        return f"keys: {self.keys}, values: {self.values}"

    def add(self, item: int, value: int) -> None:
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
            
####################################################
# undirected graph
# FIXME: convert to directed graph
####################################################

#change: renamed the class
class GraphDirected:
    #unchanged
    def __init__(self, num_vertices: int) -> None:
        self.num_vertices = num_vertices
        self.num_edges = 0
        self.adj_list = []
        for _ in range(num_vertices):
            self.adj_list.append({})
    
    #unchanged
    def __str__(self) -> str:
        return f"adj: {self.adj_list}"

    #changed to directed
    def add_edge(self, v: int, w: int, weight: int) -> None:
        self.adj_list[v][w] = weight
        #self.adj_list[w][v] = weight
        #change: commented out the undirected weight
        self.num_edges += 1

    #unchanged
    def adj(self, v: int):
        return self.adj_list[v] # returns vertices adjacent to v

    #README: this function no longer works two ways
    #make sure other functions dont use this as an undirected tool
    def has_edge(self, v: int, w: int) -> bool:
        if w in self.adj_list[v]:
            return True
        return False

####################################################
# edge class
####################################################

#unchanged
class Edge:
    def __init__(self, src, dest, cost):
        self.src = src
        self.dest = dest
        self.cost = cost
        
####################################################
# Algorithm
####################################################

class Dijkstra:
    #change: the graph is now directed
    def __init__(self, graph: GraphDirected, init_v: int = 0) -> None:
        self.graph = graph 
        #undirected graphs
        
        self.source = init_v 
        #starting vertex
        
        self.dist_to = [float('inf')] * graph.num_vertices 
        #calculated distance
        
        self.dist_to[init_v] = 0 
        #self distance will always be zero
        
        self.edge_to = [None] * graph.num_vertices 
        #start all vertices at None
        
        self.is_marked = [False] * graph.num_vertices 
        #start all vertices as unmarked

        
        self.shortest_path(self.graph) 
        #call the shortest path

    def shortest_path(self, graph: GraphDirected):
        #no changes
        pq = MinHeap()
        pq.add(self.source, 0)  # Set distance to source as 0

        # Set distance to other vertices to be inf in PQ
        #no change
        for v in range(graph.num_vertices):
            if v != self.source:
                pq.add(v, float('inf'))
        
        #no changes
        p1 = pq.remove_smallest()
        self.scan(graph, pq, p1)
        
        #no changes
        while pq.size > 0:
            p1 = pq.remove_smallest()
            if self.is_marked[p1]:
                continue
            self.scan(graph, pq, p1)
    
    def scan(self, graph: GraphDirected, pq: MinHeap,point: int):
        self.is_marked[point] = True
        #no change
        
        for neighbor, weight in graph.adj(point).items():
        #README: this loop will only check directed adjacent vertices
            if self.is_marked[neighbor]:
                continue
            if self.dist_to[neighbor] > self.dist_to[point] + weight:
                self.dist_to[neighbor] = self.dist_to[point] + weight
                self.edge_to[neighbor] = point
                pq.add(neighbor, self.dist_to[point] + weight)

    #changed for no path case
    def get_shortest_path(self, dest):
        start = self.source
        end = dest
        path = []

        while end is not None:  # Check if end is not None
            path.append(end)
            end = self.edge_to[end]
            
        

        path.append(start)
        path.reverse()
        
        if(self.dist_to[dest]==float('inf')):#if there is no path, return None
            return "None", path

        return self.dist_to[dest], path
    
    
####################################################
# Main Function
# this is where objects will be created from classes
####################################################
def main():
    V, E, Q = map(int, input().split())
   
    # YOUR CODE HERE
    
    ####################
    # Edges
    ####################
    wk11_edge=[]
    #declare list

    edge_count=0
    #declare edge counter

    while edge_count<E:
        edge_count+=1
        #increment
    
        src, dest, wght = map(int, input().split())
        #map to correct variables

        wk11_edge.append(Edge(src,dest,wght))
        #create edges
        
    ####################
    # Graph
    ####################
    
    wk11_graph = GraphDirected(num_vertices=V)
    #declare graph
    
    
    for edge in wk11_edge:
        wk11_graph.add_edge(edge.src, edge.dest, edge.cost)
    #add edges to the graph
    
    ####################
    # Algorithm
    ####################

    
    #Q loop
    Q_count=0
    
    while Q_count<Q:
        Q_count+=1
        #increment
    
        start, end = map(int, input().split())
        #map to correct variables
        
        dijkstra_temp = Dijkstra(wk11_graph,start)
        #create temporary algorithm object

        target, holder=dijkstra_temp.get_shortest_path(end)
        #get the target and its list
        
        print(target)
        #print the actual target
        
        
if __name__ == "__main__":
    main()


# 
