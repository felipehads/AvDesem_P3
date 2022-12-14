import simpy
import random


def processoAviao(env, nomeAviao, aeroporto):

    dadosAviao = {
        'nome do aviao': nomeAviao,
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

    aeroporto.registrarMetrica(dadosAviao)
    indexDoAviaoAtual = len(aeroporto.registrosDeMetrica) - 1

    # FILA DE POUSO
    dadosAviao['tempos']['pouso'].append(env.now)
    atualizarDadosAviao(indexDoAviaoAtual, dadosAviao, aeroporto)

    # Espera uma pista de pouso estar disponível
    pistaUtilizada = yield aeroporto.pistas.get()
    dadosAviao['tempos']['pouso'].append(env.now)
    atualizarDadosAviao(indexDoAviaoAtual, dadosAviao, aeroporto)

    # PROCESSO DE POUSO - TEMPO
    yield env.process(lidarComTiposDeProcedimento(env, 'pousar', aeroporto))
    dadosAviao['tempos']['pouso'].append(env.now)
    dadosAviao['pista de pouso'] = pistaUtilizada['id']
    atualizarDadosAviao(indexDoAviaoAtual, dadosAviao, aeroporto)

    # LIBERA A PISTA DE POUSO
    yield aeroporto.pistas.put(pistaUtilizada)

    
    # GERA A PORCENTAGEM DE GASOLINA NO TANQUE
    porcentagemDeGasolinaAtual = random.randint(0, 100)

    if porcentagemDeGasolinaAtual <= 70:

        # FILA DE ABASTECIMENTO
        dadosAviao['tempos']['abastecimento'].append(env.now)
        atualizarDadosAviao(indexDoAviaoAtual, dadosAviao, aeroporto)   

        # Espera uma bomba de combustível estar disponível
        bombaUtilizada = yield aeroporto.bombasDeCombustivel.get()
        dadosAviao['tempos']['abastecimento'].append(env.now)
        atualizarDadosAviao(indexDoAviaoAtual, dadosAviao, aeroporto)    

        # PROCESSO DE ABASTECER - TEMPO
        yield env.process(lidarComTiposDeProcedimento(env, 'abastecer', aeroporto))
        dadosAviao['tempos']['abastecimento'].append(env.now)
        dadosAviao['bomba de combustivel'] = bombaUtilizada['id']
        atualizarDadosAviao(indexDoAviaoAtual, dadosAviao, aeroporto)   

        # LIBERA A BOMBA DE COMBUSTÍVEL
        yield aeroporto.bombasDeCombustivel.put(bombaUtilizada)   

      
    
    # FILA DE EMBARQUE/DESEMBARQUE
    dadosAviao['tempos']['desembarque'].append(env.now)
    atualizarDadosAviao(indexDoAviaoAtual, dadosAviao, aeroporto)   

    # Espera uma ponte de embarque/desembarque estar disponível
    ponteDeDesembarqueUtilizada = yield aeroporto.pontesDeDesembarque.get()
    dadosAviao['tempos']['desembarque'].append(env.now)
    atualizarDadosAviao(indexDoAviaoAtual, dadosAviao, aeroporto)   

    # PROCESSO DE EMBARQUE/DESEMBARQUE - TEMPO
    yield env.process(lidarComTiposDeProcedimento(env, 'embarque', aeroporto))
    dadosAviao['tempos']['desembarque'].append(env.now)
    dadosAviao['ponte de desembarque(finger)'] = ponteDeDesembarqueUtilizada['id']
    atualizarDadosAviao(indexDoAviaoAtual, dadosAviao, aeroporto)   

    # LIBERA A PISTA DE EMBARQUE/DESEMBARQUE
    yield aeroporto.pontesDeDesembarque.put(ponteDeDesembarqueUtilizada)


    
    # FILA DE DECOLAGEM
    dadosAviao['tempos']['decolagem'].append(env.now)
    atualizarDadosAviao(indexDoAviaoAtual, dadosAviao, aeroporto)

    # Espera uma pista estar disponível
    pistaDeDecolagemUtilizada = yield aeroporto.pistas.get()
    dadosAviao['tempos']['decolagem'].append(env.now)
    atualizarDadosAviao(indexDoAviaoAtual, dadosAviao, aeroporto)   

    # PROCESSO DE DECOLAGEM - TEMPO
    yield env.process(lidarComTiposDeProcedimento(env, 'decolar', aeroporto))
    dadosAviao['tempos']['decolagem'].append(env.now)
    dadosAviao['pista de decolagem'] = pistaDeDecolagemUtilizada['id']
    atualizarDadosAviao(indexDoAviaoAtual, dadosAviao, aeroporto)   

    # LIBERA A PISTA DE DECOLAGEM
    yield aeroporto.pistas.put(pistaDeDecolagemUtilizada)
  
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
    
def atualizarDadosAviao(indexDoAviaoAtual, novosDados, aeroporto):
    aeroporto.registrosDeMetrica[indexDoAviaoAtual] = novosDados