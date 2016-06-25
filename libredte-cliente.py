#!/usr/bin/python
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
Cliente LibreDTE para integración con servicios web desde línea de comandos
@author Esteban De La Fuente Rubio, DeLaF (esteban[at]sasco.cl)
@version 2016-06-24
"""

# módulos que se usarán
import sys
import getopt
import os
from libredte.sdk import LibreDTE

# configuración predeterminada (no modificar acá, usar opciones)
hash = '' # --hash=HASH_USUARIO
url = 'https://libredte.cl' # --url=NUEVA_URL

# función con modo de uso
def usage() :
    print()
    print('LibreDTE ¡facturación electrónica libre para Chile!                  libredte.cl')
    print()
    print('Modo de uso:')
    print('  $ '+os.path.basename(sys.argv[0])+' <COMANDO> --hash=<HASH USUARIO> <OPCIONES>')
    print()

# cargar comando (módulo) que se desea usar
if len(sys.argv) == 1 :
    usage()
    sys.exit(2)
main = getattr(__import__("comandos."+sys.argv[1], fromlist=["main"]), "main")
options = getattr(__import__("comandos."+sys.argv[1], fromlist=["options"]), "options")
long_options = getattr(__import__("comandos."+sys.argv[1], fromlist=["long_options"]), "long_options")

# definir opciones por defecto
if len(options) :
    options += ':'
options += 'h'
long_options += ['help', 'url=', 'hash=']

# obtener parámetros del comando
try:
    opts, args = getopt.getopt(sys.argv[2:], options, long_options)
except getopt.GetoptError:
    usage()
    sys.exit(2)

# asignar url y hash si se indicaron
for var, val in opts:
    if var == '--hash' :
        hash = val
    elif var == '--url' :
        url = val
    elif var in ('-h', '--help') :
        usage();
        sys.exit(0)

# crear cliente
Cliente = LibreDTE(hash, url)

# lanzar comando con sus opciones
sys.exit(main(Cliente, opts))
