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
@version 2016-07-30
"""

# opciones en formato corto
options = ''

# opciones en formato largo
long_options = ['dte=', 'folio=', 'rut=', 'pdf=']

# función principal del comando
def main (Cliente, args) :
    dte, folio, rut, pdf = parseArgs(args)
    if not pdf :
        pdf = 'dte_'+str(rut)+'_T'+str(dte)+'F'+str(folio)+'.pdf'
    generar_pdf = Cliente.get('/dte/dte_emitidos/pdf/'+str(dte)+'/'+str(folio)+'/'+str(rut))
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
    pdf = False
    for var, val in args:
        if var == '--dte' :
            dte = val
        elif var == '--folio' :
            folio = val
        elif var == '--rut' :
            rut = val
        elif var == '--pdf' :
            pdf = val
    return dte, folio, rut, pdf
