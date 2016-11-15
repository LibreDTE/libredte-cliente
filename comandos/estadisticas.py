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
long_options = ['certificacion', 'csv=', 'cantidad=']

# función principal del comando
def main (Cliente, args) :
    certificacion, csv, cantidad = parseArgs(args)
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
        statsContribuyentesActivos(datos['contribuyentes_activos'], cantidad)
    return 0

# función que procesa los argumentos del comando
def parseArgs(args) :
    certificacion = 0
    csv = 0
    cantidad = 5
    for var, val in args:
        if var == '--certificacion' :
            certificacion = 1
        if var == '--csv' :
            csv = val
        if var == '--cantidad' :
            cantidad = val
    return certificacion, csv, cantidad

# función que genera un archivo CSV con los datos de los contribuyentes activos
# Va un contribuyente por línea con las columnas de datos ordenados de la siguiente forma:
#   rut, razón social, usuario, grupos, nombre, emitidos, recibidos, total, sobre la cuota
def csvContribuyentesActivos(datos, archivo, sep = ';') :
    print('Generando archivo '+archivo+'... ¡pronto!')

# función que genera la estadísticas de los contribuyentes activos
def statsContribuyentesActivos(datos, cantidad) :
    print('Generando estadística... ¡pronto!')
    # empresas que más emiten
    print('Empresas que más documentos emiten:')
    empresas = statsEmpresasConMasEmision(datos, cantidad)
    for e in empresas :
        print('  - '+e['razon_social']+' ('+e['emitidos']+')')

    # empresas que más reciben
    print('Empresas que más documentos reciben:')
    empresas = statsEmpresasConMasRecepcion(datos, cantidad)
    for e in empresas :
        print('  - '+e['razon_social']+' ('+e['recibidos']+')')
    # empresas que más emiten y reciben (total)
    print('Empresas que más documentos emiten y reciben (total):')
    empresas = statsEmpresasConMasEmisionRecepcion(datos, cantidad)
    for e in empresas :
        print('  - '+e['razon_social']+' ('+e['total']+')')
    # empresas que están sobre la cuota
    print('Empresas que están sobre la cuota:')
    empresas = statsEmpresasSobreCuota(datos)
    for e in empresas :
        print('  - '+e['razon_social']+' ('+e['sobre_cuota']+')')

# función que entrega un arreglo con las empresas que más documentos emiten
# retorna un arreglo de diccionarios con índices: razon_social y emitidos
# ordenados de mayor a menor emitidos. ejemplo:
# [{'razon_social': 'empresa 1', 'emitidos': 10}]
def statsEmpresasConMasEmision(datos, cantidad) :
    empresas = []
    # TODO
    return empresas

# función que entrega un arreglo con las empresas que más documentos reciben
# retorna un arreglo de diccionarios con índices: razon_social y recibidos
# ordenados de mayor a menor recibidos. ejemplo:
# [{'razon_social': 'empresa 1', 'recibidos': 10}]
def statsEmpresasConMasRecepcion(datos, cantidad) :
    empresas = []
    # TODO
    return empresas

# función que entrega un arreglo con las empresas que más documentos emiten
# y reciben (total)
# retorna un arreglo de diccionarios con índices: razon_social y total
# ordenados de mayor a menor totales. ejemplo:
# [{'razon_social': 'empresa 1', 'total': 10}]
def statsEmpresasConMasEmisionRecepcion(datos, cantidad) :
    empresas = []
    # TODO
    return empresas

# función que entrega un arreglo con las empresas que están sobre la cuota
# retorna un arreglo de diccionarios con índices: razon_social y sobre_cuota
# ordenados de mayor a menor sobre la cuota. ejemplo:
# [{'razon_social': 'empresa 1', 'sobre_cuota': 10}]
def statsEmpresasSobreCuota(datos) :
    empresas = []
    # TODO
    return empresas

