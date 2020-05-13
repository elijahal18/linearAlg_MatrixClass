import random

class MatrixError(Exception):
    pass

class Matrix(object):
    def __init__(self, p, q):#constructer
        self.rows=[[0]*q for x in range(p)]
        self.p=p
        self.q=q

    #getter and setter
    def __getitem__(self, i):
        return self.rows[i]
    
    def __setitem__(self, i, val):
        self.rows[i]=val

    #string representation
    def __str__(self):
        s="\n".join([str(i) for i in [rows for rows in self.rows] ])
        return s+'\n'

    #returns transpose matrix
    def getTranspose(self):
        p, q=self.q, self.p
        res=Matrix(p, q)
        res.rows=[list(item) for item in zip(*self.rows)]
        return res

    #returns shape of matrix
    def shape(self):
        return (self.p, self.q)

    #checks equality
    def __eq__(self, mat):
        return (mat.rows == self.rows)

    #returns matrix added together 
    def __add__(self, mat):  
        if self.shape() != mat.shape():#checks if same size
            raise MatrixError("different sizes!")
        res=Matrix(self.p, self.q)       
        for x in range(self.p):#add each item
            row=[sum(item) for item in zip(self.rows[x], mat[x])]
            res[x]=row
        return res

    #returns matrix subtracted 
    def __sub__(self, mat):   
        if self.shape()!=mat.shape():#checks if same size
            raise MatrixError("Trying to sub matrixes of varying rank!")
        res=Matrix(self.p, self.q)
        for x in range(self.p):#subtract each item
            row=[item[0]-item[1] for item in zip(self.rows[x], mat[x])]
            res[x]=row
        return res

    def __mul__(self, mat):#dot product
        othp, othq=mat.shape()
        if (self.q != othp):#checks if columns =to row of other matrix
            raise MatrixError("Trying to mul matrixes of varying rank!")
        #tranpose in order to multiply
        mat_t=mat.getTranspose()
        res=Matrix(self.p, othq)   
        for x in range(self.p):
            for y in range(mat_t.p):
                res[x][y]=sum([item[0]*item[1] for item in zip(self.rows[x], mat_t[y])])#add all items multiplied respectivly
        return res
    
def lstmat(rows):#matrix maker from lists
    p=len(rows)
    q=len(rows[0])
    Mat=Matrix(p,q)
    Mat.rows=rows
    return Mat
    
def makeId(mkMat, p):#makes Identity matrix
    rows=[[0]*p for x in range(p)]
    i=0     
    for row in rows:
        row[i]=1
        i+=1
    return lstmat(rows)

def Matcopy(A):#makes a copy of a matrix
    listA=[]
    for i in range(A.shape()[0]):#goes through and copies each row and appends each row
        listA.append(A[i].copy())
    newA=lstmat(listA)
    return newA#returns copy

def if_Square(A):#checks if its a square matrix
    if A.shape()[1] != A.shape()[0]:
        return False
    return True

def lu_decomposition(A):#returns L and U
    if if_Square(A)==False:
        return 
    q=A.shape()[1]                                                                                                                                                                                                              
    L=lstmat([[0.0]*q for i in range(q)])
    U=lstmat([[0.0]*q for i in range(q)])
    Anew=Matcopy(A)                                                                                                                                                                                                                  
    for j in range(q):                                                                                                                                                                                                  
        L[j][j]=1.0  #set pivot to 1                                                                                                                                                                                    
        for i in range(j+1):
            s1=sum(U[k][j] * L[i][k] for k in range(i))
            U[i][j]=Anew[i][j]-s1#delete items below in respective column
        if U[j][j]==0:
            print('not possible. Error')
            return False                                                                                                                                                                
        for i in range(j, q):
            s2=sum(U[k][j] * L[i][k] for k in range(j))
            L[i][j]=(Anew[i][j]-s2) / U[j][j]#compute lower triangular column from U and A
    return (L, U)    

def determinant(A):
    q=A.shape()[1]
    L,U=lu_decomposition(A)
    det=1
    for i in range(q):
        det*=U[i][i]#finds determinant by multiplying diagonals
    return det

def isNonSingular(A):#checks if Matrix is nonSingular or not using determinant
    det=determinant(A)
    if det != 0:
        return det
    return False  
    
def inverse(A):
    t=if_Square(A)
    if t==False:
        return False
    s=isNonSingular(A)
    if s!=False and t!=False:#checkers for nonSquar/singularity
        q=A.shape()[1]
        AM=Matcopy(A)
        IM=makeId(Matrix, q)
        indices=list(range(q))   
        for dia in range(q): 
            diaScaler=1.0 / AM[dia][dia]#finds scalar for diagonal
            for row in range(q): 
                AM[dia][row]*=diaScaler#multiplies row of diagonal according to salor
                IM[dia][row]*=diaScaler
            for i in indices[0:dia]+indices[dia+1:]:#for other rows set items in column above and below to 0
                rowScaler=AM[i][dia]# find the scalor for each one below and above
                for colum in range(q): #apply to whole row
                    AM[i][colum]=AM[i][colum]-rowScaler * AM[dia][colum]
                    IM[i][colum]=IM[i][colum]-rowScaler * IM[dia][colum]
        return IM#IM becomes inv
    else:
        return False
    
def gaussian(A,B=None):#either finds gaussian of A or A including B and returns either A or A and B
    q=A.shape()[1]
    p=A.shape()[0]
    indices=list(range(p))
    AM=Matcopy(A)
    if B is not None:#all of these statments are for when B=None
        BM=Matcopy(B)
    for dia in range(min(q,p)):#steps are the same as Inv except only for rows below and also need to keep track of B
        if(AM[dia][dia]==0):
            print('error')
            return None,None
        fdScaler=1.0 / AM[dia][dia]
        for colum in range(q): 
            AM[dia][colum] *= fdScaler
        if B is not None:
            BM[dia][0]*=fdScaler
        for i in indices[dia+1:]:
            crScaler=AM[i][dia]
            for colum in range(q): 
                AM[i][colum]=AM[i][colum]-crScaler * AM[dia][colum]
            if B is not None:
                BM[i][0]=BM[i][0]-crScaler * BM[dia][0]
    if B is not None:
        return AM,BM
    return AM

#takes the matrix A and B then solves for X
def solveX(A,B):
    newB=Matcopy(B)#dont want to try to affect B directly
    inv=inverse(A)
    if inv is not False:#try to do it through inv
        x=inv*B
        return x
    elif if_Square(A) and isNonSingular(A):#try to do it through LU
        q=A.shape()[1]   
        L,U=lu_decomposition(A)#take LU
        c=[0.0 * q for i in range(q)]
        for row in range(q):#solve for intermediary c
            count=0
            while c[count]!=0:
                newB[row][0]-=L[row][count]*c[count]
                count+=1
            if count!=q-1:
                if L[row][count+1]!=0:
                    print('infinite solutions') 
            if L[row][count]==0:
                print('no solutions')
            c[row]=newB[row][0]/L[row][count]
        #UX now =c
        x=[0.0*q for i in range(n)]
        for row in range(n-1,-1,-1):#solve for x by going from the bottom up
            count=q-1
            while x[count]!=0.0:
                c[row]-=U[row][count]*x[count]
                count-=1
            if U[row][count-1]!=0 and count!=0:
                print('infinite solutions') 
            if U[row][count]==0:
                print('no solutions')
            x[row]=c[row]/U[row][count]
        return x
    else:#gaussian elim (for unusual mats)
        AM,BM=gaussian(A,newB)#finds gaussian
        x=[]
        p=A.shape()[0]
        q=A.shape()[1]
        for i in range(p-1,-1,-1):#solves for gaussian from the bottom up
            row=[]
            for j in range(q-1,-1,-1):
                if AM[i][j]!=0:
                    row.append(AM[i][j])
            if len(row)!=len(x)+1:#some checkers for no solution/infinite solution (will return False)
                if BM[i]==0:
                    print('inf solution')
                else:
                    print('no solution')
                return False
            elif len(row)==0:
                print(1)
                if BM[i]==0:
                    print('inf solution')
                else:
                    print('no solution')
                return False
            else:
                tot=BM[i][0]
                count=0
                while(count!=len(row)-1):
                    tot-=row[count]*x[count]
                    count+=1
                x.append(tot/row[count])
        x=x[::-1]
        return x
        #in all cases returns x
        
#tests
print('***TEST***')
print('making matrix from list [[1,2,3][3,2,1][2,3,1]] and testing repr and basic values')
A=lstmat([[1,2,3],[3,2,1],[2,3,1]])
print('A:\n',A,'\nshape',A.shape(),'/is square?',if_Square(A),'/determinante',determinant(A),'/transpose:\n',A.getTranspose())

print('testing addition/dot/subtraction')
B=lstmat([[1,1,1],[1,1,1],[1,1,1]])
print('B=',B)
add=A+B
sub=A-B
mul=A*B
print('A+B\n',add,'A-B\n',sub,'AdotB\n',mul)

print('testing more complex tools (LU/Inverse/Gaussian)')
L,U=lu_decomposition(A)
Inv=inverse(A)
gas=gaussian(A)
print('LU of A',L,U,'\nInv of A',Inv,'\ngaussian',gas)

print('solving system for new B')
B=lstmat([[2],[0],[1]])

print('B=',B)
Agas,Bgas=gaussian(A,B)
print('using gausian A=:\n',Agas,'B=\n',Bgas)


x=solveX(A,B)
print('AX=B\nX=\n',x)

newA=lstmat([[3,3],[2,3],[4,2]])

newB=lstmat([[1],[2],[3]])

print('trying to solve a bad matrix. B=\n',newB,'\nA=',newA)
x=solveX(newA,newB)
print(x)
print('***Test Done***')
