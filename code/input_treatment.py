import linear_programming as lp


class InputTreatment:
    filepath = ""

    def __init__(self, filepath):
        self.filepath = filepath

    def read_file(self):
        num_variables = 0
        num_constrafloats = 0
        A = []
        c = []
        b = []
        signals = []
        non_negativity = []
        try:
            file_pointer = open(self.filepath, 'r')
        except IOError:
            print("Error: File Doesn't Exists!")
            return num_variables, num_constrafloats, A, b, c, signals,
            non_negativity
        num_variables = int(file_pointer.readline())
        num_constraints = int(file_pointer.readline())
        non_negativity = file_pointer.readline().replace("\r\n", "").split(" ")
        c = file_pointer.readline().replace("\r\n", "").split(" ")

        i = 0
        line = file_pointer.readline()
        while(line):
            line = line.split(" ")
            b.append(float(line[len(line) - 1]))
            signals.append(line[len(line) - 2])
            A.append([line[k] for k in (range(len(line) - 2))])
            line = file_pointer.readline()
            i += 1

        return lp.LinearProgramming(num_variables, num_constraints, A, b, c,
                                    signals, non_negativity)
