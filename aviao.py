import simpy
import random


def processoAviao(env, nomeAviao, aeroporto):

    dadosAviao = {
        'nome do avião': nomeAviao,
        'pista de pouso': None,
        'bomba de combustivel': None,
        'pista de desembarque(finger)': None,
        'pista de decolagem': None,
    }

    # FILA DE POUSO
    aeroporto.filas['fila de pouso'].append(
        nomeAviao + '- Chegada - ' + str(env.now))
    # Espera uma pista de pouso estar disponível
    pistaUtilizada = yield aeroporto.pistas.get()
    aeroporto.filas['fila de pouso'].append(
        nomeAviao + '- Pouso - ' + str(env.now))

    # PROCESSO DE POUSO - TEMPO
    yield env.process(lidarComTiposDeProcedimento(env, 'pousar', aeroporto))

    dadosAviao['pista de pouso'] = pistaUtilizada['id']
    # LIBERA A PISTA DE POUSO
    yield aeroporto.pistas.put(pistaUtilizada)
    

    # GERA A PORCENTAGEM DE GASOLINA NO TANQUE
    porcentagemDeGasolinaAtual = random.randint(0, 100)
    # print(porcentagemDeGasolinaAtual)

    if porcentagemDeGasolinaAtual <= 70:

      # FILA DE ABASTECIMENTO
      aeroporto.filas['fila de abastecimento'].append(nomeAviao + '- Chegada - ' + str(env.now))
      # Espera uma bomba de combustível estar disponível
      bombaUtilizada = yield aeroporto.bombasDeCombustivel.get()
      aeroporto.filas['fila de abastecimento'].append(nomeAviao + '- Abastecido - ' + str(env.now))

      # PROCESSO DE ABASTECER - TEMPO
      yield env.process(lidarComTiposDeProcedimento(env, 'abastecer', aeroporto))

      dadosAviao['bomba de combustivel'] = bombaUtilizada['id']
      # LIBERA A BOMBA DE COMBUSTÍVEL
      yield aeroporto.bombasDeCombustivel.put(bombaUtilizada)
      

    # FILA DE EMBARQUE/DESEMBARQUE
    aeroporto.filas['fila de desembarque'].append( nomeAviao + '- Chegada - ' + str(env.now))
    # Espera uma ponte de embarque/desembarque estar disponível
    pistaDeDesembarqueUtilizada = yield aeroporto.pontesDeDesembarque.get()
    aeroporto.filas['fila de desembarque'].append(nomeAviao + '- Desembarque finalizado - ' + str(env.now))

    # PROCESSO DE EMBARQUE/DESEMBARQUE - TEMPO
    yield env.process(lidarComTiposDeProcedimento(env, 'embarque', aeroporto))

    dadosAviao['pista de desembarque(finger)'] = pistaDeDesembarqueUtilizada['id']
    # LIBERA A PISTA DE EMBARQUE/DESEMBARQUE
    yield aeroporto.pontesDeDesembarque.put(pistaDeDesembarqueUtilizada)

    

    # FILA DE DECOLAGEM
    aeroporto.filas['fila de decolagem'].append(nomeAviao + '- Chegada - ' + str(env.now))
    # Espera uma pista estar disponível
    pistaDeDecolagemUtilizada = yield aeroporto.pistas.get()
    aeroporto.filas['fila de decolagem'].append(nomeAviao + '- Decolagem realizada - ' + str(env.now))

    # PROCESSO DE DECOLAGEM - TEMPO
    yield env.process(lidarComTiposDeProcedimento(env, 'decolar', aeroporto))

    dadosAviao['pista de decolagem'] = pistaDeDecolagemUtilizada['id']
    # LIBERA A PISTA DE DECOLAGEM
    yield aeroporto.pistas.put(pistaDeDecolagemUtilizada)

    

def lidarComTiposDeProcedimento(env, procedimento, aeroporto):
    match procedimento:
        case 'pousar':
            yield env.timeout(aeroporto.tempoDePouso)
        case 'embarque':
            yield env.timeout(aeroporto.tempoDeEmbarque)
        case 'abastecer':
            yield env.timeout(aeroporto.tempoDeAbastecimento)
        case 'decolar':
            yield env.timeout(aeroporto.tempoDeDecolagem)
    pass
