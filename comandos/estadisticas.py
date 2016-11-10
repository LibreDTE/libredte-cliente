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
Comando para consultar las estadísticas de la aplicación web de LibreDTE
@author Esteban De La Fuente Rubio, DeLaF (esteban[at]sasco.cl)
@version 2016-11-10
"""

# opciones en formato corto
options = ''

# opciones en formato largo
long_options = ['certificacion', 'csv=']

# función principal del comando
def main (Cliente, args) :
    certificacion, csv = parseArgs(args)
    if certificacion :
        ambiente = 'certificacion'
    else :
        ambiente = 'produccion'
    respuesta = Cliente.get('/estadisticas/'+ambiente)
    if respuesta.status_code!=200 :
        print('Error al obtener los datos para la estadística: '+respuesta.json())
        return respuesta.status_code
    datos = respuesta.json()
    if csv :
        csvContribuyentesActivos(datos['contribuyentes_activos'], csv)
    else :
        statsContribuyentesActivos(datos['contribuyentes_activos'])
    return 0

# función que procesa los argumentos del comando
def parseArgs(args) :
    certificacion = 0
    csv = 0
    for var, val in args:
        if var == '--certificacion' :
            certificacion = 1
        if var == '--csv' :
            csv = val
    return certificacion, csv

# función que genera un archivo CSV con los datos de los contribuyentes activos
# Va un contribuyente por línea con las columnas de datos ordenados de la siguiente forma:
#   rut, razón social, usuario, grupos, nombre, emitidos, recibidos, total, sobre la cuota
def csvContribuyentesActivos(datos, archivo, sep = ';') :
    print('Generando archivo '+archivo+'... ¡pronto!')

# función que genera la estadísticas de los contribuyentes activos
def statsContribuyentesActivos(datos) :
    print('Generando estadística... ¡pronto!')
