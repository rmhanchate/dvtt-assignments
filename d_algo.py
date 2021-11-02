#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from copy import deepcopy
from utils import print_dict, parse

dcubes = [[[['0', 'X', '0'], ['X', '0', '0'], ['1', '1', '1'], ['N', 'N', 'N']], [['0', 'X', '1'], ['X', '0', '1'], ['1', '1', '0'], ['N', 'N', 'N']], [['0', '0', '0'], ['X', '1', '1'], ['1', 'X', '1'], ['N', 'N', 'N']], [['0', '0', '1'], ['X', '1', '0'], ['1', 'X', '0'], ['N', 'N', 'N']], [['0', '0', '0'], ['0', '1', '1'], ['1', '0', '1'], ['1', '1', '0']], [['0', '0', '1'], ['0', '1', '0'], ['1', '0', '0'], ['1', '1', '1']], [['0', '1', 'N'], ['1', '0', 'N'], ['N', 'N', 'N'], ['N', 'N', 'N']], [['0', '0', '0'], ['1', '1', '1'], ['N', 'N', 'N'], ['N', 'N', 'N']]],
          [[['1', '1', 'D'], ['0', 'X', 'E'], ['X', '0', 'E'], ['N', 'N', 'N']], [['1', '1', 'E'], ['0', 'X', 'D'], ['X', '0', 'D'], ['N', 'N', 'N']], [['0', '0', 'E'], ['X', '1', 'D'], ['1', 'X', 'D'], ['N', 'N', 'N']], [['0', '0', 'D'], ['X', '1', 'E'], ['1', 'X', 'E'], ['N', 'N', 'N']], [['0', '1', 'D'], ['1', '0', 'D'], ['0', '0', 'E'], ['1', '1', 'E']], [['0', '0', 'D'], ['1', '1', 'D'], ['0', '1', 'E'], ['1', '0', 'E']], [['0', 'D', 'N'], ['1', 'E', 'N'], ['N', 'N', 'N'], ['N', 'N', 'N']], [['0', '0', 'E'], ['1', '1', 'D'], ['N', 'N', 'N'], ['N', 'N', 'N']]],
          [[['E', '1', 'E'], ['1', 'E', 'E'], ['D', '1', 'D'], ['1', 'D', 'D']], [['E', '1', 'D'], ['1', 'E', 'D'], ['D', '1', 'E'], ['1', 'D', 'E']], [['E', '0', 'E'], ['0', 'E', 'E'], ['D', '0', 'D'], ['0', 'D', 'D']], [['E', '0', 'D'], ['0', 'E', 'D'], ['D', '0', 'E'], ['0', 'D', 'E']], [['E', '0', 'E'], ['D', '0', 'D'], ['D', '1', 'E'], ['E', '1', 'D']], [['E', '0', 'D'], ['D', '0', 'E'], ['D', '1', 'D'], ['E', '1', 'E']], [['D', 'E', 'N'], ['E', 'D', 'N'], ['N', 'N', 'N'], ['N', 'N', 'N']], [['D', 'D', 'D'], ['E', 'E', 'E'], ['N', 'N', 'N'], ['N', 'N', 'N']]]]

dinter = {'0': {'0': '0', '1': 'C', 'X': '0', 'D': 'C', 'E': 'C', 'N': 'C'},
          '1': {'0': 'C', '1': '1', 'X': '1', 'D': 'C', 'E': 'C', 'N': 'C'},
          'X': {'0': '0', '1': '1', 'X': 'X', 'D': 'D', 'E': 'E', 'N': 'C'},
          'D': {'0': 'C', '1': 'C', 'X': 'D', 'D': 'D', 'E': 'C', 'N': 'C'},
          'E': {'0': 'C', '1': 'C', 'X': 'E', 'D': 'C', 'E': 'E', 'N': 'C'},
          'N': {'0': 'C', '1': 'C', 'X': 'C', 'D': 'C', 'E': 'C', 'N': 'C'}}

gatei = {'and': 0, 'nand': 1, 'or': 2, 'nor': 3, 'xor': 4, 'xnor': 5, 'not': 6, 'wire': 7}

class checkpoint(object):
    
    def __init__(self):
        self.locat = []
        self.typef = []
        self.paths = []
        self.state = []
        self.visit = []
        
    def add_path(self, locat, typef, paths, state, visit):
        self.locat.append(locat)
        self.typef.append(typef)
        self.paths.append(paths)
        self.state.append(state)
        self.visit.append(visit)

# Primitive D-Cube of Failure
def primdc(graph):
    
    def create_pdcf(graph, paths):
        visit = [0]*len(paths)
        visit[0] = 1
        [graph[graph[fault_site][1][0]][3], graph[graph[fault_site][1][1]][3], graph[fault_site][3]] = paths[0]
        dut.add_path(fault_site, 'pdcf', paths, [graph]*len(paths), visit)
    
    if graph[fault_site][0] == 'wire':
        tcube = [graph[graph[fault_site][1][0]][3], graph[graph[graph[fault_site][1][0]][2][0]][3] if graph[graph[fault_site][1][0]][2][0] != fault_site else graph[graph[graph[fault_site][1][0]][2][1]][3], graph[graph[graph[fault_site][1][0]][2][1]][3] if graph[graph[fault_site][1][0]][2][1] == fault_site else graph[graph[graph[fault_site][1][0]][2][0]][3]]
        for i in range(len(tcube)): tcube[i] = dinter[tcube[i]][dcubes[1][gatei[graph[fault_site][0]]][(1 if graph[fault_site][3] == 'D' else 0)][i]]
        graph[graph[fault_site][1][0]][3] = tcube[0]
        if graph[graph[fault_site][1][0]][2][0] != fault_site:
            graph[graph[graph[fault_site][1][0]][2][0]][3] = tcube[1]
            graph[graph[graph[fault_site][1][0]][2][1]][3] = tcube[2]
        else:
            graph[graph[graph[fault_site][1][0]][2][1]][3] = tcube[1]
            graph[graph[graph[fault_site][1][0]][2][0]][3] = tcube[2]
        
    elif graph[fault_site][0] in ['and', 'nand', 'or', 'nor', 'xor', 'xnor']:
        tcube = [graph[graph[fault_site][1][0]][3], graph[graph[fault_site][1][1]][3], graph[fault_site][3]]
        paths = [[dinter[tcube[j]][dcubes[1][gatei[graph[fault_site][0]]][i][j]] for j in range(len(tcube))] for i in range(len(dcubes[1][gatei[graph[fault_site][0]]])) if 'C' not in [dinter[tcube[j]][dcubes[1][gatei[graph[fault_site][0]]][i][j]] for j in range(len(tcube))]]
        if len(paths) == 1: [graph[graph[fault_site][1][0]][3], graph[graph[fault_site][1][1]][3], graph[fault_site][3]] = paths[0]
        elif len(paths) > 1:
            if dut.locat:
                if dut.locat[-1] == fault_site and dut.typef[-1] == 'pdcf':
                    choice = dut.visit[-1].index(0)
                    graph = deepcopy(dut.state[-1][choice])
                    dut.visit[-1][choice] = 1
                    [graph[graph[fault_site][1][0]][3], graph[graph[fault_site][1][1]][3], graph[fault_site][3]] = dut.paths[-1][choice]
                    for i in range(len(graph[fault_site][1])): graph[graph[fault_site][1][i]][3] = dut.paths[choice][i]
                else: create_pdcf(graph, paths)
            else: create_pdcf(graph, paths)
        else: return 1, graph

    elif graph[fault_site][0] == 'not':
        tcube = [graph[graph[fault_site][1][0]][3], graph[fault_site][3]]
        for i in range(len(tcube)): tcube[i] = dinter[tcube[i]][dcubes[1][gatei[graph[fault_site][0]]][(1 if graph[fault_site][3] == 'D' else 0)][i]]
        [graph[graph[fault_site][1][0]][3], graph[fault_site][3]] = tcube
    
    return 0, graph

# D Drive for Propagating Fault Effect
def ddrive(graph, node):
    
    def create_pdf_fan(node, graph):
        paths = [i for i in graph[node][2]]
        visit = [0]*len(paths)
        visit[0] = 1
        dut.add_path(node, 'pdf_fan', paths, [graph]*len(paths), visit)
        return paths[0]
    
    def create_pdf(node, paths, graph):
        visit = [0]*len(paths)
        visit[0] = 1
        [graph[graph[graph[node][2][0]][1][0]][3], graph[graph[graph[node][2][0]][1][1]][3], graph[graph[node][2][0]][3]] = paths[0]
        dut.add_path(node, 'pdf', paths, [graph]*len(paths), visit)
        return graph
    
    while(True):
        
        if len(graph[node][2]) == 2:
            [graph[node][3], graph[graph[node][2][0]][3], graph[graph[node][2][1]][3]] = dcubes[2][gatei['wire']][0] if graph[node][3] == 'D' else dcubes[2][7][1]
            if dut.locat:
                if dut.locat[-1] == node and dut.typef[-1] == 'pdf_fan':
                    try:
                        choice = dut.visit[-1].index(0)
                        graph = deepcopy(dut.state[-1][choice])
                        dut.visit[-1][choice] = 1
                        node = dut.paths[-1][choice]
                    except IndexError: return 1, graph
                else: node = create_pdf_fan(node, graph)
            else: node = create_pdf_fan(node, graph)
        
        elif len(graph[node][2]) == 1:
            if graph[graph[node][2][0]][0] in ['and', 'nand', 'or', 'nor', 'xor', 'xnor', 'not']:
                tcube = [graph[graph[graph[node][2][0]][1][0]][3], graph[graph[graph[node][2][0]][1][1]][3], graph[graph[node][2][0]][3]] if graph[graph[node][2][0]][0] in ['and', 'nand', 'or', 'nor', 'xor', 'xnor'] else [graph[graph[graph[node][2][0]][1][0]][3], graph[graph[node][2][0]][3]]
                paths = [[dinter[tcube[j]][dcubes[2][gatei[graph[graph[node][2][0]][0]]][i][j]] for j in range(len(tcube))] for i in range(len(dcubes[2][gatei[graph[graph[node][2][0]][0]]])) if 'C' not in [dinter[tcube[j]][dcubes[2][gatei[graph[graph[node][2][0]][0]]][i][j]] for j in range(len(tcube))]]
                if tcube == ['D', 'D', 'X']: paths.append(['D', 'D', 'D']) if graph[graph[node][2][0]][0] in ['and', 'or'] else paths.append(['D', 'D', 'E'])
                elif tcube == ['E', 'E', 'X']: paths.append(['E', 'E', 'E']) if graph[graph[node][2][0]][0] in ['and', 'or'] else paths.append(['E', 'E', 'D'])
                if len(paths) == 1:
                    if graph[graph[node][2][0]][0] in ['and', 'nand', 'or', 'nor', 'xor', 'xnor']: [graph[graph[graph[node][2][0]][1][0]][3], graph[graph[graph[node][2][0]][1][1]][3], graph[graph[node][2][0]][3]] = paths[0] 
                    else: [graph[graph[graph[node][2][0]][1][0]][3], graph[graph[node][2][0]][3]] = paths[0]
                    node = graph[node][2][0]
                elif len(paths) > 1:
                    if dut.locat:
                        if dut.locat[-1] == node and dut.typef[-1] == 'pdf':
                            choice = dut.visit[-1].index(0)
                            graph = deepcopy(dut.state[-1][choice])
                            dut.visit[-1][choice] = 1
                            [graph[graph[graph[node][2][0]][1][0]][3], graph[graph[graph[node][2][0]][1][1]][3], graph[graph[node][2][0]][3]] = dut.paths[-1][choice]
                        else: graph = create_pdf(node, paths, graph)
                    else: graph = create_pdf(node, paths, graph)
                    node = graph[node][2][0]
                else: return 1, graph
                
            elif graph[graph[node][2][0]][0] == 'out': break
        
    return 0, graph

# Justification
def justify(graph):
    
    for i in [str(j) for j in sorted([int(i) for i in list(graph.keys()) if graph[i][0] != 'out'], reverse = True)]:
        if graph[i][3] != 'X' and graph[i][3] in ['0', '1']:
            
            if graph[i][0] == 'wire' and fault_site not in [graph[graph[i][1][0]][2][0], graph[graph[i][1][0]][2][1]]:
                tcube = [graph[graph[i][1][0]][3], graph[graph[graph[i][1][0]][2][0]][3], graph[graph[graph[i][1][0]][2][1]][3]]
                if tcube in [['X']*len(tcube), ['D']*len(tcube), ['E']*len(tcube)]: continue
                else:
                    paths = [[dinter[tcube[j]][dcubes[0][7][k][j]] for j in range(len(tcube))] for k in range(len(dcubes[0][7])) if 'C' not in [dinter[tcube[j]][dcubes[0][7][k][j]] for j in range(len(tcube))]]
                    if paths: [graph[graph[i][1][0]][3], graph[graph[graph[i][1][0]][2][0]][3], graph[graph[graph[i][1][0]][2][1]][3]] = paths[0]
                    else: return 1, graph
            
            elif graph[i][0] in ['and', 'nand', 'or', 'nor', 'xor', 'xnor', 'not']:
                tcube = [graph[graph[i][1][0]][3], graph[graph[i][1][1]][3], graph[i][3]] if graph[i][0] in ['and', 'nand', 'or', 'nor', 'xor', 'xnor'] else [graph[graph[i][1][0]][3], graph[i][3]]
                if (tcube == ['X', 'X', 'X'] and graph[i][0] in ['and', 'nand', 'or', 'nor', 'xor', 'xnor']) or (tcube == ['X', 'X'] and graph[i][0] == 'not'): continue
                elif 'X' in tcube:
                    paths = [[dinter[tcube[j]][dcubes[0][gatei[graph[i][0]]][k][j]] for j in range(len(tcube))] for k in range(len(dcubes[0][gatei[graph[i][0]]])) if 'C' not in [dinter[tcube[j]][dcubes[0][gatei[graph[i][0]]][k][j]] for j in range(len(tcube))]]
                    visit = [0]*len(paths)
                    if len(paths) == 1:
                        if graph[i][0] in ['and', 'nand', 'or', 'nor', 'xor', 'xnor']: [graph[graph[i][1][0]][3], graph[graph[i][1][1]][3], graph[i][3]] = paths[0]
                        else: [graph[graph[i][1][0]][3], graph[i][3]] = paths[0]
                        visit[0] = 1
                    elif len(paths) > 1:
                        if dut.locat[-1] == i and dut.typef[-1] == 'sc':
                            choice = dut.visit[-1].index(0)
                            graph = deepcopy(dut.state[-1][choice])
                            dut.visit[-1][choice] = 1
                            [graph[graph[i][1][0]][3], graph[graph[i][1][1]][3], graph[i][3]] = dut.paths[-1][choice]
                        else:
                            visit = [0]*len(paths)
                            visit[0] = 1
                            [graph[graph[i][1][0]][3], graph[graph[i][1][1]][3], graph[i][3]] = paths[0]
                            dut.add_path(i, 'sc', paths, [graph]*len(paths), visit)
                    else: return 1, graph
            
    return 0, graph

# Stack Operations
def stack_ops(graph, called_by):
    
    flag = 1
    while(flag):
        if not dut.locat: return 1, graph
        if dut.typef[-1] == 'pdcf' and dut.visit[-1][-1] == 0:
            flag, graph = primdc(graph)
            if called_by == 'ddrive' and flag == 0: flag, graph = ddrive(graph, dut.locat[-1])
            elif called_by == 'justify' and flag == 0:
                flag, graph = ddrive(graph, dut.locat[-1])
                if flag == 0: flag, graph = justify(graph)
        elif dut.typef[-1] in ['pdf_fan', 'pdf'] and dut.visit[-1][-1] == 0:
            flag, graph = ddrive(graph, dut.locat[-1])
            if called_by == 'justify' and flag == 0: flag, graph = justify(graph)
        elif dut.typef[-1] == 'sc' and dut.visit[-1][-1] == 0: flag, graph = justify(graph)
        else:
            dut.locat.pop()
            dut.paths.pop()
            dut.state.pop()
            dut.typef.pop()
            dut.visit.pop()
            
    return flag, graph

# Driver Function
def main():
    
    filename = 'dvtt.isc'
    lines = open(filename,'r').readlines()
    gates = {'not', 'and', 'nand', 'or', 'nor', 'xor', 'xnor', 'buff'}
    graph = parse(lines, gates)
    graph = {k: v[0:-1] for k, v in graph.items()}
    for i in graph.keys(): graph[i].append('X')
    
    global fault_site
    fault_site = '10'
    fault_type = 'sa1'
    test_vector = {'1': 'X', '4': 'X', '7': 'X'}
    graph[fault_site][3] = 'D' if fault_type == 'sa0' else 'E'
    
    global dut
    dut = checkpoint()
    
    flag, graph = primdc(graph)
    if flag == 1: flag, graph = stack_ops(graph, 'primdc')
    if flag == 1: sys.exit('Fault Untestable')
        
    node = fault_site
    flag, graph = ddrive(graph, node)
    if flag == 1: flag, graph = stack_ops(graph, 'ddrive')
    if flag == 1: sys.exit('Fault Untestable')
        
    flag, graph = justify(graph)
    if flag == 1: flag, graph = stack_ops(graph, 'justify')
    if flag == 1: sys.exit('Fault Untestable')
        
    for i in [str(j) for j in sorted([int(i) for i in list(graph.keys()) if graph[i][0] == 'inpt'])]:
        if graph[i][3] in ['D', 'E']: test_vector[i] = '1' if graph[i][3] == 'D' else '0'
        else: test_vector[i] = graph[i][3]
        
    print('\nFault', fault_type, 'at', fault_site)
    print('\nFinal Circuit Values: ')
    print_dict(graph)
    print('\nTest Vectors: ')
    print_dict(test_vector)

if __name__ == '__main__':
    main()
