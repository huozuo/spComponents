'''
just for test
'''

import networkx as nx
import numpy as np

def list_of_groups(list_info, per_list_len):
    '''
    :param list_info:   列表
    :param per_list_len:  每个小列表的长度
    :return:
    '''
    list_of_group = zip(*(iter(list_info),) *per_list_len)
    end_list = [list(i) for i in list_of_group] # i is a tuple
    count = len(list_info) % per_list_len
    end_list.append(list_info[-count:]) if count !=0 else end_list
    return end_list

# g = nx.Graph()
#
# g.add_edge(1,3)
# g.add_edge(2,3)
# g.add_edge(3,4)
#
# for start,end in g.edges:
#     print(start,end)
#     print(type(start))

# ll = [1,2,3,4,5,6]
#
# print(list_of_groups(ll,3))

a = np.zeros((3,2))
a[2][0] = 2
a[0][1] = 2
b = np.zeros((3,1))
b[2][0] = 3
c = np.concatenate((a,b),axis=1)
print(c)

print("21.12.27.15:43 test")
print("21.12.27.15:48 test")
print("21.12.27.16:11 test")
print("21.12.28.15:57 test")
print("21.12.28.17:22 test")