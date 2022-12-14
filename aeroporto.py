import simpy

from aviao import *

class Aeroporto:
  
  def __init__(self, env):
    # Ambiente de simulação
    self.env = env

    # Variáveis de recursos
    self.pistas = simpy.Store(env, 1)
    self.pontesDeDesembarque = simpy.Store(env, 1)
    self.bombasDeCombustivel = simpy.Store(env, 1)
    
    # Variáveis de tempo
    self.tempoDePouso = 15
    self.tempoDeEmbarque = 15
    self.tempoDeAbastecimento = 15
    self.tempoDeDecolagem = 15

    # Métricas
    self.registrosDeMetrica = []

    self.preencherRecursos()

    pass

  def registrarMetrica(self, metrica):
    self.registrosDeMetrica.append(metrica)

  def preencherRecursos(self):

    for i in range(self.pistas.capacity):
      self.pistas.put({'id': i})

    for i in range(self.pontesDeDesembarque.capacity):
      self.pontesDeDesembarque.put({'id': i})

    for i in range(self.bombasDeCombustivel.capacity):
      self.bombasDeCombustivel.put({'id': i})

    pass

  def processoGeralAeroporto(self, env):

    i = 0

    env.process(processoAviao(env, 'Avião %d' %i, self))


    while True:
      yield env.timeout(15)
      i += 1
      env.process(processoAviao(env, 'Avião %d' %i, self))
      


  