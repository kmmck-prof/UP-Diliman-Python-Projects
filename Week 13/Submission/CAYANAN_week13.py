#!/usr/bin/env python
# coding: utf-8

# In[3]:


import heapq
def connected_components(n: int, m: int, edges):
    #################
    #Vertices
    #################
    V=n
    
    #None array of size V
    connections=[None]*V
    
    
    
    #################
    #Edges
    #################
    E=m
    
    
    ################################
    #Process Connections
    ################################
    edge_count=0
    while edge_count<E:
        #reduce by 1 to match the indexes of a list
        a=edges[edge_count][0] - 1
        b=edges[edge_count][1] - 1
        
        edge_count+=1
        
        #order in increasing size using set() and list()
        temp=list(set([a,b]))
        
        #call the recursive function that organizes array pointer
        recursion_connect(temp[0],temp[1],connections)
            #explanation of the function,
            #if the vertice is not a root, it will point to a non-negative integer
            #if this is detected, the recursive function calls itself to the next node
            #this is repeated until BOTH inputs are pointing to a negative integer
            #the two roots are compared in order to see which is "heavier"
            #the heavier root becomes the new root, and the lighter root becomes connected to that node
    
    
    ##################################
    #Final Output
    ##################################
        
    
    #declare a new list for holding the root sizes
    #use minheap
    weight_list=[]
    
    #declare a new variable to keep track of the indexes
    set_count=0
    
    #check every node inside the connections array
    for i in connections:
        #if i is NONE, then it is a single node set
        if(i==None):
            #increase the integer
            set_count+=1
            
            #add to a sorted list
            heapq.heappush(weight_list,0)
            
        #if i is less than zero, then it is root that represents a single unique set
        elif(i<0):
            #increase the integer
            set_count+=1
            
            #add to a sorted list
            heapq.heappush(weight_list,i)
    
    #convert the weights to positive and then output
    final_output1=set_count
    final_output2=""
    
    #add the weights to final output
    #convert to positive
    #recall: that the root does not include itself as part of the weight
    #therefore: final size = (positive weight)+1
    for j in weight_list:
        final_output2 +=str((j*-1)  + 1)
        final_output2 +=" "
    
    print(final_output1)
    print(final_output2)
        
    
    pass

def recursion_connect(x,y,array,none_state=0):
    current_state=none_state
    
    #if both nodes are not part of any set, 
    if(array[x]==None and array[y]==None):
        #let the smaller vertice be the root node
        array[x]=-1
        
        #let the larger vertice be the connected node
        array[y]=x
              

    #if only one of the nodes point to None, then connect it to a placeholder weight "-1"
    #perform recursion
    #the recursion will repeat until it reaches the base case of "(negative weight)+(negative weight)=(final weight)"
    elif(array[x]==None):
        #connect x to placeholder weight
        array[x]=-1
        
        #perform recursion
        #enable the none state
        recursion_connect(x,y,array,1)

    
    #same logic
    elif(array[y]==None):
        #connect y to placeholder weight
        array[y]=-1
        
        #perform recursion
        #enable the none state
        recursion_connect(x,y,array,1)

    #if array x is non-negative, then perform recursion to its next pointer
    #where "array[x]" is the integer of the node it is pointing to
    elif(array[x]>=0):
        recursion_connect(array[x],y,array,current_state)
    
    #if array y is non-negative, then perform recursion to its next pointer
    #where "array[y]" is the integer of the node it is pointing to
    elif(array[y]>=0):
        recursion_connect(x,array[y],array,current_state)
        
    #if both nodes are roots, then they should be negative
    elif(array[x]<0 and array[y]<0):
        #if the none_state is enabled, then that means that their exists a placeholder tree for the NONE input
        #reduce the weight of any root
        if(none_state==1):
            #reduce the weight via addition of 1
            array[x]+=1
        
        #if the two nodes already share the same root, do nothing
        if(x==y):
            return
        
        #x is less, therefore it is a heavier root
        elif(array[x]<=array[y]):
            #add the combined weight to root x
            array[x] += (array[y]-1)
            
            #point the "lighter" node to root x
            array[y] = x
        
        #y is less, therefore it is a heavier root
        else:
            #add the combined weight to root y
            array[y] += (array[x]-1)
            
            #point the "lighter" node to root y
            array[x]=y

def main():
    N_input, M_input=map(int, input().split())
    E_input=[]
    m_count=0
    while m_count<M_input:
        m_count+=1
        a,b=map(int, input().split())
        E_input+=[(a,b)]
    
    connected_components(N_input,M_input,E_input)
    
main()

