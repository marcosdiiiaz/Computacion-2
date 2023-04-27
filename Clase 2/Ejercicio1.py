import argparse
import os

parser = argparse.ArgumentParser(description = 'Padre: Calcular raiz cuadrada positiva - Hijo: Calcular raiz raiz cuadrada negativa')

parser.add_argument('-n', type = int, help = 'Tiene que ser un numero')
parser.add_argument()

args = parser.parse_args()
