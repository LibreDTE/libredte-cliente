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
Comando para generar un DTE a partir de los datos de JSON o un XML
@author Esteban De La Fuente Rubio, DeLaF (esteban[at]sasco.cl)
@version 2017-11-10
"""

# módulos usados
import os
from json import dumps as json_encode
import csv
import shutil
import subprocess

# opciones en formato largo
long_options = ['emisor=', 'csv=', 'dir=', 'getXML', 'email', 'cotizacion']

# función principal del comando
def main(Cliente, args, config) :
    emisor, csv, dir, getXML, email, cotizacion = parseArgs(args)
    if emisor == None :
        print('Debe especificar el emisor que creará los documentos')
        return 1
    if not dir :
        print('Debe especificar un directorio de salida para los archivos a generar')
        return 1
    if csv == None :
        print('Debe especificar el archivo que desea procesar')
        return 1
    # crear directorio para archivos si no existe
    if not os.path.exists(dir):
        os.makedirs(dir)
    # procesar cada documento que se debe generar
    documentos = getDocumentos(csv)
    if documentos == None :
        return 1
    dte_ok = 0
    dte_fail = 0
    cmd_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    for documento in documentos :
        documento_id = "T"+str(documento["Encabezado"]["IdDoc"]["TipoDTE"])+"F"+str(documento["Encabezado"]["IdDoc"]["Folio"])
        print("Procesando el DTE "+documento_id+"... ", end="")
        documento["Encabezado"]["Emisor"] = {"RUTEmisor": emisor}
        if os.path.exists(dir+"/"+documento_id) :
            shutil.rmtree(dir+"/"+documento_id)
        os.makedirs(dir+"/"+documento_id)
        with open(dir+"/"+documento_id+"/solicitud.json", 'w') as f:
            f.write(json_encode(documento, indent=4, sort_keys=False)+"\n")
        if os.name == 'posix':
            cmd = "python3"
        elif os.name == 'nt' :
            cmd = "python.exe"
        cmd += " "+cmd_dir+"/libredte-cliente.py dte_generar"
        cmd += " --url="+config["auth"]["url"]+" --hash="+config["auth"]["hash"]
        cmd += " --json="+dir+"/"+documento_id+"/solicitud.json"
        cmd += " --dir="+dir+"/"+documento_id
        if email :
            cmd += " --email"
        if cotizacion == 1 :
            cmd += " --cotizacion"
        """
        # Sólo funciona en python 3.5 o superior (y se quiere compatibilidad con 3.4 o superior)
        result = subprocess.run(cmd.split(" "), stdout=subprocess.PIPE)
        if result.returncode == 0 :
            print("[Ok]")
            dte_ok += 1
        else :
            print("[Mal]")
            with open(dir+"/"+documento_id+'/dte_generar.log', 'w') as f :
                f.write(result.stdout.decode('utf-8'))
            dte_fail += 1
        """
        try :
            subprocess.check_output(cmd.split(" "))
            print("[Ok]")
            dte_ok += 1
        except subprocess.CalledProcessError as e :
            print("[Mal]")
            with open(dir+"/"+documento_id+'/dte_generar.log', 'w') as f :
                f.write(e.output.decode('utf-8'))
            dte_fail += 1
    print("\nSe procesaron "+str(dte_ok+dte_fail)+" documentos:")
    if dte_ok :
        print(" - OK: "+str(dte_ok))
    if dte_fail :
        print(" - Mal: "+str(dte_fail)+" (revisar archivo dte_generar.log en cada caso para ver causa del error)")
    return 0

# función que procesa los argumentos del comando
def parseArgs(args) :
    emisor = None
    csv = None
    dir = ''
    getXML = 0
    email = 0
    cotizacion = 0
    for var, val in args:
        if var == '--emisor' :
            emisor = val
        elif var == '--csv' :
            csv = val
        elif var == '--dir' :
            dir = val
        elif var == '--getXML' :
            getXML = 1
        elif var == '--email' :
            email = 1
        elif var == '--cotizacion' :
            cotizacion = 1
    return emisor, csv, dir, getXML, email, cotizacion

# función que entrega un arreglo con los diccionarios que representan los DTE
# del CSV de documentos
def getDocumentos(archivo) :
    documentos = []
    documento = None
    try :
        with open(archivo, 'r') as fd:
            reader = csv.reader(fd, delimiter=';', quotechar='"')
            cabecera = True
            for row in reader:
                if cabecera :
                    cabecera = False
                    continue
                if row[0] != '' :
                    if documento != None :
                        documentos.append(documento)
                    documento = crearDocumento(row)
                else :
                    documeto = agregarItem(documento, row[11:19])
                if documento == None :
                    print("Documento T"+row[0]+"F"+row[1]+" no pudo ser procesado desde el archivo CSV")
                    return None
            documentos.append(documento)
    except FileNotFoundError:
        print("Archivo CSV no encontrado")
        return None
    return documentos

# función que crea un documento a partir de una fila del CSV
def crearDocumento(datos) :
    # verificar campos mínimos
    if datos[0] == '' :
        print("Falta tipo de documento")
        return None
    if datos[1] == '' :
        print("Falta folio del documento")
        return None
    if datos[4] == '' :
        print("Falta RUT del receptor")
        return None
    if int(datos[0]) not in [39, 41] :
        if datos[5] == '' :
            print("Falta razón social del receptor")
            return None
        if datos[6] == '' :
            print("Falta giro del receptor")
            return None
        if datos[9] == '' :
            print("Falta dirección del receptor")
            return None
        if datos[10] == '' :
            print("Falta comuna del receptor")
            return None
    # armar dte
    documento = {
        "Encabezado" : {
            "IdDoc" : {
                "TipoDTE" : int(datos[0]),
                "Folio" : int(datos[1])
            },
            "Receptor" : {
                "RUTRecep" : datos[4].replace(".","")
            }
        },
        "Detalle": []
    }
    if datos[2] != '' :
        documento["Encabezado"]["IdDoc"]["FchEmis"] = datos[2]
    if datos[3] != '' :
        documento["Encabezado"]["IdDoc"]["FchVenc"] = datos[3]
    if datos[5] != '' :
        documento["Encabezado"]["Receptor"]["RznSocRecep"] = datos[5]
    if datos[6] != '' :
        documento["Encabezado"]["Receptor"]["GiroRecep"] = datos[6]
    if datos[7] != '' :
        documento["Encabezado"]["Receptor"]["Contacto"] = datos[7]
    if datos[8] != '' :
        documento["Encabezado"]["Receptor"]["CorreoRecep"] = datos[8]
    if datos[9] != '' :
        documento["Encabezado"]["Receptor"]["DirRecep"] = datos[9]
    if datos[10] != '' :
        documento["Encabezado"]["Receptor"]["CmnaRecep"] = datos[10]
    if datos[19] != '' :
        documento["Encabezado"]["IdDoc"]["TermPagoGlosa"] = datos[19]
    return agregarItem(documento, datos[11:19])

# funcion que agrega el item al DTE
def agregarItem(documento, item) :
    if item[2] == '' :
        print("Falta nombre del item")
        return None
    if item[4] == '' :
        print("Falta cantidad del item")
        return None
    if item[6] == '' :
        print("Falta precio del item")
        return None
    detalle = {
        "NmbItem" : item[2],
        "QtyItem" : item[4],
        "PrcItem" : item[6]
    }
    if item[0] != '' :
        detalle["CdgItem"] = {
            "TpoCodigo" : "INT1",
            "VlrCodigo" : item[0]
        }
    if item[1] != '' :
        detalle["IndExe"] = int(item[1])
    if item[3] != '' :
        detalle["DscItem"] = item[3]
    if item[5] != '' :
        detalle["UnmdItem"] = item[5]
    if item[7] != '' :
        if "," in item[7] or "." in item[7] :
            detalle["DescuentoPct"] = int(float(item[7].replace(",","."))*100)
        else :
            detalle["DescuentoMonto"] = float(item[7])
    documento["Detalle"].append(detalle)
    return documento
