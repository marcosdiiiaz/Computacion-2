import argparse
import io
import multiprocessing
import socket
from PIL import Image

def convertir_a_grises(datos_imagen):
    imagen = Image.open(io.BytesIO(datos_imagen)).convert('L')
    return imagen

def proceso_hijo(tuberia, evento):
    while True:
        datos_imagen = tuberia.recv()
        if datos_imagen == b'exit':
            break

        imagen_gris = convertir_a_grises(datos_imagen)

        with io.BytesIO() as salida:
            imagen_gris.save(salida, format="JPEG")
            datos_grises = salida.getvalue()

        tuberia.send(datos_grises)
        evento.set()

def gestionar_conexion(socket_cliente, tuberia_hijo, evento):
    try:
        direccion_cliente = socket_cliente.getpeername()
        print(f'Conexion desde {direccion_cliente}')

        datos = b''
        while True:
            pedazo = socket_cliente.recv(1024)
            if not pedazo:
                break
            datos += pedazo

            if b'\xFF\xD9' in datos:
                break

        lineas_peticion = datos.split(b'\r\n')
        metodo = lineas_peticion[0].split(b' ')

        procesar_peticion(metodo, datos, socket_cliente, tuberia_hijo, evento)

    finally:
        socket_cliente.close()

def procesar_peticion(metodo, datos, socket_cliente, tuberia_hijo, evento):
    try:
        if metodo[0] == b'POST':
            print(f'Peticion POST recibida. Convirtiendo a escala de grises...')

            idx_inicio = datos.find(b'\r\n\r\n') + 4
            idx_fin = datos.rfind(b'\xFF\xD9') + 2

            datos_imagen = datos[idx_inicio:idx_fin]

            tuberia_hijo.send(datos_imagen)

            evento.wait()

            datos_grises = tuberia_hijo.recv()

            evento.clear()

            respuesta = f'HTTP/1.1 200 OK\r\nContent-Length: {len(datos_grises)}\r\n\r\n'.encode('utf-8')
            socket_cliente.sendall(respuesta + datos_grises)

            print('Imagen en escala de grises enviada al cliente.')

    except Exception as e:
        print(str(e))
        respuesta = b'HTTP/1.1 405 Metodo No Permitido\r\nContent-Length: 22\r\n\r\n'
        mensaje_error = b'Peticion rechazada por el servidor\n'
        socket_cliente.sendall(respuesta + mensaje_error)

def iniciar_servidor(ip, puerto):

    if ':' in ip:
        socket_servidor = socket.create_server((ip, puerto), family=socket.AF_INET6, dualstack_ipv6=True)
    else:
        socket_servidor = socket.create_server((ip, puerto))

    evento_conversion = multiprocessing.Event()

    print(f'Servidor iniciando en {socket_servidor.getsockname()}')

    while True:
        print('Esperando una conexion...')
        socket_cliente, _ = socket_servidor.accept()

        tuberia_hijo, tuberia_padre = multiprocessing.Pipe()
        proceso_procesamiento_imagen = multiprocessing.Process(
            target=proceso_hijo, args=(tuberia_hijo, evento_conversion))
        proceso_procesamiento_imagen.start()

        gestionar_conexion(socket_cliente, tuberia_padre, evento_conversion)

        tuberia_padre.send(b'exit')
        proceso_procesamiento_imagen.join()

if __name__ == '__main__':
    argumentos = argparse.ArgumentParser(description='Tp2 - procesa imagenes')
    argumentos.add_argument('-i', '--ip', default='::', help='Direccion de escucha')
    argumentos.add_argument('-p', '--port', type=int, default=8080, help='Puerto de escucha')

    args = argumentos.parse_args()
    
    try:
        iniciar_servidor(args.ip, args.port)
    except KeyboardInterrupt:
        print('Servidor detenido.')
