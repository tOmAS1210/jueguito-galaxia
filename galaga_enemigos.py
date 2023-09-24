import pygame
import colores
import random
import galaga_personaje
import galaga_disparo
disparo = galaga_disparo.DisparoPersonaje()

#-----------enemigos-----------
class Enemigos(pygame.sprite.Sprite): #clase para objetos de juego visibles 
    def __init__(self):
        super().__init__()
        nave = ["images/nave_enemiga.png","images/nave_enemiga_2.png"]
        self.image = pygame.image.load(random.choice(nave))
        self.image = pygame.transform.scale(self.image,(70,70))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0,740,85)
        self.rect.y = random.randrange(-1000,-100,85)
        self.visible = True
        self.velocidady = random.randint(1,3)
        self.velocidadx = random.randrange(-2,3)
        
        self.cadencia = 600 #disparo coldown en milisegundos
        self.ultimo_disparo = pygame.time.get_ticks() #tiene un tiempo determinado al no estar en un while o for que haga aumentar su tiempo

    def update(self):
        self.rect.y += self.velocidady
        disparo.update()
        if self.rect.y > 0:
            self.rect.x += self.velocidadx
        if self.rect.y > 800 or self.rect.left < -50 or self.rect.right > 850:
            self.rect.x = random.randrange(0,740,85)
            self.rect.y = random.randrange(-1000,-100,85)
    
    def posicion_inicial(self):
        self.rect.x = random.randrange(0,740,85)
        self.rect.y = random.randrange(-1000,-100,85)