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
Comando para imprimir en la impresora por defecto y en una impresora en específico
@author TODO
@version 2017-01-11
"""
'''
se utilizó pywin32-220.win32-py3.5.exe
'''
# módulos usados por el comando
from lxml import objectify
import os
import win32print
import win32api
from time import sleep 
# opciones en formato corto
options = ''

# opciones en formato largo
long_options = ['pdf=', 'impresora=']

# función principal del comando
def main (Cliente, args) :
    pdf,impresora = parseArgs(args)
    if impresora == None :
        impresora = getDefaultPrinter()
    if os.name == 'nt' :
        return printWindows(pdf,impresora);
    else:
        if os.name == 'posix':
            return printLinux(pdf,impresora)
    print('No soportado')
    return 1

# función que procesa los argumentos del comando
def parseArgs(args) :
    pdf = ''
    impresora = None
    for var, val in args:
        if var == '--pdf' :
            pdf = val
        if var == '--impresora' :
            impresora = val
    return pdf, impresora
def getDefaultPrinter() :
    Default=win32print.GetDefaultPrinter()#Función que entrega un string con el nombre de la impresora
    return Default
def printWindows(pdf,impresora) :
    ImpresoraPorDefecto = str(win32print.GetDefaultPrinter())#Primero guardamos la impresora por defecto
    win32print.SetDefaultPrinter(impresora)#Luego se cambia la impresora por defecto por la impresora específica
    win32api.ShellExecute(0,"print",pdf,None,".",0)
    sleep(5)#Se espera un tiempo para que se envíe el archivo a la impresora
    win32print.SetDefaultPrinter(ImpresoraPorDefecto)#Vuelve a estar la impresora por defecto original
def printLinux(pdf, impresora) :
    print('No soportado')
    return 1
