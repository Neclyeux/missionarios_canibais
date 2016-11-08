#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

class Estado():
    """
        Representa um estado dentro de uma árvore de estados para resolver o problema de
        atravessar missionários e canibais para a outra margem do rio.
        Um estado contém a quantinade de missionários à esquerda do rio (missionarios_esq),
        a quantidade de missionarios à direita do rio (missionarios_dir), a quantidade de
        canibais à esquerda do rio (canibais_esq), a quantidade de canibais a direita do
        rio (canibais_dir), o lado do rio (lado_rio), seu pai (pai) e seus filhos (filhos),
        além do numero de gerações até aquele estado. Um estado pode ser válido ou não,
        assim como pode ser a solução do problema ou não.
    """

    def __init__(self, num_pessoas, missionarios_esq, missionarios_dir, canibais_esq, canibais_dir, lado_rio, tam_barco):
        """
            Inicializa um estado com as informações de quantidade de missionários e canibais de
            cada lado do rio, além da informação de em que lado do rio está o barco.
        """
        self.tamanho_barco = tam_barco
        self.num_pessoas = num_pessoas
        self.missionarios_esq = missionarios_esq
        self.missionarios_dir = missionarios_dir
        self.canibais_esq = canibais_esq
        self.canibais_dir = canibais_dir
        self.lado_rio = lado_rio
        self.pai = None
        self.filhos = []
        self.profundidade = 0

    def __str__(self):
        """
            Define a representação em string de um estado.
        """
        return 'Missionarios esq: {}\t| Missionarios dir: {} | Lado do rio: {}\nCanibais esq: {}\t       | Canibais dir: {}\t       |'.format(
            self.missionarios_esq, self.missionarios_dir, self.lado_rio, self.canibais_esq, self.canibais_dir
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
        resultado_dir = self.missionarios_dir == self.canibais_dir == self.num_pessoas
        return resultado_esq and resultado_dir

    #Calcula o valor deste estado usando a função f, que verifica o número de pessoas no lado origem do rio
    def custo_f(self):
        return self.missionarios_esq + self.canibais_esq

    #Calcula o valor deste estado usando a função f, que verifica o número de missionarios no lado destino do rio, mais o número de geracões(a profundidade) para se atingir esse estado.
    def custo_h(self):
        return self.missionarios_dir + self.profundidade
    
    def gerar_filhos(self):
        """
            Gera todos os possíveis filhos de um estado, se este for um estado válido e não
            for um estado final.
        """
        # Encontra o novo lado do rio
        novo_lado_rio = 'dir' if self.lado_rio == 'esq' else 'esq'
        # Gera a lista de possíveis movimentos
        if self.tamanho_barco == 2:
            movimentos = [
                {'missionarios': 2, 'canibais': 0},
                {'missionarios': 1, 'canibais': 0},
                {'missionarios': 1, 'canibais': 1},
                {'missionarios': 0, 'canibais': 1},
                {'missionarios': 0, 'canibais': 2},
            ]
        
        elif self.tamanho_barco == 3:
            movimentos = [
                {'missionarios': 2, 'canibais': 0},
                {'missionarios': 1, 'canibais': 0},
                {'missionarios': 1, 'canibais': 1},
                {'missionarios': 0, 'canibais': 1},
                {'missionarios': 0, 'canibais': 2},
                {'missionarios': 3, 'canibais': 0},
                {'missionarios': 1, 'canibais': 2},
                {'missionarios': 2, 'canibais': 1},
                {'missionarios': 0, 'canibais': 3},
            ]
        elif self.tamanho_barco == 4:
            movimentos = [
                {'missionarios': 2, 'canibais': 0},
                {'missionarios': 1, 'canibais': 0},
                {'missionarios': 1, 'canibais': 1},
                {'missionarios': 0, 'canibais': 1},
                {'missionarios': 0, 'canibais': 2},
                {'missionarios': 3, 'canibais': 0},
                {'missionarios': 1, 'canibais': 2},
                {'missionarios': 2, 'canibais': 1},
                {'missionarios': 0, 'canibais': 3},
                {'missionarios': 0, 'canibais': 4},
                {'missionarios': 4, 'canibais': 0},
                {'missionarios': 2, 'canibais': 2},
                {'missionarios': 3, 'canibais': 1},
                {'missionarios': 1, 'canibais': 3},
            ]
        else:
            print "Tamanho do barco grande demais!!!"
            return
                
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
            filho = Estado(self.num_pessoas, missionarios_esq, missionarios_dir, canibais_esq,
                           canibais_dir, novo_lado_rio, self.tamanho_barco)
            filho.pai = self
            filho.profundidade = self.profundidade + 1
            if filho.estado_valido():
                self.filhos.append(filho)


class Missionarios_Canibais():
    """
        Resolve o problema dos missionários e canibais, gerando para isso uma árvore de estados.
    """

    def __init__(self, num_pessoas, tam_barco):
        """
            Inicializa uma instância do problema com uma raiz pré-definida e ainda sem solução.
        """
        
        """ Insere a raiz na fila de execução, que será utilizada para fazer uma busca em largura; cria uma pilha de execução vazia que será usada na busca em profundidade;
        e uma fronteira de estados, usada nas buscas heurísticas.
        """
        self.num_pessoas = num_pessoas
        self.tam_barco = tam_barco
        self.fila = [Estado(self.num_pessoas, self.num_pessoas, 0, self.num_pessoas, 0, 'esq', self.tam_barco)]
        self.pilha = None
        self.fronteira_estados = [Estado(self.num_pessoas, self.num_pessoas, 0, self.num_pessoas, 0, 'esq', self.tam_barco)]
        self.solucao = []
        self.numero_estados = 0
        self.estados_visitados = []

    def verifica(self, elemento, fila):
        for i in fila:
            if elemento == i:
                return True
        return False

    
    #retorna o estado com menor valor na fronteira de estados. Variável estado_menor_custo indica o estado menos custoso, que irá gerar os próximos estados.
    def menor_custo(self):
        estado_menor_custo = self.fronteira_estados[0]
        minimo = self.fronteira_estados[0].custo_f()
        for estado in self.fronteira_estados:
            if estado.custo_f() < minimo:
                minimo = estado.custo_f()
                estado_menor_custo = estado
        return estado_menor_custo

    #Retorna o estado com menor custo na funcao h, que verifica o numero de expansoes para se chegar até aquele estado
    # e o numero de missionarios na margem de origem do rio.
    
    def menor_custo_h(self):
        estado_menor_numero = self.fronteira_estados[0]
        minimo = self.fronteira_estados[0].custo_h()
        for estado in self.fronteira_estados:
            if estado.custo_h() < minimo:
                minimo = estado.missionarios_esq
                estado_menor_custo = estado
        return estado_menor_numero

    def mostrar_resultados(self, solucao, profundidade_solucao, tempo, tamanho_fronteira, profundidade_maxima, numero_estados_visitados ):
        string = ''
        string += '-> SOLUCAO: \n\n'
        for i in solucao:
            string += str(i) + '\n'
            string += 60 * '-' + '\n'
        string += '\nProfundidade da solucao: ' + str(profundidade_solucao) + '\n'
        string += 'Profundidade maxima atingida: ' + str(profundidade_maxima) + '\n'
        string += 'Total de estados visitados: ' + str(numero_estados_visitados) + '\n'
        string += 'Tempo de execucao total: ' + str(tempo) + ' segundos\n'
        string += 'Tamanho maximo atingido pela fronteira de espaco de estados: ' + str(tamanho_fronteira) + '\n'
        return string


    """
        Encontra a solução gerando uma árvore de estados a ser percorrida com o algoritmo de
        busca em largura, que utiliza uma FILA em sua execução.
    """
    def gerar_solucao_busca_largura(self):
        numero_estados_visitados = 0
        profundidade_maxima = 0
        tamanho_maximo_fronteira = 0
        inicio = time.time()
        for elemento in self.fila:
            numero_estados_visitados+=1
            self.solucao.append(elemento)
            if elemento.profundidade > profundidade_maxima:
                profundidade_maxima = elemento.profundidade
            if len(self.fila) > tamanho_maximo_fronteira:
                tamanho_maximo_fronteira = len(self.fila)
            if elemento.estado_final():
                fim = time.time()
                profundidade_solucao = elemento.profundidade
                print "BUSCA EM LARGURA"    
                return self.mostrar_resultados(self.solucao, profundidade_solucao, fim-inicio, tamanho_maximo_fronteira, profundidade_maxima, numero_estados_visitados)
                break;
            elemento.gerar_filhos()
            for i in elemento.filhos:
                if not self.verifica(i, self.fila):
                    self.fila.append(i)
        
        
    """
        Encontra a solução gerando uma árvore de estados a ser percorrida com o algoritmo de
        busca em profundidade, que utiliza uma PILHA em sua execução.
    """
    def gerar_solucao_busca_profundidade(self):
        self.pilha = Pilha()
        self.pilha.push(Estado(self.num_pessoas, self.num_pessoas, 0, self.num_pessoas, 0, 'esq', self.tam_barco))
        numero_estados_visitados = 0
        profundidade_maxima = 0
        tamanho_maximo_fronteira = 0
        inicio = time.time()
        while not self.pilha.isEmpty():
            if len(self.pilha) > tamanho_maximo_fronteira:
                tamanho_maximo_fronteira = len(self.pilha) 
            elemento = self.pilha.pop()
            numero_estados_visitados+=1
            if elemento.profundidade > profundidade_maxima:
                profundidade_maxima = elemento.profundidade
            if elemento.estado_final():
                # Se a solução foi encontrada, o caminho que compõe a solução é gerado realizando
                # o caminho de volta até a raiz da árvore de estados e então encerra a busca
                fim = time.time()
                profundidade_solucao = elemento.profundidade
                self.solucao = [elemento]
                while elemento.pai:
                    self.solucao.insert(0, elemento.pai)
                    elemento = elemento.pai
                print "BUSCA EM PROFUNDIDADE"    
                return self.mostrar_resultados(self.solucao, profundidade_solucao, fim-inicio, tamanho_maximo_fronteira, profundidade_maxima, numero_estados_visitados)
                break;
            self.estados_visitados.append(elemento)
            elemento.gerar_filhos()
            for i in elemento.filhos:
                if not self.verifica(i, self.pilha.items):
                    if not self.verifica(i, self.estados_visitados):
                        self.pilha.push(i)


    def gerar_solucao_busca_gulosa(self):
        estados_visitados = []
        solucao =[]
        numero_estados_visitados = 0
        profundidade_maxima = 0
        tamanho_maximo_fronteira = 0
        inicio = time.time()
        while not self.solucao:
            for elemento in self.fronteira_estados:
                numero_estados_visitados+=1
                solucao.append(elemento)
                if elemento.profundidade > profundidade_maxima:
                    profundidade_maxima = elemento.profundidade
                if len(self.fronteira_estados) > tamanho_maximo_fronteira:
                    tamanho_maximo_fronteira = len(self.fronteira_estados)
                if elemento.estado_final():
                    fim = time.time()
                    profundidade_solucao = elemento.profundidade
                    print "BUSCA GULOSA"
                    # Se a solução foi encontrada, o caminho que compõe a solução é gerado realizando
                    # o caminho de volta até a raiz da árvore de estados e então encerra a busca
                    return self.mostrar_resultados(solucao, profundidade_solucao, fim-inicio, tamanho_maximo_fronteira, profundidade_maxima,
                            numero_estados_visitados)
                    break;
                estados_visitados.append(elemento)
                 #Caso não seja encontrado o estado final, o estado menor custo da fronteira é expandido e a busca continua.
            estado_menor_custo = self.menor_custo()
            estado_menor_custo.gerar_filhos()
            self.fronteira_estados = []
            for i in estado_menor_custo.filhos:
                if not self.verifica(i, estados_visitados):
                    self.fronteira_estados.append(i)   

        
    def gerar_solucao_busca_A(self):
        estados_visitados = []
        solucao = []
        numero_estados_visitados = 0
        profundidade_maxima = 0
        tamanho_maximo_fronteira = 0
        inicio = time.time()
        while not self.solucao:
            for elemento in self.fronteira_estados:
                numero_estados_visitados+=1
                solucao.append(elemento)
                if elemento.profundidade > profundidade_maxima:
                    profundidade_maxima = elemento.profundidade
                if len(self.fronteira_estados) > tamanho_maximo_fronteira:
                    tamanho_maximo_fronteira = len(self.fronteira_estados)
                if elemento.estado_final():
                    fim = time.time()
                    profundidade_solucao = elemento.profundidade
                    print "BUSCA A*"
                    # Se a solução foi encontrada, o caminho que compõe a solução é gerado realizando
                    # o caminho de volta até a raiz da árvore de estados e então encerra a busca
                    return self.mostrar_resultados(solucao, profundidade_solucao, fim-inicio, tamanho_maximo_fronteira, profundidade_maxima,
                            numero_estados_visitados)
                    break;
                estados_visitados.append(elemento)
                 #Caso não seja encontrado o estado final, o estado menor custo da fronteira é expandido e a busca continua.
            estado_menor_custo = self.menor_custo_h()
            estado_menor_custo.gerar_filhos()
            for i in estado_menor_custo.filhos:
                if not self.verifica(i, self.fronteira_estados) and not self.verifica(i, estados_visitados):
                    self.fronteira_estados.append(i) 
            self.fronteira_estados.remove(estado_menor_custo)
            
class Pilha():
    def __init__(self) :
        self.items = []

    #quantidade de itens na pilha
    def __len__(self):
        return len(self.items)

    #empilha
    def push(self, item) :
        self.items.append(item)

    #desempilha
    def pop(self) :
        return self.items.pop()

    #verifica se a pilha esta vazia
    def isEmpty(self) :
        return (self.items == [])

if __name__ == "__main__":
##    estado = Estado(3,0,3,0,'esq',4)
##    estado.gerar_filhos()
##    print "ESTADO PAI"
##    print estado
##    for filho in estado.filhos:
##        print "FILHO"
##        print filho
    problema = Missionarios_Canibais(2, 2)
    solucao = problema.gerar_solucao_busca_profundidade()
    print solucao
        
