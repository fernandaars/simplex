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
    file = input_treatment.InputTreatment()

    verbose_mode = False
    if(len(sys.argv) == 4):
        if(sys.argv[3] == "--verbose"):
            verbose_mode = True

    lp = file.read_file(sys.argv[1], verbose_mode)
    lp.turn_into_FPI(verbose_mode)
    s = simplex.Simplex(lp)
    s.solve_LP(verbose_mode)
    file.write_file(sys.argv[2], lp)
