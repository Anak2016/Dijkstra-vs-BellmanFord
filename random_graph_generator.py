# ==================================
# === method's name contain in this file
# ====================================
#
# Generate_random_pair(current_node_index, node_size, dict_node_pair)
# Generate_adjacency_matrix(node_size,dict_node_pair)
# Generate_df_table(node_size)
#
# ====================================

import random
import numpy as np
import pandas as pd


def report(node_size,edges, table, offset = None, show_edge = False):
    print("node_size: {:d}".format(node_size))
    if show_edge:
        print("edges    : ", edges)
    print("Table is shown below:")
    if offset is None:
        print(table)
    else:
        print(table.iloc[-offset:])


#edge_node_ratio = average degree
#node_size = 10 20  40  80  160 320
#edge_size = 50 100 200 400 800 1600
#edge_node_ratio = 5
'''
dict_node_pair = {node_size1:[(left1,right1),...., (leftX, rightX)],
                ..... ,node_sizeN:[(left1,right1),...., (leftY, rightY)] }
'''
class Data_Generator:

    def __init__(self, iteration = 5, node_size=10, percentage = 50,  edge_node_ratio = None, dict_node_pair={}, verbose = False):

        self.iteration = iteration
        self.node_size = node_size
        self.verbose = verbose

        # print(iteration, node_size, percentage, edge_node_ratio, dict_node_pair, verbose)
        # exit()

        if edge_node_ratio:
            self.edge_node_ratio = edge_node_ratio
        else:
            self.edge_node_ratio = node_size * node_size / 5
        self.dict_node_pair = dict_node_pair

        if percentage is None:
            self.percentage = None
        else:
            self.percentage = percentage

        # print(self.iteration, self.node_size, self.edge_node_ratio, self.dict_node_pair, self.percentage)
        # exit()

        # self.dict_node_pair = {}
        # self.dict_node_pair[node_size] = []

    def get_node_list(self, node_size):
        return [ i for i in range(0,node_size)]

    def get_node_size(self):
        return self.node_size

    def get_iteration(self):
        return self.iteration

    def get_edge_node_ratio(self):
        return self.edge_node_ratio

    def get_dict_node_pair(self):
        return self.dict_node_pair

    #create new set of node_size
    def create_set_pair_node(self, node_size):
        dict_node_pair = self.dict_node_pair

        #update node_size
        self.node_size = node_size
        dict_node_pair[node_size] = []

        return dict_node_pair


    #it generate non-uqiue edges.
    #   eg. (0,3), (0,6), (0,3) # (0,3) is generate 2 times
    # def Generate_random_pair(self,current_node_index, dict_node_pair):
    def Generate_random_pair(self,current_node_index):

        node_size = self.get_node_size()
        dict_node_pair = self.dict_node_pair


        # rand = None
        # random.seed(101)
        if current_node_index == node_size-1:
            rand = random.randint(current_node_index,node_size-1)
        rand = random.randint(current_node_index,node_size-1)

        # print("node_size         : ", node_size)
        # print("current_node_index: ", current_node_index)
        # print("rand              : ", rand)
        # print("dict_node_pair    : ", dict_node_pair)

        # garantee no node_pair with self loop.
        if rand == current_node_index:
            return False
        else:
            #if empty, return pair
            if not dict_node_pair[node_size]:
                node_pair = (current_node_index, rand)
                dict_node_pair[node_size].append(node_pair)
                return True
            else:
                try:
                    #if not empty, check if edge is unique
                    for left, right in dict_node_pair[node_size]:

                        # if current_node_index == 0 and rand == 8:
                        #     print("Debug at (0,8)")

                        # check if node_pair already exist
                        if left == current_node_index and right == rand:
                            return False

                    node_pair = (current_node_index, rand)
                    dict_node_pair[node_size].append(node_pair)
                    return True
                    # return current_node_index, rand

                except: # error = maximum recursion
                    print("=============================")
                    print("These are parameter that cause error")
                    print("current_node_index, rand = {:d},{:d}".format(current_node_index, rand))
                    print("=============================")
                    exit()


    def show_adacency_matrix(self, node_size):
        adj_matrix = self.Generate_adjacency_matrix(node_size)
        print(adj_matrix)

    def show_df_table(self, node_size):
        table = self.Generate_df_table(node_size)
        print(table)

    #create dict where key = node_size and value = adjacency matrix
    # def Generate_adjacency_matrix(self, dict_node_pair):
    def Generate_adjacency_matrix(self, node_size):
        #edge must be generated before Generate_adjacency_matrix can be called

        # node_size = self.get_node_size()
        dict_node_pair = self.dict_node_pair

        # key_list, value_list = Get_key_value(dict_node_pair)
        try:
            pair_list = dict_node_pair[node_size]

        except:
            print("In Generate_adjacency_matrix, node_size is not a key of dict_node_pair") # Error
            exit()

        pair_list = dict_node_pair[node_size]
        adj_matrix = np.zeros(shape=(node_size, node_size))
        vertices  = range(0,node_size) # 0, .... , node_size -1

        adj_matrix = pd.DataFrame(adj_matrix, columns = vertices , index = vertices)

        random.seed(9001)
        edge_val_list = [random.randint(1,10) for i in range(1,len(pair_list)+ 1 )]

        keys = [ key for key,value in dict_node_pair.items()]

        if node_size in keys:
            pass
        else:
            print("given node_size was not generated")
            exit()

        if len(edge_val_list) != len(pair_list):
            print("length mismatch between value_list and edge_val_list")
            print("terminating the program....")
            exit()

        i = 0
        #cannot use enumerate with list of tuple
        for col,row in pair_list:
            adj_matrix[col][row] = edge_val_list[i]
            i = i + 1

        # print(adj_matrix)
        return adj_matrix

    def Generate_df_table(self, node_size):
        # node_size = self.get_node_size()

        np_sp = np.zeros(shape=(node_size, 1))
        inf = float("inf")
        np_sp1 = [[0]]
        np_sp2 = [[inf] for i in range(1, node_size)]
        np_sp = np_sp1 + np_sp2

        np_prev = [[''] for i in range(1,node_size+1)]
        table = np.hstack([np_sp, np_prev])

        sp = "shortest_distance"
        table_cols = [sp, 'prev_node']

        # table = np.zeros(shape=(node_size, 2))
        vertices = [i for i in range(0, node_size)]

        table = pd.DataFrame(table, columns=table_cols, index= vertices)
        return table

    # def show_dict_node_pair(self, dict_node_pair):
    def show_dict_node_pair(self):

        dict_node_pair = self.dict_node_pair

        for key, value in dict_node_pair.items():
            try:
                print("key: {:d}".format(key) + " value = ", value)
                print("len: ", len(value))
                print()
            except:
                print("key or value are not int")

    def run_random_model2(self):
        import itertools
        import numpy as np

        node_size = self.node_size
        iteration = self.iteration
        dict_node_pair = self.dict_node_pair
        dict_node_pair[node_size] = []
        percentage = self.percentage

        # print(iteration, node_size, percentage, dict_node_pair)
        # exit()

        if percentage is None:
            print("Error: you must specify edge percentage parameter")
            exit()

        edges_list = []
        for n in range(0,iteration):
            total_edges = (node_size**2) - node_size
            num_edges = total_edges * percentage /100
            num_edges = int(num_edges)


            for i in range(0,node_size):
                for j in range(i+1,node_size):
                    edges_list.append((i,j))
                    edges_list.append((j,i))


            # edges_list = list(itertools.permutations(edges_list))
            edges_list   = np.random.permutation(edges_list)
            edges_list   = [(i,j) for i,j in edges_list]
            edges_list = edges_list[:num_edges]
            # edges_list = edges_list.tolist()
            dict_node_pair[node_size] = edges_list

            if self.verbose:
                print("for node_size = ", node_size)
                # print("dict_node_pair[{:d}] = ".format(node_size))
                # print(dict_node_pair[node_size])
                print("value type = ", type(dict_node_pair[node_size]))
                print("len = ", len(set(dict_node_pair[node_size])))

            # print("here")
            # exit()

            edges_list = []
            node_size = node_size * 2

        return dict_node_pair

    #FIX HERE
    def run_random_model1(self):
        # lets generate 3 different node_size
        node_size = self.node_size
        iteration = self.iteration
        edge_node_ratio = self.edge_node_ratio

        # print(iteration,node_size,edge_node_ratio)
        # exit()

        loop = 0
        for n in range(0, iteration):
            edge_size = edge_node_ratio * node_size
            avg_node_degree = edge_node_ratio

            # dict_node_pair[node_size] = []
            self.create_set_pair_node(node_size)
            dict_node_pair = self.get_dict_node_pair()

            while edge_size > 0:

                if loop % 10 == 0:
                    print("loop = ", loop)

                # for each node index, geerate rand_node_pair for the index
                for node in range(0, node_size - 1): #node

                    if edge_size == 0:
                        break

                    random.seed(101)
                    rand_edge_size = random.randint(0, 2 * avg_node_degree)

                    # x = (node_size-0.3 *node_size )/2 # tuning parameter for random generator
                    # rand_edge_size = random.randint(0,node_size-1)
                    # rand_edge_size = random.randint(0, int(x) )

                    # rand_edge_size cannot exceed edge_size limit
                    if rand_edge_size >= edge_size:
                        rand_edge_size = edge_size

                    generated_edge = 0
                    # generate node_pair of size = rand_edge_size
                    for j in range(0, rand_edge_size):  # 0-8
                        # generate rand_node_pair
                        # Is_generated = Generator.Generate_random_pair(node, dict_node_pair)
                        Is_generated = self.Generate_random_pair(node)

                        if Is_generated: # Always False after len(dict_node_pair[5]) = 9 ***
                            generated_edge = generated_edge + 1

                    # print("edge_size      = {:d}".format(edge_size))
                    # print("generated_edge = {:d}".format(generated_edge))

                    # edge_size = edge_size - rand_edge_size
                    edge_size = edge_size - generated_edge
                    loop = loop + 1

            if self.verbose:
                print("for node_size = ", node_size)
                print("dict_node_pair[{:d}] = ".format(node_size))
                print(dict_node_pair[node_size])
                print("value type = ", type(dict_node_pair[node_size]))
                print("len = ", len(set(dict_node_pair[node_size])))

            # exit()
            # print()
            node_size = node_size * 2


        return dict_node_pair

if __name__ == "__main__":

    import parameter as param
    iteration = param.iteration
    node_size = param.node_size
    edge_node_ratio = param.ratio
    dict_node_pair = param.dict_node_pair
    verbose = True

    # for random model 1
    # Generator = Data_Generator(iteration, node_size, edge_node_ratio, dict_node_pair)
    # Generator.run_random_model1()

    # for random mode 2
    Generator = Data_Generator(iteration, node_size, dict_node_pair, percentage=50, verbose = verbose)
    dict_node_pair = Generator.run_random_model2()

    # print(dict_node_pair)