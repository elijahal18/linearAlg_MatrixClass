import matfunctions as matfunc
print('===================================================================================================')
print('                                  MATRIX CALCULATOR')
print('Now that the test is done you can work with your own matrix')#after tests are done 

cont=True#start trying to get an input
while cont:
    print('\n')
    print('Remember to always make sure what is being inputed is correct. Email eal510@nyu.edu with errors')
    print('\n')
    print('What would you like to do with the Matrix: \n(1) Add\n(2) Subtract\n(3) gaussian(for A and B)\n(4) Dot Product\n(5) Transpose\n(6) get inv\n(7) get LU\n(8) solve system')
    print('===================================================================================================')
    choice=input()
    choice=int(choice)
    if choice < 1 or choice > 8:#inputs should be in this range
        print("You must input an integer among the options given.\n")
        continue
    if 8>choice > 4:#these inputs need one mat the other ones need two
        numMats=1
    else:
        numMats=2
        
    matrices=[]
    for mat in range(numMats):#go through ammount of mats needed
        if (choice==8 or choice==3) and mat==0:
            print('A matrix')
        elif (choice==8 or choice==3) and mat==1:
            print('B matrix')
        print('Input the number of rows and collumns in matrix ',str(mat+1),' seperated by a comma (example input for 3 rows 2 columns=3,2).')
        inp=input()
        try:
            dim=list(inp.split(','))
            rows=int(dim[0])
            columns=int(dim[1])
        except:#exceptions for user mistakes
            print('somethings wrong')
            continue
        if rows < 1:
            print('min row is 1.\n')
            continue
        if columns < 1:
            print('min column is 1.\n')
            continue
        matrix=[]
        for rowNum in range(rows):#goes through each row making a list
            print('Input row '+str(rowNum+1),' of matrix ',str(mat+1),', spaced by commas.(need ',columns,' entries)')
            row=input()
            row=list(row.split(','))
            if len(row) != columns:
                print('dont have enough numbers for column.\n')
                continue
            for item in range(len(row)):
                row[item]=int(row[item])
            matrix.append(row)
            print('\n')
        matrices.append(matrix)#appends this list to the list representing the matrix

    try:
        mat1=matfunc.lstmat(matrices[0])#uses this/these lists to try to make matrix
        if numMats==2:
            mat2=matfunc.lstmat(matrices[1])
            mats=[mat1,mat2]
        else:
            mats=[mat1]
    except:
        print('you inputed something wrong')#if input error break program
        break
    result=[]
    if choice == 1:#calling on the functions needed
        print("computing\n",mats[0],'+\n', mats[1],'...')
        result.append(mats[0]+mats[1])
    elif choice == 2:
        print("computing\n",mats[0],'-\n', mats[1],'...')
        result.append(mats[0]-mats[1])
    elif choice == 3:
        print("computing\n",mats[0],'+\n', mats[1],'...')
        Amat,Bmat=matfunc.gaussian(mats[0],mats[1])
        result.append(Amat)
        result.append(Bmat)
        print('returning A and then B with gaussian elim applied')
    elif choice == 4:
        print("computing\n",mats[0],'*\n', mats[1],'...')
        result.append(mats[0]*mats[1])
    elif choice == 5:
        print("computing transpose of\n",mats[0],'...')
        result.append(mats[0].getTranspose())
    elif choice == 6:
        print("computing inverse of\n",mats[0],'...')
        result.append(matfunc.inverse(mats[0]))
    elif choice == 7:
        print("computing lu decomposition of\n",mats[0],'...')
        L,U=matfunc.lu_decomposition(mats[0])
        result.append(L)
        result.append(U)
    elif choice==8:
        print("Computing X for equation\n AX=B\n",'A=',mats[0],'B=',mats[1], 'And X= vector of variables with the same size as B')
        print(mats[0],mats[1])
        print('...')
        x=matfunc.solveX(mats[0],mats[1])
        result.append(x)
    print('\n')
    print('===================================================================================================')
    print('\n')
    print('equals:\n')
    for i in range(len(result)):
        print(result[i])
    

    print('\n')
    if numMats==1:
        print('**Hidden info**would you additionally like to get the determinant[Yes/No]')
        inp=input()
        if inp=='Yes' and matfunc.if_Square(mats[0]):
            print(matfunc.determinant(mats[0]))
    print('\n would you like to continue [Y/N]')
    repeat=input()
    if repeat == 'Y':
        print('\n')
        continue
    elif repeat=='N':
        print('Thank you for participating!')
        cont=False

