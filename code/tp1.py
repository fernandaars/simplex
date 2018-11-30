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
import simplex as simplex
import input_treatment as file

if __name__ == '__main__':
    file_handler = file.InputTreatment(sys.argv[1])
    linear_prog = file_handler.read_file()
    linear_prog.print_LP()
    linear_prog.turn_into_FPI()
    linear_prog.print_LP()
    s = simplex.Simplex(linear_prog)
    s.solveLP()
