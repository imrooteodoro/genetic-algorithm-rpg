from utils.config import *
import random
import numpy as np
from services.persona import Criatura

def inicializar_populacao():
    return [Criatura(np.array([random.uniform(*lim) for lim in LIMITES])) for _ in range(TAMANHO_POPULACAO)]


def selecao_torneio(populacao, k=3):
    competidores = random.sample(populacao, k)
    return max(competidores, key=lambda c: c.fitness)


def crossover(pai1, pai2):
    ponto = random.randint(1, TAMANHO_CROMOSSOMO - 1)
    filho = np.concatenate((pai1.cromossomo[:ponto], pai2.cromossomo[ponto:]))
    return filho


def mutacao(cromossomo):
    for i, (min_val, max_val) in enumerate(LIMITES):
        if random.random() < TAXA_MUTACAO:
            delta = (max_val - min_val) * 0.2
            cromossomo[i] += random.uniform(-delta, delta)
            cromossomo[i] = np.clip(cromossomo[i], min_val, max_val)
    return cromossomo


def nova_geracao(populacao):
    populacao.sort(key=lambda c: c.fitness, reverse=True)
    nova = [Criatura(np.copy(c.cromossomo)) for c in populacao[:2]]
    
    while len(nova) < TAMANHO_POPULACAO:
        pai1 = selecao_torneio(populacao)
        pai2 = selecao_torneio(populacao)
        filho_cromossomo = crossover(pai1, pai2)
        filho_cromossomo = mutacao(filho_cromossomo)
        nova.append(Criatura(filho_cromossomo))
    return nova

