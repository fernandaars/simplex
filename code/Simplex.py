# Orlando Enrico Liz Silvério Silva

import numpy as np

class Simplex:
        
    '''
    Resolve uma PL com o Simplex
    '''
    def resolveSimplex(self, modelo):
        tableau, varsArtificiais, solBasicaViavel = modelo._tableau()
        n, m = tableau.shape

        # Parte 1 (Somente se houverem variáveis artificiais)
        if len(varsArtificiais) != 0:
            viavel, tableauVals  = self._parte1(tableau, varsArtificiais, solBasicaViavel)
            tableau, solBasicaViavel = tableauVals
            if not viavel:
                return 'Inviavel', None, None

            # Remove variáveis artificiais
            tableau = np.column_stack((tableau[:, 0:m-len(varsArtificiais) - 1], tableau[:, -1]))

        # Parte 2
        tableau, obj, solBasicaViavel, limitada = self._parte2(tableau, modelo.c, solBasicaViavel)
        if limitada:
            numVars = tableau.shape[1] - 1
            x = np.zeros(numVars)
            for i, coord in enumerate(solBasicaViavel):
                linha, coluna = coord
                x[coluna] = tableau[linha, -1]
            return 'Resolvido', obj[-1], x
        else:
            return 'Ilimitada', None, None


    '''
    Parte 1 do simplex
    '''
    def _parte1(self, tableau, varsArtificiais, solBasicaViavel):

        n, m = tableau.shape
        
        # Cria a função objetivo
        c = np.zeros(m - 1)
        colunasArtificiais = list(map(lambda x: x[1], varsArtificiais))
        c[colunasArtificiais] = -1 # deve ser -1
        obj = self._calculaObj(tableau, c, solBasicaViavel)
        tableau, obj, solBasicaViavel, limitada = self._simplex(tableau, obj, solBasicaViavel)

        # Se o valor objetivo é 0 é viável      
        if np.isclose(obj[-1], 0):
            return True, (tableau, solBasicaViavel)
        else:
            return False, (None, None)


    '''
    Parte 2 do simplex. Tableau começa com a solução básica viável
    '''
    def _parte2(self, tableau, c, solBasicaViavel):

        n, m = tableau.shape
        obj = self._calculaObj(tableau, c, solBasicaViavel)
        tableau, obj, solBasicaViavel, limitada = self._simplex(tableau, obj, solBasicaViavel)
        return tableau, obj, solBasicaViavel, limitada


    '''
    Algoritmo Simplex. Usa uma solução básica viável como entrada. 
    Usa também a regra de Bland para evitar ciclagem.
    '''
    def _simplex(self, tableau, obj, solBasicaViavel):

        while True:

            # Encontra a variável para entrar na base. Usa Regra de Bland (seleciona o primeiro)
            negativos = np.where(obj[:-1] < 0)[0]
            if len(negativos) == 0:
                break

            novaBase = negativos[0]

            # Encontra a variável para sair da base
            linha = -1
            minCusto = float('Inf')
            for i in range(tableau.shape[0]):
                if tableau[i, novaBase] > 0:
                    custo = tableau[i, -1] / tableau[i, novaBase]
                    if custo < minCusto:
                        linha = i
                        minCusto = custo

            if linha == -1:
                return tableau, obj, solBasicaViavel, False

            saida = list(filter(lambda x: x[0] == linha, solBasicaViavel))
            tableau, obj = self._pivot(tableau, obj, linha, novaBase)
            assert len(saida) == 1
            solBasicaViavel.remove(saida[0])
            solBasicaViavel.append((linha, novaBase))

        return tableau, obj, solBasicaViavel, True


    '''
    Calcula o valor objetivo
    '''
    def _calculaObj(self, tableau, c, solBasicaViavel):
        
        n, m = tableau.shape

        obj = np.append(c, 0)
        for coord in solBasicaViavel:
            linha, coluna = coord
            obj = obj - obj[coluna] * tableau[linha, :]
        obj = -1 * obj

        return obj


    '''
    Pivoteamento
    '''
    def _pivot(self, tableau, obj, linha, coluna):

        tableau[linha, :] = tableau[linha, :] / tableau[linha, coluna]
        linhas, colunas = tableau.shape
        for r in range(linhas):
            if r != linha:
                tableau[r, :] = tableau[r, :] - tableau[r, coluna] * tableau[linha, :]
                obj = obj - obj[coluna] * tableau[linha, :]

        return tableau, obj