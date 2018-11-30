# Orlando Enrico Liz Silvério Silva

import numpy as np
import sys
import fractions as frac

from FPI import FPI
from Simplex import Simplex
np.set_printoptions(formatter={'all':lambda x: str(frac.Fraction(x).limit_denominator())})


'''
Lê o arquivo com os dados do problema
'''
def lePL(filepath):

	file = open(filepath, 'r')
	numVars = int(file.readline()) 
	numRestricoes = int(file.readline()) 

	negRestricoes = np.array(file.readline().split(' ')).astype("int")

	c = file.readline().split(' ')
	if c[-1] == '\n':
		c = c[:-1]
	
	c = [frac.Fraction(float(c[i])) for i in range(len(c))]
	matrix = []
	for i in range(numRestricoes):
		linha = file.readline().split(' ')
		if linha[-1][-1] == '\n':
			linha[-1] = linha[-1][:-1] 
		matrix.append(linha)
	file.close()

	b = [matrix[i][-1] for i in range(len(matrix))]
	sinais = [matrix[i][-2] for i in range(len(matrix))]
	matrix = [matrix[i][:-2] for i in range(len(matrix))]

	b = np.array([frac.Fraction(float(b[i])) for i in range(len(b))])
	for i in range(len(matrix)):
		for j in range(len(matrix[i])):
			matrix[i][j] = frac.Fraction(float(matrix[i][j]))

	A = np.zeros(shape=(numRestricoes, numVars));

	for i in range(len(matrix)):
		for j in range(len(matrix[i])):
			A[i][j] = frac.Fraction(float(matrix[i][j]));
		
	file.close()
	
	return numVars, numRestricoes, A, b, c, sinais, negRestricoes


'''
Escreve o arquivo de saída com os resultados
'''
def escrevePL(filepath, solucao, obj, x):

	file = open(filepath, 'w')

	if solucao == "Inviavel":
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


if __name__ == '__main__':

	numVars, numRestricoes, A, b, c, sinais, negRestricoes = lePL(sys.argv[1])

	modelo = FPI(A, b, c, sinais, negRestricoes)
	solver = Simplex()
	solucao, obj, x = solver.resolveSimplex(modelo)

	escrevePL(sys.argv[2], solucao, obj, x)