import pygame
import colores
import random
import galaga_enemigos
import galaga_personaje
import galaga_disparo
import galaga_disparo_enemigo
#import sqlite3
from funciones import *

    
ANCHO_VENTANA = 800
ALTO_VENTANA = 800

pygame.init()
#-----------sonido--------------
pygame.mixer.init()
#pygame.mixer.music.set_volume(0)
sonido_disparo = pygame.mixer.Sound("disparo_laser.mp3")
sonido_fondo = pygame.mixer.Sound("undertale_sonido.mp3")
sonido_fondo.set_volume(0.01)
sonido_fondo.play(-1)

#-----------ventana------------------
ventana = pygame.display.set_mode((ANCHO_VENTANA,ALTO_VENTANA))
pygame.display.set_caption("juego de navesitas")

#-----------fondo inicio-------------
imagen_inicio = conseguir_imagen("fondo_inicio.jpg",800,800)

#-----------boton inicio-----------
imagen_boton = conseguir_imagen("boton_galaga.png",150,50)

#-----------texto para boton inicio------------------
imagen_jugar_boton = conseguir_imagen("jugar.png",150,50)
imagen_puntaje_boton = conseguir_imagen("puntaje.png",150,50)

#-------------flecha para atras---------------------
imagen_retroceder = conseguir_imagen("flecha_atras.png",120,50)

#-----------marco titulo-------------
imagen_marco_titulo = conseguir_imagen("marco_titulo.png",300,100)
imagen_titulo = conseguir_imagen("logo.png",250,100)
#-----------fondo juego--------------
imagen_fondo = conseguir_imagen("fondo_galaga.jpg",800,800)
y = 0
posicion_fondo = [0,y]

#----------imagen vida personaje---------------
vida_llena = conseguir_imagen("vida llena.png",50,50)
vida_vacia = conseguir_imagen("vida vacia.png",50,50)

#-----------imagen game over----------------
game_over_fondo = conseguir_imagen("fondo_fin_del_juego.jpg",800,800)
game_over_texto = conseguir_imagen("mensaje_fin_del_juego.png",300,200)

#-----------imagen puntos-------------------
fondo_puntaje = conseguir_imagen("puntaje_fondo.jpg",800,800) #el perro
fondo_del_fondo_puntaje = conseguir_imagen("puntaje_fondo_fondo.png",200,200) #el agujero que tapa el sol del perro
#-----------fps----------------
clock = pygame.time.Clock() #creo un objeto que ayuda a controlar el tiempo

#-----------sprite lista-------
all_lista_sprite = pygame.sprite.Group() #permite controlar un grupo de objetos de tipo sprite (aca guardo los sprites de mi nave, enemigos y disparos)
lista_enemigos = pygame.sprite.Group() #permite controlar objetos de tipo sprite (aca guardo el sprite de los enemigos)
lista_disparos = pygame.sprite.Group()
lista_disparos_enemigos = pygame.sprite.Group()

#-----------personaje----------
personaje = galaga_personaje.Personaje() #instanciamos la clase personaje
all_lista_sprite.add(personaje)

#-----------enemigos-----------
for i in range(35):
    enemigos = galaga_enemigos.Enemigos()
    lista_enemigos.add(enemigos)
    all_lista_sprite.add(enemigos)

enemigo_cooldown = 1000 #disparo coldown en milisegundos
ultimo_disparo_enemigo = pygame.time.get_ticks() #tiene un tiempo determinado al no estar en un while o for que haga aumentar su tiempo

#------------timer-------------
timer_segundos = pygame.USEREVENT #este es un evento que creo yo mismo
pygame.time.set_timer(timer_segundos,10)

#------------ingreso de texto-------------
font_input = pygame.font.SysFont("segoeuisemibold", 30) #obtengo la fuente que tendra la letra y su tamaño
usuario = ''

#-----------derrota-----------------
derrota = 0

#-----------menu,juego,puntos------------
opciones = 0

#-----------cronometro del juego, si llega a 0 termina el juego--------------
cantidad_vueltas_tiempo = 0 #cierta cantidad de vueltas sera un segundo (40 vueltas)
tiempo_de_juego = 120 #le voy restando 1 cada segundo

#----------variable para mostrar x tiempo la imagen de game over------------------
cantidad_vueltas_derrota = 0

#--------------lista puntaje--------------------
lista_puntaje = crear_tabla()


flag_correr = True
while flag_correr:
    lista_eventos = pygame.event.get()
    #-------------menu de inicio-----------------
    if opciones == 0:
            
        #-----------muestro el fondo-------------    
        ventana.blit(imagen_inicio,posicion_fondo)
        
        #-----------muestro el boton jugar--------------
        rect_jugar = pygame.draw.rect(ventana,colores.WHITE,(200,400,150,50)) #para la colision
        ventana.blit(imagen_boton,(200,400))
        ventana.blit(imagen_jugar_boton,(200,400))    
        
        #-----------muestro el boton puntaje------------
        rect_puntaje = pygame.draw.rect(ventana,colores.WHITE,(470,400,150,50)) #para la colision
        ventana.blit(imagen_boton,(470,400))
        ventana.blit(imagen_puntaje_boton,(470,400))
        
        #-----------muestro el titulo-------------
        ventana.blit(imagen_marco_titulo,(285,130))
        ventana.blit(imagen_titulo,(300,130))

        #-----------eventos-------------
        for evento in lista_eventos:
            if evento.type == pygame.QUIT:
                flag_correr = False

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if rect_jugar.collidepoint(evento.pos) and len(usuario) != 0: #el rect colisiona con la cordenada del mouse
                    opciones = 1
                    if derrota == 2:
                        personaje.vida = 3
                        personaje.score = 0
                        cantidad_vueltas_tiempo = 0
                        tiempo_de_juego = 120
                        personaje.posicion_inicial()
                        all_lista_sprite.remove(lista_disparos,lista_disparos_enemigos) #dejo de mostrar la lista de disparos
                        lista_disparos.empty() # vacio las listas para que no sean invisibles y colisionen igual
                        lista_disparos_enemigos.empty()# vacio las listas para que no sean invisibles y colisionen igual
                        
                        for enemigos in lista_enemigos:
                            enemigos.posicion_inicial()
                else:
                    print("ingrese un nombre antes de jugar")

                if rect_puntaje.collidepoint(evento.pos):    
                    opciones = 2
        
        #-------------colocar usuario------------------------             
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_BACKSPACE:
                    usuario = usuario[0:-1] #slice : comienza en el primer numero y termina en el segundo
                else:
                    if len(usuario)<13:
                        usuario += evento.unicode
        rect_usuario = pygame.Rect((800/2)-115, 500, 250,60)
        pygame.draw.rect(ventana, colores.WHITE, rect_usuario, 2)
        font_input_surface = font_input.render(usuario, True, colores.WHITE)
        ventana.blit(font_input_surface,(rect_usuario.x+20, rect_usuario.y+10))
    
    #------------------pantalla jugable-----------------    
    elif opciones == 1:
        for evento in lista_eventos:
            if evento.type == pygame.QUIT:
                flag_correr = False
                
            #------------------movimiento de los sprites----------------
            if evento.type == pygame.USEREVENT:
                if evento.type == timer_segundos:
                    all_lista_sprite.update()
        
            #----------------disparo del personaje----------------    
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                        disparo_actual = pygame.time.get_ticks()
                        if disparo_actual - personaje.ultimo_disparo > personaje.cadencia:
                            disparo = galaga_disparo.DisparoPersonaje()
                            disparo.rect.x = personaje.rect.x + 30
                            disparo.rect.y = personaje.rect.y - 20
                            all_lista_sprite.add(disparo)
                            lista_disparos.add(disparo)                    
                            sonido_disparo.set_volume(0.05)
                            sonido_disparo.play()
                            personaje.ultimo_disparo = disparo_actual

        #--------disparo y coldown del enemigo---------
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - enemigos.ultimo_disparo > enemigos.cadencia:
            enemigo_atacando = random.choice(lista_enemigos.sprites()) #elige un enemigo al azar para que sea el que ataque
            disparos_enemigos = galaga_disparo_enemigo.DisparoEnemigos(enemigo_atacando.rect.centerx,enemigo_atacando.rect.bottom) #bottom = abajo 
            all_lista_sprite.add(disparos_enemigos)
            lista_disparos_enemigos.add(disparos_enemigos)
            enemigos.ultimo_disparo = tiempo_actual #luego de que un enemigo dispare, el ultimo disparo pasa a ser el mas actual
        
        #-----------mostrar y mover fondo juego-------------------
        y_relativa = y % imagen_fondo.get_rect().height
        ventana.blit(imagen_fondo,(0,y_relativa - imagen_fondo.get_rect().height))
        if y_relativa < ALTO_VENTANA:
            ventana.blit(imagen_fondo,(0,y_relativa))
        y += 2 #va moviendo el fondo en la posicion y

        #-----------dibujar a mi personaje, enemigos y disparos-------------
        all_lista_sprite.draw(ventana)

        #-----------colision entre mi disparo y los enemigos-------------
        enemigo_hit_lista = pygame.sprite.groupcollide(lista_disparos,lista_enemigos,True,True)#comprueba si hubo colision entre las 2 listas
        for enemigos in enemigo_hit_lista:
            enemigos = galaga_enemigos.Enemigos()
            lista_enemigos.add(enemigos)
            all_lista_sprite.add(enemigos)
            personaje.score += 100
        
        #-------------------elimino mi disparo si se va de la pantalla-------------------
        for disparo in lista_disparos:
            if disparo.rect.y < -10: #si el disparo se va del limite, se lo remueve
                all_lista_sprite.remove(disparo)
                lista_disparos.remove(disparo)
        
        #------------barra de vida----------------------
        if personaje.vida == 3:
            ventana.blit(vida_llena,(0,740))
            ventana.blit(vida_llena,(40,740))
            ventana.blit(vida_llena,(80,740))
        if personaje.vida == 2:
            ventana.blit(vida_llena,(0,740))
            ventana.blit(vida_llena,(40,740))
            ventana.blit(vida_vacia,(80,740))
        if personaje.vida == 1:
            ventana.blit(vida_llena,(0,740))
            ventana.blit(vida_vacia,(40,740))
            ventana.blit(vida_vacia,(80,740))
        
        #-----------colicion entre un enemigo y el jugador------------
        enemigo_impactado = pygame.sprite.spritecollide(personaje,lista_enemigos,True) #si un enemigo me colpea, se elimina
        for enemigo in enemigo_impactado: #volviendo a crear al enemigo eliminado si es que me golpea
            enemigos = galaga_enemigos.Enemigos()
            lista_enemigos.add(enemigos)
            all_lista_sprite.add(enemigos)
            personaje.vida -= 1

        #----------colicion entre un disparo enemigo y el jugador---------
        personaje_disparado = pygame.sprite.spritecollide(personaje,lista_disparos_enemigos,True)
        if personaje_disparado:
            personaje.vida -= 1
        
        #----------mostrar el puntaje---------------------
        mostrar_score(ventana,personaje.score)
        
        #----------vida personaje---------------
        if personaje.vida == 0 or tiempo_de_juego == 0:
            derrota = 1

        #-----------cronometro-------------------------
        font = pygame.font.SysFont("Arial", 30)
        tiempo = font.render("TIEMPO: {0}".format(tiempo_de_juego),True,colores.WHITE)
        ventana.blit(tiempo,(0,40))

        cantidad_vueltas_tiempo += 1
        if cantidad_vueltas_tiempo == 40: #40 vueltas serian aprox 1 segundo (calculado a ojo)
            cantidad_vueltas_tiempo = 0
            tiempo_de_juego -= 1
        
        #---------game over-----------------
        if derrota == 1:
            all_lista_sprite.remove(lista_disparos) #al morir remuevo los disparos
            #-------------muestra el fondo al perder----------
            ventana.blit(game_over_fondo,(0,0))
            ventana.blit(game_over_texto,(250,100))
            #-----------muestra todas las vidas vacias--------------
            ventana.blit(vida_vacia,(0,740))
            ventana.blit(vida_vacia,(40,740))
            ventana.blit(vida_vacia,(80,740))
            #-------------el tiempo que se vera la imagen de game over-------------------
            cantidad_vueltas_derrota += 1
            if cantidad_vueltas_derrota == 120: #120 equivaldria a unos 3 segundos aprox
                subir_tabla(usuario,personaje.score)
                cantidad_vueltas_derrota = 0
                opciones = 0
                derrota = 2
                
    #-----------pantalla de puntuaciones-------------------            
    if opciones == 2:  
        i = 0
        solo_diez = 0
        rect_retroceder = pygame.draw.rect(ventana,colores.RED1,(0,46,120,50))
        ventana.blit(fondo_puntaje,(0,0))
        ventana.blit(fondo_del_fondo_puntaje,(290,220))
        ventana.blit(imagen_retroceder,(0,50))
        lista_puntaje = obtener_score_ordenado()
        for puntajes in lista_puntaje: 
            solo_diez += 1
            i += 50
            if solo_diez <= 10: #para que muestre a los 10 con puntaje mas alto
                #if len(puntajes[1]) > 0: #para mostrar los usuarios que no esten vacios
                font = pygame.font.SysFont("Arial",30)
                texto_score = font.render("Jugador: {0} | SCORE: {1}".format(puntajes[1],puntajes[2]),True,colores.WHITE)
                texto_titulo_score = font.render("TOP 10 MEJORES",True,colores.WHITE)
                ventana.blit(texto_score,(0,250 + i))
                ventana.blit(texto_titulo_score,(50,200))
                    
        for evento in lista_eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if rect_retroceder.collidepoint(evento.pos): 
                    opciones = 0



    pygame.display.flip()
    clock.tick(60)
    
    
    
pygame.quit()