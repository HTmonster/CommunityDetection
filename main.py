'''
Author: Theo_hui
Date: 2021-05-18 14:55:13
Descripttion: 

'''
import random

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from communities.algorithms import louvain_method,girvan_newman,hierarchical_clustering,spectral_clustering,bron_kerbosch
from communities.utilities import modularity_matrix, modularity
from communities.visualization import draw_communities

from vote_algorithms import algo_vote #自己写的算法


#读取gml格式数据到邻接矩阵
def read_gml_to_adjacency(filename,
                          show_network=False,#读取完后是否显示
                          label=None         #gml文件的label
                          ):
    # 读取数据
    G=nx.read_gml(filename,label=label)
    # 显示网络
    if show_network:
        nx.draw(G,with_labels=True,node_color="#9fe6a0",node_shape='s',node_size=200)
        plt.show()
    # 邻接矩阵
    adj_matrix=np.array(nx.adjacency_matrix(G).todense())
    return adj_matrix

# 进行社区可视化
# def draw_communities(adj_matrix,communities):
#     # colors =['coral','skyblue','read','limegreen','darkorange','palegreen']

#     G=nx.from_numpy_matrix(adj_matrix)
#     node_colors=[0 for _ in G.nodes]
    
#     for node in G.nodes:
#         for i,community in enumerate(communities):
#             if node in community:
#                 node_colors[node] = i
#                 break
#     # print(node_colors)

#     pos=[[0,0] for _ in G.nodes]
#     for i,community in enumerate(communities):
#         community=list(community)
#         pos[community[0]]=[5*(i+1),5*(i+1)]
#         for node in community[1:]:
#             pos[node]=[5*(i+1)+random.uniform(-3.0,3.0),5*(i+1)+random.uniform(-3.0,3.0)]
#     nx.draw(G,with_labels=True,node_color=node_colors,node_shape='s',node_size=200,font_color='w')
#     plt.show()

    # V = [node for node in G.nodes()]
    # print(V)
    # com_dict = {node:com for node, com in zip(V, communities)}
    # print(com_dict)
    # com = [[V[i] for i in range(G.number_of_nodes()) if communities[i] == j] for j in range(12)]

    # # 构造可视化所需要的图
    # G_graph = nx.Graph()
    # for each in com:
    #     G_graph.update(nx.subgraph(G, each))
    # color = [com_dict[node] for node in G_graph.nodes()]

    # # 可视化(社区布局)
    # pos = nx.spring_layout(G_graph, seed=4, k=0.33)
    # nx.draw(G, pos, with_labels=False, node_size=1, width=0.1, alpha=0.2)
    # nx.draw(G_graph, pos, with_labels=True, node_color=color, node_size=70, width=0.5, font_size=5, font_color='#000000')
    # plt.show()

    
if __name__ == "__main__":
    #0. 社区数
    n=12
    
    
    #1. 准备数据
    #adj_matrix=read_gml_to_adjacency("./Dataset/karate/karate.gml",label='label')
    adj_matrix=read_gml_to_adjacency("./Dataset/football/football.gml",label='label')
    #adj_matrix=read_gml_to_adjacency("./Dataset/dolphins/dolphins.gml",label='label')
    #adj_matrix=read_gml_to_adjacency("./Dataset/lesmis/lesmis.gml",label='label')
    #adj_matrix=read_gml_to_adjacency("./Dataset/power/power.gml",label=None)
    
    # print(adj_matrix,modularity_matrix(adj_matrix))

    
    # #====================[Louvain算法]========================
    communities,_=louvain_method(adj_matrix,n=n)
    print(communities)
    #计算聚合度
    print(modularity(modularity_matrix(adj_matrix),communities))
    #可视化
    # draw_communities(adj_matrix, communities)
    draw_communities(adj_matrix, communities)

    #====================[  GN算法 ]=========================
    communities,_=girvan_newman(adj_matrix,n=n)
    print(communities)
    #计算聚合度
    print(modularity(modularity_matrix(adj_matrix),communities))
    # #可视化
    # draw_communities(adj_matrix, communities)

    #===================[ 层次聚类 ]===========================               
    communities=hierarchical_clustering(adj_matrix, metric="euclidean", linkage="complete",n=n)
    print(communities)
    #计算聚合度
    print(modularity(modularity_matrix(adj_matrix),communities))
    #可视化
    # draw_communities(adj_matrix, communities)

    #==================[ 谱聚类 ]=============================               
    communities=spectral_clustering(adj_matrix, k=n)
    print(communities)
    #计算聚合度
    print(modularity(modularity_matrix(adj_matrix),communities))
    # #可视化
    # draw_communities(adj_matrix, communities)

    #===================[Bron-Kerbosch]=======================   
    communities = bron_kerbosch(adj_matrix, pivot=True)
    print(communities)
    #计算聚合度
    print(modularity(modularity_matrix(adj_matrix),communities))
    # #可视化
    # draw_communities(adj_matrix, communities)

    #===================[自己发明的]============================ 
    communities=algo_vote(adj_matrix,n=n)
    print(communities)
    #计算聚合度
    print(modularity(modularity_matrix(adj_matrix),communities))
    #可视化
    # draw_communities(adj_matrix, communities)