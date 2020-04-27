import sys
class Matrix:
    def __init__(self):
        print("")

    def multiplication(self, X, Y):
        result = [[sum(a*b for a,b in zip(X_row,Y_col)) for Y_col in zip(*Y)] for X_row in X]

        for r in result:
            print(r)

    def transpose(self, n):
        for row in m :
            print(row)
        rez = [[m[j][i] for j in range(len(m))] for i in range(len(m[0]))]
        print("\n")
        for row in rez:
            print(row)

    def transposeMatrix(self,m):
        return map(list,zip(*m))

    def getMatrixMinor(self, m,i,j):
        return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

    def getMatrixDeternminant(self, m):
        #base case for 2x2 matrix
        if len(m) == 2:
            return m[0][0]*m[1][1]-m[0][1]*m[1][0]

        determinant = 0
        for c in range(len(m)):
            determinant += ((-1)**c)*m[0][c]*self.getMatrixDeternminant(self.getMatrixMinor(m,0,c))
        return determinant

    def inverse(self, m):
        determinant = self.getMatrixDeternminant(m)

        #special case for 2x2 matrix:
        if len(m) == 2:
            cofactors = [[m[1][1]/determinant, -1*m[0][1]/determinant],
                         [-1*m[1][0]/determinant, m[0][0]/determinant]]

            for row in cofactors:
                print(row)
            sys.exit()

        #find matrix of cofactors
        cofactors = []
        for r in range(len(m)):
            cofactorRow = []
            for c in range(len(m)):
                minor = self.getMatrixMinor(m,r,c)
                cofactorRow.append(((-1)**(r+c)) * self.getMatrixDeternminant(minor))
            cofactors.append(cofactorRow)
        cofactors = self.transposeMatrix(cofactors)
        for r in range(len(cofactors)):
            for c in range(len(cofactors)):
                cofactors[r][c] = cofactors[r][c]/determinant

        print(cofactors)
        for row in cofactors:
            print(row)

if __name__ == '__main__':
    mtrx = Matrix()

    actionType = input("choose your action type:");
    if actionType == "1":      # multiplication
        # b = input("first matrix:")
        # c = input("second matrix:")

        X = [[12,7,3],
            [4 ,5,6],
            [7 ,8,9]]

        # 3x4 matrix
        Y = [[5,8,1,2],
            [6,7,3,0],
            [4,5,9,1]]

        mtrx.multiplication(X,Y)
    elif actionType == "2":
        m = [[1,0],[1,1],[1,4],[1,2],[1,5],[1,6]]

        mtrx.transpose(m)
    else:
        m = [[1,1],[2,6]]
        mtrx.inverse(m)