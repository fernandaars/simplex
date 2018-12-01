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

    def __create_tableau(self):
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

    def __verify_tableau(self):
        if(self.__verify_unboundedness() is True):
            self.lp.status = "ilimitado"
            return 3
        i = 1
        while(i < self.tableau_height):
            ones = numpy.where(self.tableau[i, self.lp.num_constraints:
                                            self.tableau_width - 1] == 1)
            if(len(ones) != 0):
                for one in ones[0]:
                    non_zeros = numpy.where(self.tableau[:, one +
                                            self.lp.num_constraints] != 0)
                    if(len(non_zeros[0]) == 1):
                        self.lp.base[i - 1] = one
                        break
            i += 1

        if(numpy.count_nonzero(self.lp.base == -1) == 0):
            return 0

    def __verify_unboundedness(self):
        i = self.lp.num_constraints
        while(i < self.tableau_width - 1):
            row = self.tableau[:, i]
            if(len(numpy.where(row <= 0)[0]) == self.tableau_height):
                self.lp.status = "ilimitado"
                return True
            i += 1
        return False

    def __pivoting_is_finished(self):
        line = self.tableau[0, self.lp.num_constraints: self.tableau_width - 1]
        if(len(numpy.where(line < 0)[0]) == 0):
            return -1
        else:
            return numpy.where(line < 0)[0][0] + self.lp.num_constraints

    def __pivot(self, ypivot, verbose_mode):
        i = 1
        line = self.tableau[1:,
                            self.tableau_width - 1] / self.tableau[1:, ypivot]
        if(verbose_mode is not False):
            self.print_tableau()
        while(True):
            if(line.min() < 0):
                line[line.argmin()] = float('Inf')
            else:
                break
        xpivot = line.argmin() + 1
        pivot_value = self.tableau[xpivot][ypivot]

        self.lp.base[xpivot - 1] = ypivot - self.lp.num_constraints
        self.tableau[xpivot] = self.tableau[xpivot] / pivot_value

        i = 0
        while(i < self.tableau_height):
            if(i != xpivot):
                line_value = self.tableau[i][ypivot]
                self.tableau[i] += self.tableau[xpivot] * -1 * line_value
            i += 1
        if(verbose_mode is not False):
            self.print_tableau()
            print("PIVOT: [" + str(ypivot) + "][" + str(xpivot) + "]")

    def __get_results(self, verbose_mode):
        if(self.lp.status == "ilimitado"):
            print("")
        else:
            if(self.tableau[0, -1] >= 0):
                self.lp.status = "otimo"
                self.lp.x = [0 for i in xrange(self.lp.num_variables)]
                self.lp.objective_value = self.tableau[0][self.tableau_width -
                                                          1]
                self.lp.certificate = self.tableau[0][0:self.lp
                                                      .num_constraints]
                i = 0
                while(i < (len(self.lp.base))):
                    self.lp.x[self.lp.base[i]] = self.tableau[i + 1, self
                                                              .tableau_width -
                                                              1]
                    i += 1

        if(verbose_mode is not False):
            self.lp.print_LP()

    def solve_LP(self, verbose_mode):
        self.__create_tableau()
        tableau_state = self.__verify_tableau()
        while(tableau_state is not True):
            ypivot = self.__pivoting_is_finished()
            while(ypivot != -1):
                self.__pivot(ypivot, verbose_mode)
                ypivot = self.__pivoting_is_finished()
                tableau_state = self.__verify_unboundedness()
                if(tableau_state is True):
                    break
            tableau_state = True
        self.__get_results(verbose_mode)

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