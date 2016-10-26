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
Comando para escanear timbres de DTEs y agregar sus datos a un CSV
@author Esteban De La Fuente Rubio, DeLaF (esteban[at]sasco.cl)
@version 2016-08-25
"""

# módulos usados por el comando
from lxml import objectify

# opciones en formato corto
options = ''

# opciones en formato largo
long_options = ['csv=']

# función principal del comando
def main (Cliente, args) :
    csv, modo, s = parseArgs(args)
    if csv == '':
        print('Debe especificar archivo CSV donde se guardarán los DTE escaneados')
        return 1
    fd = open(csv, modo)
    if modo == 'w' :
        fd.write('RE'+s+'RS'+s+'TD'+s+'F'+s+'FE'+s+'RR'+s+'RSR'+s+'MNT'+s+'IT1'+s+'TSTED'+s+'IDK'+s+'FA'+s+'D'+s+'H'+"\n")
    while True :
        ted = input('Escanear TED: ')
        if ted == '' :
            break
        datos = getDatos(ted, s)
        if datos :
            fd.write(datos+"\n")
        else :
            print('[error] no fue posible extraer los datos del TED')
    fd.close()
    return 0

# función que procesa los argumentos del comando
def parseArgs(args) :
    csv = ''
    modo = 'w'
    separador = ';'
    for var, val in args:
        if var == '--csv' :
            csv = val
        if var == '--modo' :
            modo = val
        if separador == '--separador' :
            separador = val
    return csv, modo, separador

# función que extre los datos del XML
def getDatos(xml, s = ";") :
    # correcciones al XML
    xml = xml.replace(">TED version", "<TED version")
    xml = xml.replace(">TED  version", "<TED version")
    # cargar XML
    TED = objectify.fromstring(xml)
    if TED is None :
        return False
    # extraer datos del XML
    RE = TED.DD[0].RE[0]
    RS = TED.DD[0].CAF[0].DA[0].RS[0]
    TD = str(TED.DD[0].TD[0])
    F = str(TED.DD[0].F[0])
    FE = TED.DD[0].FE[0]
    RR = TED.DD[0].RR[0]
    RSR = TED.DD[0].RSR[0]
    MNT = str(TED.DD[0].MNT[0])
    IT1 = TED.DD[0].IT1[0]
    FA = TED.DD[0].CAF[0].DA[0].FA[0]
    D = str(TED.DD[0].CAF[0].DA[0].RNG[0].D[0])
    H = str(TED.DD[0].CAF[0].DA[0].RNG[0].H[0])
    IDK = str(TED.DD[0].CAF[0].DA[0].IDK[0])
    TSTED = TED.DD[0].TSTED[0]
    # entregar fila del CSV
    return RE+s+RS+s+TD+s+F+s+FE+s+RR+s+RSR+s+MNT+s+IT1+s+TSTED+s+IDK+s+FA+s+D+s+H
