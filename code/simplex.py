import sys
import numpy
import fractions as frac
numpy.set_printoptions(formatter={'all': lambda x:
                                  str(frac.Fraction(x).limit_denominator())})


class Simplex:
    lp = 0
    tableau = []
    auxiliary_tableau = []
    tableau_width = 0
    tableau_height = 0

    def __init__(self, lp):
        self.lp = lp

    # Create a Tableau
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

    # Verify if Tableau has a Basic Solution
    def __verify_tableau(self):
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

        count = 0
        if(self.__verify_unboundedness() is True):
            self.lp.status = "ilimitado"
            return True

        for variable in self.lp.base:
            if(variable == -1):
                count += 1
        if(count == 0):
            return False
        else:
            return True

    # Create a Auxiliary Tableau to Find a Basic Solution
    def __auxiliary_tableau(self, verbose_mode):
        new_width = self.tableau_width + self.tableau_height - 1
        self.auxiliary_tableau = numpy.zeros(shape=(self.tableau_height,
                                                    new_width))
        i = 1
        while (i < self.tableau_height):
            j = 0
            while (j < self.tableau_width - 1):
                self.auxiliary_tableau[i, j] = self.tableau[i, j]
                j += 1
            i += 1
        self.auxiliary_tableau[:, -1] = self.tableau[:, -1]

        i = 1
        while(i < self.tableau_height):
            j = 0
            self.auxiliary_tableau[i, i + self.tableau_width - 2] = +1
            self.auxiliary_tableau[0, i + self.tableau_width - 2] = +1
            i += 1

        original_width = self.tableau_width
        self.tableau = self.auxiliary_tableau
        self.tableau_width = new_width
        ypivot = self.__pivoting_is_finished("auxiliary")
        if(verbose_mode is True):
            self.print_tableau()
        while(ypivot != -1):
            self.__pivot(ypivot, verbose_mode)
            ypivot = self.__pivoting_is_finished("auxiliary")

        if(verbose_mode is True):
            self.print_tableau()
        artificial_vars = self.tableau[0, original_width - 1: new_width - 1]
        if(self.auxiliary_tableau[0, -1] > 0 or len(numpy
                                                    .where(artificial_vars !=
                                                           0)[0]) != 0):
            self.lp.status = "inviavel"
            return True
        else:
            self.auxiliary_tableau = self.tableau
            self.tableau_width = original_width
            self.tableau = numpy.zeros(shape=(self.tableau_height,
                                              self.tableau_width))
            i = 0
            while (i < self.tableau_height):
                j = 0
                while (j < self.tableau_width - 1):
                    self.tableau[i, j] = self.auxiliary_tableau[i, j]
                    j += 1
                i += 1
            self.tableau[:, -1] = self.auxiliary_tableau[:, -1]
            return False

    # Verify if the LP is Unbounded
    def __verify_unboundedness(self):
        i = self.lp.num_constraints
        while(i < self.tableau_width - 1):
            row = self.tableau[:, i]
            if(len(numpy.where(row <= 0)[0]) == self.tableau_height):
                self.lp.status = "ilimitado"
                return True
            i += 1
        return False

    # Verify if the Pivoting is Finished
    def __pivoting_is_finished(self, tableau_type):
        line = self.tableau[0, self.lp.num_constraints: self.tableau_width - 1]
        if(tableau_type == "normal"):
            if(len(numpy.where(line < 0)[0]) == 0):
                if(self.tableau[0, -1] < 0):
                    self.lp.status = "inviavel"
                return -1
            else:
                return numpy.where(line < 0)[0][0] + self.lp.num_constraints
        else:
            if(len(numpy.where(line == 1)[0]) == 0):
                return -1
            else:
                return numpy.where(line == 1)[0][-1] + self.lp.num_constraints

    # Do the Pivoting Process with a Given Pivot
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

    # Get the Final Results and Status of Tableau
    def __get_results(self, verbose_mode):
        if(self.lp.status == "ilimitado"):
            i = 0
            self.lp.certificate = [0 for k in xrange(self.lp.num_variables)]
            while(i < (len(self.lp.base))):
                self.lp.certificate[self.lp.base[i]] = self.tableau[i + 1, - 1]
                i += 1
        else:
            if(self.lp.status == "inviavel"):
                self.lp.certificate = self.auxiliary_tableau[0, :self
                                                             .lp
                                                             .num_constraints]
            else:
                if(self.tableau[0, -1] >= 0):
                    self.lp.status = "otimo"
                    self.lp.x = [0 for i in xrange(self.lp.num_variables)]
                    self.lp.objective_value = self.tableau[0][self
                                                              .tableau_width -
                                                              1]
                    self.lp.certificate = self.tableau[0][0:self.lp
                                                          .num_constraints]
                    i = 0
                    while(i < (len(self.lp.base))):
                        aux = self.tableau[i + 1, self.tableau_width - 1]
                        self.lp.x[self.lp.base[i]] = aux
                        i += 1

        if(verbose_mode is not False):
            self.lp.print_LP()

    # Start the Main Process of Simplex
    def solve_LP(self, verbose_mode):
        # True -> Tableau Solution is Defined
        # False -> Tableau Solution is Unknown

        # Create tableau,
        self.__create_tableau()
        # verify if tableau has a basic solution.
        tableau_state = self.__verify_tableau()
        # If tableau hasn't a basic solution and isn't unbounded,
        if(tableau_state is True and self.lp.status != "ilimitado"):
            # create a auxiliary tableau.
            tableau_state = self.__auxiliary_tableau(verbose_mode)
        # While tableau hasn't a defined solution,
        while(tableau_state is False):
            # find a pivot,
            ypivot = self.__pivoting_is_finished("normal")
            # test if pivoting process is not finished
            while(ypivot != -1):
                # do the process of pivoting
                self.__pivot(ypivot, verbose_mode)
                ypivot = self.__pivoting_is_finished("normal")
                # verify again the unboundeness of the tableau
                tableau_state = self.__verify_unboundedness()
                # if tableau is unbounded, stop
                if(tableau_state is True):
                    break
            tableau_state = True
        # analyse final results
        self.__get_results(verbose_mode)

    # Print Tableau
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
