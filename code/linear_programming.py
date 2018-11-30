
class LinearProgramming:
    num_variables = 0   # Num of Variables in the PL
    num_constraints = 0   # Num of Constrains that the PL is Subject to
    A = []   # Matrix of Constraints
    c = []   # Vector of Coeficients of the Variables that will be Maximized
    b = []   # Vector of Limits of the Constrains
    signals = []  # Vector of Signals Used in the Constrains
    non_negativity = []  # Vector of Boolleans that Shows if a Variable is
    # Non-Negative

    def __init__(self, num_variables, num_constraints, A, b, c, signals,
                 non_negativity):
        self.num_variables = int(num_variables)
        self.num_constraints = int(num_constraints)
        for line in A:
            self.A.append(map(float, line))
        self.b = map(float, b)
        self.c = map(float, c)
        self.signals = signals
        self.non_negativity = map(int, non_negativity)

    def _retify_negativity(self):
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

    def _retify_signals(self):
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

    def _add_slacks(self):
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

    def turn_into_FPI(self):
        self._retify_negativity()
        self._retify_signals()
        self._add_slacks()

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
