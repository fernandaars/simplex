import sys
import numpy
import fractions as frac
numpy.set_printoptions(formatter={'all': lambda x:
                                  str(frac.Fraction(x).limit_denominator())})


class Simplex:
    lp = 0
    tableau = []
    tableau_width = 0
    tableau_height = 0

    def __init__(self, lp):
        self.lp = lp

    def _create_tableau(self):
        self.tableau_width = self.lp.num_constraints + self.lp.num_variables
        self.tableau_width += 1
        self.tableau_height = self.lp.num_constraints + 1
        self.tableau = numpy.zeros(shape=(self.tableau_height,
                                   self.tableau_width))

        i = 0
        for i in xrange(self.lp.num_constraints):
            self.tableau[i + 1][i] = frac.Fraction(1)

        i = self.lp.num_constraints
        for variable in self.lp.c:
            self.tableau[0, i] = frac.Fraction(-1 * variable)
            i += 1
        self.tableau[0, i] = 0

        i = 1
        for constrains in self.lp.A:
            j = self.lp.num_constraints
            for variable in constrains:
                self.tableau[i, j] = frac.Fraction(variable)
                j += 1
            self.tableau[i, j] = frac.Fraction(self.lp.b[i - 1])
            i += 1

    def _verify_base(self):
        for i in xrange(self.lp.num_constraints):
            if(self.tableau[i + 1][i + self.lp.num_constraints] != 1):
                return False
        return True

    def _tableau_is_finished(self):
        line = self.tableau[0, self.lp.num_constraints: self.tableau_width - 1]
        i = 0
        while(i < len(line)):
            if(line[i] < 0):
                return i + self.lp.num_constraints
            i += 1
        return -1

    def _pivot(self, ypivot):
        i = 1
        line = self.tableau[1:,
                            self.tableau_width - 1] / self.tableau[1:, ypivot]
        self.print_tableau()
        while(True):
            if(line.min() < 0):
                line[line.argmin()] = float('Inf')
            else:
                break
        xpivot = line.argmin() + 1
        pivot_value = self.tableau[xpivot][ypivot]

        self.lp.base[xpivot - 1] = ypivot - self.lp.num_constraints
        print("PIVOT: [" + str(ypivot) + "][" + str(xpivot) + "]")

        self.tableau[xpivot] = self.tableau[xpivot] / pivot_value

        i = 0
        while(i < self.tableau_height):
            if(i != xpivot):
                line_value = self.tableau[i][ypivot]
                self.tableau[i] += self.tableau[xpivot] * -1 * line_value
            i += 1
        self.print_tableau()

    def _write_results(self):
        self.lp.x = [0 for i in xrange(self.lp.num_variables)]
        self.lp.objective_value = self.tableau[0][self.tableau_width - 1]
        self.lp.certificate = self.tableau[0][0:self.lp.num_constraints - 1]

        if(self.lp.state == "otimo"):
            i = 0
            while(i < (len(self.lp.base))):
                self.lp.x[self.lp.base[i]] = self.tableau[i + 1, self.tableau_width - 1]
                i += 1

    def solveLP(self):
        self._create_tableau()
        ypivot = self._tableau_is_finished()
        while(ypivot != -1):
            self._pivot(ypivot)
            ypivot = self._tableau_is_finished()
        self.lp.state = "otimo"
        self._write_results()

    def print_tableau(self):
        i = 0
        num_chars = len(str(self.tableau.max()))
        if (num_chars < len(str(self.tableau.min()))):
            num_chars = len(str(self.tableau.min()))
        num_chars += 1
        print("")
        while(i < self.tableau_height):
            if(i == 1):
                for k in xrange(self.tableau_width * num_chars + 1):
                    sys.stdout.write("-")
                print("")
            j = 0
            while(j < self.tableau_width):
                sys.stdout.write(str('{:^' + str(num_chars) + '}').format(
                    str(self.tableau[i, j])))
                if(j == self.lp.num_constraints - 1):
                    sys.stdout.write("|")
                if(j == self.tableau_width - 2):
                    sys.stdout.write("|")
                j += 1
            sys.stdout.write("\n")
            i += 1
        print("")
