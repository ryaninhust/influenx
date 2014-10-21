def simpath_spread(S,eta,U,G):
    Sigma = 0       # Initilize the Sigma
    result = 0
    V = G.nodes()   # V is all nodes set
    spd_dict = {}
    for u in S:
        temp = set(V) - set(S)  # V minus S
        temp.add(u)     # V minus S append u
        [result,spd_dict] = back_track(u,eta,temp,U,G)
        #Sigma += Sigma # Each node in S calls BackTrack
        Sigma += result
    return Sigma,spd_dict


def back_track(u,eta,W,U,G):
    spd_dict = {}
    b = G.edge
    Q  = list()     # Stack that maintain the current nodes on the path
# Initilize the Q,spd,pp and D
    Q.append(u)
    spd = 1
    pp = 1  # Maintain the weight of the current path
# Produce D
    D = {}  # D[x] maintains the out-neighbors of x
    while Q:
        [Q,D,spd,pp,spd_dict] = forward(Q,D,spd,spd_dict,pp,eta,W,U,G,b,u)
        u = Q.pop()
        #print ('D',u,spd,pp)
        if Q:   # When the Q is Null,stop the process
            v = Q[-1]
            pp = float(pp)/ b[v][u]['influence']
        #print (b[v][u],pp)
    return spd,spd_dict


def forward(Q,D,spd,spd_dict,pp,eta,W,U,G,b,u):
    x  = Q[-1]
    i = 0
    flag = True
    while flag:
        ys = G.successors(x)
        if len(ys) == 0:
            flag = False
            break
        while len(ys) > 0:
            y = ys[i]
            i += 1
            if y not in Q and y not in D.get(x, []) and y in W:     # y is not included in Q and Dx
                if pp * b[x][y]['influence'] < eta:
                    x_list = D.get(x, [])
                    x_list.append(y)
                    D[x] = x_list
                else:
                    Q.append(y)
                    pp *= b[x][y]['influence']
                    spd += pp
                    x_list = D.get(x, [])
                    x_list.append(y)
                    D[x] = x_list
                    x = Q[-1]
                    #print U
                    for v in U:
                        if v not in Q:
                            tmp_pp = spd_dict.get(v, 0)
                            tmp_pp += pp
                            spd_dict[v] = tmp_pp
                                #print 'ss',spd_dict[s][u]
                    i = 0
                    break
            if i == len(ys):
                flag = False
                #print 'here',spd_dict
                break
    return Q,D,spd,pp,spd_dict
