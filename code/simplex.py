import sys


class Simplex:
    linear_prog = 0
    tableau = []

    def __init__(self, linear_prog):
        self.linear_prog = linear_prog

    def createTableau(self):
        i = 0
        line = []
        self.tableau.append(line)
        while(i < self.linear_prog.num_constraints):
            self.tableau[0].append(0)
            i += 1
        i = 0
        while(i < len(self.linear_prog.c)):
            self.tableau[0].append(self.linear_prog.c[i])
            i += 1
        self.tableau[0].append(0)

        i = 0
        while(i < self.linear_prog.num_constraints):
            self.tableau.append(line)
            for j in range(self.linear_prog.num_constraints):
                self.tableau[i].append(0)
            for var in self.linear_prog.A[i]:
                self.tableau[i].append(var)
            self.tableau[i].append(self.linear_prog.b[i])
            i += 1

    def solveLP(self):
        self.createTableau()
        self.printTableau()
        # if(self.verifyBase()):
        #     self.createBase()
        # self.startPivoting()

    def printTableau(self):
        for a in self.tableau:
            for b in a:
                sys.stdout.write(str(b)+" ")
            print()
        print()
