import linear_programming


class InputTreatment:
    def read_file(self, filepath, verbose_mode):
        A = []
        c = []
        b = []
        signals = []
        non_negativity = []
        try:
            file_pointer = open(filepath, 'r')
        except IOError:
            print("Error: File Doesn't Exists!")
            return -1
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
        file_pointer.close()

        return linear_programming.LinearProgramming(num_variables,
                                                    num_constraints, A, b, c,
                                                    signals, non_negativity,
                                                    verbose_mode)

    def write_file(self, filepath, lp):
        file_pointer = open(filepath, 'w')
        file_pointer.write("Status: " + str(lp.status))
        if(lp.status == "otimo"):
            file_pointer.write("\nObjetivo: " + str(lp.objective_value))
            file_pointer.write("\nSolucao:\n")
            for var in lp.x:
                file_pointer.write(str(var) + " ")
        file_pointer.write("\nCertificado:\n")
        for var in lp.certificate:
            file_pointer.write(str(float(var)) + " ")
        file_pointer.close()
