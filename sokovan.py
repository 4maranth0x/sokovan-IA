from funciones import leerMapa, busqueda_preferente_por_amplitud
def inicio():
  mapa = input("¿Qué nivel jugaré? ")
  with open(f"nivelesAqui/{mapa}.txt", "r") as file:
    content = file.readlines()
  matriz, estado_inicial, estado_meta, cajas_faltantes, cajas = leerMapa(content)
  return matriz, estado_inicial, estado_meta, cajas_faltantes, cajas

mapa, estado_inicial, estado_meta, caja_falta, caja_total = inicio()

class Estado:
    def __init__(self, jugador, cajas):
        self.jugador = jugador
        self.cajas = set(cajas)
        self.paredes = set((x, y) for x in range(len(mapa)) for y in range(len(mapa[0])) if mapa[x][y] == 1)
        self.cajas_ocupadas = set(cajas)
        self.cajas_faltantes = caja_falta
        self.es_meta = None
        
    def es_estado_meta(self):
        if self.es_meta is not None:
            return self.es_meta
        
        self.es_meta = len(self.cajas) == len(estado_meta) and self.cajas.issuperset(estado_meta)
        return self.es_meta
    
    def expandir(self):
        hijos = []
        for movimiento in ["U", "D", "L", "R"]:
            dx, dy = movimientos[movimiento]
            jugador_nuevo = (self.jugador[0] + dx, self.jugador[1] + dy)
            
            if jugador_nuevo in self.paredes:
                continue
            
            if jugador_nuevo in self.cajas_ocupadas:
                caja_nueva = (jugador_nuevo[0] + dx, jugador_nuevo[1] + dy)
                
                if caja_nueva in self.paredes or caja_nueva in self.cajas_ocupadas:
                    continue
                
                cajas_nuevas = self.cajas.copy()
                cajas_nuevas.remove(jugador_nuevo)
                cajas_nuevas.add(caja_nueva)
                hijos.append(Estado(jugador_nuevo, cajas_nuevas))
            else:
                hijos.append(Estado(jugador_nuevo, self.cajas))
                
        return hijos




# Creamos el estado inicial y el estado meta
jugador = estado_inicial[0]
cajas = set(tuple(c) for c in estado_inicial[1])
estado_inicial = Estado(jugador, cajas)
estado_meta = set(tuple(c) for c in estado_meta)

# Creamos un diccionario para los movimientos
movimientos = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}

# Ejecutamos la búsqueda
solucion = busqueda_preferente_por_amplitud(estado_inicial,64)

# Imprimimos la solución
if solucion:
    for movimiento in solucion:
        print(movimiento)
else:
    print("No se encontró solución.")

