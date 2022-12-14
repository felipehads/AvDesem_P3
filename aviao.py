import simpy
import random


def processoAviao(env, nomeAviao, aeroporto):

    dadosAviao = {
        'nome do avião': nomeAviao,
        'pista de pouso': None,
        'bomba de combustivel': None,
        'ponte de desembarque(finger)': None,
        'pista de decolagem': None,
        'tempos': {  # [0] - ENTRA NA FILA | [1] - SAI DA FILA/INICIA O PROCESSO | [2] - FINALIZA O PROCESSO
            'pouso': [], 
            'abastecimento': [],
            'desembarque': [],
            'decolagem': []
        }
    }

    # FILA DE POUSO
    dadosAviao['tempos']['pouso'].append(env.now)
    # Espera uma pista de pouso estar disponível
    pistaUtilizada = yield aeroporto.pistas.get()
    dadosAviao['tempos']['pouso'].append(env.now)
    

    # PROCESSO DE POUSO - TEMPO
    yield env.process(lidarComTiposDeProcedimento(env, 'pousar', aeroporto))
    dadosAviao['tempos']['pouso'].append(env.now)

    dadosAviao['pista de pouso'] = pistaUtilizada['id']
    # LIBERA A PISTA DE POUSO
    yield aeroporto.pistas.put(pistaUtilizada)
    

    # GERA A PORCENTAGEM DE GASOLINA NO TANQUE
    porcentagemDeGasolinaAtual = random.randint(0, 100)
    # print(porcentagemDeGasolinaAtual)

    if porcentagemDeGasolinaAtual <= 70:

      # FILA DE ABASTECIMENTO
      dadosAviao['tempos']['abastecimento'].append(env.now)
      # Espera uma bomba de combustível estar disponível
      bombaUtilizada = yield aeroporto.bombasDeCombustivel.get()
      dadosAviao['tempos']['abastecimento'].append(env.now)

      # PROCESSO DE ABASTECER - TEMPO
      yield env.process(lidarComTiposDeProcedimento(env, 'abastecer', aeroporto))
      dadosAviao['tempos']['abastecimento'].append(env.now)

      dadosAviao['bomba de combustivel'] = bombaUtilizada['id']
      # LIBERA A BOMBA DE COMBUSTÍVEL
      yield aeroporto.bombasDeCombustivel.put(bombaUtilizada)
      

    # FILA DE EMBARQUE/DESEMBARQUE
    dadosAviao['tempos']['desembarque'].append(env.now)
    # Espera uma ponte de embarque/desembarque estar disponível
    ponteDeDesembarqueUtilizada = yield aeroporto.pontesDeDesembarque.get()
    dadosAviao['tempos']['desembarque'].append(env.now)

    # PROCESSO DE EMBARQUE/DESEMBARQUE - TEMPO
    yield env.process(lidarComTiposDeProcedimento(env, 'embarque', aeroporto))
    dadosAviao['tempos']['desembarque'].append(env.now)

    dadosAviao['ponte de desembarque(finger)'] = ponteDeDesembarqueUtilizada['id']
    # LIBERA A PISTA DE EMBARQUE/DESEMBARQUE
    yield aeroporto.pontesDeDesembarque.put(ponteDeDesembarqueUtilizada)

    
    # FILA DE DECOLAGEM
    dadosAviao['tempos']['decolagem'].append(env.now)
    # Espera uma pista estar disponível
    pistaDeDecolagemUtilizada = yield aeroporto.pistas.get()
    dadosAviao['tempos']['decolagem'].append(env.now)

    # PROCESSO DE DECOLAGEM - TEMPO
    yield env.process(lidarComTiposDeProcedimento(env, 'decolar', aeroporto))
    dadosAviao['tempos']['decolagem'].append(env.now)

    dadosAviao['pista de decolagem'] = pistaDeDecolagemUtilizada['id']
    # LIBERA A PISTA DE DECOLAGEM
    yield aeroporto.pistas.put(pistaDeDecolagemUtilizada)

    aeroporto.registrarMetrica(dadosAviao)

    # print(dadosAviao)
    pass


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
