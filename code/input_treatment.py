import linear_programming


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

        return linear_programming.LinearProgramming(num_variables, num_constraints, A, b, c,
                                    signals, non_negativity)

    def write_file(self, filepath, lp):
        file_pointer = open(filepath, 'w')
        if lp. == "Inviavel":
            file.write("Status: inviavel\n")
            file.write("Certificado: \n")
            file.write("\n")
        elif solucao == "Ilimitada":
            file.write("Status: ilimitado\n")
            file.write("Certificado: \n")
            file.write("\n")
        elif solucao == "Resolvido":
            file.write("Status: otimo\n")
            file.write("Objetivo: " + format(obj, '.3f') + "\n")
            file.write("Solucao: \n")
            for item in x:
                file.write(str(format(item, '.3f'))+" ")
            file.write("\nCertificado: \n")
            file.write("\n")
        file.close()
