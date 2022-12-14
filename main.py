import simpy

from aeroporto import Aeroporto
from metricas import Metricas

env = simpy.Environment()
tempoDeSimulacao = 3600
aeroporto = Aeroporto(env)
metricas = Metricas(aeroporto)

env.process(aeroporto.processoGeralAeroporto(env))

env.run(until=tempoDeSimulacao)


metricas.utilizacaoPistas(aeroporto.pistas.capacity, tempoDeSimulacao)
metricas.utilizacaoPontesDesembarque(aeroporto.pontesDeDesembarque.capacity, tempoDeSimulacao)
metricas.utilizacaoBombasDeCombustivel(aeroporto.bombasDeCombustivel.capacity, tempoDeSimulacao)
metricas.avioesAtendidosPorHora(tempoDeSimulacao)
metricas.tempoMedioPorAviaoEmFila()
metricas.tempoMedioPorAviaoEmSolo()
