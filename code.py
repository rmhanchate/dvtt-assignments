#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 16:28:57 2021

@author: rmh
"""

from copy import deepcopy
from functools import reduce

# Reads ISCAS-85 Netlist
def read_file(filename):
    
    f = open(filename,'r')
    lines = f.readlines()
    f.close()
    
    return lines

# Prints Graph
def print_dict(dictionary):
    
    for k, v in dictionary.items(): print(k, ':', *v, sep='\t')
    print('\n')

# Parsing
def parse(lines, gates):
    
    data = list()
    graph = dict()
    for i in range(len(lines)):
        line = lines[i].replace('\n', '').split('\t')
        if line[0] == "*": continue
        elif len(line) > 3:
            if line[2] in gates: data.append(line + lines[i+1].replace('\n', '').split("\t"))
            elif (line[0][:1] != '\t'): data.append(line)
    
    out_count = 1
    for i in range(len(data)):
        if data[i][2] == 'inpt': graph[data[i][0]] = [data[i][2], [], [], ['sa0', 'sa1']]
        elif data[i][2] in gates:
            for j in data[i][-1*int(data[i][4]):]:
                if data[int(j) - 1][1][-3:] == 'fan':
                    graph[data[int(j) - 1][0]] = ['wire', [data[int(j) - 1][3][:-3]], [data[i][1][:-3]], ['sa0', 'sa1']]
                    for k in graph[data[int(j) - 1][0]][1]:
                        if k not in graph.keys(): graph[k] = [data[int(k) - 1][2], data[int(k) - 1][-1*int(data[int(k) - 1][4]):], [j], ['sa0', 'sa1']]
                        elif j not in graph[k][2]: graph[k][2].append(j)
                else: graph[data[int(j) - 1][0]] = [data[int(j) - 1][2], data[int(j) - 1][-1*int(data[int(j) - 1][4]):], [data[i][1][:-3]], ['sa0', 'sa1']]
        if data[i][3] == '0':
                graph[data[i][0]] = [data[i][2], data[i][-1*int(data[i][4]):], [str(len(data) + out_count)], ['sa0', 'sa1']]
                graph[str(len(data) + out_count)] = ['out', [data[i][0]], [], []]
                out_count += 1
    
    return graph

# Equivalence Fault Collapsing
def equifault(graph):
    
    for i in reversed(range(1, len(graph) + 1)):
        if graph[str(i)][0] == 'out' or graph[str(i)][0] == 'inpt': continue
        elif graph[str(i)][0] == 'and' or graph[str(i)][0] == 'nand':
            for j in graph[str(i)][1]: graph[str(j)][3].remove('sa0')
        elif graph[str(i)][0] in 'or' or graph[str(i)][0] == 'nor':
            for j in graph[str(i)][1]: graph[str(j)][3].remove('sa1')
        elif graph[str(i)][0] in 'not':
            for j in graph[str(i)][1]: graph[str(j)][3].clear()
        else: continue
    
    return graph

# Dominance Fault Collapsing
def domifault(graph):
    
    for i in reversed(range(1, len(graph) + 1)):
        flag = 0
        if graph[str(i)][0] == 'out': continue
        elif graph[str(i)][0] == 'and' or graph[str(i)][0] == 'nand':
            graph[str(i)][3].clear()
            for j in graph[str(i)][1]:
                if 'sa0' in graph[str(j)][3]: flag = 1; break
            for k in graph[str(i)][1]: 
                if j != k and flag == 1:
                    try: graph[str(k)][3].remove('sa0')
                    except ValueError: continue
        elif graph[str(i)][0] == 'or' or graph[str(i)][0] == 'nor':
            graph[str(i)][3].clear()
            for j in graph[str(i)][1]:
                if 'sa1' in graph[str(j)][3]: flag = 1; break
            for k in graph[str(i)][1]: 
                if j != k and flag == 1:
                    try: graph[str(k)][3].remove('sa1')
                    except ValueError: continue
        else: continue
    
    return graph

# Parallel Fault Simulation
def parallel_sim(graph, faults, test_vector):
    
    fault_list = [str(j) for j in sorted([int(i) for i in list(faults.keys())])]
    for i in graph.keys(): graph[i].append([0]*(len(faults) + 1))
    for i in [str(j) for j in sorted([int(i) for i in list(graph.keys())])]:
        if graph[i][0] == 'inpt': graph[i][4] = [test_vector[i]]*(len(faults) + 1)
        elif graph[i][0] == 'wire' or graph[i][0] == 'buff': graph[i][4] = [j for j in graph[graph[i][1][0]][4]]
        elif graph[i][0] == 'not': graph[i][4] = [not j for j in graph[graph[i][1][0]][4]]
        elif graph[i][0] == 'and': graph[i][4] = [int(all([[graph[j][4] for j in graph[i][1]][k][l] for k in range(len(graph[i][1]))])) for l in range(len(faults) + 1)]
        elif graph[i][0] == 'nand': graph[i][4] = [int(not all([[graph[j][4] for j in graph[i][1]][k][l] for k in range(len(graph[i][1]))])) for l in range(len(faults) + 1)]
        elif graph[i][0] == 'or': graph[i][4] = [int(any([[graph[j][4] for j in graph[i][1]][k][l] for k in range(len(graph[i][1]))])) for l in range(len(faults) + 1)]
        elif graph[i][0] == 'nor': graph[i][4] = [int(not any([[graph[j][4] for j in graph[i][1]][k][l] for k in range(len(graph[i][1]))])) for l in range(len(faults) + 1)]
        elif graph[i][0] == 'xor': graph[i][4] = [reduce(lambda x, y: x ^ y, [[graph[j][4] for j in graph[i][1]][k][l] for k in range(len(graph[i][1]))]) for l in range(len(faults) + 1)]
        elif graph[i][0] == 'xnor': graph[i][4] = [reduce(lambda x, y: int(not (x ^ y)), [[graph[j][4] for j in graph[i][1]][k][l] for k in range(len(graph[i][1]))]) for l in range(len(faults) + 1)]
        if i in faults.keys(): graph[i][4][fault_list.index(i) + 1] = 0 if faults[i] == 'sa0' else 1
    
    return graph

# Deductive Fault Simulation
def deductive_sim(graph, test_vector):

    for i in graph.keys(): graph[i].append([0, dict()])
    faults = dict()
    for i in [str(j) for j in sorted([int(i) for i in list(graph.keys())])]:
        if graph[i][0] == 'inpt': graph[i][4][0] = deepcopy(test_vector[i])
        elif graph[i][0] == 'wire' or graph[i][0] == 'buff': graph[i][4] = deepcopy(graph[graph[i][1][0]][4])
        elif graph[i][0] == 'not': graph[i][4] = [int(not graph[graph[i][1][0]][4][0]), deepcopy(graph[graph[i][1][0]][4][1])]
        elif graph[i][0] in ['and', 'nand', 'or', 'nor', 'xor', 'xnor']:
            if graph[i][0] == 'and': graph[i][4][0] = int(all([graph[j][4][0] for j in graph[i][1]]))
            elif graph[i][0] == 'nand': graph[i][4][0] = int(not all([graph[j][4][0] for j in graph[i][1]]))
            elif graph[i][0] == 'or': graph[i][4][0] = int(any([graph[j][4][0] for j in graph[i][1]]))
            elif graph[i][0] == 'nor': graph[i][4][0] = int(not any([graph[j][4][0] for j in graph[i][1]]))
            if graph[i][4][0] == (0 if graph[i][0] in ['and', 'nor'] else 1):
                for j in graph[i][1]:
                    if graph[j][4][0] == (0 if graph[i][0] in ['and', 'nand'] else 1): graph[i][4][1] = deepcopy(graph[j][4][1]) if not graph[i][4][1] else {x: graph[i][4][1][x] for x in graph[i][4][1] if x in graph[j][4][1]}
                    else: graph[i][4][1] = deepcopy(graph[j][4][1]) if not graph[i][4][1] else {x: dict([(k1, v1) for k1, v1 in deepcopy(faults).items() if k1 not in list(graph[j][4][1].keys())])[x] for x in dict([(k2, v2) for k2, v2 in deepcopy(faults).items() if k2 not in list(graph[j][4][1].keys())]) if x in graph[i][4][1]}
            else:
                for j in graph[i][1]: graph[i][4][1].update(graph[j][4][1])
        elif graph[i][0] == 'xor' or graph[i][0] == 'xnor': pass
        graph[i][4][1][i] = 'sa0' if graph[i][4][0] == 1 else 'sa1'
        faults.update(graph[i][4][1])

    return graph

# Driver Code
def main():
    
    filename = 'dvtt.isc'
    lines = read_file(filename)
    gates = {'not', 'and', 'nand', 'or', 'nor', 'xor', 'xnor', 'buff'}
    
    print('\nParsed Circuit:')
    graph = parse(lines, gates)
    graph_copy = deepcopy(graph)
    print_dict(graph)
    
    print('Equivalence Collapse Fault Circuit:')
    graph = equifault(graph)
    print_dict(graph)
    
    print('Dominance Collapse Fault Circuit:')
    graph = domifault(graph)
    print_dict(graph)
    
    graph = {k: v for k, v in graph.items() if v[0] != 'out'}
    
    print('Parallel Fault Simulation:')
    faults = {'2': 'sa1', '9': 'sa0'}
    test_vector = {'1': 0, '4': 1, '7': 1}
    graph = parallel_sim(graph, faults, test_vector)
    print_dict(graph)
    
    graph = deepcopy(graph_copy)
    graph = {k: v for k, v in graph.items() if v[0] != 'out'}
    
    print('Deductive Fault Simulation:')
    graph = deductive_sim(graph, test_vector)
    print_dict(graph)

if __name__ == '__main__':
    main()