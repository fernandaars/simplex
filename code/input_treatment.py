import linear_programming as lp


class InputTreatment:
    filepath = ""

    def __init__(self, filepath):
        self.filepath = filepath

    def read_file(self):
        num_variables = 0
        num_constraints = 0
        A = []
        c = []
        b = []
        signals = []
        non_negativity = []
        try:
            filePointer = open(self.filepath, 'r')
        except IOError:
            print("Error: File Doesn't Exists!")
            return num_variables, num_constraints, A, b, c, signals,
            non_negativity
        num_variables = int(filePointer.readline())
        num_constraints = int(filePointer.readline())
        non_negativity = filePointer.readline().replace("\r\n", "").split(" ")
        c = filePointer.readline().replace("\r\n", "").split(" ")
        print(c)

        i = 0
        line = filePointer.readline()
        while(line):
            print(line)
            line = line.split(" ")
            b.append(int(line[len(line) - 1]))
            signals.append(line[len(line) - 2])
            A.append([line[k] for k in (range(len(line) - 2))])
            line = filePointer.readline()
            i += 1

        return lp.LinearProgramming(num_variables, num_constraints, A, b, c,
                                    signals, non_negativity)
