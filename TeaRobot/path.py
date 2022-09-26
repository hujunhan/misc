import numpy as np
from scipy.sparse import csr, csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree
import matplotlib.pyplot as plt
import cv2
import networkx as nx
from networkx.algorithms.matching import max_weight_matching
from networkx.algorithms.euler import eulerian_circuit
import itertools
import three_darrow
from mpl_toolkits.mplot3d.axes3d import Axes3D
def showPath(P,path,x,y):
    H=2048
    W=1536
    Origin_IMG=cv2.imread('tea_rec.jpg')
    IMG=np.zeros_like(Origin_IMG)
    IMG[::]=255
    # P[:,0]=P[:,0]/x*1000/
    # P[:,1]=P[:,1]/y*1000
    count=0
    last_p=0
    for now_p in path:
        last_point=np.asarray((P[last_p][0]*H,P[last_p][1]*W)).astype(int)
        now_point=np.asarray((P[now_p][0]*H,P[now_p][1]*W)).astype(int)
        cv2.arrowedLine(IMG,(last_point[0],last_point[1]),(now_point[0],now_point[1]),(0,0,255),5,tipLength=0)
        last_p=now_p
        count+=1
        # cv2.imwrite('output/'+str(count)+'.jpg',IMG)
    cv2.imwrite('pure_path.jpg',IMG)
def showPath2D(P,path,x,y):
    H=2048
    W=1536
    Origin_IMG=cv2.imread('tea_rec.jpg')
    Origin_IMG = cv2.cvtColor(Origin_IMG, cv2.COLOR_BGR2RGB)
    IMG=np.zeros_like(Origin_IMG)
    IMG[::]=255
    # P[:,0]=P[:,0]/x*1000/
    # P[:,1]=P[:,1]/y*1000
    count=0
    last_p=0
    plt.imshow(IMG)
    for now_p in path:
        last_point=np.asarray((P[last_p][0]*H,P[last_p][1]*W)).astype(int)
        now_point=np.asarray((P[now_p][0]*H,P[now_p][1]*W)).astype(int)
        plt.arrow(last_point[0],last_point[1],now_point[0]-last_point[0],now_point[1]-last_point[1],
           width=0.01,head_width=40,head_length=40,length_includes_head=True,color=(1,0,0))
        last_p=now_p
        count+=1
        # cv2.imwrite('output/'+str(count)+'.jpg',IMG)
    plt.xticks([])
    plt.yticks([])
    plt.show()
def showPath3D(P,path,aa,bb):
    H=2048
    W=1536
    Origin_IMG=cv2.imread('tea_rec.jpg')
    IMG=np.zeros_like(Origin_IMG)
    IMG[::]=255
    # P[:,0]=P[:,0]/x*1000/
    # P[:,1]=P[:,1]/y*1000
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.get_proj = lambda: np.dot(Axes3D.get_proj(ax), np.diag([H/W, W/W, H/W, 1]))
    rand_z=np.random.random(len(path))*3+5
    # rand_z=np.zeros_like(path)
    print(rand_z)
    count=0
    last_p=0
    x=[]
    y=[]
    z=[]
    for now_p in path:
        last_point=np.asarray((P[last_p][0]*H,P[last_p][1]*W,rand_z[last_p]))
        x.append(last_point[0])
        y.append(last_point[1])
        z.append(last_point[2])
        now_point=np.asarray((P[now_p][0]*H,P[now_p][1]*W,rand_z[now_p]))
        ax.arrow3D(last_point[0],last_point[1],last_point[2],
           now_point[0]-last_point[0],now_point[1]-last_point[1],now_point[2]-last_point[2],
           mutation_scale=10,
           arrowstyle="-|>",
           linestyle='dashed')
        last_p=now_p
        count+=1
        # cv2.imwrite('output/'+str(count)+'.jpg',IMG)
    ax.set_zlim(0, 10)

    ax.scatter(x,y,z, c=z, cmap='Greens')
    plt.show()
    
def getPath(original_path):
    P=np.asarray(original_path)
    if P.shape[1]!=2:
        print('The shape of input should be (n,2)')
        return
    
    N=len(P)

    ## Construct the distance grap
    Graph=np.zeros((N,N))
    for i in range(N):
        for j in range(i,N):
            distance=np.linalg.norm(P[i]-P[j])
            Graph[i,j]=distance

    ## Use the MST to generate the approximate shortest path
    MST=minimum_spanning_tree(Graph)
    MST_Matrix=MST.toarray()

    ## Find the O set (with odd edges)
    odd_vertex=[]
    edge_count=np.zeros(N)
    for i in range(N):
        for j in range(N):
            if MST_Matrix[i,j]!=0:
                edge_count[i]+=1
                edge_count[j]+=1

    for i in range(N):
        if edge_count[i] % 2 !=0:
            odd_vertex.append(i)

    ## Find the M set (minimum cost perfect matching)
    odd_ix=np.ix_(odd_vertex,odd_vertex)
    nx_graph=nx.from_numpy_array(-1*Graph[odd_ix])
    matching=max_weight_matching(nx_graph,maxcardinality=True)

    ## Add M set to the T set
    for match in matching:
        x=odd_vertex[match[0]]
        y=odd_vertex[match[1]]
        MST_Matrix[x,y]=Graph[x,y]


    ## Find the eulerian tour
    nxgraph_eul=nx.from_numpy_array(MST_Matrix+MST_Matrix.T)
    nxgraph_eul=nx.eulerize(nxgraph_eul)
    print(nxgraph_eul)
    eul_tour=list(eulerian_circuit(nxgraph_eul,source=0))


    ## Shortcut eulerian tour
    path = list(itertools.chain.from_iterable(eul_tour))
    path = list(dict.fromkeys(path).keys())
    return path
def getGlobalPath(xlim,ylim,zlim):
    sample_points=10
    X_range=xlim
    Y_range=ylim
    Z_range=zlim
    X=np.random.rand(sample_points)*X_range
    Y=np.random.rand(sample_points)*Y_range
    Z=np.random.rand(sample_points)*Z_range
    Theta1=(np.random.rand(sample_points)-0.5)*np.pi
    Theta2=(np.random.rand(sample_points)-0.5)*np.pi
    P_true=np.vstack([X,Y,Z,Theta1,Theta2]).T
    P_true=np.insert(P_true,0,[0,0,0,0,0],axis=0)
    X1=X+np.random.rand(sample_points)*0.1
    Y1=Y+np.random.rand(sample_points)*0.1
    P=np.vstack([X1,Y1]).T
    P=np.insert(P,0,[0,0],axis=0)
    path=getPath(P)
    # print(path)
    
    
    ## 5 axis global via point
    sorted_XY=np.zeros((sample_points+1,5)) ## global point
    sorted_P_true=np.zeros((sample_points+1,5)) ## go down and pick point
    sorted_X1Y1=np.zeros((sample_points+1,5)) ## go up 
    
    for i in range(len(path)):
        sorted_XY[i][0:2]=P_true[path[i]][0:2]
        sorted_X1Y1[i][0:2]=P[path[i]]
        sorted_P_true[i]=P_true[path[i]]

    all_point=[]
    all_point.append(P_true[0])
    ## Between every two gobal point, add two local point (pickup and go up)
    for i in range(1,sample_points+1):
        all_point.append(sorted_X1Y1[i])
        all_point.append(sorted_P_true[i])
        all_point.append(sorted_XY[i])
    all_point=np.asarray(all_point)
    return all_point
def read_path(path):
    pp=np.load(path)
    res=[]
    for p in pp:
        res.append([p[0],p[1]])
    return res
if __name__ == '__main__':
    ## Generate random (tea) points in (W,H) 
    # np.random.seed(2021)
    P=read_path('path.npy')
    P.insert(0,[0,0])
    P=np.asarray(P)
    path=getPath(P)
    showPath2D(P,path,1,1)
    
    
