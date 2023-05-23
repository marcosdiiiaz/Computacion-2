#Escriba un programa que abra un archvo de texto pasado por argumento utilizando el modificador -f.
#* El programa deberá generar tantos procesos hijos como líneas tenga el archivo de texto.
#* El programa deberá enviarle, vía pipes (os.pipe()), cada línea del archivo a un hijo.
#* Cada hijo deberá invertir el orden de las letras de la línea recibida, y se lo enviará al proceso padre nuevamente, 
# también usando os.pipe().
# El proceso padre deberá esperar a que terminen todos los hijos, y mostrará por pantalla las líneas invertidas que recibió por pipe.
#* Debe manejar los errores.

#!/usr/bin/python3

import os
import argparse

def invertir_lineas(file):
    r2, w2 = os.pipe()

    try:
        with open(file) as f:
            lines = f.readlines()

            for i in range(len(lines)):
                lines[i] = lines[i].rstrip('\n')

            for i in range(1, len(lines)):
                if '\n' not in lines[i]:
                    lines[i] += '\n'

        for line in lines:
            r1, w1 = os.pipe()
            pid = os.fork()
            if pid == 0:
                os.close(w1)
                data = os.read(r1, 1024)
                data_d = data.decode()[::-1]
                os.close(r1)
                os.close(r2)
                os.write(w2, data_d.encode())
                os.close(w2)
                exit(0)

            elif pid < 0:
                print('Error al hacer fork')
                exit(1)

            else:
                os.close(r1)
                os.write(w1, line.encode())
                os.close(w1)
                os.waitpid(pid, 0)

    except IOError:
        print(f'Error al abrir el archivo: {file}')

    os.close(w2)

    while True:
        data = os.read(r2, 1024)
        if not data:
            break
        print(data.decode())
    os.close(r2)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Invertir lineas')
    parser.add_argument('-f', '--file', help='Archivo a leer')
    args = parser.parse_args()
    file = args.file

    invertir_lineas(file)
