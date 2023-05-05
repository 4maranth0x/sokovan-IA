#Integrantes
# Maria Paula Giraldo. 2022411-3743
#Natalia Andrea Marin Hernandez. 2041622-3743
#Alejandro Lasso Medina. 2040393
# #

import sys
from collections import deque

#Identifica la tupla que representa la posición del jugador dentro de un archivo de texto y la retorna
def posicionJugador(content):
  jugadorPos = None
  for linea in content:
    if "W" not in linea:
      jugadorPos = tuple(map(int, linea.split(",")))
      break
  return jugadorPos

#Identifica las tuplas que representan la posición de las cajas dentro de un archivo de texto y las retornas
def posicionCajas(content):
  cajasPos = []
  i = 0
  while i < len(content) - 1:
    if "W" not in content[i]:
      cajaPos = tuple(map(int, content[i + 1].split(",")))
      cajasPos.append(cajaPos)
    i += 1
  return cajasPos

#Lee los carácteres dentro de un archivo de texto y los transcribe como una matriz para reprensentar el mapa
def leerMapa(content):
  contentM = [linea.strip() for linea in content]
  filas = len(contentM)
  columnas = max(len(linea) for linea in contentM)
  mapa = []
  cajasFaltantes = 0
  estadoInicial = []
  estadoMeta = []
  jugadorPos = posicionJugador(content)
  cajasPos = posicionCajas(content)
  if jugadorPos is None:
    sys.exit("no hay jugador")
  cajas = len(cajasPos)
  estadoInicial.append(jugadorPos)
  estadoInicial.append(cajasPos)
  for i in range(filas - (cajas + 1)):
    fila = []
    for j in range(columnas):
      if j >= len(contentM[i]):
        fila.append(1)  # fuera del mapa
      elif contentM[i][j] == 'W':
        fila.append(1)  # pared
      elif contentM[i][j] == '0':
        fila.append(0)  # camino
      elif contentM[i][j] == 'X':
        fila.append(2)  # objetivo
        cajasFaltantes += 1
        estadoMeta.append([i,j])
      else:
        fila.append(0)  # camino
    mapa.append(fila)
  return mapa, estadoInicial, estadoMeta, cajasFaltantes, cajas

#Realiza una búsqueda de los movimientos usados para hallar una solución mediante el algoritmo por BFS
def busquedaPreferentePorAmplitud(estadoInicial, profundidadMaxima):
    cola = deque([(estadoInicial, 0)])
    visitados = set()
    while cola:
        estadoActual, profundidadActual = cola.popleft()
        if estadoActual.esEstadoMeta():
            return estadoActual.solucion()
        if profundidadActual >= profundidadMaxima:
            continue
        for hijo in estadoActual.expandir():
            if hijo not in visitados:
                visitados.add(hijo)
                cola.append((hijo, profundidadActual + 1))
    return None