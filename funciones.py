import pygame
import colores
import  sqlite3



def conseguir_imagen(nombre_imagen,ancho,alto):
    imagen = pygame.image.load(nombre_imagen)
    imagen = pygame.transform.scale(imagen,(ancho,alto))
    return imagen

def mostrar_score(ventana,score_personaje):
        font = pygame.font.SysFont("Arial",50)
        texto = font.render("PUNTAJE: {0}".format(score_personaje),True,colores.WHITE)
        ventana.blit(texto,(0,0))   
    
def crear_tabla():
    with sqlite3.connect("record_scores.db") as conexion:
        try:
            sentencia = ''' create  table puntaje
            (
            id integer primary key autoincrement,
            usuario text,
            score integer
            )   
            '''
            conexion.execute(sentencia)
            print("Se creo la tabla de puntaje")                       
        except sqlite3.OperationalError:
            print("La tabla de puntos ya existe")

def comitear_tabla(usuario,score):
    with sqlite3.connect("record_scores.db") as conexion:
        try:
            conexion.execute("insert into puntaje(usuario,score) values (?,?)", (f"{usuario}",score))
            conexion.commit()# Actualiza los datos realmente en la tabla
        except:
            print("Error")

def obtener_score_ordenado():
    with sqlite3.connect("record_scores.db") as conexion:
        cursor=conexion.execute("SELECT * FROM puntaje ORDER BY score DESC;")
        lista_puntajes = []
    for fila in cursor: 
        #print(fila) 
        lista_puntajes.append(fila)
    return lista_puntajes