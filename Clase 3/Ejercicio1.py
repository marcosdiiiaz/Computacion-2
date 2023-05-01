#PIPES
#Escribir un programa en Python que comunique dos procesos. 
#El proceso padre deberá leer un archivo de texto y enviar cada línea del archivo al proceso hijo a través de un pipe. 
#El proceso hijo deberá recibir las líneas del archivo y, por cada una de ellas, contar la cantidad de palabras 
#que contiene y mostrar ese número.
#2- Verificar si es posible que dos procesos hijos (o nieto) lean el PIPE del padre.
#3- Verificar si el PIPE sigue existiendo cuendo el padre muere (termina el proceso), cuando el hijo muere [o cuendo mueren ambos]
#$ ls -l /proc/[pid]/fd/

#!/usr/bin/python3

import argparse
import os
import multiprocessing

parser = argparse.ArgumentParser(description='Proceso padre lee .txt y Proceso hijo lo recibe, y cuenta cantidad de palabras')

parser.add_argument('file', help = 'Archivo .txt a leer', type = str)
#parser.add_argument('-n', help = 'Cantidad de palabras por linea', type = int)

args = parser.parse_args()

pid = os.fork()

padre_conn, hijo_conn = multiprocessing.Pipe()

if pid > 0:
    with open(args.file) as f:
        contenido = f.read()
        for i in contenido:
            padre_conn.send(i)

else:
    


