'''
Author: Theo_hui
Date: 2021-05-18 15:33:29
Descripttion: 自己设计的一种基于选举制的启发式社区发现算法
'''
import time
import random

import networkx as nx
import matplotlib.pyplot as plt


def algo_vote_canidates_selecte(G,n,distance_threshold=2,show_shell=False):
    ''' 从群体G中选择出n个社区的候选者（关键节点）,依据为节点的入度
    G：群体 networkx形式
    n: 社区数
    distance_threshold:候选者之间距离的最小阈值
    '''
    #shell 图 可视化
    if show_shell:
        nx.draw_shell(G,with_labels=True,node_color="#a7bbc7",node_shape='s',node_size=200)
        plt.show()
    Candidates,Degrees=[],[]
    # 获得每个节点的入度
    for node in G.nodes():
        Degrees.append(G.degree(node))
    
    # 打印结果
    with open("./logs/{}_degrees.csv".format(int(time.time())),'w') as f:
        for i,d in enumerate(Degrees):
            f.write("{},{}\n".format(i,d))
    # 排序
    Degrees=sorted(enumerate(Degrees),key=lambda x:x[1],reverse=True)
    
    #选取候选者
    i=0
    while len(Candidates)<n and i<len(G.nodes):
        node,degree=Degrees[i]
        for s in Candidates:
            if nx.shortest_path_length(G,source=node,target=s)<distance_threshold:
                continue
        else:
            Candidates.append(node)    
        i+=1

    return Candidates


def algo_vote_voter_chose(G,candidates):
    ''' 选民根据意愿进行选择'''
    def min_only(l):
        ''' 得到l的最小值，并判断是否最小值是否唯一'''
        min_v=min(l)
        if l.count(min_v)==1:
            return min_v,True
        else:
            return min_v,False
    
    def max_only(l):
        ''' 得到l的最大值，并判断是否最大值是否唯一'''
        max_v=max(l)
        if l.count(max_v)==1:
            return max_v,True
        else:
            return max_v,False

    #选民
    votes=[x for x in G.nodes if x not in candidates]
    #print(votes)
    
    #每个选民进行选择
    Communities ={x:[x,] for x in candidates}
    #print(Communities)
    with open("./logs/{}_chose.csv".format(int(time.time())),'w') as f:
        # 头部
        header="voter,"
        for s in candidates:
            header+=str(s)+","
        for s in candidates:
            header+="nei_"+str(s)+","
        header+="chosed\n"
        f.write(header)

        #每个选民投票
        unsolved=[]
        random.shuffle(votes)
        for v in votes:
            # 计算距离每个候选者之间的距离
            distance =[nx.shortest_path_length(G,source=v,target=s) for s in candidates]
            # 最小距离
            mindistance,only = min_only(distance)
            
            if not only:
                # 最小距离冲突 寻求邻居节点意见
                neighbor_count=[0 for _ in candidates]
                for neighbor  in G.neighbors(v):
                    for s in candidates:
                        if neighbor in Communities[s]:
                            neighbor_count[candidates.index(s)]+=1
                            break
                # 顺从大多数
                max_vote,only=max_only(neighbor_count)
                if not only:
                    #邻居势均力敌 后面又解决
                    unsolved.append(v)
                else:
                    f.write("{},{},{},{}\n".format(v,str(distance)[1:-1],str(neighbor_count)[1:-1],candidates[neighbor_count.index(max_vote)]))
                    Communities[candidates[neighbor_count.index(max_vote)]].append(v)
            else:
                # 没有冲突 直接加入
                f.write("{},{},{},{}\n".format(v,str(distance)[1:-1]," ,"*(len(distance)-1),candidates[distance.index(mindistance)]))
                Communities[candidates[distance.index(mindistance)]].append(v)
        
        # 处理没有解决的
        for v in unsolved:
            neighbor_count=[0 for s in candidates]
            for neighbor  in G.neighbors(v):
                for s in candidates:
                    if neighbor in Communities[s]:
                        neighbor_count[candidates.index(s)]+=1
                        break
            # 顺从大多数
            max_vote,only=max_only(neighbor_count)
            if not only:
                #邻居依旧势均力敌 随机选择
                candidates_max_index=[x[0] for x in enumerate(neighbor_count) if x[1]==max_vote]
                chosed=candidates[random.choice(candidates_max_index)]
            else:
                chosed=candidates[neighbor_count.index(max_vote)]
            
            f.write("{},{},{},{}\n".format(v,str(distance)[1:-1],str(neighbor_count)[1:-1],chosed))
            Communities[chosed].append(v)
        
        #社区转换
        Communities=[set(Communities[key]) for key in Communities.keys()]
        return Communities



def algo_vote(adj_matrix,n=2):
    '''
    adj_matrix:邻接矩阵
    n:社区数（默认为2）
    '''
    G=nx.from_numpy_matrix(adj_matrix)

    #选择n个社区候选者
    candidates=algo_vote_canidates_selecte(G,n)
    #print(candidates)
    #选民投票
    communities=algo_vote_voter_chose(G,candidates)
    print(communities)
    return communities
