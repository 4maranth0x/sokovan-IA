import os

#Lee el mapa que se le entrega en el input y lo asume como mapa
def leerMapa():    
    mapa = input("¿Qué nivel jugaré?")
    nivel_ruta = os.path.join("nivelesAqui", mapa)
    with open(f"nivelesAqui/{mapa}.txt", "r") as file:
        content = file.readlines()
    content = [linea.strip().split() for linea in content]
    return content

nivel = leerMapa()
print(nivel)