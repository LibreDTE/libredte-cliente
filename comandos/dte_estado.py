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
Comando para actualizar el estado de un DTE enviado al SII
@author Esteban De La Fuente Rubio, DeLaF (esteban[at]sasco.cl)
@version 2016-06-25
"""

# opciones en formato corto
options = ''

# opciones en formato largo
long_options = ['dte=', 'folio=', 'rut=', 'metodo=']

# función principal del comando
def main (Cliente, args) :
    dte, folio, rut, metodo = parseArgs(args)
    estado = Cliente.get('/dte/dte_emitidos/actualizar_estado/'+str(dte)+'/'+str(folio)+'/'+str(rut)+'/'+str(metodo))
    if estado.status_code!=200 :
        print('Error al obtener el estado del DTE emitido: '+estado.json())
        return estado.status_code
    print(estado.json())
    return 0

# función que procesa los argumentos del comando
def parseArgs(args) :
    dte = 0
    folio = 0
    rut = 0
    metodo = 1 # =1 webservice, =0 correo
    for var, val in args:
        if var == '--dte' :
            dte = val
        elif var == '--folio' :
            folio = val
        elif var == '--rut' :
            rut = val
        elif var == '--metodo' and val == 'email':
            metodo = 0
    return dte, folio, rut, metodo
