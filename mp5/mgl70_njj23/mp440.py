import inspect
import sys
import numpy as np
import numpy.matlib
import matplotlib.pyplot as plt
import pprint
import numpy.linalg as lin
'''
Raise a "not defined" exception as a reminder
'''
def _raise_not_defined():
    print "Method not implemented: %s" % inspect.stack()[1][3]
    sys.exit(1)

'''
Kalman 2D
'''
def kalman2d(data):
    scalar=.325
    Q = np.array([[10**-4,2*10**-5],[2*10**-5,10**-4]])
    R= np.array([[10**-2,5*10**-3],[5*10**-3,2**-2]])
    pk = scalar*np.matlib.identity(2)
    xk = np.zeros(2)
    estimated= []
    for i in range(len(data)):
        u1 = data[i][0]
        u2 = data[i][1]

        uk = np.array([[u1],[u2 ]])
        #uk = np.matrix([u1,u2])
        z1 = data[i][2]
        z2 = data[i][3]

        zk = np.array([[z1],[z2]])
        #zk = np.matrix([z1,z2])
        #time Update
        x_time = xk + uk
        pk_time = pk + Q
        #measurement Update
        Kk= pk_time * lin.inv(pk_time+R)
        xk= x_time + Kk.dot(zk-x_time)
        pk= pk_time.dot(np.identity(2)-Kk)
        temp = xk.tolist()
        list = []
        list.append(temp[0][0])
        list.append(temp[1][0])
        estimated.append(list)
        #estimated.append(xk.tolist())
        #print "u is: " + str(u1)
        #print "z is: " + str(z1)
        print "x is: " + str(xk)
        print "pk is: " + str(pk)
        #print "Kk is: " + str(Kk)
        #print " "

    #estimated = [[0],[0]]
    # Your code starts here
    # You should remove _raise_not_defined() after you complete your code
    # Your code ends here
    #_raise_not_defined()
    return estimated

'''
Plotting
'''
def plot(data, output):
    #pprint.pprint (data)
    x_num =[]
    y_num = []
    for x in range(len(data)):
        x_num.append(data[x][2])
        y_num.append(data[x][3])
    plt.plot(x_num,y_num,color="blue",marker="x",ms=5,label="label")
    g = sorted(output, key=lambda x: x[0])
    x_num =[]
    y_num = []
    for x in range(len(output)):
        x_num.append(g[x][0])
        y_num.append(g[x][1])
    plt.plot(x_num,y_num,color ="red",marker="o",ms=5,label="label")
    plt.show()
    # Your code starts here
    # You should remove _raise_not_defined() after you complete your code
    # Your code ends here
    return

'''
Kalman 2D
'''
scalar=0.48
pk = scalar*np.matlib.identity(2)
xk = np.array([[0],[0]])
def kalman2d_shoot(ux, uy, ox, oy, reset=False):
    global pk
    global xk
    global scalar

    decision = (0, 0, False)
    Q = np.array([[10**-4,2*10**-5],[2*10**-5,10**-4]])
    R= np.array([[10**-2,5*10**-3],[5*10**-3,2**-2]])
    print "old value: " + str(ox) + " new value: " + str(xk.tolist()[0][0])
    #initialize if reset is set to true
    if reset:
        pk = scalar*np.matlib.identity(2)
        xk = np.array([[0],[0]])
    uk = np.array([[ux],[uy]])
    zk = np.array([[ox],[oy]])

    #time Update
    x_time = xk + uk
    pk_time = pk + Q
    #measurement Update
    Kk= pk_time * lin.inv(pk_time+R)
    xk= x_time + Kk.dot(zk-x_time)
    pk= pk_time.dot(np.identity(2)-Kk)

    x= pk.tolist()


    if np.trace(pk)<.01:
        column = xk.tolist()
        decision = (column[0][0],column[1][0],True)

    # Your code starts here
    # Your code ends here
    return decision

'''
Kalman 2D
'''
def kalman2d_adv_shoot(ux, uy, ox, oy, reset=False):
    decision = (0, 0, False)
    # Your code starts here
    # Your code ends here
    _raise_not_defined()
    return decision
