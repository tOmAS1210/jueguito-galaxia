from typing import Any
import pygame
import colores
import random
import galaga_personaje

class Disparo_enemigos(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load("galaga_laser_enemigo.png")
        self.image = pygame.transform.scale(self.image,(10,50))
        self.image.set_colorkey(colores.BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y += 5