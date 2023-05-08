#* Escriba un programa que abra un archivo de texto pasado por argumento utilizando el modificador -f.
#* El programa deberá generar tantos procesos hijos como líneas tenga el archivo de texto.
#* El programa deberá enviarle, vía pipes (os.pipe()), cada línea del archivo a un hijo.
#* Cada hijo deberá invertir el orden de las letras de la línea recibida, y se lo enviará al proceso padre nuevamente,
#también usando os.pipe().
#* El proceso padre deberá esperar a que terminen todos los hijos, y mostrará por pantalla las líneas invertidas
#que recibió por pipe.
#* Debe manejar los errores.

#!/usr/bin/python3

import argparse
import os

parser = argparse.ArgumentParser(description = 'Invertir el orden de lineas recibidas')

parser.add_argument('-f','--file', help = 'Archivo que se lee')

args = parser.parse_args()

r, w = os.pipe()
r1, w1 = os.pipe()

todo = []

try:
    pid = os.fork()
    if pid > 0:
        with open(args.file) as f:
            content = f.read()
            lines = content
            for i in lines:
                os.write(w, i.encode())
            os.close(w)

    else:
        os.close(w)
        data = os.read(r, 1024)
        os.close(r)
        lines = data.decode().split('\n')
        for i in lines:
            pid2 = os.fork()
            if pid2 == 0:
                mirrored = i[::-1]
                todo.append(mirrored)
                os._exit(0)
                
            else:
                for i in todo:
                    os.close(r1)
                    os.write(w1, i.encode())
                    os.close(w1)

except FileNotFoundError:
    print('No se encontro el archivo', args.file)

while True:
        data = os.read(r1, 1024)
        if not data:
            break
        print(data)
