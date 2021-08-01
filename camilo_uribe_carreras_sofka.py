# Reto técnico Sofka U - Carreras de dados desde la consola
# Presentado por Camilo Uribe Vargas

import os
import json
try:
    from tabulate import tabulate
except ImportError:
    print("""Por favor instala el paquete "tabulate" para presentar los resultados:  pip install tabulate""")
    quit()
import random

#La clase carrera recibe el número de jugadores,
# guarda la lista de carros que compiten y contiene los rankings 

class Carrera():
    def __init__(self, jugadores):
        self.jugadores = jugadores
        self.lista_carros = []
        self.rankings = carga_rankings()

#El método inicio_carrera genera un objeto pista y un objeto carro por cada participante.
    def inicio_carrera(self):
        self.pista = Pista(input("Longitud de la pista en metros: "))

        for i in range(0,int(self.jugadores)):
            nombre_piloto=input("Nombre del piloto {}: ".format(i+1))
            nuevo_carro = Carro(nombre_piloto, i, self.rankings) 
            self.lista_carros.append(nuevo_carro) 
            print(self.lista_carros[i])
        

# Inician los turnos. Mientras el carro no halla completado la pista, sigue compitiendo.
#  Una vez halla completado la pista el último carro, se termina la carrera.
# 
        while self.pista.carrera_en_curso:
            for carro in self.lista_carros: 
                if carro.porcentaje_avance < 100: 
                    carro.avance()
                elif carro.porcentaje_avance >= 100 and carro.posicion == len(self.lista_carros): 
                    self.pista.finalizar_carrera()
                    break
                else:
                    continue                 
        actualiza_tabla_resultados()    

        self.premiacion()  
        
#La función actualizar posiciones recibe una lista con los resultados parciales ordenada 
# por distancia recorrida y asigna la posición al índice en la lista. (El carro con mayor distancia recorrida será el primero en la carrera)
    def actualizar_posiciones(self, resultados_parciales):
        for elemento in resultados_parciales:
            for carro in self.lista_carros:
                if carro.piloto == elemento[1]:
                    carro.posicion = resultados_parciales.index(elemento)+1
                    elemento.insert(0,carro.posicion)
        return resultados_parciales
           
# ULa función premiación se invoca cuando se termina la carrera y genera un objeto de la clase Podio,
#  que recibe la lista de carros con sus propiedades actualizadas             
    def premiacion(self):
        self.podio = Podio(self.lista_carros)
        self.podio.llenar_podio()

            
      
#La clase pista tiene como propiedades la longitud y una función para marcar cuando ha terminado la carrera, 
# que se activa cuando llega el tercer carro a la meta 
class Pista():
    def __init__(self, longitud_pista):
        self.longitud = int(longitud_pista)
        self.carrera_en_curso = True

    def finalizar_carrera(self):
        self.carrera_en_curso = False
       

#La clase carro es la principal, y sus instancias representan a cada jugador. Tiene propiedades piloto(nombre), carril de salida, 
#posicion actual, distancia recorrida, porcentaje de avance y victorias de carreras anteriores.
class Carro():
    def __init__(self, nombre_piloto,ID, rankings):
        self.distancia_recorrida = 0
        self.piloto = nombre_piloto
        self.carril = ID+1
        self.posicion = self.carril
        self.porcentaje_avance= 0
        self.avance_turno= 0
        self.victorias = self.chequear_victorias(rankings)
        
        
    def __str__(self): 
        return "{} saldrá en el carril {}".format(self.piloto, self.carril) 
 
 #La función chequear_victorias revisa el historial de los rankings para ver cuantas carreras ha ganado el jugador anteriormente
    def chequear_victorias(self, rankings):
        victorias = 0
        for campeon in rankings:
            if self.piloto in campeon:
                victorias = campeon[1]   
        return victorias

# La función avance espera que el jugador presione la tecla enter para lanzar un dado y determinar su movimiento en el turno aleatoriamente.
# Esta funcion actualiza la distancia recorrida y el porcentaje de avance. Adicionalmente, avisa si el carro cruzó la línea de meta.

    def avance(self):
        print("--------------------------")
        print(r"""       .-------.    ______
      /   o   /|   /\     \
     /_______/o|  /o \  o  \
     | o     | | /   o\_____\
     |   o   |o/ \o   /o    /
     |     o |/   \ o/  o  /
     '-------'     \/____o/""")
        tirar_dados = input("{}: presiona enter para tirar el dado, buena suerte!!! ".format(self.piloto))
        self.avance_turno = random.randint(1, 6)*100
        self.distancia_recorrida += self.avance_turno       
        self.porcentaje_avance = round(self.distancia_recorrida*100/nueva_carrera.pista.longitud, 1)
        actualiza_tabla_resultados()        

        if self.porcentaje_avance >= 100 :
            
            cls()
            print()
            print(r"""{} ___
    _-_-  _/\______\\__
 _-_-__  / ,-. -|-  ,-.`-.
     _-_- `( o )----( o )-'
           `-'      `-'""".format(self.piloto.upper()))
            print("{} HA CRUZADO LA META!!!!!!!!! ".format(self.piloto.upper()))
            print()
        print("{} ha avanzado {}m".format(self.piloto, self.avance_turno))

#   Dado que las posiciones se obtienen al comparar las distancias recorridas,
#  inmediatamente llegan los carros a la meta se les asignan distancias recorridas diferentes de acuerdo a su posicion,
#  para evitar sobrepasos a posiciones establecidas en el podio.

        if self.porcentaje_avance >= 100 and self.posicion == 1:
            self.distancia_recorrida = float('inf')
        if self.porcentaje_avance >= 100 and self.posicion == 2:
            self.distancia_recorrida = 10e4

#La clase podio recibe la lista de carros una vez ha terminado la carrera.        

class Podio():
    def __init__(self, lista_carros):
        self.lista_carros = lista_carros
        self.primer_lugar = None
        self.segundo_lugar = None
        self.tercer_lugar = None  
        
#La función llenar_podio es inmediatamente invocada, y asigna los lugares del podio de acuerdo a la posicion de llegada.
    def llenar_podio(self):
        for carro in self.lista_carros:
            if carro.posicion == 1:
                self.primer_lugar = carro.piloto
                carro.victorias += 1
            elif carro.posicion == 2 :
                self.segundo_lugar = carro.piloto
            elif carro.posicion == 3 :
                self.tercer_lugar = carro.piloto
        actualiza_tabla_resultados()
        print("""
        """)
        print("         2.{} 1.{} 3.{}".format(self.segundo_lugar, self.primer_lugar, self.tercer_lugar))
        print(r"""                            
                   @-----@
                   |  @  |
            @-----@|  |  |
            |  @  ||  |  |  
            |  |  ||  |  |@-----@
            |  |  ||  |  ||  @  |""")
        guarda_rankings(nueva_carrera.rankings, self.primer_lugar)
        quit()
    

# La función actualiza_tabla_resultados es invocada después de cada turno,
# toma información de cada carro y la organiza para presentar las posiciones parciales de la carrera.

def actualiza_tabla_resultados(): 
    resultados_parciales = []
    for carro in nueva_carrera.lista_carros:
        info_carro_actualizada = [carro.carril, carro.piloto, carro.distancia_recorrida, "{}%".format(carro.porcentaje_avance), carro.victorias]
        resultados_parciales.append(info_carro_actualizada)
        
    cls()
    resultados_parciales = nueva_carrera.actualizar_posiciones(sorted(resultados_parciales, key = lambda x: x[2], reverse=True)) # Organiza los carros de acuerdo a la distancia recorrida, en orden descendente
    print()
    print(tabulate(resultados_parciales, headers=['Posicion','Carril', 'Piloto', 'Distancia recorrida [m]', 'Porcentaje de avance', 'Victorias'], tablefmt='orgtbl'))


#La función carga_rankings lee victorias anteriores desde un archivo JSON en el directorio. 
# Si el archivo no existe, se crea uno nuevo.

def carga_rankings():
    try:
        with open('rankings.json', 'r') as archivo:
            rankings = json.load(archivo)  
    except FileNotFoundError:
        return []  # Si no existe el archivo, retorna una lista vacía
    return rankings

# La funcion guarda rankings toma los resultados de esta carrera y 
# los escribe en el archivo rankings como una lista de dos elementos (piloto y victorias)

def guarda_rankings(rankings, ganador):
    repite_campeonato = False
    for elemento in rankings:
        if ganador in elemento:
            elemento[1] += 1
            repite_campeonato = True
    if not repite_campeonato:
        rankings.append([ganador, 1]) 
    
    with open('rankings.json', 'w') as archivo:
        json.dump(rankings, archivo)  # Write the list to the json file


def cls():  # Limpia la consola tras cada actualización de la tabla de resultados
    os.system('cls' if os.name=='nt' else 'clear')



if __name__=="__main__":
    
    while True: 
        
        inicio_juego = input('¿Deseas iniciar una carrera?  (y/n): ') 
        primera_letra = inicio_juego[0].lower() 

        if inicio_juego == '' or not primera_letra in ['y','n']: 
            print('Por favor decide si quieres iniciar una carrera (y/n): ') 
        else: 
            break 
if primera_letra == 'y': 
    numero_jugadores = input("Ingresa el número de jugadores: ")
    nueva_carrera = Carrera(numero_jugadores)
    
    if nueva_carrera.jugadores == '0' :
        print("No puede haber carrera con 0 pilotos" )
        quit()
    else:
        nueva_carrera.inicio_carrera()
if primera_letra == 'n': 
    print("Cuando quieras jugar me avisas!!!!!" )
    quit()
   
    