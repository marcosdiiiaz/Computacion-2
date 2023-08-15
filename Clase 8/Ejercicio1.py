
######################

import argparse

parser = argparse.ArgumentParser(description = 'Segmento de memoria compartida.')
parser.add_argument('-f', '--file', help='Ruta del archivo', required = True)
args = parser.parse_args()

