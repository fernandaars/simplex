# -*- coding: utf-8 -*-

# ...........: Trabalho Pratico 1 :...........
# ...: Disciplina de Pesquisa Operacional :...
# .Autora: Fernanda Aparecida Rodrigues Silva.
# ............................................
# ...:Departamento de Ciencia da Computacao:..
# ...:Universidade Federal de Minas Gerais:...
# ............................................


# External Imports
import sys

# Internal Imports
import simplex
import input_treatment

if __name__ == '__main__':
    file_handler = input_treatment.InputTreatment(sys.argv[1])
    lp = file_handler.read_file()
    lp.print_LP()
    lp.turn_into_FPI()
    lp.print_LP()
    s = simplex.Simplex(lp)
    s.solveLP()
