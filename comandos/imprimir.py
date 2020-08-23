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
@author Fernando Lizana Nuñez (f.lizananuez[at]uandresbello.edu)
@author Esteban De La Fuente Rubio, DeLaF (esteban[at]sasco.cl)
@version 2020-08-23
"""

# módulos usados por el comando
import os
if os.name == 'posix':
    try:
        import cups
    except ModuleNotFoundError:
        pass
elif os.name == 'nt' :
    try:
        import win32print
        import win32api
    except ModuleNotFoundError:
        pass
from time import sleep

# opciones en formato largo
long_options = ['pdf=', 'impresora=']

# función principal del comando
def main (Cliente, args, config) :
    # importar módulo según corresponda
    if os.name == 'posix':
        try:
            import cups
        except ModuleNotFoundError:
            print('Falta instalar módulo de CUPS para Python (pycups)')
            return 3
    elif os.name == 'nt' :
        try:
            import win32print
            import win32api
            from time import sleep
        except ModuleNotFoundError:
            print('Falta instalar pywin32')
            return 3
    # procesar comando
    pdf, impresora = parseArgs(args)
    if impresora is None :
        impresora = getDefaultPrinter()
    if impresora is None :
        print('No hay impresora disponible')
        return 2
    if os.name == 'posix':
        return printLinux(pdf, impresora)
    elif os.name == 'nt' :
        return printWindows(pdf, impresora);
    print('Sistema', os.name, 'no soportado')
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

# entrega la impresora por defecto del sistema
def getDefaultPrinter() :
    if os.name == 'nt' :
        defaultPrinter = win32print.GetDefaultPrinter() # función que entrega un string con el nombre de la impresora
    else :
        conn = cups.Connection()
        defaultPrinter = conn.getDefault()
        if defaultPrinter is None :
            printers = conn.getPrinters()
            for printer in printers :
                defaultPrinter = printer
                break
    return defaultPrinter

# imprimir en linux
def printLinux(pdf, impresora) :
    conn = cups.Connection()
    conn.printFile(impresora, pdf, 'DTE', {})
    return 0

# imprimir en windows
def printWindows(pdf, impresora, delay = 5) :
    ImpresoraPorDefecto = str(win32print.GetDefaultPrinter()) # primero guardamos la impresora por defecto
    win32print.SetDefaultPrinter(impresora) # luego se cambia la impresora por defecto por la impresora específica
    win32api.ShellExecute(0, 'print', pdf, None, '.', 0)
    sleep(delay) # se espera un tiempo para que se envíe el archivo a la impresora
    win32print.SetDefaultPrinter(ImpresoraPorDefecto) # vuelve a estar la impresora por defecto original
    return 0
