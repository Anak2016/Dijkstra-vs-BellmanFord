

# def Bellman-Ford():

import pandas as pd
import numpy as np
from random_graph_generator import *
import time

time_list = {}
node_size_list = []
def update(i,j, adj_matrix, table, vertices):
    sp = "shortest_distance"
    dist_j = table[sp][j]
    i = vertices[i]
    j = vertices[j]
    new_dist = float(table[sp][i]) + float(adj_matrix[i][j])
    # print(adj_matrix[i][j])
    # print(table[sp][j])
    # print(new_dist)
    # exit()

    table[sp][j] = min([float(dist_j),float(new_dist)])
    # print(table[sp][i])
    # exit()

def run_file(Generator = None ,iteration_num = None, node_size = 10, edge_node_ratio = None, dict_node_pair = {}, verbose = False):

    # print(iteration, node_size, edge_node_ratio, dict_node_pair, verbose)
    # exit()

    print("Running Bellman_Ford.py...")


    print("Bellman_Ford's iteration = ", iteration_num)

    adj_matrix = Generator.Generate_adjacency_matrix(node_size)
    table = Generator.Generate_df_table(node_size)

    vertices = Generator.get_node_list(node_size)
    edges = [ pair for pair in dict_node_pair[node_size]]

    # Generator.show_df_table(node_size)
    # Generator.show_adacency_matrix(node_size)

    start = time.time()
    for i in range(0,len(vertices)-1):
        for i,j in edges:
            update(i,j, adj_matrix, table, vertices) # fixed update for Bellman-Ford

    end = time.time()
    total = end - start

    time_list[node_size] = total

    if verbose:
        report(node_size, edges, table, offset = 5)

    return total

if __name__ == "__main__":

    import parameter as param
    iteration = param.iteration
    node_size = param.node_size
    edge_node_ratio = param.ratio
    dict_node_pair = param.dict_node_pair

    run_file(iteration, node_size, edge_node_ratio, dict_node_pair, verbose = True)