class Metricas:

  def __init__(self, aeroporto):
    self.registrosDeMetrica = aeroporto.registrosDeMetrica 
    self.tempos = {
      'tempo de pouso': aeroporto.tempoDePouso,
      'tempo de desembarque': aeroporto.tempoDeEmbarque,
      'tempo de abastecimento': aeroporto.tempoDeAbastecimento,
      'tempo de decolagem': aeroporto.tempoDeDecolagem
    }

  def __separarAvioesPorIdDoRecurso(self, nomeDoRecurso, quantidade):
    quantidadeDeAvioesPorPista = [0] * quantidade
    for registro in self.registrosDeMetrica:
      if(registro[nomeDoRecurso] is not None):
        quantidadeDeAvioesPorPista[registro[nomeDoRecurso]] += 1
    return quantidadeDeAvioesPorPista
  

  def utilizacaoPistas(self, numeroDePistas, tempoTotalSimulacao):
    # [0] - Quantidade de aviões na pista 0 | [1] - Quantidade de aviões na pista 1 | [2] - Quantidade de aviões na pista 2 ...
    quantidadeDeAvioesPorPistaDePouso = self.__separarAvioesPorIdDoRecurso('pista de pouso', numeroDePistas)
    quantidadeDeAvioesPorPistaDeDecolagem = self.__separarAvioesPorIdDoRecurso('pista de decolagem', numeroDePistas)
  
    for i in range(numeroDePistas):
      tempoTotalPouso = (quantidadeDeAvioesPorPistaDePouso[i] * self.tempos['tempo de pouso'])
      tempoTotalDecolagem = (quantidadeDeAvioesPorPistaDeDecolagem[i] * self.tempos['tempo de decolagem'])

      utilizacaoPista = (tempoTotalPouso + tempoTotalDecolagem) / tempoTotalSimulacao

      print('Utilização da pista %d: %.2f' %
            (i, utilizacaoPista))
      
 
  def utilizacaoPontesDesembarque(self, numeroDePontes, tempoTotalSimulacao):
    quantidadeDeAvioesPorPonteDeDesembarque = self.__separarAvioesPorIdDoRecurso('ponte de desembarque(finger)', numeroDePontes)

    for i in range(numeroDePontes):
      tempoTotalDesembarque = (
          quantidadeDeAvioesPorPonteDeDesembarque[i] * self.tempos['tempo de desembarque'])
      
      utilizacaoPonte = tempoTotalDesembarque / tempoTotalSimulacao

      print('Utilização da ponte de desembarque %d: %.2f' %
            (i, utilizacaoPonte))

  def utilizacaoBombasDeCombustivel(self, numeroDeBombas, tempoTotalSimulacao):
    quantidadeDeAvioesPorBombaDeCombustivel = self.__separarAvioesPorIdDoRecurso(
        'bomba de combustivel', numeroDeBombas)

    for i in range(numeroDeBombas):
      tempoTotalAbastecimento = (
          quantidadeDeAvioesPorBombaDeCombustivel[i] * self.tempos['tempo de abastecimento'])

      utilizacaoBombas = tempoTotalAbastecimento / tempoTotalSimulacao

      print('Utilização da bomba de combustível %d: %.2f' %
            (i, utilizacaoBombas))


  def avioesAtendidosPorHora(self, tempoTotalSimulacao):
    throughput = len(self.registrosDeMetrica) / (tempoTotalSimulacao/(60 * 60))
    print('Aviões atendidos por horas (throughput): %.2f' % throughput)

  def tempoMedioPorAviaoEmFila(self):
    tempoTotalEmFila = 0
    for registro in self.registrosDeMetrica:
      tempoTotalEmFila+= self.__tempoDecorridoEntreProcessos(registro['tempos']['pouso'], 1, 0)
      
      if(len(registro['tempos']['abastecimento']) > 0):
        tempoTotalEmFila += self.__tempoDecorridoEntreProcessos(
            registro['tempos']['abastecimento'], 1, 0)

      tempoTotalEmFila += self.__tempoDecorridoEntreProcessos(
          registro['tempos']['desembarque'], 1, 0)

      tempoTotalEmFila += self.__tempoDecorridoEntreProcessos(
          registro['tempos']['decolagem'], 1, 0)

    tempoMedio = (tempoTotalEmFila/len(self.registrosDeMetrica))
    print('Tempo médio em fila: %.2f segundos' %tempoMedio)
    return tempoMedio
    
  def tempoMedioPorAviaoEmSolo(self):
    tempoTotalEmSolo = 0
    for registro in self.registrosDeMetrica:
      if(len(registro['tempos']['abastecimento']) > 0):
        tempoTotalEmSolo += self.__tempoDecorridoEntreProcessos(
            registro['tempos']['abastecimento'], 2, 0)

      tempoTotalEmSolo += self.__tempoDecorridoEntreProcessos(
          registro['tempos']['desembarque'], 2, 0)

      tempoTotalEmSolo += self.__tempoDecorridoEntreProcessos(
          registro['tempos']['decolagem'], 2, 0)

    tempoMedio = (tempoTotalEmSolo/len(self.registrosDeMetrica))
    print('Tempo médio em solo: %.2f segundos' % tempoMedio)
    return tempoMedio

  def __tempoDecorridoEntreProcessos(self, registro, final, começo):
    return registro[final] - registro[começo]
    
  # def __somatorioDeTempoDeUsoPorRecurso(self, nomeDoRecurso, tempoDoProcesso, numeroDoRecurso):
  #   somatorioDeTempo = 0

  #   for registro in self.registrosDeMetrica:
  #     if registro[nomeDoRecurso] == numeroDoRecurso:
  #       somatorioDeTempo += self.tempos[tempoDoProcesso]

  #   return somatorioDeTempo
