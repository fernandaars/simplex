# Orlando Enrico Liz Silvério Silva

import numpy as np
import fractions as frac

class FPI(object):
    '''
    Coloca a PL em FPI, ou seja, na forma:
        max c^T x
        sujeito a Ax = b
        x >= 0
    '''
    def __init__(self, A, b, c, sinais, neg_restricoes):

        # variáveis para transformar a solução de volta a forma original
        self.vars = {i: str(i) for i in range(A.shape[1])}
        self.folga = []

        # Partes do Tableau
        self.A = A
        self.b = b
        self.c = c 
        self._dominioVariaveis(neg_restricoes)
        self._variaveisFolga(sinais)

  
    '''
    Altera A e c para que todas as variáveis tenham domínio >= 0
    '''
    def _dominioVariaveis(self, neg_restricoes):

        for i, sinal in enumerate(neg_restricoes):
            if sinal == '0':
                self.c = np.append(self.c, -1 * self.c[i])
                self.A = np.append(self.A, np.array([-1 * self.A[:, i]]).T, 1)
                self.vars[i] = self.vars[i] + '-' + str(self.A.shape[1] - 1)


    '''
    Adiciona variáveis de folga para transformar inequações em equações
    '''
    def _variaveisFolga(self, sinais):
        for i, sinal in enumerate(sinais):
            linhas = self.A.shape[0]
            if sinal == '>=':
                self.A = np.append(self.A, -1 * np.zeros(shape=[linhas, 1]), 1)
                self.A[i, -1] = -1
                self.c = np.append(self.c, 0)
                self.folga.append(self.A.shape[1] - 1)
            elif sinal == '<=':
                self.A = np.append(self.A, 1 * np.zeros(shape=[linhas, 1]), 1)
                self.A[i, -1] = 1
                self.c = np.append(self.c, 0)
                self.folga.append(self.A.shape[1] - 1)


    '''
    Cria o tableau para a parte 1 do simplex. Adiciona variáveis artificiais se necessário
    '''
    def _tableau(self):
        artificiais = []
        solBasicaViavel = []
        novoB = np.array(self.b)
        linhas, colunas = self.A.shape
        numArtificiais = min(linhas, colunas)
        tableau = np.array(self.A)

        tableau = tableau + frac.Fraction()

        for linha, coluna in enumerate(self.folga):
            if tableau[linha, coluna] == -1 and novoB[linha] < 0:
                tableau[linha] = -1 * tableau[linha]
                novoB[linha] = -1 * novoB[linha]
                numArtificiais -= 1
                solBasicaViavel.append((linha, coluna))
            elif tableau[linha, coluna] == 1 and novoB[linha] > 0:
                solBasicaViavel.append((linha, coluna))
                numArtificiais -= 1

        tableau = np.append(tableau, np.zeros(shape=[linhas, numArtificiais]), 1)

        # Adiciona as variáveis artificiais
        linhas, colunas = tableau.shape
        solBasicaViavel_linhas = set(map(lambda x: x[0], solBasicaViavel))
        valArtificial = 0
        for i in range(linhas):
            if i in solBasicaViavel_linhas:
                continue
            artificiais.append((i, colunas -numArtificiais + valArtificial))
            solBasicaViavel.append((i, colunas -numArtificiais + valArtificial))
            if tableau[i, -1] < 0:
                tableau[i, :] = -1 * tableau[i, :]
            tableau[i, colunas -numArtificiais + valArtificial] = 1
            valArtificial += 1

        return np.column_stack((tableau, novoB)), artificiais, solBasicaViavel