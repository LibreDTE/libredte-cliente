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
Comando para sincronizar documentos emitidos de manera local con el servidor de LibreDTE
@author Esteban De La Fuente Rubio, DeLaF (esteban[at]sasco.cl)
@version 2017-01-28
"""

# módulos usados
from base64 import b64encode, b64decode
from json import dumps as json_encode
import os
import codecs

# opciones en formato corto
options = 'v'

# opciones en formato largo
long_options = ['dir=']

# cliente de LibreDTE
LibreDTE = None

# verbose
verbose = False

# función principal del comando
def main(Cliente, args, config) :
    global LibreDTE
    global verbose
    dir, verbose = parseArgs(args)
    LibreDTE = Cliente
    if not dir or not os.path.isdir(dir) :
        print('Debes indicar un directorio (--dir) que se sincronizará con el servidor de LibreDTE')
        return 1
    archivos_xml = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f)) and f[-4:].lower()=='.xml']
    for xml in archivos_xml :
        enviarXML(dir, xml)
    return 0

# función que procesa los argumentos del comando
def parseArgs(args) :
    dir = None
    verbose = 0
    for var, val in args:
        if var == '--dir' :
            dir = val
        if var == '-v' :
            verbose = len(val)
    return dir, verbose

def enviarXML(dir_path, archivo_xml) :
    global LibreDTE
    global verbose
    xml = loadXML(dir_path+'/'+archivo_xml)
    xml_base64 = json_encode(b64encode(bytes(xml, 'iso-8859-1')).decode('iso-8859-1'))
    cargar = LibreDTE.post('/dte/dte_emitidos/cargar_xml', xml_base64)
    if cargar.status_code!=200 :
        print('Error al cargar el XML '+archivo_xml+': '+json_encode(cargar.json()))
        return cargar.status_code
    elif verbose :
        print('Archivo XML '+archivo_xml+' fue cargado con éxito')

# función que carga un XML
def loadXML (archivo_xml) :
    datos_xml = ''
    fd = codecs.open(archivo_xml, 'r', 'iso-8859-1')
    for linea in fd :
        datos_xml += linea
    fd.close()
    return datos_xml
