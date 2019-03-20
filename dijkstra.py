# from igraph import *
import pandas as pd
import numpy as np
from random_graph_generator import *
import time


inf = float("inf")
time_list = {}
node_size_list = []
# check for distance of unvistied node
def get_min_unvisited(unvisited,table):
        min_dist = inf
        min_node = ''

        for i,v in enumerate(unvisited):
                dist = table.loc[v]['shortest_distance']
                if float(min_dist) > float(dist):
                        min_dist = dist
                        min_node = v
        return min_node, min_dist

def node_neighbor(current_node, adj_matrix,table):
        current_node_neigh= adj_matrix[current_node]
        node_neigh = []
        edge_value = []
        min_edge = inf

        #get edges value connected to current_node
        # we can use Generator to get edges and thier value then pass to this method
        for i,neigh in enumerate(current_node_neigh):
                if neigh != 0:
                        node_neigh.append(current_node_neigh.index.values[i])
                        edge_value.append(neigh)
                        if min_edge > neigh:
                                min_edge = neigh
        # print(current_node_neigh)
        # print(edge_value)
        # print(node_neigh)
        # exit()

        update_table(current_node, node_neigh, edge_value, table)
        # exit()
        return node_neigh, edge_value, min_edge



#calculate_node_distance from start
# given node_name, edge_value from current to neigh , table,
def update_table(current_node,node_neigh,edge_value,table):

        #calculate node_distance by added shortest_dist of prev_node
        for niegh , dist in zip(node_neigh, edge_value):
                # neigh = table['shortest_distance'][node]
                sp_neigh_node = float(table['shortest_distance'][niegh])
                sp_current_node = float(table['shortest_distance'][current_node])
                added_dist = float(dist)

                if sp_neigh_node != inf:
                        if sp_neigh_node > sp_current_node + added_dist:
                                table.loc[niegh]['prev_vertex'] = current_node
                                sp_neigh_node = sp_current_node + added_dist
                        else:
                                sp_neigh_node = sp_neigh_node
                else:
                        table.loc[niegh]['prev_vertex'] = current_node
                        sp_neigh_node = sp_current_node + added_dist

                table['shortest_distance'][niegh] = str(sp_neigh_node)

def run_file(Generator = None ,iteration_num = None, node_size = 10, edge_node_ratio = None, dict_node_pair = {}, verbose = False):

        # print(iteration, node_size, edge_node_ratio, dict_node_pair, verbose)
        # exit()

        print("Running dijkstra.py...")

        print("Dijkstra's iteration = ", iteration_num)

        adj_matrix = Generator.Generate_adjacency_matrix(node_size)
        table = Generator.Generate_df_table(node_size)

        unvisited = Generator.get_node_list(node_size)
        edges = [pair for pair in dict_node_pair[node_size]]

        # Generator.show_df_table(node_size)
        # Generator.show_adacency_matrix(node_size)

        start = time.time()

        while len(unvisited) > 0:
                current_node, min_dist = get_min_unvisited(unvisited, table)
                try:
                        unvisited.remove(current_node)
                except:
                        if verbose:
                                print("Done. all nodes are explored")
                        break

                #return these value, so it is easier to investigate when debug.
                node_neighs, edge_value, min_edge = node_neighbor(current_node, adj_matrix, table)

        end = time.time()
        total = end - start

        if verbose:
                report(node_size, edges, table, offset=5)

        return total

if __name__ == "__main__":

        import parameter as param
        iteration = param.iteration
        node_size = param.node_size
        edge_node_ratio = param.ratio
        dict_node_pair = param.dict_node_pair

        run_file(iteration, node_size, edge_node_ratio, dict_node_pair, verbose = True)