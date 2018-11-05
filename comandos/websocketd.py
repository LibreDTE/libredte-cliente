# -*- coding: utf-8 -*-

"""
LibreDTE
Copyright (C) SASCO SpA (https://sasco.cl)

Este programa es software libre: usted puede redistribuirlo y/o modificarlo bajo
los términos de la Licencia Pública General Affero de GNU publicada por la
Fundación para el Software Libre, ya sea la versión 3 de la Licencia, o (a su
elección) cualquier versión posterior de la misma.

Este programa se distribuye con la esperanza de que sea útil, pero SIN GARANTÍA
ALGUNA; ni siquiera la garantía implícita MERCANTIL o de APTITUD PARA UN
PROPÓSITO DETERMINADO. Consulte los detalles de la Licencia Pública General
Affero de GNU para obtener una información más detallada.

Debería haber recibido una copia de la Licencia Pública General Affero de GNU
junto a este programa.
En caso contrario, consulte <http://www.gnu.org/licenses/agpl.html>.
"""

"""
Comando para crear un servidor de websockets para procesar solicitudes desde
la aplicación web en el computador local.

Esto permite, por ejemplo, enviar a imprimir desde la aplicación web
directamente a una impresora conectada en la red local o una impresora del
sistema. Para la impresión está soportado el caso de imprimir con ESCPOS o el
PDF del DTE.

@author Esteban De La Fuente Rubio, DeLaF (esteban[at]sasco.cl)
@version 2018-11-04
"""

# módulos usados
import asyncio
import websockets
import functools
import json
import socket
import zipfile
import io
import os, os.path
from datetime import datetime
import subprocess

# opciones en formato largo
long_options = ['printer_type=', 'printer_host=', 'printer_port=']

# función principal del comando
def main(Cliente, args, config) :
    printer_type, printer_host, printer_port = parseArgs(args)
    try :
        server = websockets.serve(
            functools.partial(
                on_message,
                printer_type = printer_type,
                printer_host = printer_host,
                printer_port = printer_port
            ),
            'localhost',
            2186
        )
        asyncio.get_event_loop().run_until_complete(server)
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt :
        print()
        return 1
    return 0

# función que procesa los argumentos del comando
def parseArgs(args) :
    printer_type = 'network'
    printer_host = '127.0.0.1'
    printer_port = 9100
    for var, val in args:
        if var == '--printer_type' :
            printer_type = val
        elif var == '--printer_host' :
            printer_host = val
        elif var == '--printer_port' :
            printer_port = val
    return printer_type, printer_host, printer_port


# función que se ejecuta cuando el websocket recibe un mensaje
@asyncio.coroutine
def on_message(websocket, path, printer_type, printer_host, printer_port):
    # verificar las partes pasadas al script
    # al menos se debe pasar una acción que es la que se está realizando
    parts = path.split('/')
    if len(parts) < 2 or parts[1] == '':
        yield from websocket.send(json.dumps({
            'status': 1,
            'message': 'Falta indicar la acción que se realizará en el websocket'
        }))
        return 1
    message = yield from websocket.recv()
    # procesar impresión
    if parts[1] == 'print' :
        # obtener formato de impresión
        try:
            formato = parts[2]
        except IndexError:
            formato = 'escpos'
        # obtener datos del archivo para impresión
        z = zipfile.ZipFile(io.BytesIO(message))
        datos = z.read(z.infolist()[0])
        # opciones para impresión con ESCPOS
        if formato == 'escpos' :
            if printer_type == 'network' :
                try :
                    print_network(printer_host, printer_port, datos)
                except (ConnectionRefusedError, OSError) as e:
                    yield from websocket.send(json.dumps({
                        'status': 1,
                        'message': 'No fue posible imprimir en ' + printer_host + ':' + str(printer_port) + ' (' + str(e) + ')'
                    }))
                    return 1
            else :
                yield from websocket.send(json.dumps({
                    'status': 1,
                    'message': 'Tipo de impresora ' + printer_type + ' no soportada con formato ' + formato
                }))
                return 1
        # opciones para impresión usando el PDF
        elif formato == 'pdf' :
            if printer_type == 'network' :
                try :
                    print_network(printer_host, printer_port, datos)
                except (ConnectionRefusedError, OSError) as e:
                    yield from websocket.send(json.dumps({
                        'status': 1,
                        'message': 'No fue posible imprimir en ' + printer_host + ':' + str(printer_port) + ' (' + str(e) + ')'
                    }))
                    return 1
            elif printer_type == 'system' :
                # directorio principal y temporal
                cmd_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
                if not os.path.exists(cmd_dir+"/tmp") :
                    os.makedirs(cmd_dir+"/tmp")
                # crear archivo temporal con el PDF
                dt = datetime.now()
                ms = (dt.day * 24 * 60 * 60 + dt.second) * 1000 + dt.microsecond / 1000.0
                pdf_file = cmd_dir+"/tmp/dte_"+str(ms)+".pdf"
                with open(pdf_file, 'wb') as f:
                    f.write(datos)
                # armar comando a ejecutar
                if os.name == 'posix':
                    cmd = "python3"
                elif os.name == 'nt' :
                    cmd = "python.exe"
                cmd += " "+cmd_dir+"/libredte-cliente.py imprimir"
                cmd += " --pdf="+pdf_file
                # ejecutar comando que imprime usando el cliente de LibreDTE
                try :
                    subprocess.check_output(cmd.split(" "))
                except subprocess.CalledProcessError as e :
                    yield from websocket.send(json.dumps({
                        'status': 1,
                        'message': 'No fue posible imprimir en la impresora local (' + str(e) + ')'
                    }))
                    return 1
                # quitar archivo temporal del PDF
                os.remove(pdf_file)
            else :
                yield from websocket.send(json.dumps({
                    'status': 1,
                    'message': 'Tipo de impresora ' + printer_type + ' no soportada con formato ' + formato
                }))
                return 1
        else :
            yield from websocket.send(json.dumps({
                'status': 1,
                'message': 'Formato ' + formato + ' no soportado'
            }))
            return 1
    # todo ok
    return 0

# función que realiza la impresión en una impresora de red
def print_network(host, port, data) :
    printer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    printer_socket.connect((host, port))
    printer_socket.send(data)
    printer_socket.shutdown(0)
    printer_socket.close()
