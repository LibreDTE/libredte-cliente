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
Comando para generar un DTE a partir de los datos de JSON o un XML
@author Esteban De La Fuente Rubio, DeLaF (esteban[at]sasco.cl)
@version 2016-06-25
"""

# módulos usados
from base64 import b64encode, b64decode
import os
from json import dumps as json_encode
from json import loads as json_decode
import codecs

# opciones en formato corto
options = ''

# opciones en formato largo
long_options = ['json=', 'xml=', 'archivo=', 'formato=', 'cedible=', 'papel=', 'web=', 'dir=', 'normalizar=', 'getXML']

# función principal del comando
def main(Cliente, args) :
    json, xml, archivo, formato, cedible, papel, web, dir, normalizar, getXML = parseArgs(args)
    data = None
    if json :
        data = loadJSON(json)
        formato = 'json'
    if xml :
        data = loadXML(xml)
        formato = 'xml'
    if archivo != None and formato != None and formato not in ('json', 'xml') :
        data = '"'+b64encode(bytes(loadFile(archivo), 'UTF8')).decode('UTF8')+'"'
    if data == None :
        print('Debe especificar un archivo JSON o bien un archivo XML a enviar')
        return 1
    if not dir :
        print('Debe especificar un directorio de salida para los archivos a generar')
        return 1
    # crear directorio para archivos si no existe
    if not os.path.exists(dir):
        os.makedirs(dir)
    # crear DTE temporal
    emitir = Cliente.post('/dte/documentos/emitir?normalizar='+str(normalizar)+'&formato='+formato, data)
    if emitir.status_code!=200 :
        print('Error al emitir DTE temporal: '+json_encode(emitir.json()))
        return emitir.status_code
    with open(dir+'/temporal.json', 'w') as f:
        f.write(json_encode(emitir.json()))
    # crear DTE real
    generar = Cliente.post('/dte/documentos/generar?getXML='+str(getXML), emitir.json())
    if generar.status_code!=200 :
        print('Error al generar DTE real: '+json_encode(generar.json()))
        return generar.status_code
    dte_emitido = generar.json()
    xml_emitido = dte_emitido['xml']
    dte_emitido['xml'] = None
    with open(dir+'/emitido.json', 'w') as f:
        f.write(json_encode(dte_emitido))
    if getXML :
        with codecs.open(dir+'/emitido.xml', 'w', 'iso-8859-1') as f:
            f.write(b64decode(xml_emitido).decode('iso-8859-1'))
    columnas = ['emisor', 'dte', 'folio', 'certificacion', 'tasa', 'fecha', 'sucursal_sii', 'receptor', 'exento', 'neto', 'iva', 'total', 'usuario', 'track_id']
    valores = []
    for col in columnas :
        if dte_emitido[col] != None :
            valores.append(str(dte_emitido[col]))
        else :
            valores.append('')
    with open(dir+'/emitido.csv', 'w') as f:
        f.write(';'.join(columnas)+"\n")
        f.write(';'.join(valores)+"\n")
    # obtener el PDF del DTE
    generar_pdf = Cliente.get('/dte/dte_emitidos/pdf/'+str(generar.json()['dte'])+'/'+str(generar.json()['folio'])+'/'+str(generar.json()['emisor'])+'?cedible='+str(cedible)+'&papelContinuo='+str(papel))
    if generar_pdf.status_code!=200 :
        print('Error al generar PDF del DTE: '+json_encode(generar_pdf.json()))
        return generar_pdf.status_code
    # guardar PDF en el disco
    with open(dir+'/emitido.pdf', 'wb') as f:
        f.write(generar_pdf.content)
    return 0

# función que procesa los argumentos del comando
def parseArgs(args) :
    json = ''
    xml = ''
    archivo = None
    formato = None
    cedible = 1
    papel = 0
    web = False
    dir = ''
    normalizar = 1
    getXML = 0
    for var, val in args:
        if var == '--json' :
            json = val
        elif var == '--xml' :
            xml = val
        elif var == '--archivo' :
            archivo = val
        elif var == '--formato' :
            formato = val
        elif var == '--cedible' :
            cedible = val
        elif var == '--papel' :
            papel = val
        elif var == '--web' :
            web = val
        elif var == '--dir' :
            dir = val
        elif var == '--normalizar' :
            normalizar = val
        elif var == '--getXML' :
            getXML = 1
    return json, xml, archivo, formato, cedible, papel, web, dir, normalizar, getXML

# función que carga un JSON
def loadJSON (archivo) :
    return json_decode(loadFile(archivo))

# función que carga un XML
def loadXML (archivo) :
    return '"'+b64encode(bytes(loadFile(archivo), 'UTF8')).decode('UTF8')+'"'

# función que carga un archivo
def loadFile (archivo) :
    with open(archivo, 'r') as content_file:
        content = content_file.read()
    return content
