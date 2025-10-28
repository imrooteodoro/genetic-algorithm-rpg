import numpy as np
from utils.config import *
import random

class Criatura:
    _id_counter = 0
    
    def __init__(self, cromossomo):
        self.cromossomo = np.copy(cromossomo)
        self.fitness = 0
        self.tipo = random.choice(list(SPRITES_POR_TIPO.keys()))
        self.sprite_path = random.choice(SPRITES_POR_TIPO[self.tipo])
        
        Criatura._id_counter += 1
        self.id = Criatura._id_counter
        
        self.decodificar()

    def decodificar(self):
        (self.forca,
         self.agilidade,
         self.inteligencia,
         self.vitalidade,
         self.fe,
         self.carisma) = self.cromossomo

    def calcular_fitness(self):
        if self.tipo == "Templário":
            self.fitness = self.fe * 1.5 + self.forca
        elif self.tipo == "Clérigo":
            self.fitness = self.fe * 2 + self.carisma
        elif self.tipo == "Dragão":
            self.fitness = self.forca * 1.8 + self.vitalidade
        elif self.tipo == "Mago":
            self.fitness = self.inteligencia * 2 + self.agilidade
        else:
            self.fitness = self.forca + self.vitalidade + self.agilidade * 0.5
        return self.fitness
