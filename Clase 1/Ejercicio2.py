#!/usr/bin/python3

import argparse

parser = argparse.ArgumentParser(description='Repetidor de cadenas de texto n veces')

parser.add_argument('-t','--texto', help='La cadena de texto a repetir', type=str)
parser.add_argument('-n','--numero', help='El número de veces que se debe repetir el texto', type=int)

args = parser.parse_args()

for i in range(args.numero):
    print(args.texto)
