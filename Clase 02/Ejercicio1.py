#!/usr/bin/python3
import argparse

argpar = argparse.ArgumentParser(description = 'Generador de números impares')

argpar.add_argument('n', type=int, help = 'Debe ser un número entero positivo')

args = argpar.parse_args()

if args.n <= 0:
    print('n debe ser un número entero positivo')
else:
    for i in range(1,args.n):
        if i % 2 != 0:
            print (i)
