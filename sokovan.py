#Integrantes
# Maria Paula Giraldo. 2022411-3743
#Natalia Andrea Marin Hernandez. 2041622-3743
#Alejandro Lasso Medina. 2040393
# #

from funciones import leerMapa, busquedaPreferentePorAmplitud, busquedaProfundidad, busquedaProfundidadIterativa

#Inicia el programa, recibe un archivo de texto y retorna el mapa, la posición del jugador, 
#la posición de las cajas, el número de cajas faltantes y el número de cajas.
def inicio():
  mapa = input("¿Qué nivel jugaré? ")
  with open(f"nivelesAqui/{mapa}.txt", "r") as file:
    content = file.readlines()
  matriz, estadoInicial, estadoMeta, cajasFaltantes, cajas = leerMapa(content)
  return matriz, estadoInicial, estadoMeta, cajasFaltantes, cajas

mapa, estadoInicial, estadoMeta, cajaFalta, cajaTotal = inicio()

#Clase que identifica y desarrolla el estado del juego
class Estado:
    def __init__(self, jugador, cajas):
        self.jugador = jugador
        self.cajas = set(cajas)
        self.paredes = set((x, y) for x in range(len(mapa)) for y in range(len(mapa[0])) if mapa[x][y] == 1)
        self.cajasOcupadas = set(cajas)
        self.cajasFaltantes = cajaFalta
        self.esMeta = None
        
    #Identifica si el estado actual es meta o no
    def esEstadoMeta(self):
        if self.esMeta is not None:
            return self.esMeta  
        self.esMeta = len(self.cajas) == len(estadoMeta) and self.cajas.issuperset(estadoMeta)
        return self.esMeta
    #Expande las casillas aledañas a la posición del jugador
    def expandir(self):
        hijos = []
        for movimiento in ["U", "D", "L", "R"]:
            dx, dy = movimientos[movimiento]
            jugadorNuevo = (self.jugador[0] + dx, self.jugador[1] + dy)
            if jugadorNuevo in self.paredes:
                continue
            if jugadorNuevo in self.cajasOcupadas:
                cajaNueva = (jugadorNuevo[0] + dx, jugadorNuevo[1] + dy)
                if cajaNueva in self.paredes or cajaNueva in self.cajasOcupadas:
                    continue
                cajasNuevas = self.cajas.copy()
                cajasNuevas.remove(jugadorNuevo)
                cajasNuevas.add(cajaNueva)
                hijos.append(Estado(jugadorNuevo, cajasNuevas))
            else:
                hijos.append(Estado(jugadorNuevo, self.cajas))         
        return hijos
#Se crea el estado inicial y el estado meta
jugador = estadoInicial[0]
cajas = set(tuple(c) for c in estadoInicial[1])
estadoInicial = Estado(jugador, cajas)
estadoMeta = set(tuple(c) for c in estadoMeta)

#Diccionario para los movimientos
movimientos = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}
#Imprime la solución generada por el algorítmo BFS
solucionAmplitud = busquedaPreferentePorAmplitud(estadoInicial,64)
if solucionAmplitud:
    for movimiento in solucionAmplitud:
        print(movimiento)
else:
    print("No se encontró solución.")
#Imprime la solución generada por el algorítmo DFS
solucionProfundidad = busquedaProfundidad(estadoInicial,64)
if solucionProfundidad:
    for movimiento in solucionProfundidad:
        print(movimiento)
else:
    print("No se encontró solución.")
#Imprime la solución generada por el algorítmo IDDFS
solucionIterativa = busquedaProfundidadIterativa(estadoInicial,64)
if solucionIterativa:
    for movimiento in solucionIterativa:
        print(movimiento)
else:
    print("No se encontró solución.")
