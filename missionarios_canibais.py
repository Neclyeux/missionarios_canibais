#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Estado():
    """
        Representa um estado dentro de uma árvore de estados para resolver o problema de
        atravessar missionários e canibais para a outra margem do rio.
        Um estado contém a quantinade de missionários à esquerda do rio (missionarios_esq),
        a quantidade de missionarios à direita do rio (missionarios_dir), a quantidade de
        canibais à esquerda do rio (canibais_esq), a quantidade de canibais a direita do
        rio (canibais_dir), o lado do rio (lado_rio), seu pai (pai) e seus filhos (filhos).
        Um estado pode ser válido ou não, assim como pode ser a solução do problema ou não.
    """

    def __init__(self, missionarios_esq, missionarios_dir, canibais_esq, canibais_dir, lado_rio):
        """
            Inicializa um estado com as informações de quantidade de missionários e canibais de
            cada lado do rio, além da informação de em que lado do rio está o barco.
        """
        self.missionarios_esq = missionarios_esq
        self.missionarios_dir = missionarios_dir
        self.canibais_esq = canibais_esq
        self.canibais_dir = canibais_dir
        self.lado_rio = lado_rio
        self.pai = None
        self.filhos = []

    def __str__(self):
        """
            Define a representação em string de um estado.
        """
        return 'Missionarios: {}\t| Missionarios: {}\nCanibais: {}\t| Canibais: {}'.format(
            self.missionarios_esq, self.missionarios_dir, self.canibais_esq, self.canibais_dir
        )

    def __eq__(self, estado2):
        if (self.missionarios_esq == estado2.missionarios_esq and
            self.missionarios_dir == estado2.missionarios_dir and
            self.canibais_esq == estado2.canibais_esq and
            self.canibais_dir == estado2.canibais_dir and
            self.lado_rio == estado2.lado_rio):
            return True
        return False
        
    def estado_valido(self):
        """
            Verifica se o estado é válido, ou seja, não possue mais canibais que missionários
            em nenhum lado do rio.
        """
        # Não se pode gerar estados onde o número de canibais ou missionários em qualquer lado
        # do rio seja negativo
        if ((self.missionarios_esq < 0) or (self.missionarios_dir < 0)
            or (self.canibais_esq < 0) or (self.canibais_dir < 0)):
            return False
        # Verifica se em ambas as margens do rio o número de missionários não é inferior ao número
        # de canibais. Lembrando que caso não hajam missionários em um dos lados, não é necessário
        # verificar o número de canibais nele.
        return ((self.missionarios_esq == 0 or self.missionarios_esq >= self.canibais_esq) and
                (self.missionarios_dir == 0 or self.missionarios_dir >= self.canibais_dir))


    def estado_final(self):
        """
            Verifica se o estado é um estado final, ou seja, é uma das possíveis soluções do
            problema.
        """
        # Um estado é um estado final se todos os missionários e canibais atravessaram o rio
        resultado_esq = self.missionarios_esq == self.canibais_esq == 0
        resultado_dir = self.missionarios_dir == self.canibais_dir == 3
        return resultado_esq and resultado_dir

    def gerar_filhos(self):
        """
            Gera todos os possíveis filhos de um estado, se este for um estado válido e não
            for um estado final.
        """
        # Encontra o novo lado do rio
        novo_lado_rio = 'dir' if self.lado_rio == 'esq' else 'esq'
        # Gera a lista de possíveis movimentos
        movimentos = [
            {'missionarios': 2, 'canibais': 0},
            {'missionarios': 1, 'canibais': 0},
            {'missionarios': 1, 'canibais': 1},
            {'missionarios': 0, 'canibais': 1},
            {'missionarios': 0, 'canibais': 2},
        ]
        # Gera todos os possíveis estados e armazena apenas os válidos na lista de filhos
        # do estado atual
        for movimento in movimentos:
            if self.lado_rio == 'esq':
                # Se o barco estiver a esquerda do rio, os missionários e canibais saem da
                # margem esquerda do rio e vão para a direita
                missionarios_esq = self.missionarios_esq - movimento['missionarios']
                missionarios_dir = self.missionarios_dir + movimento['missionarios']
                canibais_esq = self.canibais_esq - movimento['canibais']
                canibais_dir = self.canibais_dir + movimento['canibais']
            else:
                # Caso contrário, os missionários e canibais saem da margem direita do rio
                # e vão para a esquerda
                missionarios_dir = self.missionarios_dir - movimento['missionarios']
                missionarios_esq = self.missionarios_esq + movimento['missionarios']
                canibais_dir = self.canibais_dir - movimento['canibais']
                canibais_esq = self.canibais_esq + movimento['canibais']
            # Cria o estado do filho e caso este seja válido, o adiciona à lista de filhos do pai
            filho = Estado(missionarios_esq, missionarios_dir, canibais_esq,
                           canibais_dir, novo_lado_rio)
            filho.pai = self
            if filho.estado_valido():
                self.filhos.append(filho)


class Missionarios_Canibais():
    """
        Resolve o problema dos missionários e canibais, gerando para isso uma árvore de estados.
    """

    def __init__(self):
        """
            Inicializa uma instância do problema com uma raiz pré-definida e ainda sem solução.
        """
        # Insere a raiz na fila de execução, que será utilizada para fazer uma busca em largura
        self.fila_execucao = [Estado(3, 0, 3, 0, 'esq')]
        self.pilha_execucao = None
        self.solucao = None
        self.numero_estados = 0
        self.estados_visitados = []

    def verifica(self, elemento, fila):
        for i in fila:
            if elemento == i:
                return True
        return False

    def gerar_solucao_busca_largura(self):
        """
            Encontra a solução gerando uma árvore de estados a ser percorrida com o algoritmo de
            busca em largura, que utiliza uma fila em sua execução.
        """
        # Realiza a busca em largura em busca da solução
        for elemento in self.fila_execucao:
            self.numero_estados+=1
            print 'Numero de estados visitados: ', self.numero_estados
            print elemento
            print 34 * '-'
            if elemento.estado_final():
                # Se a solução foi encontrada, o caminho que compõe a solução é gerado realizando
                # o caminho de volta até a raiz da árvore de estados e então encerra a busca
                break;
            # Caso o elemento não seja a solução, gera seus filhos e os adiciona na fila de execução
            elemento.gerar_filhos()
            for i in elemento.filhos:
                if not self.verifica(i, self.fila_execucao):
                    self.fila_execucao.append(i)
        

    def gerar_solucao_busca_profundidade(self):
        self.pilha_execucao = Pilha()
        self.pilha_execucao.push(Estado(3, 0, 3, 0, 'esq'))
        while not self.pilha_execucao.isEmpty():
            self.numero_estados+=1
            print 'Numero de estados visitados: ', self.numero_estados
            elemento = self.pilha_execucao.pop()
            #print elemento
            if elemento.estado_final():
                # Se a solução foi encontrada, o caminho que compõe a solução é gerado realizando
                # o caminho de volta até a raiz da árvore de estados e então encerra a busca
                self.solucao = [elemento]
                while elemento.pai:
                    self.solucao.insert(0, elemento.pai)
                    elemento = elemento.pai
                break;
            self.estados_visitados.append(elemento)
            elemento.gerar_filhos()
            for i in elemento.filhos:
                if not self.verifica(i, self.pilha_execucao.items):
                    if not self.verifica(i, self.estados_visitados):
                        self.pilha_execucao.push(i)   


    def gerar_solucao_heuristica_gulosa(self):
        pass

    def gerar_solucao_heuristica_A(self):
        pass

class Pilha():
    def __init__(self) :
        self.items = []

    #empilha
    def push(self, item) :
        self.items.append(item)

    #desempilha
    def pop(self) :
        return self.items.pop()

    #verifica se a pilha esta vazia
    def isEmpty(self) :
        return (self.items == [])

    

if __name__ == '__main__':
    # Instancia o problema e gera sua solução
    problema = Missionarios_Canibais()
    problema.gerar_solucao_busca_profundidade()
    # Exibe a solução em tela, separando cada passo
    for estado in problema.solucao:
        print estado
        print 34 * '-'
