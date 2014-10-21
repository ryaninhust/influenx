def simpath_spread(S,eta,U,G,b):
    Sigma = 0       # Initilize the Sigma
    result = 0
    V = G.nodes()   # V is all nodes set
    spd_dict = {}   # D[x] maintains the out-neighbors of x
    for j in G.nodes():
        spd_dict[j] = {}
    for k in G.nodes():
        for p in G.nodes():
            spd_dict[k][p] = 0      #Initilize the Edge Weight Value
    for u in S:
        temp = set(V) - set(S)  # V minus S
        temp.add(u)     # V minus S append u
        [result,spd_dict] = back_track(u,eta,temp,U,G,b,spd_dict)
        #Sigma += Sigma # Each node in S calls BackTrack
        Sigma += result
    return Sigma,spd_dict


def back_track(u,eta,W,U,G,b,spd_dict):
    Q  = list()     # Stack that maintain the current nodes on the path
# Initilize the Q,spd,pp and D
    Q.append(u)
    spd = 1
    pp = 1  # Maintain the weight of the current path
# Produce D
    D = {}  # D[x] maintains the out-neighbors of x
    for i in G.nodes():
        D[i] = []
    while Q:
        [Q,D,spd,pp,spd_dict] = forward(Q,D,spd,spd_dict,pp,eta,W,U,G,b,u)
        u = Q.pop()
        #print ('D',u,spd,pp)
        if Q:   # When the Q is Null,stop the process
            v = Q[-1]
            pp = float(pp)/ b[v][u]
        #print (b[v][u],pp)
    return spd,spd_dict


def forward(Q,D,spd,spd_dict,pp,eta,W,U,G,b,u):
    x  = Q[-1]
    i = 0
    flag = True
    v = ''
    s = ''
    while flag:
        ys = G.successors(x)
        if len(ys) == 0:
            flag = False
            break
        while len(ys) > 0:
            y = ys[i]
            i += 1
            if y not in Q and y not in D[x] and y in W:     # y is not included in Q and Dx
                if pp * b[x][y] < eta:
                    D[x].append(y)
                else:
                    Q.append(y)
                    pp *= b[x][y]
                    spd += pp
                    D[x].append(y)  # Add y to x
                    x = Q[-1]
                    #print U
                    for v in U:
                        if v not in Q:
                            #print 'v=',v,W-set(v)
                            for s in W - set(v):
                                #print 'w',W - set(v),s,u,spd_dict[s][u]
                                spd_dict[s][u] += pp
                                #print 'ss',spd_dict[s][u]
                    i = 0
                    break
            if i == len(ys):
                flag = False
                #print 'here',spd_dict
                break
    return Q,D,spd,pp,spd_dict
