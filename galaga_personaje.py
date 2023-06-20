import pygame
import colores
import random
import galaga_disparo
disparo = galaga_disparo.Disparo_personaje()

class Personaje(pygame.sprite.Sprite): #clase con sub clase de sprite
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.image.load("nave_personaje.png")
        self.image = pygame.transform.scale(self.image,(70,70))
        self.rect = self.image.get_rect()
        self.rect.centerx = 400
        self.rect.y = 700
        self.score = 0
        self.vida = 3
        #disparos
        self.cadencia = 500 #disparo coldown en milisegundos
        self.ultimo_disparo = pygame.time.get_ticks() #tiene un tiempo determinado al no estar en un while o for que haga aumentar su tiempo
        

    def update(self):
        lista_teclas = pygame.key.get_pressed()
        if True in lista_teclas:
            if self.rect.x > 0:
                if lista_teclas[pygame.K_LEFT]:
                    self.rect.x -= 5
                    disparo.update()
            if self.rect.x < 730:
                if lista_teclas[pygame.K_RIGHT]:
                    self.rect.x += 5
                    disparo.update()
    
    def posicion_inicial(self):
        self.rect.centerx = 400
        self.rect.y = 700

