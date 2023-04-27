import argparse
import sys

parser = argparse.ArgumentParser(description = 'Contar palabras, lineas del archivo y imprimir longitud promedio de las palabras') 

parser.add_argument('file', help = 'Es el archivo a leer')
parser.add_argument('average',nargs = '?', help = 'Promedio de longitud de palabras')

args = parser.parse_args()

try:
    with open(args.file) as f:
        contenido = f.read()
        words_quantity = len(contenido.split())
        print('La cantidad de palabras es: ',words_quantity)
    
    with open(args.file) as c:
        total_lines = sum(1 for line in c)
        print('La cantidad de filas es: ',total_lines)

except FileNotFoundError:
    sys.stderr = open("errors.log","a")
    print('El archivo', args.file, 'no existe', file = sys.stderr)

if args.average:
    words = contenido.split()
    word_lengths = [len(word) for word in words]
    average_length = sum(word_lengths) / len(words)
    print('El promedio de longitud de palabras es: ', average_length) 

