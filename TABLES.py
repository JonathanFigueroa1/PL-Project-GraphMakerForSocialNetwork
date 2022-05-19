import sys
import networkx as nx
from itertools import islice

numberOfGraphs = 0
graphList = []
ref = []
attrs = []




def createNewGraph():
    createGraph(input("Name of the Table?: "))
def createGraph(name):
    global numberOfGraphs, ref, graphList
    
    numberOfGraphs += 1
    graphName = name

    
    while graphName in graphList:
        graphName = input("Already Exist ")
   
    at = input("Add Attributes: ")
    while (not at == 'END'):
        attrs.append(at)
        at = input("Add Attributes: ")
    
    locals()[graphName] = nx.Graph()
    
    ref.append(locals()[graphName])
   
    graphList.append(graphName)
    print("Created a new network: ", graphName)

def createGraphFromFile(name, fileName):
    global numberOfGraphs, ref, graphList, attrs
    
    numberOfGraphs += 1

    graphName = name

   
    while graphName in graphList:
        graphName = input("Already Exists. ")

    
    locals()[graphName] = nx.Graph()
    
    ref.append(locals()[graphName])
 
    graphList.append(graphName)

    file = open(fileName, 'r')

    
    line1 = file.readline().strip()
    attrs = line1.split(',')
    for line in file:
        if line != '\n':
            line = line.strip()
            person = line.split(',')
            attributes= person[1:]
            locals()[graphName].add_node(person[0], Attributes=attributes)
    file.close()
    print("Created a new Table: ", graphName)

def remove(node, graphName):
    global graphList, numberOfGraphs, ref
    graph = getGraph(graphName)
    graph.remove_node(node)
    print("Erase info "+ node)

def getGraph(name):
    global graphList, numberOfGraphs, ref
    while name not in graphList:
        name = input("Network invalid! ")
    i = graphList.index(name)
    return ref[i]

def getNode(name):
    global ref
    for graph in ref :
        for node in graph.nodes :
            if(node == name) :
                return node
    print("Table not found")



def viewListOfGraphs():
   global graphList, numberOfGraphs
   print("LIST OF TABLES")
    
   if numberOfGraphs ==0:
       print("There are no Table.")
   else:
       print("There are", end, "= ")
       print(numberOfGraphs, end,"= ")
       print("networks.")
       print("They are", end,"= ")
       print(graphList)

def add(fileName, graphName):
    global attrs
    graph = getGraph(graphName)
    file = open(fileName, 'r')

    # Read each individual line and create the person
    for line in file:
        if line != '\n':
            line = line.strip()
            person = line.split(',')
            attributes = person[1:]
            graph.add_node(person[0], Attributes=attributes)
    file.close()

def addNode(graphName, nodeName):
    global attrs
    graph = getGraph(graphName)
    created= []
    for i in range(1, len(attrs)):
        created.append(input('Enter the information for '+attrs[i]+": "))
    graph.add_node(nodeName, Attributes=created[0:])
    print("Added node "+nodeName)

def operations(name):
    global graphList
    while name not in graphList:
        print("Table not found ")
        return
    print("Showing Table"+ name + "\n")
    flag = input('''Table option:
                [1] Union with another Table
                [2] Separate Table 
                [3] Copy Table
                [4] Erase Table
                [5] Exit menu
                Enter Obtion: ''')
    if(flag=='1'):
        union(name)
    elif(flag=='2'):
        disjointUnion(name)
    elif(flag=='3'):
        directedCopy(name)
    elif(flag=='4'):
        undirectedCopy(name)
    else: return



def displayGraph(graphName):
    global graphList, numberOfGraphs, ref
    i = graphList.index(graphName)
    print(ref[i].nodes(data=True))


def union(graph1):
    global graphList, numberOfGraphs, ref
    print("Table union")
    index1 =0
    index2 =0
    if numberOfGraphs < 2:
        print("No other Table to union")
    else:
        index1 = graphList.index(graph1)
        print(graphList)
        second = input("Table ")
        while second not in graphList:
            second = input("Table not valid ")
        index2 = graphList.index(second)

        graphName = input("New name: ")

        numberOfGraphs += 1
        while graphName in graphList:
            graphName = input("Already use! ")

        locals()[graphName] = nx.union(ref[index1],ref[index2])
        ref.append(locals()[graphName])
        graphList.append(graphName)


def disjointUnion(graph1):
    global graphList, numberOfGraphs, ref
    print("Erase")
    index1 =0
    index2 =0
    if numberOfGraphs < 2:
        print("Erase Table")
    else:
        print(graphList)
        index1 = graphList.index(graph1)
        second = input("Table to erase ")
        while second not in graphList:
            second = input("Table not found! ")
        index2 = graphList.index(second)

        graphName = input("New name?: ")

        numberOfGraphs += 1
        while graphName in graphList:
            graphName = input("Already use ")

        locals()[graphName] = nx.disjoint_union(ref[index1],ref[index2])
        ref.append(locals()[graphName])
        graphList.append(graphName)



def undirectedCopy(graph1):
    global graphList, numberOfGraphs, ref
    print("Copy")
    index1 = 0
    if numberOfGraphs < 1:
        print("Table not found ")
    else:
        index1 = graphList.index(graph1)

        graphName = input("New name: ")

        numberOfGraphs += 1
        while graphName in graphList:
            graphName = input("Already use ")

        locals()[graphName] = nx.to_undirected(ref[index1])
        ref.append(locals()[graphName])
        graphList.append(graphName)



def directedCopy(graph1):
    global graphList, numberOfGraphs, ref
    print("Table copy")
    index1 = 0
    if numberOfGraphs < 1:
        print("Already use: ")
        return
    else:
        while graph1 not in graphList:
            print("Table not Found! ")
            return
        index1 = graphList.index(graph1)

        graphName = input("New name: ")

        numberOfGraphs += 1
        while graphName in graphList:
            graphName = input("Already use!: ")

        locals()[graphName] = nx.to_directed(ref[index1])
        ref.append(locals()[graphName])
        graphList.append(graphName)



def subgraph():
    global graphList, numberOfGraphs, ref
    print("Table copy 2")
    if numberOfGraphs < 1:
        print("Table not found! ")
    else:
        print(graphList)
        first = input("Table to use?: ")
        while first not in graphList:
            first = input("Not found ")
        index1 = graphList.index(first)
        graphName = input("New name: ")
        numberOfGraphs += 1
        while graphName in graphList:
            graphName = input("Already use ")
        

        fileName = input("Table name to export: ")
        fileName = fileName+".csv"
       

        file = open(fileName, 'r')
        lst = []
        g = nx.Graph()
        

        for line in file:
             if line != '\n':
                 line = line.strip()
                 person = line.split(',')
                 personNode = g.add_node(person[0], age=person[1], gender=person[2], grade=person[3], vaccinated=person[4], infected=person[5])
                 lst.append(personNode)
        file.close()
        locals()[graphName] = ref[index1].subgraph(lst)
        ref.append(locals()[graphName])
        graphList.append(graphName)



