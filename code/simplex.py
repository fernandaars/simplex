import sys
import numpy
import fractions as frac
numpy.set_printoptions(formatter={'all': lambda x: str(frac.Fraction(x)
                                .limit_denominator())})


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
        i = self.lp.num_constraints
        while (i < self.tableau_width - 1):
            if(self.tableau[0][i] < 0):
                return False
        return True

    def _find_ypivot(self):
        new_obj = self.tableau[self.lp.num_constraints - 1: self.tableau_width - 1:1][0]
        neg_values = numpy.where(new_obj[:-1] < 0)
        # Bland's Rule
        return neg_values[0]

    def _pivot(self, ypivot):
        i = 1
        min_cost = float('Inf')
        xpivot = -1
        for constrain in xrange(self.lp.num_constraints):
            new_cost = self.tableau[i][ypivot] / self.tableau[i][0]
            [self.tableau_width]
            if(new_cost < min_cost):
                xpivot = i
                min_cost = new_cost
            i += 1
        pivot_value = self.tableau[xpivot][ypivot]
        self.tableau[xpivot] = self.tableau[xpivot] / pivot_value
        self.print_tableau()

        # i = 0
        # while(i < self.tableau_height):
        #     j = 0
        #     line_value = self.tableau[i][ypivot]
        #     while (j < self.tableau_width):
        #         coefficient = -1*line_value


    def solveLP(self):
        self._create_tableau()
        # self._retify_tableau()
        self.print_tableau()
        #if(self._verify_base()):
        #    print("BASE \n")
            # self.create_base()
        while(not self._tableau_is_finished()):
            print("EI")
            y = self._find_ypivot()
            self._pivot(y)
            break

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
