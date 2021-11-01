#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from copy import deepcopy

def print_dict(dictionary):
    for k, v in {k: v for k, v in dictionary.items() if v[0] != 'out'}.items(): print(k, ':', *v, sep='\t', end='\n')

def parse(lines, gates):
    data = list()
    graph = dict()
    for i in range(len(lines)):
        line = lines[i].replace('\n', '').split('\t')
        if len(line) > 3:
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
    graph = {k: v[0:-1] for k, v in graph.items()}
    for i in graph.keys(): graph[i].append('X')
    
    return graph

# sc pdcf pdf
# 0  1    2
# and nand or nor xor xnor not wire
# 0   1    2  3   4   5    6   7
dcubes = [[[['0', 'X', '0'], ['X', '0', '0'], ['1', '1', '1'], ['N', 'N', 'N']],
           [['0', 'X', '1'], ['X', '0', '1'], ['1', '1', '0'], ['N', 'N', 'N']],
           [['0', '0', '0'], ['X', '1', '1'], ['1', 'X', '1'], ['N', 'N', 'N']],
           [['0', '0', '1'], ['X', '1', '0'], ['1', 'X', '0'], ['N', 'N', 'N']],
           [['0', '0', '0'], ['0', '1', '1'], ['1', '0', '1'], ['1', '1', '0']],
           [['0', '0', '1'], ['0', '1', '0'], ['1', '0', '0'], ['1', '1', '1']],
           [['0', 'N', '1'], ['1', 'N', '0'], ['N', 'N', 'N'], ['N', 'N', 'N']],
           [['0', '0', '0'], ['1', '1', '1'], ['N', 'N', 'N'], ['N', 'N', 'N']]],
          [[['1', '1', 'D'], ['0', 'X', 'E'], ['X', '0', 'E'], ['N', 'N', 'N']],
           [['1', '1', 'E'], ['0', 'X', 'D'], ['X', '0', 'D'], ['N', 'N', 'N']],
           [['0', '0', 'E'], ['X', '1', 'D'], ['1', 'X', 'D'], ['N', 'N', 'N']],
           [['0', '0', 'D'], ['X', '1', 'E'], ['1', 'X', 'E'], ['N', 'N', 'N']],
           [['0', '1', 'D'], ['1', '0', 'D'], ['0', '0', 'E'], ['1', '1', 'E']],
           [['0', '0', 'D'], ['1', '1', 'D'], ['0', '1', 'E'], ['1', '0', 'E']],
           [['0', 'N', 'D'], ['1', 'N', 'E'], ['N', 'N', 'N'], ['N', 'N', 'N']],
           [['0', '0', 'E'], ['1', '1', 'D'], ['N', 'N', 'N'], ['N', 'N', 'N']]],
          [[['E', '1', 'E'], ['1', 'E', 'E'], ['D', '1', 'D'], ['1', 'D', 'D']],
           [['E', '1', 'D'], ['1', 'E', 'D'], ['D', '1', 'E'], ['1', 'D', 'E']],
           [['E', '0', 'E'], ['0', 'E', 'E'], ['D', '0', 'D'], ['0', 'D', 'D']],
           [['E', '0', 'D'], ['0', 'E', 'D'], ['D', '0', 'E'], ['0', 'D', 'E']],
           [['E', '0', 'E'], ['D', '0', 'D'], ['D', '1', 'E'], ['E', '1', 'D']],
           [['E', '0', 'D'], ['D', '0', 'E'], ['D', '1', 'D'], ['E', '1', 'E']],
           [['D', 'N', 'E'], ['E', 'N', 'D'], ['N', 'N', 'N'], ['N', 'N', 'N']],
           [['D', 'D', 'D'], ['E', 'E', 'E'], ['N', 'N', 'N'], ['N', 'N', 'N']]]]

dinter = {'0': {'0': '0', '1': 'C', 'X': '0', 'D': 'C', 'E': 'C', 'N': 'C'},
          '1': {'0': 'C', '1': '1', 'X': '1', 'D': 'C', 'E': 'C', 'N': 'C'},
          'X': {'0': '0', '1': '1', 'X': 'X', 'D': 'D', 'E': 'E', 'N': 'C'},
          'D': {'0': 'C', '1': 'C', 'X': 'D', 'D': 'D', 'E': 'C', 'N': 'C'},
          'E': {'0': 'C', '1': 'C', 'X': 'E', 'D': 'C', 'E': 'E', 'N': 'C'},
          'N': {'0': 'C', '1': 'C', 'X': 'C', 'D': 'C', 'E': 'C', 'N': 'C'}}

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

def primdc(graph):
    
    flag = 0
    if graph[fault_site][0] == 'wire':
        tcube = [graph[graph[fault_site][1][0]][3], graph[graph[graph[fault_site][1][0]][2][0]][3] if graph[graph[fault_site][1][0]][2][0] != fault_site else graph[graph[graph[fault_site][1][0]][2][1]][3], graph[graph[graph[fault_site][1][0]][2][1]][3] if graph[graph[fault_site][1][0]][2][1] == fault_site else graph[graph[graph[fault_site][1][0]][2][0]][3]]
        for i in range(len(tcube)): tcube[i] = dinter[tcube[i]][dcubes[1][7][(1 if graph[fault_site][3] == 'D' else 0)][i]]
        graph[graph[fault_site][1][0]][3] = tcube[0]
        if graph[graph[fault_site][1][0]][2][0] != fault_site:
            graph[graph[graph[fault_site][1][0]][2][0]][3] = tcube[1]
            graph[graph[graph[fault_site][1][0]][2][1]][3] = tcube[2]
        else:
            graph[graph[graph[fault_site][1][0]][2][1]][3] = tcube[1]
            graph[graph[graph[fault_site][1][0]][2][0]][3] = tcube[2]
        
    elif graph[fault_site][0] == 'and':
        tcube = [graph[graph[fault_site][1][0]][3], graph[graph[fault_site][1][1]][3], graph[fault_site][3]]
        paths = [[dinter[tcube[j]][dcubes[1][0][i][j]] for j in range(len(tcube))] for i in range(len(dcubes[1][0])) if 'C' not in [dinter[tcube[j]][dcubes[1][0][i][j]] for j in range(len(tcube))]]
        if len(paths) == 1:
            tcube = paths[0]
            [graph[graph[fault_site][1][0]][3], graph[graph[fault_site][1][1]][3], graph[fault_site][3]] = tcube
        elif len(paths) > 1:
            if dut.locat:
                if dut.locat[-1] == fault_site and dut.typef[-1] == 'pdcf':
                    choice = dut.visit[-1].index(0)
                    graph = deepcopy(dut.state[-1][choice])
                    dut.visit[-1][choice] = 1
                    [graph[graph[fault_site][1][0]][3], graph[graph[fault_site][1][1]][3], graph[fault_site][3]] = dut.paths[-1][choice]
                    for i in range(len(graph[fault_site][1])):
                        graph[graph[fault_site][1][i]][3] = dut.paths[choice][i]
                else:
                    locat = fault_site
                    typef = 'pdcf'
                    state = [graph]*len(paths)
                    visit = [0]*len(paths)
                    choice = 0
                    visit[choice] = 1
                    [graph[graph[fault_site][1][0]][3], graph[graph[fault_site][1][1]][3], graph[fault_site][3]] = paths[choice]
                    dut.add_path(locat, typef, paths, state, visit)
            else:
                locat = fault_site
                typef = 'pdcf'
                state = [graph]*len(paths)
                visit = [0]*len(paths)
                choice = 0
                visit[choice] = 1
                [graph[graph[fault_site][1][0]][3], graph[graph[fault_site][1][1]][3], graph[fault_site][3]] = paths[choice]
                dut.add_path(locat, typef, paths, state, visit)
        else:
            flag = 1
            return flag, graph
                
    elif graph[fault_site][0] == 'nand':
        tcube = [graph[graph[fault_site][1][1]][3], graph[graph[fault_site][1][1]][3], graph[fault_site][3]]
        paths = [[dinter[tcube[j]][dcubes[1][0][i][j]] for j in range(len(tcube))] for i in range(len(dcubes[1][1])) if 'C' not in [dinter[tcube[j]][dcubes[1][1][i][j]] for j in range(len(tcube))]]
        if len(paths) == 1:
            tcube = paths[0]
            [graph[graph[fault_site][1][0]][3], graph[graph[fault_site][1][1]][3], graph[fault_site][3]] = tcube
        elif len(paths) > 1:
            if dut.locat:
                if dut.locat[-1] == fault_site and dut.typef[-1] == 'pdcf':
                    choice = dut.visit[-1].index(0)
                    graph = deepcopy(dut.state[-1][choice])
                    dut.visit[-1][choice] = 1
                    [graph[graph[fault_site][1][0]][3], graph[graph[fault_site][1][1]][3], graph[fault_site][3]] = dut.paths[-1][choice]
                    for i in range(len(graph[fault_site][1])):
                        graph[graph[fault_site][1][i]][3] = dut.paths[-1][choice][i]
                else:
                    locat = fault_site
                    typef = 'pdcf'
                    state = [graph]*len(paths)
                    visit = [0]*len(paths)
                    choice = 0
                    visit[choice] = 1
                    [graph[graph[fault_site][1][0]][3], graph[graph[fault_site][1][1]][3], graph[fault_site][3]] = paths[choice]
                    dut.add_path(locat, typef, paths, state, visit)
            else:
                locat = fault_site
                typef = 'pdcf'
                state = [graph]*len(paths)
                visit = [0]*len(paths)
                choice = 0
                visit[choice] = 1
                [graph[graph[fault_site][1][0]][3], graph[graph[fault_site][1][1]][3], graph[fault_site][3]] = paths[choice]
                dut.add_path(locat, typef, paths, state, visit)
        else:
            flag = 1
            return flag, graph
                    
    elif graph[fault_site][0] == 'or': 
        tcube = [graph[graph[fault_site][1][0]][3], graph[graph[fault_site][1][1]][3], graph[fault_site][3]]
        paths = [[dinter[tcube[j]][dcubes[1][2][i][j]] for j in range(len(tcube))] for i in range(len(dcubes[1][2])) if 'C' not in [dinter[tcube[j]][dcubes[1][2][i][j]] for j in range(len(tcube))]]
        if len(paths) == 1:
            tcube = paths[0]
            [graph[graph[fault_site][1][0]][3], graph[graph[fault_site][1][1]][3], graph[fault_site][3]] = tcube
        elif len(paths) > 1:
            if dut.locat:
                if dut.locat[-1] == fault_site and dut.typef[-1] == 'pdcf':
                    choice = dut.visit[-1].index(0)
                    graph = deepcopy(dut.state[-1][choice])
                    dut.visit[-1][choice] = 1
                    [graph[graph[fault_site][1][0]][3], graph[graph[fault_site][1][1]][3], graph[fault_site][3]] = dut.paths[-1][choice]
                    for i in range(len(graph[fault_site][1])):
                        graph[graph[fault_site][1][i]][3] = dut.paths[-1][choice][i]
                else:
                    locat = fault_site
                    typef = 'pdcf'
                    state = [graph]*len(paths)
                    visit = [0]*len(paths)
                    choice = 0
                    visit[choice] = 1
                    [graph[graph[fault_site][1][0]][3], graph[graph[fault_site][1][1]][3], graph[fault_site][3]] = paths[choice]
                    dut.add_path(locat, typef, paths, state, visit)
            else:
                locat = fault_site
                typef = 'pdcf'
                state = [graph]*len(paths)
                visit = [0]*len(paths)
                choice = 0
                visit[choice] = 1
                [graph[graph[fault_site][1][0]][3], graph[graph[fault_site][1][1]][3], graph[fault_site][3]] = paths[choice]
                dut.add_path(locat, typef, paths, state, visit)
        else:
            flag = 1
            return flag, graph
    
    elif graph[fault_site][0] == 'nor': 
        tcube = [graph[graph[fault_site][1][0]][3], graph[graph[fault_site][1][1]][3], graph[fault_site][3]]
        paths = [[dinter[tcube[j]][dcubes[1][3][i][j]] for j in range(len(tcube))] for i in range(len(dcubes[1][3])) if 'C' not in [dinter[tcube[j]][dcubes[1][3][i][j]] for j in range(len(tcube))]]
        if len(paths) == 1:
            tcube = paths[0]
            [graph[graph[fault_site][1][0]][3], graph[graph[fault_site][1][1]][3], graph[fault_site][3]] = tcube
        elif len(paths) > 1:
            if dut.locat:
                if dut.locat[-1] == fault_site and dut.typef[-1] == 'pdcf':
                    choice = dut.visit[-1].index(0)
                    graph = deepcopy(dut.state[-1][choice])
                    dut.visit[-1][choice] = 1
                    [graph[graph[fault_site][1][0]][3], graph[graph[fault_site][1][1]][3], graph[fault_site][3]] = dut.paths[-1][choice]
                    for i in range(len(graph[fault_site][1])):
                        graph[graph[fault_site][1][i]][3] = dut.paths[-1][choice][i]
                else:
                    locat = fault_site
                    typef = 'pdcf'
                    state = [graph]*len(paths)
                    visit = [0]*len(paths)
                    choice = 0
                    visit[choice] = 1
                    [graph[graph[fault_site][1][0]][3], graph[graph[fault_site][1][1]][3], graph[fault_site][3]] = paths[choice]
                    dut.add_path(locat, typef, paths, state, visit)
            else:
                locat = fault_site
                typef = 'pdcf'
                state = [graph]*len(paths)
                visit = [0]*len(paths)
                choice = 0
                visit[choice] = 1
                [graph[graph[fault_site][1][0]][3], graph[graph[fault_site][1][1]][3], graph[fault_site][3]] = paths[choice]
                dut.add_path(locat, typef, paths, state, visit)
        else:
            flag = 1
            return flag, graph
    
    elif graph[fault_site][0] == 'xor': pass
    elif graph[fault_site][0] == 'xnor': pass
    elif graph[fault_site][0] == 'not': pass

    return flag, graph

def ddrive(graph, node):
    flag = 0
    while(not flag):
        if len(graph[node][2]) == 2:
            [graph[node][3], graph[graph[node][2][0]][3], graph[graph[node][2][1]][3]] = dcubes[2][7][0] if graph[node][3] == 'D' else dcubes[2][7][1]
            if dut.locat:
                if dut.locat[-1] == node and dut.typef[-1] == 'pdf_fan':
                    try:
                        choice = dut.visit[-1].index(0)
                        graph = deepcopy(dut.state[-1][choice])
                        dut.visit[-1][choice] = 1
                        node = dut.paths[-1][choice]
                    except IndexError:
                        flag = 1
                        return flag, graph
                else:
                    locat = node
                    typef = 'pdf_fan'
                    paths = [i for i in graph[node][2]]
                    state = [graph]*len(paths)
                    visit = [0]*len(paths)
                    choice = 0
                    visit[choice] = 1
                    node = paths[choice]
                    dut.add_path(locat, typef, paths, state, visit)
            else:
                locat = node
                typef = 'pdf_fan'
                paths = [i for i in graph[node][2]]
                state = [graph]*len(paths)
                visit = [0]*len(paths)
                choice = 0
                visit[choice] = 1
                node = paths[choice]
                dut.add_path(locat, typef, paths, state, visit)
    
        elif len(graph[node][2]) == 1:
            if graph[graph[node][2][0]][0] == 'and':
                tcube = [graph[graph[graph[node][2][0]][1][0]][3], graph[graph[graph[node][2][0]][1][1]][3], graph[graph[node][2][0]][3]]
                paths = [[dinter[tcube[j]][dcubes[2][0][i][j]] for j in range(len(tcube))] for i in range(len(dcubes[2][0])) if 'C' not in [dinter[tcube[j]][dcubes[2][0][i][j]] for j in range(len(tcube))]]
                if tcube == ['D', 'D', 'X']: paths.append(['D', 'D', 'D'])
                elif tcube == ['E', 'E', 'X']: paths.append(['E', 'E', 'E'])
                if len(paths) == 1:
                    tcube = paths[0]
                    [graph[graph[graph[node][2][0]][1][0]][3], graph[graph[graph[node][2][0]][1][1]][3], graph[graph[node][2][0]][3]] = tcube
                    node = graph[node][2][0]
                elif len(paths) > 1:
                    if dut.locat:
                        if dut.locat[-1] == node and dut.typef[-1] == 'pdf':
                            choice = dut.visit[-1].index(0)
                            graph = deepcopy(dut.state[-1][choice])
                            dut.visit[-1][choice] = 1
                            [graph[graph[graph[node][2][0]][1][0]][3], graph[graph[graph[node][2][0]][1][1]][3], graph[graph[node][2][0]][3]] = dut.paths[-1][choice]
                        else:
                            locat = node
                            typef = 'pdf'
                            state = [graph]*len(paths)
                            visit = [0]*len(paths)
                            choice = 0
                            visit[choice] = 1
                            [graph[graph[graph[node][2][0]][1][0]][3], graph[graph[graph[node][2][0]][1][1]][3], graph[graph[node][2][0]][3]] = paths[choice]
                            dut.add_path(locat, typef, paths, state, visit)
                    else:
                        locat = node
                        typef = 'pdf'
                        state = [graph]*len(paths)
                        visit = [0]*len(paths)
                        choice = 0
                        visit[choice] = 1
                        [graph[graph[graph[node][2][0]][1][0]][3], graph[graph[graph[node][2][0]][1][1]][3], graph[graph[node][2][0]][3]] = paths[choice]
                        dut.add_path(locat, typef, paths, state, visit)
                    node = graph[node][2][0]
                else:
                    flag = 1
                    return flag, graph
                
            elif graph[graph[node][2][0]][0] == 'nand':
                tcube = [graph[graph[graph[node][2][0]][1][0]][3], graph[graph[graph[node][2][0]][1][1]][3], graph[graph[node][2][0]][3]]
                paths = [[dinter[tcube[j]][dcubes[2][1][i][j]] for j in range(len(tcube))] for i in range(len(dcubes[2][1])) if 'C' not in [dinter[tcube[j]][dcubes[2][1][i][j]] for j in range(len(tcube))]]
                if tcube == ['D', 'D', 'X']: paths.append(['D', 'D', 'E'])
                elif tcube == ['E', 'E', 'X']: paths.append(['E', 'E', 'D'])
                if len(paths) == 1:
                    tcube = paths[0]
                    [graph[graph[graph[node][2][0]][1][0]][3], graph[graph[graph[node][2][0]][1][1]][3], graph[graph[node][2][0]][3]] = tcube
                    node = graph[node][2][0]
                elif len(paths) > 1:
                    if dut.locat:
                        if dut.locat[-1] == node and dut.typef[-1] == 'pdf':
                            choice = dut.visit[-1].index(0)
                            graph = deepcopy(dut.state[-1][choice])
                            dut.visit[-1][choice] = 1
                            [graph[graph[graph[node][2][0]][1][0]][3], graph[graph[graph[node][2][0]][1][1]][3], graph[graph[node][2][0]][3]] = dut.paths[-1][choice]
                        else:
                            locat = node
                            typef = 'pdf'
                            state = [graph]*len(paths)
                            visit = [0]*len(paths)
                            choice = 0
                            visit[choice] = 1
                            [graph[graph[graph[node][2][0]][1][0]][3], graph[graph[graph[node][2][0]][1][1]][3], graph[graph[node][2][0]][3]] = paths[choice]
                            dut.add_path(locat, typef, paths, state, visit)
                    else:
                        locat = node
                        typef = 'pdf'
                        state = [graph]*len(paths)
                        visit = [0]*len(paths)
                        choice = 0
                        visit[choice] = 1
                        [graph[graph[graph[node][2][0]][1][0]][3], graph[graph[graph[node][2][0]][1][1]][3], graph[graph[node][2][0]][3]] = paths[choice]
                        dut.add_path(locat, typef, paths, state, visit)
                    node = graph[node][2][0]
                else:
                    flag = 1
                    return flag, graph
            
            elif graph[graph[node][2][0]][0] == 'or':
                tcube = [graph[graph[graph[node][2][0]][1][0]][3], graph[graph[graph[node][2][0]][1][1]][3], graph[graph[node][2][0]][3]]
                paths = [[dinter[tcube[j]][dcubes[2][2][i][j]] for j in range(len(tcube))] for i in range(len(dcubes[2][2])) if 'C' not in [dinter[tcube[j]][dcubes[2][2][i][j]] for j in range(len(tcube))]]
                if tcube == ['D', 'D', 'X']: paths.append(['D', 'D', 'D'])
                elif tcube == ['E', 'E', 'X']: paths.append(['E', 'E', 'E'])
                if len(paths) == 1:
                    tcube = paths[0]
                    [graph[graph[graph[node][2][0]][1][0]][3], graph[graph[graph[node][2][0]][1][1]][3], graph[graph[node][2][0]][3]] = tcube
                    node = graph[node][2][0]
                elif len(paths) > 1:
                    if dut.locat:
                        if dut.locat[-1] == node and dut.typef[-1] == 'pdf':
                            choice = dut.visit[-1].index(0)
                            graph = deepcopy(dut.state[-1][choice])
                            dut.visit[-1][choice] = 1
                            [graph[graph[graph[node][2][0]][1][0]][3], graph[graph[graph[node][2][0]][1][1]][3], graph[graph[node][2][0]][3]] = dut.paths[-1][choice]
                        else:
                            locat = node
                            typef = 'pdf'
                            state = [graph]*len(paths)
                            visit = [0]*len(paths)
                            choice = 0
                            visit[choice] = 1
                            [graph[graph[graph[node][2][0]][1][0]][3], graph[graph[graph[node][2][0]][1][1]][3], graph[graph[node][2][0]][3]] = paths[choice]
                            dut.add_path(locat, typef, paths, state, visit)
                    else:
                        locat = node
                        typef = 'pdf'
                        state = [graph]*len(paths)
                        visit = [0]*len(paths)
                        choice = 0
                        visit[choice] = 1
                        [graph[graph[graph[node][2][0]][1][0]][3], graph[graph[graph[node][2][0]][1][1]][3], graph[graph[node][2][0]][3]] = paths[choice]
                        dut.add_path(locat, typef, paths, state, visit)
                    node = graph[node][2][0]
                else:
                    flag = 1
                    return flag, graph
            
            elif graph[graph[node][2][0]][0] == 'nor':
                tcube = [graph[graph[graph[node][2][0]][1][0]][3], graph[graph[graph[node][2][0]][1][1]][3], graph[graph[node][2][0]][3]]
                paths = [[dinter[tcube[j]][dcubes[2][3][i][j]] for j in range(len(tcube))] for i in range(len(dcubes[2][3])) if 'C' not in [dinter[tcube[j]][dcubes[2][3][i][j]] for j in range(len(tcube))]]
                if tcube == ['D', 'D', 'X']: paths.append(['D', 'D', 'E'])
                elif tcube == ['E', 'E', 'X']: paths.append(['E', 'E', 'D'])
                if len(paths) == 1:
                    tcube = paths[0]
                    [graph[graph[graph[node][2][0]][1][0]][3], graph[graph[graph[node][2][0]][1][1]][3], graph[graph[node][2][0]][3]] = tcube
                    node = graph[node][2][0]
                elif len(paths) > 1:
                    if dut.locat:
                        if dut.locat[-1] == node and dut.typef[-1] == 'pdf':
                            choice = dut.visit[-1].index(0)
                            graph = deepcopy(dut.state[-1][choice])
                            dut.visit[-1][choice] = 1
                            [graph[graph[graph[node][2][0]][1][0]][3], graph[graph[graph[node][2][0]][1][1]][3], graph[graph[node][2][0]][3]] = dut.paths[-1][choice]
                        else:
                            locat = node
                            typef = 'pdf'
                            state = [graph]*len(paths)
                            visit = [0]*len(paths)
                            choice = 0
                            visit[choice] = 1
                            [graph[graph[graph[node][2][0]][1][0]][3], graph[graph[graph[node][2][0]][1][1]][3], graph[graph[node][2][0]][3]] = paths[choice]
                            dut.add_path(locat, typef, paths, state, visit)
                    else:
                        locat = node
                        typef = 'pdf'
                        state = [graph]*len(paths)
                        visit = [0]*len(paths)
                        choice = 0
                        visit[choice] = 1
                        [graph[graph[graph[node][2][0]][1][0]][3], graph[graph[graph[node][2][0]][1][1]][3], graph[graph[node][2][0]][3]] = paths[choice]
                        dut.add_path(locat, typef, paths, state, visit)
                    node = graph[node][2][0]
                else:
                    flag = 1
                    return flag, graph
                
            elif graph[graph[node][2][0]][0] == 'xor': pass
            elif graph[graph[node][2][0]][0] == 'xnor': pass
            elif graph[graph[node][2][0]][0] == 'not': pass
            elif graph[graph[node][2][0]][0] == 'out': break
        
    return flag, graph

def justify(graph):
    flag = 0
    for i in [str(j) for j in sorted([int(i) for i in list(graph.keys()) if graph[i][0] != 'out'], reverse = True)]:
        if graph[i][3] != 'X' and graph[i][3] in ['0', '1']:
            if graph[i][0] == 'wire' and fault_site not in [graph[graph[i][1][0]][2][0], graph[graph[i][1][0]][2][1]]:
                tcube = [graph[graph[i][1][0]][3], graph[graph[graph[i][1][0]][2][0]][3], graph[graph[graph[i][1][0]][2][1]][3]]
                if tcube in [['X']*len(tcube), ['D']*len(tcube), ['E']*len(tcube)]: continue
                else:
                    paths = [[dinter[tcube[j]][dcubes[0][7][k][j]] for j in range(len(tcube))] for k in range(len(dcubes[0][7])) if 'C' not in [dinter[tcube[j]][dcubes[0][7][k][j]] for j in range(len(tcube))]]
                    if paths: [graph[graph[i][1][0]][3], graph[graph[graph[i][1][0]][2][0]][3], graph[graph[graph[i][1][0]][2][1]][3]] = paths[0]
                    else: 
                        flag = 1
                        return flag, graph
            
            elif graph[i][0] == 'and':
                tcube = [graph[graph[i][1][0]][3], graph[graph[i][1][1]][3], graph[i][3]]
                if tcube == ['X', 'X', 'X']: continue
                elif 'X' in tcube:
                    paths = [[dinter[tcube[j]][dcubes[0][0][k][j]] for j in range(len(tcube))] for k in range(len(dcubes[0][0])) if 'C' not in [dinter[tcube[j]][dcubes[0][0][k][j]] for j in range(len(tcube))]]
                    state = [graph]*len(paths)
                    visit = [0]*len(paths)
                    choice = 0
                    if len(paths) == 1:
                        [graph[graph[i][1][0]][3], graph[graph[i][1][1]][3], graph[i][3]] = paths[0]
                        visit[0] = 1
                    elif len(paths) > 1:
                        if dut.locat[-1] == node and dut.typef[-1] == 'sc':
                            choice = dut.visit[-1].index(0)
                            graph = deepcopy(dut.state[-1][choice])
                            dut.visit[-1][choice] = 1
                            [graph[graph[i][1][0]][3], graph[graph[i][1][1]][3], graph[i][3]] = dut.paths[-1][choice]
                        else:
                            locat = node
                            typef = 'sc'
                            state = [graph]*len(paths)
                            visit = [0]*len(paths)
                            choice = 0
                            visit[choice] = 1
                            [graph[graph[i][1][0]][3], graph[graph[i][1][1]][3], graph[i][3]] = paths[choice]
                            dut.add_path(locat, typef, paths, state, visit)
                    else:
                        flag = 1
                        return flag, graph
            
            elif graph[i][0] == 'nand':
                tcube = [graph[graph[i][1][0]][3], graph[graph[i][1][1]][3], graph[i][3]]
                if tcube == ['X', 'X', 'X']: continue
                elif 'X' in tcube:
                    paths = [[dinter[tcube[j]][dcubes[0][1][k][j]] for j in range(len(tcube))] for k in range(len(dcubes[0][1])) if 'C' not in [dinter[tcube[j]][dcubes[0][1][k][j]] for j in range(len(tcube))]]
                    state = [graph]*len(paths)
                    visit = [0]*len(paths)
                    locat = node
                    typef = 'sc'
                    choice = 0
                    if len(paths) == 1:
                        [graph[graph[i][1][0]][3], graph[graph[i][1][1]][3], graph[i][3]] = paths[0]
                        visit[0] = 1
                    elif len(paths) > 1:
                        if dut.locat[-1] == node and dut.typef[-1] == 'sc':
                            choice = dut.visit[-1].index(0)
                            graph = deepcopy(dut.state[-1][choice])
                            dut.visit[-1][choice] = 1
                            [graph[graph[i][1][0]][3], graph[graph[i][1][1]][3], graph[i][3]] = dut.paths[-1][choice]
                        else:
                            visit[choice] = 1
                            [graph[graph[i][1][0]][3], graph[graph[i][1][1]][3], graph[i][3]] = paths[choice]
                            dut.add_path(locat, typef, paths, state, visit)
                    else:
                        flag = 1
                        return flag, graph
            
            elif graph[i][0] == 'or':
                tcube = [graph[graph[i][1][0]][3], graph[graph[i][1][1]][3], graph[i][3]]
                if tcube == ['X', 'X', 'X']: continue
                elif 'X' in tcube:
                    paths = [[dinter[tcube[j]][dcubes[0][2][k][j]] for j in range(len(tcube))] for k in range(len(dcubes[0][2])) if 'C' not in [dinter[tcube[j]][dcubes[0][2][k][j]] for j in range(len(tcube))]]
                    state = [graph]*len(paths)
                    visit = [0]*len(paths)
                    choice = 0
                    if len(paths) == 1:
                        [graph[graph[i][1][0]][3], graph[graph[i][1][1]][3], graph[i][3]] = paths[0]
                        visit[0] = 1
                    elif len(paths) > 1:
                        if dut.locat[-1] == node and dut.typef[-1] == 'sc':
                            choice = dut.visit[-1].index(0)
                            graph = deepcopy(dut.state[-1][choice])
                            dut.visit[-1][choice] = 1
                            [graph[graph[i][1][0]][3], graph[graph[i][1][1]][3], graph[i][3]] = dut.paths[-1][choice]
                        else:
                            locat = node
                            typef = 'sc'
                            state = [graph]*len(paths)
                            visit = [0]*len(paths)
                            choice = 0
                            visit[choice] = 1
                            [graph[graph[i][1][0]][3], graph[graph[i][1][1]][3], graph[i][3]] = paths[choice]
                            dut.add_path(locat, typef, paths, state, visit)
                    else:
                        flag = 1
                        return flag, graph
                
            elif graph[i][0] == 'nor':
                tcube = [graph[graph[i][1][0]][3], graph[graph[i][1][1]][3], graph[i][3]]
                if tcube == ['X', 'X', 'X']: continue
                else:
                    paths = [[dinter[tcube[j]][dcubes[0][3][k][j]] for j in range(len(tcube))] for k in range(len(dcubes[0][3])) if 'C' not in [dinter[tcube[j]][dcubes[0][3][k][j]] for j in range(len(tcube))]]

                    state = [graph]*len(paths)
                    visit = [0]*len(paths)
                    choice = 0
                    if len(paths) == 1:
                        [graph[graph[i][1][0]][3], graph[graph[i][1][1]][3], graph[i][3]] = paths[0]
                        visit[0] = 1
                    elif len(paths) > 1:
                        if dut.locat[-1] == node and dut.typef[-1] == 'sc':
                            choice = dut.visit[-1].index(0)
                            graph = deepcopy(dut.state[-1][choice])
                            dut.visit[-1][choice] = 1
                            [graph[graph[i][1][0]][3], graph[graph[i][1][1]][3], graph[i][3]] = dut.paths[-1][choice]
                        else:
                            locat = node
                            typef = 'sc'
                            state = [graph]*len(paths)
                            visit = [0]*len(paths)
                            choice = 0
                            visit[choice] = 1
                            [graph[graph[i][1][0]][3], graph[graph[i][1][1]][3], graph[i][3]] = paths[choice]
                            dut.add_path(locat, typef, paths, state, visit)
                    else:
                        flag = 1
                        return flag, graph
            
            elif graph[i][0] == 'xor': pass
            elif graph[i][0] == 'xnor': pass
            
    return flag, graph

def flagging(graph, called_by):
    flag = 1
    while(flag):
        if not dut.locat:
            flag = 1
            break
        if dut.typef[-1] == 'pdcf' and dut.visit[-1][-1] == 0:
            flag, graph = primdc(graph)
            if called_by == 'ddrive' and flag == 0: 
                flag, graph = ddrive(graph, node)
            elif called_by == 'justify' and flag == 0:
                flag, graph = ddrive(graph, node)
                if flag == 0: flag, graph = justify(graph)
        elif dut.typef[-1] in ['pdf_fan', 'pdf'] and dut.visit[-1][-1] == 0:
            flag, graph = ddrive(graph, dut.locat[-1])
            if called_by == 'justify' and flag == 0:
                flag, graph = justify(graph)
        elif dut.typef[-1] == 'sc' and dut.visit[-1][-1] == 0:
            flag, graph = justify(graph)
        else:
            dut.locat.pop()
            dut.paths.pop()
            dut.state.pop()
            dut.typef.pop()
            dut.visit.pop()
    return flag, graph


filename = 'dvtt.isc'
lines = open(filename,'r').readlines()
gates = {'not', 'and', 'nand', 'or', 'nor', 'xor', 'xnor', 'buff'}
graph = parse(lines, gates)

fault_site = '10'
fault_type = 'sa1'
test_vector = {'1': 'X', '4': 'X', '7': 'X'}
graph[fault_site][3] = 'D' if fault_type == 'sa0' else 'E'
dut = checkpoint()
flag = 0

flag, graph = primdc(graph)
if flag == 1: flag, graph = flagging(graph, 'primdc')
if flag == 1: 
    print('Fault Untestable')
    exit()
node = fault_site
flag, graph = ddrive(graph, node)
if flag == 1: flag, graph = flagging(graph, 'ddrive')
if flag == 1: 
    print('Fault Untestable')
    exit()
flag, graph = justify(graph)
if flag == 1: flag, graph = flagging(graph, 'justify')
if flag == 1: 
    print('Fault Untestable')
    exit()
for i in [str(j) for j in sorted([int(i) for i in list(graph.keys()) if graph[i][0] == 'inpt'])]:
    if graph[i][3] in ['D', 'E']: test_vector[i] = '1' if graph[i][3] == 'D' else '0'
    else: test_vector[i] = graph[i][3]

print('Test Vectors: ')
print_dict(test_vector)
