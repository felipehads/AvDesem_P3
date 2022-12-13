class Metricas:

  def __init__(self, aeroporto):
    self.registrosDeMetrica = aeroporto.registrosDeMetrica 

  def utilizacaoPistas(self, numeroDePistas, tempoTotalSimulacao):
    for i in range(numeroDePistas):
      tempoUtilizacaoPouso = self.__somatorioDeTempoDeUsoPorRecurso('pista de pouso', 'pouso', i)
      tempoUtilizacaoDecolagem = self.__somatorioDeTempoDeUsoPorRecurso('pista de decolagem', 'decolagem', i)

      print('Utilização da pista %d = ' %i ,(tempoUtilizacaoPouso + tempoUtilizacaoDecolagem)/tempoTotalSimulacao)

  def utilizacaoPontesDesembarque(self, numeroDePontes, tempoTotalSimulacao):
    for i in range(numeroDePontes):
      tempoUtilizacaoPonteDesembarque = self.__somatorioDeTempoDeUsoPorRecurso(
          'ponte de desembarque(finger)', 'pouso', i)

      print('Utilização das pontes de desembarque(finger) %d = ' % i, tempoUtilizacaoPonteDesembarque/tempoTotalSimulacao)

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

  def __tempoDecorridoEntreProcessos(self,registro, final, começo):
    return registro[final] - registro[começo]
    
  def __somatorioDeTempoDeUsoPorRecurso(self, nomeDoRecurso, nomeDoProcesso, numeroDoRecurso):
    somatorioDeTempo = 0

    for registro in self.registrosDeMetrica:
      if registro[nomeDoRecurso] == numeroDoRecurso:
        somatorioDeTempo += self.__tempoDecorridoEntreProcessos(
            registro['tempos'][nomeDoProcesso], 2, 1)

    return somatorioDeTempo
