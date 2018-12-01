import sys


class LinearProgramming:
    num_variables = 0   # Num of Variables in the PL
    num_constraints = 0   # Num of Constrains that the PL is Subject to
    A = []   # Matrix of Constraints
    c = []   # Vector of Coeficients of the Variables that will be Maximized
    b = []   # Vector of Limits of the Constrains
    signals = []  # Vector of Signals Used in the Constrains
    non_negativity = []  # Vector of Boolleans that Shows if a Variable is
    # Non-Negative

    objective_value = 0  # LP Final Objective Value
    x = []  # Soluction Vector
    base = []
    certificate = []  # Certificate of LP State
    status = ""

    def __init__(self, num_variables, num_constraints, A, b, c, signals,
                 non_negativity, verbose_mode):
        self.num_variables = int(num_variables)
        self.num_constraints = int(num_constraints)
        for line in A:
            self.A.append(map(float, line))
        self.b = map(float, b)
        self.c = map(float, c)
        self.signals = signals
        self.non_negativity = map(int, non_negativity)
        self.base = [-1 for i in xrange(self.num_constraints)]
        if(verbose_mode is not False):
            self.print_LP()

    def __retify_negativity(self):
        i = 0
        for variable in self.non_negativity:
            if(variable == 0):
                j = 0
                for line in self.A:
                    self.A[j].append(-1 * line[i])
                    j += 1
                self.num_variables += 1
                self.c.append(-1 * self.c[i])
                self.non_negativity[i] = 1
            i += 1

    def __retify_signals(self):
        i = 0
        for limit in self.b:
            if(limit < 0):
                self.b[i] = self.b[i] * (-1)
                j = 0
                for var in self.A[i]:
                    self.A[i][j] = var * (-1)
                    j += 1
                if(self.signals[i] == ">="):
                    self.signals[i] = "<="
                if(self.signals[i] == "<="):
                    self.signals[i] = ">="
            i += 1

    def __add_slacks(self):
        i = 0
        for signal in self.signals:
            if(signal == ">=" or signal == "<="):
                j = 0
                for line in self.A:
                    self.A[j].append(0)
                    j += 1
                self.A[i][self.num_variables] = 1
                if(signal == ">="):
                    self.A[i][self.num_variables] = -1
                self.num_variables += 1
                self.c.append(0)
                self.signals[i] = "=="
            i += 1

    def turn_into_FPI(self, verbose_mode):
        self.__retify_negativity()
        self.__retify_signals()
        self.__add_slacks()
        if(verbose_mode is not False):
            self.print_LP()

    def print_LP(self):
        print("Num of Variables: " + str(self.num_variables))
        print("Num of Constrains: " + str(self.num_constraints))
        print("Objetive Function: " + str(self.c))
        i = 0
        print("Constrains: ")
        while (i < len(self.b)):
            print(str(self.A[i]) + str(self.signals[i]) +
                  str(self.b[i]))
            i += 1
        print("Non-Negative Variables: " + str(self.non_negativity))
        print("Status: " + str(self.status))
        if(self.status == "otimo"):
            print("Objetivo: " + str(self.objective_value))
            print("Solucao:")
            for var in self.x:
                sys.stdout.write(str(var) + " ")
        print("\nCertificado:")
        for var in self.certificate:
            sys.stdout.write(str(float(var)) + " ")
        print("")
