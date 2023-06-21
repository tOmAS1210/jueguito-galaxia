from typing import Any
import pygame
import colores
import random
import galaga_personaje

class DisparoPersonaje(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("galaga_laser.png")
        self.image = pygame.transform.scale(self.image,(10,50))
        self.image.set_colorkey(colores.BLACK)
        self.rect = self.image.get_rect()

    def update(self,):
        self.rect.y -= 5