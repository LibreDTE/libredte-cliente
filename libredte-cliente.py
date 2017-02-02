#!/usr/bin/python3
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
@version 2017-02-02
"""

# módulos que se usarán
import sys
import getopt
import os
import yaml
from libredte.sdk import LibreDTE

# función con modo de uso
def usage(error = False, exit = 0) :
    print()
    print('LibreDTE ¡facturación electrónica libre para Chile!                  libredte.cl')
    print()
    if error :
        print('[Error] '+error)
        print()
    print('Modo de uso:')
    print('  $ '+os.path.basename(sys.argv[0])+' <COMANDO> --hash=<HASH USUARIO> <OPCIONES>')
    print()
    if exit :
        sys.exit(exit)

# cargar comando (módulo) que se desea usar
if len(sys.argv) == 1 :
    usage('Falta indicar el comando que se desea ejecutar', 2)
cmd = sys.argv[1]
dirname = os.path.dirname(__file__)
if not dirname :
    dirname = '.'
if not os.path.isfile(dirname+"/comandos/"+cmd+".py") :
    usage('Comando solicitado "'+cmd+'" no existe', 3)
try :
    main = getattr(__import__("comandos."+cmd, fromlist=["main"]), "main")
except AttributeError :
    usage('No se encontró la función "main" en el módulo "'+cmd+'"', 4)
try :
    options = getattr(__import__("comandos."+cmd, fromlist=["options"]), "options")
except AttributeError :
    options = ''
try :
    long_options = getattr(__import__("comandos."+cmd, fromlist=["long_options"]), "long_options")
except AttributeError :
    long_options = []

# configuración predeterminada (no modificar acá, usar parámetros o archivo config.yml)
hash = '' # --hash=HASH_USUARIO
url = 'https://libredte.cl' # --url=NUEVA_URL
if os.path.isfile(dirname+"/config.yml") :
    config = yaml.safe_load(open(dirname+"/config.yml"))
    if not config :
        config = {}
    if 'auth' in config and config['auth'] :
        if 'hash' in config['auth'] :
            hash = config['auth']['hash']
        if 'url' in config['auth'] :
            url = config['auth']['url']
else :
    config = {}

# definir opciones por defecto
if len(options) :
    options += ':'
options += 'h'
long_options += ['help', 'url=', 'hash=']

# obtener parámetros del comando
try:
    opts, args = getopt.getopt(sys.argv[2:], options, long_options)
except getopt.GetoptError:
    usage('Ocurrió un error al obtener los parámetros del comando', 5)

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
sys.exit(main(Cliente, opts, config))
