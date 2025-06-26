#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#from loguru import logger
from typing import List
#import numpy as np

#import copy for future modification
import copy

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

class GraphUndirected:
    def __init__(self, num_vertices: int) -> None:
        self.num_vertices = num_vertices
        self.num_edges = 0
        self.adj_list = []
        for _ in range(num_vertices):
            self.adj_list.append({})
    
    def __str__(self) -> str:
        return f"adj: {self.adj_list}"

    def add_edge(self, v: int, w: int, weight: int) -> None:
        self.adj_list[v][w] = weight
        self.adj_list[w][v] = weight
        self.num_edges += 1
    
    #modify edge only if it exists
    def modify_edge(self, v: int, w: int, add: int) -> None:
        if(self.has_edge(v,w)):
            weight = self.adj_list[v][w]
            self.adj_list[v][w] = weight + add
            self.adj_list[w][v] = weight + add

    def adj(self, v: int):
        return self.adj_list[v] # returns vertices adjacent to v

    def has_edge(self, v: int, w: int) -> bool:
        if w in self.adj_list[v]:
            return True
        return False

class Edge:
    def __init__(self, src, dest, cost):
        self.src = src
        self.dest = dest
        self.cost = cost
        
####################################################
#Algorithm Class
####################################################

#unchanged
class PrimMST:
    def __init__(self, graph: GraphUndirected, init_v: int = 0) -> None:
        self.graph = graph
        self.source = init_v
        self.dist_to = [float("inf")] * graph.num_vertices
        self.dist_to[init_v] = 0
        self.edge_to = [None] * graph.num_vertices
        self.is_marked = [False] * graph.num_vertices
        self.mst = []

        self.prim(self.graph)

    def get_mst(self):
        return self.mst

    def prim(self, graph: GraphUndirected):
        pq = MinHeap()
        pq.add(self.source, 0)  # Set distance to source as 0

        # Set distance to other vertices to be inf in PQ
        for v in range(graph.num_vertices):
            if v != self.source:
                pq.add(v, float("inf"))

        p1 = pq.remove_smallest()
        self.scan(graph, pq, p1)
        while pq.size > 0:
            p1 = pq.remove_smallest()
            if self.is_marked[p1]:
                continue
            self.scan(graph, pq, p1)

    def scan(self, graph: GraphUndirected, pq: MinHeap,point: int):
        self.is_marked[point] = True
        for neighbor, weight in graph.adj(point).items():
            if self.is_marked[neighbor]:
                continue
            if self.dist_to[neighbor] > weight:
                self.dist_to[neighbor] = weight
                self.edge_to[neighbor] = point
                pq.add(neighbor, weight)
                
                
####################################################
# Main Function
# this is where objects will be created from classes
####################################################
def main():
    V, E= map(int, input().split())
   
    # YOUR CODE HERE
    
    ####################
    # Edges
    ####################
    wk12_edge=[]
    #declare list

    edge_count=0
    #declare edge counter
    
    while edge_count<E:
        edge_count+=1
        #increment
    
        src, dest, wght = map(int, input().split())
        #map to correct variables
        src-=1
        dest-=1

        wk12_edge.append(Edge(src,dest,wght))
        #create edges
        
    ####################
    # Graph
    ####################
    
    wk12_graph = GraphUndirected(num_vertices=V)
    #declare graph
    
    for edge in wk12_edge:
        wk12_graph.add_edge(edge.src, edge.dest, edge.cost)
    #add edges to the graph
    
    ####################
    # Algorithm Call
    ####################
    


    
    #Q loop
    Q=int(input())
    Q_count=0
    
    while Q_count<Q:
        Q_count+=1
        #increment
    
        start, end = map(int, input().split())
        #map to correct variables
        start-=1
        end-=1
        
        wk12_copy=0
        wk12_copy = GraphUndirected(num_vertices=V)
        for edge in wk12_edge:
            wk12_copy.add_edge(edge.src, edge.dest, edge.cost)
        #create copy
        
        wk12_copy.modify_edge(start, end, 2)
        #add plus 2 weight to the target edge
        
        prim_copy = PrimMST(wk12_copy,start)
        #call algo for the prim copy
        #change: initial vertice will now be the changed vertice
        
     
        prim = PrimMST(wk12_graph, start)
        #call prim for the unmodified graph
        #change: initial vertice will now be the changed vertice
        
        prim_weight=0
        copy_weight=0
        #weight integers
        
        for i in prim.edge_to:
            if (i != None):
                prim_weight+=i
        for j in prim_copy.edge_to:
            if (j != None):
                copy_weight+=j
        #add the path values to the prim weight integers
                

        if(prim.edge_to==prim_copy.edge_to):
            print("YES")
        else:
            print("NO")
        
        
if __name__ == "__main__":
    main()

