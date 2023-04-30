#!/bin/bash

# Instala make (sólo para sistemas que no lo tengan instalado)
if ! command -v make &> /dev/null
then
    echo "make no está instalado en tu sistema. Instalando make..."
    sudo apt-get update
    sudo apt-get install make
fi

# Instala pipenv (sólo para sistemas que no lo tengan instalado)
if ! command -v pipenv &> /dev/null
then
    echo "pipenv no está instalado en tu sistema. Instalando pipenv..."
    sudo apt-get update
    sudo apt-get install pipenv
fi

# Instala las dependencias
pipenv install

# Ejecuta el programa
pipenv run python sokovan.py