def busqueda_profundidad(estado_inicial, acciones_aplicables, aplica, objetivo, max_niveles=64):
    frontera = [(estado_inicial, [])]
    visitados = set()
    num_niveles = 0
    while frontera and num_niveles < max_niveles:
        estado, camino = frontera.pop()
        if estado in visitados:
            continue
        visitados.add(estado)
        if objetivo(estado):
            return camino
        if num_niveles >= 10 and len(camino) >= num_niveles:
            continue
        for accion in acciones_aplicables(estado):
            if aplica(estado, accion):
                nuevo_estado = aplica(estado, accion)
                nuevo_camino = camino + [accion]
                frontera.append((nuevo_estado, nuevo_camino))
        num_niveles += 1
    return None

def busqueda_amplitud(estado_inicial, acciones_aplicables, aplica, objetivo, max_niveles=64):
    frontera = [(estado_inicial, [])]
    visitados = set()
    num_niveles = 0
    while frontera and num_niveles < max_niveles:
        estado, camino = frontera.pop(0)
        if estado in visitados:
            continue
        visitados.add(estado)
        if objetivo(estado):
            return camino
        if num_niveles >= 10 and len(camino) >= num_niveles:
            continue
        for accion in acciones_aplicables(estado):
            if aplica(estado, accion):
                nuevo_estado = aplica(estado, accion)
                nuevo_camino = camino + [accion]
                frontera.append((nuevo_estado, nuevo_camino))
        num_niveles += 1
    return None

def busqueda_profundidad_iterativa(estado_inicial, acciones_aplicables, aplica, objetivo, max_niveles=64):
    for num_niveles in range(10, max_niveles):
        resultado = busqueda_profundidad(estado_inicial, acciones_aplicables, aplica, objetivo, num_niveles)
        if resultado is not None:
            return resultado
    return None