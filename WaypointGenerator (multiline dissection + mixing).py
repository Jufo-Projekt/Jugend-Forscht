# Waypoint generator

def dissectline(M, N, s):#dissect a line into s points
    LP=[]
    for n in range(1, s):
        LP.append([(N[0]+n/s*(M[0]-N[0])), (N[1]+n/s*(M[1]-N[1]))])
    return LP

def Mixlines(Nlist):
    M=[]#middle
    s=4#sections
    Linelist=[]#list of linepoints
    Mx=0
    My=0
    for coordinate in Nlist:#calculate middle of Nlist points
        Mx+=coordinate[0]
        My+=coordinate[1]
    M=[Mx/len(Nlist), My/len(Nlist)]

    for N in Nlist:#dissect each line (middle to edgepoint) into s bits
        Linelist.append(dissectline(M, N, s))

    Mixlist=[]#merge the lists
    for sublistitem in range(0,len(Linelist[0])):
        for listitem in range(0, len(Linelist)):
            Mixlist.append(Linelist[listitem][sublistitem])
    Mixlist.append(M)

    return Mixlist#output merged lists
    
Points=[[48.19999, 11.41763], [48.19953, 11.41666], [48.19872, 11.41723], [48.19851, 11.41824], [48.19894, 11.41939], [48.19985, 11.41949], [48.20017,11.41824]]#list of example edgepoints
ls=Mixlines(Points)
#for point in range(0, len(ls)-1):
#        canv.create_line(ls[point][0], ls[point][1], ls[point+1][0], ls[point+1][1])
