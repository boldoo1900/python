import operator
import sys

class Vector:
    def __init__(self):
        self.index = 20
        self.padan = [ {'w':0, 'x0':1, 'x1':1, 'x2':1},
                       {'w':0, 'x0':1, 'x1':2, 'x2':1},
                       {'w':1, 'x0':1, 'x1':1, 'x2':3},
                       {'w':1, 'x0':1, 'x1':2, 'x2':4},
                       {'w':2, 'x0':1, 'x1':4, 'x2':3},
                       {'w':2, 'x0':1, 'x1':4, 'x2':2} ]
        self.omomi = []

if __name__ == '__main__':
    vect = Vector()

    # #1
    # vect.omomi.append( [[6, 2*vect.padan[0]['x1'], vect.padan[0]['x2']],
    #                    [2, vect.padan[0]['x1'], 5*vect.padan[0]['x2']],
    #                    [1, 6*vect.padan[0]['x1'], vect.padan[0]['x2']]] )

    # #2
    # vect.omomi.append( [[3, 3*vect.padan[0]['x1'], 2*vect.padan[0]['x2']],
    #                    [2, -1*vect.padan[0]['x1'], 3*vect.padan[0]['x2']],
    #                    [2, 5*vect.padan[0]['x1'], 2*vect.padan[0]['x2']]])

    #3
    vect.omomi.append( [[6, 3*vect.padan[0]['x1'], 0],
                       [2, -3*vect.padan[0]['x1'], 6*vect.padan[0]['x2']],
                       [0, 8*vect.padan[0]['x1'], 1*vect.padan[0]['x2']]] )

    i = 0
    maxVal = 0
    correction = ''

    #sys.exit()
    while i < vect.index:
        print(vect.omomi[i], end="")

        padan_index = i%6
        temp = [sum(map(operator.mul, vect.omomi[i][0], [vect.padan[padan_index]["x0"], vect.padan[padan_index]["x1"], vect.padan[padan_index]["x2"]])),
                sum(map(operator.mul, vect.omomi[i][1], [vect.padan[padan_index]["x0"], vect.padan[padan_index]["x1"], vect.padan[padan_index]["x2"]])),
                sum(map(operator.mul, vect.omomi[i][2], [vect.padan[padan_index]["x0"], vect.padan[padan_index]["x1"], vect.padan[padan_index]["x2"]]))]

        maxIndexes = [i for i, x in enumerate(temp) if x == max(temp)]
        maxIndex = 0

        rightIndex = vect.padan[padan_index]['w']
        cloneRow = []

        if rightIndex in maxIndexes and len(maxIndexes) == 1:
            correction = 'o'
            vect.omomi.append(vect.omomi[i])
        else:
            if rightIndex in maxIndexes:
                maxIndexes.remove(rightIndex)
                maxIndex = maxIndexes[0]
                correction = '^'
            else:
                correction = 'x'

            #clone current omomi
            cloneRow = vect.omomi[i].copy();

            #get padan row
            padanRow = [vect.padan[padan_index]['x0'], vect.padan[padan_index]['x1'], vect.padan[padan_index]['x2']];

            # reduce row value
            cloneRow[maxIndex] = list(map(operator.sub, cloneRow[maxIndex], padanRow))

            # increase row value
            cloneRow[rightIndex] = list(map(operator.add, cloneRow[rightIndex], padanRow))

            # print(cloneRow)
            vect.omomi.append(cloneRow)

        print("      (", i+1, ",", correction, ") g(x) = ", temp)
        i+=1







