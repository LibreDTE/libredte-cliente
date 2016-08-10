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
Comando para obtener el PDF de un DTE previamente emitido
@author Esteban De La Fuente Rubio, DeLaF (esteban[at]sasco.cl)
@version 2016-08-09
"""

# opciones en formato corto
options = ''

# opciones en formato largo
long_options = ['dte=', 'folio=', 'rut=', 'cedible=', 'papel=', 'compress=', 'copias_tributarias=', 'copias_cedibles=', 'pdf=']

# función principal del comando
def main (Cliente, args) :
    dte, folio, rut, cedible, papel, compress, copias_tributarias, copias_cedibles, pdf = parseArgs(args)
    if not pdf :
        pdf = 'dte_'+str(rut)+'_T'+str(dte)+'F'+str(folio)+'.pdf'
    recurso = '/dte/dte_emitidos/pdf/'+str(dte)+'/'+str(folio)+'/'+str(rut)+'?compress'+str(compress)
    if cedible is not None :
        recurso += '&cedible='+str(cedible)
    if papel is not None :
        recurso += '&papelContinuo='+str(papel)
    if compress is not None :
        recurso += '&compress='+str(compress)
    if copias_tributarias is not None :
        recurso += '&copias_tributarias='+str(copias_tributarias)
    if copias_cedibles is not None :
        recurso += '&copias_cedibles='+str(copias_cedibles)
    generar_pdf = Cliente.get(recurso)
    if generar_pdf.status_code!=200 :
        print('Error al obtener el PDF del DTE emitido: '+generar_pdf.json())
        return generar_pdf.status_code
    with open(pdf, 'wb') as f:
        f.write(generar_pdf.content)
    return 0

# función que procesa los argumentos del comando
def parseArgs(args) :
    dte = 0
    folio = 0
    rut = 0
    cedible = None
    papel = None
    compress = 0
    copias_tributarias = None
    copias_cedibles = None
    pdf = False
    for var, val in args:
        if var == '--dte' :
            dte = val
        elif var == '--folio' :
            folio = val
        elif var == '--rut' :
            rut = val
        elif var == '--cedible' :
            cedible = val
        elif var == '--papel' :
            papel = val
        elif var == '--compress' :
            compress = val
        elif var == '--copias_tributarias' :
            copias_tributarias = val
        elif var == '--copias_cedibles' :
            copias_cedibles = val
        elif var == '--pdf' :
            pdf = val
    return dte, folio, rut, cedible, papel, compress, copias_tributarias, copias_cedibles, pdf
