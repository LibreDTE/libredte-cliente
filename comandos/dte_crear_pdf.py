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
Comando para crear un PDF de una boleta desde un xml
@author Fernando Lizana Nuñez (f.lizananuez[at]uandresbello.edu)
@author Esteban De La Fuente Rubio, DeLaF (esteban[at]sasco.cl)
@version 2017-01-16
"""

# módulos usados por el comando
import codecs
from lxml import objectify
from fpdf import FPDF
from pdf417gen import encode, render_image
import os
# opciones en formato corto
options = ''

# opciones en formato largo
long_options = ['xml=', 'pdf=', 'cedible']
DTE = None
def PDF417(aplanado):
    codes=encode(aplanado, columns=18, security_level=6)#Configuro la cantidad de columnas y el nivel de seguridad que poseerá el timbre
    image = render_image(codes)  # Crea la imagen
    image.save('imagentemporaldeltimbre.jpg')#guardo la imagen temporalmente
def TOTAL(DTE):
    suma=0
    for detalle in DTE.Detalle:
        suma=suma+int(detalle.MontoItem.text)
    return str(suma)
def TED_APLANADO(DTE):
    from lxml import etree
    DTE=DTE.TED
    A=str(etree.tostring(DTE))#transformo el DTE.TED a string
    Aplanado=(A[A.find("<"):A.find("xmlns")]+A[A.find("version"):len(A)-1])#Con esta función el string es "seccionado" para eliminar texto no deseado 
    PDF417(Aplanado)
def obtenerfechas(fecha):#con esta función se encuentra el mes dependiendo del número del mes
    Fechas=["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
    FechaArreglo=str(fecha).split("-")
    for mes in range(1,len(Fechas)+1):
        if str(mes) ==str(FechaArreglo[1]):
            Mes=Fechas[int(mes)-1]
    return str(FechaArreglo[2]+" de "+Mes+" del "+FechaArreglo[0])
def ObtenerDía(fecha):#con esta función se obtiene el día de la semana de una fecha, en este caso se ocupa el calendario de Chile
    import datetime, locale
    locale.setlocale(locale.LC_ALL,"Spanish_Chile.1252")
    return (datetime.datetime.strptime(str(fecha),"%Y-%m-%d").strftime("%A")).capitalize()#2016-12-05
def Convertir(monto):#con esta función se le agregan los puntos a los números
    return('{:,}'.format(int(monto)).replace(",","."))
def ConvertirRut(RUT):#con esta función se le agregan los puntos a los números ignorando al último dígito
    A=str(RUT).split("-")
    return("{:,}".format(int(A[0])).replace(",",".")+"-"+A[1])
def crearPDFBoleta(DTE,pdf_dir):
    class PDF(FPDF):#establesco el pié de página para cada página
        def footer(self):
            self.set_font("Arial","B",8)
            self.line(0,280,500,280)
            self.set_xy(10,283)
            self.cell(0,0,"LibreDTE ¡facturación electrónica libre para Chile!")
            self.set_xy(170,283)
            self.cell(0,0,"https://libredte.cl")
           
    pdf=PDF()
    pdf.add_page()
    pdf.set_auto_page_break(True, margin=20)#Establesco que cuando se cree la tabla dinámicamente, ésta cree otra página cuando esté a 2 cm del margen inferior
    pdf.set_text_color(255, 0, 0)#establesco el color de texto rojo
    pdf.set_line_width(.5)
    pdf.set_draw_color(255, 0, 0)#establesco las figuras como color rojo
    pdf.set_font("Arial","B",14)
    pdf.set_xy(133,17)
    pdf.cell(0,0,"R.U.T.:")
    pdf.set_xy(165,17)
    pdf.cell(0,0,ConvertirRut(DTE.Encabezado.Emisor.RUTEmisor))
    pdf.set_xy(133,23)
    pdf.cell(0,0,"BOLETA ELECTRÓNICA")
    pdf.set_xy(158,28)
    pdf.cell(0,0,"N° "+str(DTE.Encabezado.IdDoc.Folio))
    pdf.set_font("Arial","B",10)
    pdf.set_xy(140,37)
    pdf.cell(0,0,"S.I.I. - SANTIAGO CENTRO")
    pdf.set_text_color(0, 0, 255)#establesco texto de color azul
    pdf.rect(125,10,75,25)
    pdf.set_font("Arial","B",14)
    pdf.set_xy(40,10)
    pdf.cell(0,0,str(DTE.Encabezado.Emisor.RznSocEmisor))
    pdf.set_text_color(0, 0, 0)#establesco texto de color negro
    pdf.set_font("Arial","B",8)
    pdf.set_xy(40,18)
    pdf.cell(0,0,str(DTE.Encabezado.Emisor.GiroEmisor))
    pdf.set_xy(40,21)
    pdf.cell(0,0,str(DTE.Encabezado.Emisor.DirOrigen+","+DTE.Encabezado.Emisor.CmnaOrigen))
    pdf.set_font("Arial","B",9)
    pdf.set_xy(7,44)
    pdf.cell(0,0,"R.U.T.       :")
    pdf.set_xy(7,49)
    pdf.cell(0,0,"Señor(es) :")
    pdf.set_xy(7,54)
    pdf.cell(0,0,"Dirección :")
    pdf.set_xy(7,59)
    pdf.cell(0,0,"Contacto  :")
    #Fechas
    pdf.set_font("Arial","B",9)
    pdf.set_xy(145,45)
    pdf.cell(0,0,ObtenerDía(DTE.Encabezado.IdDoc.FchEmis)+" "+obtenerfechas(DTE.Encabezado.IdDoc.FchEmis))
    pdf.set_font("Arial","",9)
    pdf.set_xy(145,50)
    pdf.cell(0,0,"Vence el "+obtenerfechas(DTE.Encabezado.IdDoc.FchVenc))
    #pdf.cell(0,0,str())

    #datos
    pdf.set_font("Arial","",9)
    pdf.set_xy(25,44)
    pdf.cell(0,0,ConvertirRut(DTE.Encabezado.Receptor.RUTRecep))
    pdf.set_xy(25,49)
    pdf.cell(0,0,str(DTE.Encabezado.Receptor.RznSocRecep))
    pdf.set_xy(25,54)
    pdf.cell(0,0,str(DTE.Encabezado.Receptor.DirRecep+","+DTE.Encabezado.Receptor.CmnaRecep))
    pdf.set_xy(25,59)
    pdf.cell(0,0,str(DTE.Encabezado.Receptor.Contacto))
    pdf.set_font("Arial","B",9)#Se crean tablas dinámicas, las cuales independiente de la cantdad de elementos se van creando automáticamente
    pdf.set_line_width(.4)
    pdf.set_draw_color(0, 0, 0)
    pdf.set_xy(10,70)
    pdf.cell(ln=0, h=5.0, align='L', w=20, txt="Código", border=1)
    pdf.cell(ln=0, h=5.0, align='L', w=100, txt="Item", border=1)
    pdf.cell(ln=0, h=5.0, align='L', w=15, txt="Cant.", border=1)
    pdf.cell(ln=0, h=5.0, align='L', w=25, txt="P. unitario", border=1)
    pdf.cell(ln=1, h=5.0, align='L', w=26, txt="Total item", border=1)
    pdf.set_font("Arial","",10)
    for detalle in DTE.Detalle:
        pdf.set_font("Arial","",4)
        A=detalle.DscItem.text
        pdf.set_font("Arial","",10)
        pdf.cell(ln=0, h=9.0, align='L', w=20, txt=str(detalle.CdgItem.VlrCodigo.text), border=1)#Codigo
        pdf.cell(ln=0, h=9.0, align='L', w=100, txt=str(detalle.NmbItem.text+"\n"+A), border=1)#Item
        pdf.cell(ln=0, h=9.0, align='R', w=15, txt=str(detalle.QtyItem.text), border=1)#Cant.
        pdf.cell(ln=0, h=9.0, align='R', w=25, txt=Convertir(detalle.PrcItem.text), border=1)#precio por unidad
        pdf.cell(ln=1, h=9.0, align='R', w=26, txt=Convertir(detalle.MontoItem.text), border=1)#monto total
    pdf.ln(90)#Hago un salto de línea después de la creación de la tabla dinámica, de distancia igual a la altura del timbre + la observación,con la intención de que si se crea una nueva página, la firma y la observación van a quedar fijos en la parte inferior, al igual como si no se creara una nueva página
    pdf.cell(0,0," ")
    TED_APLANADO(DTE)
    pdf.set_font("Arial","B",9)
    directorioactual=str((os.getcwd())+"\\imagentemporaldeltimbre.jpg")
    observación= str(DTE.Encabezado.IdDoc.TermPagoGlosa.text)
    pdf.set_xy(20,195)
    pdf.cell(0,0,"Observación: "+observación[0:observación.find("RUN")+4])#Con esto, el rut aparecerá el la línea de abajo
    pdf.ln(4)
    pdf.set_x(20)
    pdf.cell(0,0,observación[observación.find("RUN")+5:])
    pdf.image(directorioactual,20,200,68,36)
    pdf.ln(20)
    pdf.set_x(150)
    pdf.cell(0,0,"Total $ :")
    pdf.set_x (170)
    pdf.cell(0,0,Convertir(TOTAL(DTE)))
    pdf.output(pdf_dir,"F")#Guardo PDF
    os.remove(directorioactual)
    pdf.close()

# función principal del comando
def main (Cliente, args) :
    global DTE
    xml, pdf, cedible = parseArgs(args)
    if xml == None :
        print('Debe indicar archivo XML')
        return 1
    if parseXML(xml) is None :
        print('No fue posible parsear el XML')
        return 1
    TipoDTE = DTE.Encabezado.IdDoc.TipoDTE
    if TipoDTE == 39 or TipoDTE == 41 :
        crearPDFBoleta(DTE,pdf)
    else :
        crearPDFFactura(xml, cedible)

# función que procesa los argumentos del comando
def parseArgs(args) :
    xml = None
    pdf = 'dte.pdf'
    cedible = False
    for var, val in args:
        if var == '--xml' :
            xml = val
        if var == '--pdf' :
            pdf = val
        if var == '--cedible' :
            cedible = True
    return xml, pdf, cedible
# función que parsea el XML y lo deja en la variable global oXML
def parseXML(archivo_xml) :
    global DTE
    datos_xml = ''
    fd = codecs.open(archivo_xml, 'r', 'iso-8859-1')
    for linea in fd :
        if linea[:5] == '<?xml' :
            continue
        datos_xml += linea
    fd.close()
    oXML = objectify.fromstring(datos_xml)
    if oXML is None :
        return None
    DTE = oXML.SetDTE.DTE.Documento
    return oXML

# retorna "objeto" del PDF creado de la factura (u otros DTE no boletas)
def crearPDFFactura(xml, cedible = False) :
    print('No está soportada la creación de PDF de facturas u otros DTE (sólo boletas)')
    return False
