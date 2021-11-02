#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Prints Graph
def print_dict(dictionary):
    for k, v in {k: v for k, v in dictionary.items() if v[0] != 'out'}.items(): print(k, ':', *v, sep='\t', end='\n')

# Parsing
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
    
    return graph
