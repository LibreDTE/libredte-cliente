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
@version 2017-04-10
"""

import sys
import getopt
import os
import yaml

from libredte import api_client

# Agregar al path el directorio actual para poder incluir módulos (como lib).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def usage(error = None, exit_code = 0) :
    """
    Muestra el modo de uso de la librería.

    :param error: El error a mostrar.
    :type error: str o bool
    :param exit_code: El código de salida.
    :type exit_code: int
    """
    print()
    print(
        'LibreDTE ¡facturación electrónica libre para Chile!                  '
        'libredte.cl'
    )
    print()
    if error is not None:
        print('[Error] '+ str(error))
        print()
    print('Modo de uso:')
    print('  $ '+os.path.basename(sys.argv[0])+' <COMANDO> <OPCIONES>')
    print()
    if exit_code :
        sys.exit(exit_code)

# Cargar comando (módulo) que se desea usar.
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
    options = getattr(
        __import__("comandos."+cmd, fromlist=["options"]), "options"
    )
except AttributeError :
    options = ''
try :
    long_options = getattr(
        __import__("comandos."+cmd, fromlist=["long_options"]), "long_options"
    )
except AttributeError :
    long_options = []

# Configuración predeterminada (no modificar acá, usar archivo config.yml).
hash_value = '' # --hash=HASH_USUARIO
url = 'https://libredte.cl' # --url=NUEVA_URL
if os.path.isfile(dirname+"/config.yml") :
    config = yaml.safe_load(open(dirname+"/config.yml"))
    if not config :
        config = {}
    if 'auth' in config and config['auth'] :
        if 'hash' in config['auth'] :
            hash_value = config['auth']['hash']
        if 'url' in config['auth'] :
            url = config['auth']['url']
else :
    config = {}

# Definir opciones por defecto.
if len(options) :
    options += ':'
options += 'h'
long_options += ['help', 'url=', 'hash=']

# Obtener parámetros del comando.
try:
    opts, args = getopt.getopt(sys.argv[2:], options, long_options)
except getopt.GetoptError:
    usage('Ocurrió un error al obtener los parámetros del comando', 5)

# Asignar url y hash si se indicaron.
for var, val in opts:
    if var == '--hash' :
        hash_value = val
    elif var == '--url' :
        url = val
    elif var in ('-h', '--help') :
        usage()
        sys.exit(0)

# Crear cliente.
Cliente = api_client.ApiClient(hash_value, url)

# Lanzar comando con sus opciones.
sys.exit(main(Cliente, opts, config))
