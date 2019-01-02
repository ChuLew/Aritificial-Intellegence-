import random
''' ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ '''
'''
                For Search Algorithms
'''
''' ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ '''
bfs= []
dfs= []
uc= []
a=[]
visited=[]
costA=0
'''
BFS add to queue
'''
def add_to_queue_BFS(node_id, parent_node_id, cost, initialize=False):
    global bfs
    if initialize==True:
        bfs= []
        bfs.append((node_id,parent_node_id))
    else:
        #check to see if the node is not in the queue
        bfs.append((node_id,parent_node_id))
    return

'''
BFS add to queue
'''
def is_queue_empty_BFS():
    global bfs
    if not bfs:
        return True
    else:
        return False

'''
BFS pop from queue
'''
def pop_front_BFS():
    (node_id, parent_node_id) = (0, 0)
    return bfs.pop(0)

'''
DFS add to queue
'''
def add_to_queue_DFS(node_id, parent_node_id, cost, initialize=False):
    global dfs
    if initialize==True:
        dfs= []
        dfs.append((node_id,parent_node_id))
    else:
        dfs.append((node_id,parent_node_id))
    return

'''
DFS add to queue
'''
def is_queue_empty_DFS():
    global dfs
    if not dfs:
        return True
    else:
        return False

'''
DFS pop from queue
'''
def pop_front_DFS():
    (node_id, parent_node_id) = (0, 0)
    global dfs
    return dfs.pop(len(dfs)-1)

'''
UC add to queue
'''
def add_to_queue_UC(node_id, parent_node_id, cost, initialize=False):
    # Your code here
    global uc
    global visited
    if initialize==True:
        uc=[]
        uc.append((node_id,parent_node_id,cost))
    else:
        sum_cost= cost
        present= False
        for x in range(len(visited)):
            if visited[x][0]==parent_node_id:
                if sum_cost<visited[x][1]:
                    del visited[x]
                    visited.append((parent_node_id,sum_cost))
                present= True
                break
        if not present:
            visited.append((parent_node_id,sum_cost))
        uc.append((node_id,parent_node_id,sum_cost))
    return

'''
UC add to queue
'''
def is_queue_empty_UC():
    global uc
    if not uc:
        return True
    else:
        return False

'''
UC pop from queue
'''
def pop_front_UC():
    (node_id, parent_node_id) = (0, 0)
    global uc
    min_cost_index= uc.index(min(uc,key= lambda t: t[2]))
    min_cost_node= uc.pop(min_cost_index)
    return (min_cost_node[0], min_cost_node[1])

'''
A* add to queue
'''
def add_to_queue_ASTAR(node_id, parent_node_id, cost, initialize=False):
    global a
    if initialize == True:
        a = []
        a.append((node_id, parent_node_id, cost))
    else:
        totalCost = cost
        a.append((node_id, parent_node_id, totalCost))
    return


'''
A* add to queue
'''
def is_queue_empty_ASTAR():
    global a
    if len(a) > 0:
        return False
    else:
        return True


'''
A* pop from queue
'''


def pop_front_ASTAR():
    (node_id, parent_node_id) = (0, 0)
    global a
    global costA
    minimumNode = a.pop(a.index(min(a, key=lambda t: t[2])))
    costA = minimumNode[2]
    return (minimumNode[0], minimumNode[1])

''' ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ '''
'''
                For n-queens problem
'''
''' ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ '''


'''
Compute a random state
'''
def get_random_state(n):
    state = []
    for x in range(n-1):
        state.append(random.randint(0,n-1))
    return state

'''
Compute pairs of queens in conflict
'''
def compute_attacking_pairs(state):
    #state = [4,5,6,3,4,5,6,5]
    number_attacking_pairs = 0

    for x in range(len(state)-1):
        count = 1
        for y in range(x+1,len(state)):
            if(state[x]==state[y]):
                 number_attacking_pairs +=1
            top = state[x]+count
            bottom = state[x]-count
            if(state[y]==top):
                number_attacking_pairs+=1
            if(state[y]==bottom):
                number_attacking_pairs+=1
            count+=1

    return number_attacking_pairs

'''
The basic hill-climing algorithm for n queens
'''
def hill_desending_n_queens(state, comp_att_pairs):
    final_state =[]
    columnList = []
    temp_state = state[:]
    minList = []
    while(final_state!=state):
        for x in range(len(state)):
            columnList.append([])
            for y in range(len(state)):
                temp_state[x] = y
                columnList[x].append(comp_att_pairs(temp_state))
            temp_state = state[:]
            minList.append(min(columnList[x]))
        z = minList.index(min(minList))
        final_state=state[:]
        state[z] = columnList[z].index(min(columnList[z]))
        minList = []
        columnList = []
    return final_state

'''
Hill-climing algorithm for n queens with restart
'''
def n_queens(n, get_rand_st, comp_att_pairs, hill_descending):
        final_state = get_random_state(n)

        while (1):
            state = hill_desending_n_queens(final_state,comp_att_pairs)
            #get to local minimum
            while (comp_att_pairs(state) < comp_att_pairs(final_state)):
                final_state = state
                state = hill_desending_n_queens(final_state,comp_att_pairs)
            #break if in valid state
            if (comp_att_pairs(final_state) == 0):
                return final_state
            #random
            final_state = get_random_state(n)
