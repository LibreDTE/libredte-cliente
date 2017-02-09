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
@version 2017-01-26
"""

# módulos usados por el comando
import codecs
from lxml import objectify
from fpdf import FPDF
from pdf417gen import encode, render_image
import os
import os.path
from lxml import etree
import datetime, locale

# opciones en formato largo
long_options = ['xml=', 'pdf=', 'copias_tributarias=', 'copias_cedibles=', 'logo=']

# función principal del comando
def main (Cliente, args, config) :
    xml, pdf, logo, copias_tributarias, copias_cedibles = parseArgs(args)
    if xml == None :
        print('Debe indicar archivo XML')
        return 1
    oDte = Dte()
    if not oDte.loadXML(xml) :
        print('No fue posible parsear el XML')
        return 2
    if oDte.getTipo() == 39 or oDte.getTipo() == 41 :
        oPdf = BoletaPdf(oDte.getDatos())
    else :
        oPdf = DtePdf(oDte.getDatos())
    #if logo is not None:
    #    oPdf.setLogo(logo)
    oPdf.setLogo(logo)
    oPdf.setCopias(copias_tributarias, copias_cedibles)
    oPdf.guardar(pdf)

# función que procesa los argumentos del comando
def parseArgs(args) :
    xml = None
    pdf = 'dte.pdf'
    logo = None
    copias_tributarias = 1
    copias_cedibles = 0
    for var, val in args:
        if var == '--xml' :
            xml = val
        elif var == '--pdf' :
            pdf = val
        elif var == '--logo' :
            logo = val
        elif var == '--copias_tributarias' :
            copias_tributarias = int(val)
        elif var == '--copias_cedibles' :
            copias_cedibles = int(val)
    return xml, pdf, logo, copias_tributarias, copias_cedibles

# clase con datos del SII
class Sii :

    direcciones_regionales = {
        "CHILLÁN VIEJO": "CHILLÁN",
        "HUECHURABA": "SANTIAGO NORTE",
        "LA CISTERNA": "SANTIAGO SUR",
        "LAS CONDES": "SANTIAGO ORIENTE",
        "LO ESPEJO": "SANTIAGO SUR",
        "PEÑALOLÉN": "ÑUÑOA",
        "PUDAHUEL": "SANTIAGO PONIENTE",
        "RECOLETA": "SANTIAGO NORTE",
        "SANTIAGO": "SANTIAGO CENTRO",
        "SAN MIGUEL": "SANTIAGO SUR",
        "SAN VICENTE": "SAN VICENTE TAGUA TAGUA",
        "TALTAL": "ANTOFAGASTA",
        "VITACURA": "SANTIAGO ORIENTE"
    }

    def getDireccionRegional(comuna) :
        comuna = comuna.upper()
        if comuna in Sii.direcciones_regionales :
            return Sii.direcciones_regionales[comuna]
        else :
            return comuna

# clase con el objeto que representa el DTE
class Dte:

    datos = None # objeto con los datos del DTE parseado desde el XML (tag Documento)

    # método que carga el XML del DTE
    def loadXML(self, archivo_xml) :
        if not os.path.isfile(archivo_xml) :
            return False
        datos_xml = ''
        fd = codecs.open(archivo_xml, 'r', 'iso-8859-1')
        for linea in fd :
            if linea[:5] == '<?xml' :
                continue
            datos_xml += linea
        fd.close()
        oXML = objectify.fromstring(datos_xml)
        if oXML is None :
            return False
        self.datos = oXML.SetDTE.DTE.Documento
        return True

    # método que entrega el objeto del DTE
    def getDatos(self) :
        return self.datos

    # método que entrega el tipo de documento
    def getTipo(self) :
        return self.datos.Encabezado.IdDoc.TipoDTE

# clase base que representa el PDF
class Pdf(FPDF):

    datos = None # datos del DTE que se deben usar para construir el PDF
    logo = None # ruta al archivo con el logo del DTE
    copias_tributarias = 1 # cantidad de hojas con la versión tributaria
    copias_cedibles = 0 # cantidad de hojas con la versión cedible

    # constructor de la clase, asigna los datos del PDF
    def __init__(self, datos) :
        super(Pdf, self).__init__('P', 'mm', 'Letter')
        self.datos = datos

    # método que establece el pié de página para cada página
    def footer(self):
        self.set_font("Arial","B",8)
        self.line(0,280,500,280)
        self.set_xy(10,283)
        self.cell(0,0,"LibreDTE ¡facturación electrónica libre para Chile!")
        self.set_xy(170,283)
        self.cell(0,0,"https://libredte.cl")

    # método que asigna el logo que se usará en el PDF
    def setLogo(self, archivo_logo) :
        if archivo_logo is not None:
            if os.path.isfile(archivo_logo) :
                self.logo = archivo_logo
        else:
            self.logo="No existe"

    # método que asigna las copias que se deben generar
    def setCopias(self, copias_tributarias, copias_cedibles = 0) :
        self.copias_tributarias = copias_tributarias
        self.copias_cedibles = copias_cedibles

    # método que obtiene el string con el TED aplanado
    def getTimbre(self) :
        TED = str(etree.tostring(self.datos.TED)) #transformo el TED a string
        return (TED[TED.find("<"):TED.find("xmlns")]+TED[TED.find("version"):len(TED)-1]) # con esta función el string es "seccionado" para eliminar texto no deseado

    # método que crea la imagen del timbre
    def crearImagenTimbre(self, timbre, archivo_timbre = 'timbre.png') :
        codes = encode(timbre, columns=18, security_level=6) # configuro la cantidad de columnas y el nivel de seguridad que poseerá el timbre
        image = render_image(codes)  # crea la imagen
        image.save(archivo_timbre) # guardo la imagen temporalmente

    # método que entrega la fecha a partir de YYYY-MM-DD en un string
    def getFecha(self, fecha):
        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        FechaArreglo = str(fecha).split("-")
        Mes=""
        for mes in range(1,len(meses)+1):
            if str(mes) ==str(FechaArreglo[1]):
                Mes = meses[int(mes)-1]
        return str(FechaArreglo[2]+" de "+Mes+" del "+FechaArreglo[0])

    # método que entrega el día de la semana el día de la semana de una fecha, en este caso se ocupa el calendario de Chile
    def getDia(self, fecha):
        if os.name == 'posix' :
            locale.setlocale(locale.LC_ALL, "es_CL.UTF-8")
        else :
            locale.setlocale(locale.LC_ALL, "Spanish_Chile.1252")
        return (datetime.datetime.strptime(str(fecha),"%Y-%m-%d").strftime("%A")).capitalize() # 2016-12-05

    # agregar puntos a un número
    def num(self, monto):#con esta función se le agregan los puntos a los números
        monto=float(monto)
        return '{:,}'.format(int(monto)).replace(",", ".")
    def num2(self, cantidad):
        if "." in cantidad:
            cantidad=cantidad.replace(".",",")#en el xml, los decimales son puntos, éstos se reemplazan por comas
            return self.num(cantidad[0:cantidad.find(",")])+ cantidad[cantidad.find(","):]
        else:
            return self.num(cantidad)#si la cantidad es un número entero
    # método para agregar los puntos a los números ignorando al último dígito
    def rut(self, rut):
        A = str(rut).split("-")
        return "{:,}".format(int(A[0])).replace(",",".")+"-"+A[1]
    def Fecha_Periodo(self,fecha):#función que recibe las fechas del periodo, y la devuelve invertida y con un "/" en vez de un "-"
        ArregloFecha=str(fecha).split("-")
        ArregloFecha.reverse()
        return str("/".join(ArregloFecha))

# clase que extiende al PDF para crear PDF de todos los DTE (menos boletas)
class DtePdf(Pdf):
    def guardar(self, archivo_pdf) :
        print('No está soportada la creación de PDF de facturas u otros DTE (sólo boletas)')

# clase que extiende al PDF para crear PDF de las boletas
class BoletaPdf(Pdf):
    def guardar(self, archivo_pdf) :
        for i in range(self.copias_tributarias) :
            self.agregar()
        self.output(archivo_pdf, "F")
        self.close()

    def agregar(self) :
        self.add_page()
        if self.logo=="No existe":
            self.AgregarNoLogo()
        else:
            self.AgregarLogo()
            self.agregarEmisor()
        self.agregarFolio()
        self.agregarReceptor()
        self.agregarExtraInfo()
        self.agregarDetalle()
        self.agregarObservacion()
        self.agregarTotales()
        self.agregarTimbre()
        

    def AgregarNoLogo(self):
        self.set_text_color(0,64,128) # establesco texto de color AZUL OSCURO
        self.set_font("Arial","B",14)
        self.set_xy(10,10)
        try:
            if str(self.datos.Encabezado.Emisor.RznSocEmisor):
                self.multi_cell(w=110, h=5,txt=str(self.datos.Encabezado.Emisor.RznSocEmisor),border = 0, align= 'L', fill= False)
        except:
            try:
                self.multi_cell(w=110, h=5,txt=str(self.datos.Encabezado.Emisor.RznSoc),border = 0, align= 'L', fill= False)
            except:
                pass
        self.ln(3)
        self.set_text_color(0, 0, 0)#Color negro
        self.set_font("Arial","B",10)
        try:
            if str(self.datos.Encabezado.Emisor.GiroEmisor):
                self.cell(0,0,str(self.datos.Encabezado.Emisor.GiroEmisor))
        except:
            try:
                if str(self.datos.Encabezado.Emisor.GiroEmis):
                    self.cell(0,0,str(self.datos.Encabezado.Emisor.GiroEmis))
            except:
                pass
        self.ln(3)
        self.cell(0,0,str(self.datos.Encabezado.Emisor.DirOrigen)+","+str(self.datos.Encabezado.Emisor.CmnaOrigen))
        self.ln(3)
        try:
            if str(self.datos.Encabezado.Emisor.Telefono) and str(self.datos.Encabezado.Emisor.CorreoEmisor):
                
                self.cell(0,0,str(self.datos.Encabezado.Emisor.Telefono)+" / "+str(self.datos.Encabezado.Emisor.CorreoEmisor))#Veo si existe en teléfono y el correo, OPCIONAL
        except:
            try:#si no existe, observo si por lo menos existe el teléfono
                if str(self.datos.Encabezado.Emisor.Telefono):
                    self.cell(0,0,str(self.datos.Encabezado.Emisor.Telefono))
            except:
                try:#si no existe el teléfono, veo si existe el correo
                    if str(self.datos.Encabezado.Emisor.CorreoEmisor):
                        self.cell(0,0,str(self.datos.Encabezado.Emisor.CorreoEmisor))
                except:
                    pass#si no existe ninguno, simplemente no se escribe nada
    def AgregarLogo(self):
        self.image(self.logo,10,10,20,20)
    def   agregarFolio(self) :
        self.set_text_color(255, 0, 0) # establesco el color de texto rojo
        self.set_line_width(.5)
        self.set_draw_color(255, 0, 0) # establesco las figuras como color rojo
        self.rect(125,10,75,25)
        self.set_font("Arial","B",14)
        self.set_xy(125,17)#aliniado con el cuadrado
        self.cell(ln=0,h=0, align='C',w=75 ,txt="R.U.T.: "+str(self.rut(self.datos.Encabezado.Emisor.RUTEmisor)), border=0)#Así está centrado
        self.set_xy(133,23)
        self.cell(0,0,"BOLETA ELECTRÓNICA")
        self.set_xy(125,28)
        self.cell(ln=0,h=0, align='C',w=75, txt=("N° "+str(self.datos.Encabezado.IdDoc.Folio)), border=0)#también está centrado
        self.set_font("Arial","B",10)
        self.set_xy(125,37)
        self.cell(ln=0,h=0,align='C',w=75,txt="S.I.I. - "+Sii.getDireccionRegional(self.datos.Encabezado.Emisor.CmnaOrigen.text),border=0)
    def agregarEmisor(self) :
        
        self.set_text_color(0,64,128) # establesco texto de color azul oscuro
        self.set_font("Arial","B",14)
        self.set_xy(40,10)
        try:
            if str(self.datos.Encabezado.Emisor.RznSocEmisor):
                self.multi_cell(w=80, h=5,txt=str(self.datos.Encabezado.Emisor.RznSocEmisor),border = 0, align= 'J', fill= False)
        except:
            try:
                if str(self.datos.Encabezado.Emisor.RznSoc):
                    self.multi_cell(w=80, h=5,txt=str(self.datos.Encabezado.Emisor.RznSoc),border = 0, align= 'J', fill= False)
            except:
                pass
        self.ln(3)
        self.set_text_color(0, 0, 0) # establesco texto de color negro
        self.set_font("Arial","B",8)
        self.set_x(40)
        try:
            if str(self.datos.Encabezado.Emisor.GiroEmisor):
                self.cell(0,0,str(self.datos.Encabezado.Emisor.GiroEmisor))
        except:
            try:
                if str(self.datos.Encabezado.Emisor.GiroEmis):
                    self.cell(0,0,str(self.datos.Encabezado.Emisor.GiroEmis))
            except:
                pass
        self.ln(3)
        self.set_x(40)
        self.cell(0,0,str(self.datos.Encabezado.Emisor.DirOrigen+", "+self.datos.Encabezado.Emisor.CmnaOrigen))
        
    def agregarReceptor(self) :
        self.set_text_color(0, 0, 0)
        if str(self.datos.Encabezado.Receptor.RUTRecep)!="66666666-6":
            self.set_font("Arial","B",9)
            self.set_xy(7,44)
            self.cell(0,0,"R.U.T.       :")
            self.set_font("Arial","",9)
            self.set_xy(25,44)
            self.cell(0,0,self.rut(self.datos.Encabezado.Receptor.RUTRecep))
        else:
            pass
        try:
            if str(self.datos.Encabezado.Receptor.RznSocRecep):
                self.set_font("Arial","B",9)
                self.set_xy(7,49)
                self.cell(0,0,"Señor(es) :")
                self.set_font("Arial","",9)
                self.set_xy(25,49)
                self.cell(0,0,str(self.datos.Encabezado.Receptor.RznSocRecep))
        except:
            pass
        try:#
            self.set_font("Arial","B",9)
            self.set_xy(7,54)
            if str(self.datos.Encabezado.Receptor.DirRecep) and str(self.datos.Encabezado.Receptor.CmnaRecep):    
                self.cell(0,0,"Dirección :")
                self.set_font("Arial","",9)
                self.set_xy(25,54)
                self.cell(0,0,str(self.datos.Encabezado.Receptor.DirRecep+","+self.datos.Encabezado.Receptor.CmnaRecep))
        
        except:
            try:
                if str(self.datos.Encabezado.Receptor.DirRecep):
                    self.cell(0,0,"Dirección :")
                    self.set_font("Arial","",9)
                    self.set_xy(25,54)
                    self.cell(0,0,str(self.datos.Encabezado.Receptor.DirRecep))
                          
            except:
                try:
                    if str(self.datos.Encabezado.Receptor.CmnaRecep):
                        self.cell(0,0,"Dirección :")
                        self.set_font("Arial","",9)
                        self.set_xy(25,54)
                        self.cell(0,0,str(self.datos.Encabezado.Receptor.CmnaRecep))
                except:
                    pass

        try:
            if str(self.datos.Encabezado.Receptor.Contacto):
                self.set_font("Arial","B",9)
                self.set_xy(7,59)
                self.cell(0,0,"Contacto  :")
                self.set_font("Arial","",9)
                self.set_xy(25,59)
                self.cell(0,0,str(self.datos.Encabezado.Receptor.Contacto))
        except:
            pass
    def agregarExtraInfo(self) :
        self.set_font("Arial","B",9)
        self.set_xy(145,45)
        self.cell(0,0,self.getDia(self.datos.Encabezado.IdDoc.FchEmis)+" "+self.getFecha(self.datos.Encabezado.IdDoc.FchEmis))
        self.set_font("Arial","",9)
        self.set_xy(145,50)
        try:
            if str(self.getFecha(self.datos.Encabezado.IdDoc.FchVenc)):
                self.cell(0,0,"Vence el "+self.getFecha(self.datos.Encabezado.IdDoc.FchVenc))#Fecha vencimiento OPCIONAL
        except:
            try:
                if str(self.datos.Encabezado.IdDoc.PeriodoDesde) and str(self.datos.Encabezado.IdDoc.PeriodoHasta):
                    self.cell(0,0,"Período del  "+self.Fecha_Periodo(self.datos.Encabezado.IdDoc.PeriodoDesde)+" al "+self.Fecha_Periodo(self.datos.Encabezado.IdDoc.PeriodoHasta) )#Periodo, opcional
            except:
                pass

    def agregarDetalle(self) :
        self.set_font("Arial","B",9)
        self.set_line_width(.4)
        self.set_draw_color(0, 0, 0)
        self.set_xy(5,70)
        self.cell(ln=0, h=5.0, align='L', w=25, txt="Código", border=1)
        self.cell(ln=0, h=5.0, align='L', w=100, txt="Item", border=1)
        self.cell(ln=0, h=5.0, align='L', w=15, txt="Cant.", border=1)
        self.cell(ln=0, h=5.0, align='L', w=15, txt="Unidad", border=1)
        self.cell(ln=0, h=5.0, align='L', w=25, txt="P. unitario", border=1)
        self.cell(ln=1, h=5.0, align='L', w=26, txt="Total item", border=1)
        self.set_font("Arial","",10)
        #
        altura=9.0
        for detalle in self.datos.Detalle:#El problema de implementar el detalle, que por cierto es opcional, es que en la librería fpdf al incluir una celda, ésta afecta a las demás, y por lo tanto al poder y no poder exsitir, se recurre al posicionamiento fijo de las celdas, para así evitar problemas de que quede alguna corrida
            self.set_font("Arial","",9)
            self.set_x(5)
            try:
                self.cell(ln=0, h=altura, align='L', w=25, txt=str(detalle.CdgItem.VlrCodigo.text), border=0)#Codigo OPCIONAL
            except:
                pass
            self.line(5,self.get_y(),5,self.get_y()+altura)#la  primera línea de la izquierda se coloca después de que ya se esriba el código(esto por que sino habría un salto de línea innecesario)
            self.set_x(30)
            self.cell(ln=0, h=altura, align='L', w=100, txt=str(detalle.NmbItem.text), border=0)#Item
            self.line(30,self.get_y(),30,self.get_y()+altura)
            self.ln(altura-1)
            self.set_font("Arial","",6)
            self.set_x(30)
            try:
                self.cell(ln=0, h=0, align='L', w=20, txt=str(detalle.DscItem.text), border=0)#detalle OPCIONAL
            except:
                pass
            self.ln(-altura+1)#se resta la altura de la celda, ya que la posición en los ejes es acumulativa, y por lo tanto, si no se resta, esta imprimiría más abajo
            self.set_font("Arial","",10)
            self.set_x(130)
            self.cell(ln=0, h=altura, align='R', w=15, txt=self.num2(detalle.QtyItem.text), border=0)#Cant.
            self.line(130,self.get_y(),130,self.get_y()+altura)
            self.set_x(145)
            try:
                self.cell(ln=0, h=altura, align='L', w=15, txt=str(detalle.UnmdItem.text), border=0)#unidad OPCIONAL
            except:
                pass
            self.line(145,self.get_y(),145,self.get_y()+altura)
            self.set_x(160)
            self.cell(ln=0, h=altura, align='R', w=25, txt=self.num(detalle.PrcItem.text), border=0)#precio por unidad
            self.line(160,self.get_y(),160,self.get_y()+altura)
            self.set_x(185)
            self.cell(ln=0, h=altura, align='R', w=26, txt=self.num(detalle.MontoItem.text), border=0)#total
            self.line(185,self.get_y(),185,self.get_y()+altura)
            self.line(211,self.get_y(),211,self.get_y()+altura)
            self.ln(altura)
        self.line(5,self.get_y(),211,self.get_y())
    def agregarObservacion(self) :
        self.ln(90) #Hago un salto de línea después de la creación de la tabla dinámica, de distancia igual a la altura del timbre + la observación,con la intención de que si se crea una nueva página, la firma y la observación van a quedar fijos en la parte inferior, al igual como si no se creara una nueva página
        try:
            self.cell(0,0," ")
            self.set_font("Arial","B",9)
            observación= str(self.datos.Encabezado.IdDoc.TermPagoGlosa.text)
            self.set_xy(20,195)
            self.cell(0,0,"Observación: "+observación[0:observación.find("RUN")+4])#Con esto, el rut aparecerá el la línea de abajo
            self.ln(4)
            self.set_x(20)
            self.cell(0,0,observación[observación.find("RUN")+5:])
        except:
            pass

    def agregarTimbre(self) :
        archivo_ted = str((os.getcwd())+"/ted.png")
        self.crearImagenTimbre(self.getTimbre(), archivo_ted)
        self.image(archivo_ted,20,200,68,36)
        self.set_xy(15,237)
        self.set_font("Arial","B",9)
        self.multi_cell(w=75, h=5,txt="Timbre Electrónico SII \n Resolución 80 de 2014 \n Verifique documento: https://libredte.cl/boletas",border = 0, align= 'C', fill= False)
        os.remove(archivo_ted)

    def agregarTotales(self) :
        self.ln(20)
        self.set_xy(150,210)
        self.cell(0,0,"Total $ :")
        self.set_x (170)
        self.cell(0,0,self.num(self.datos.Encabezado.Totales.MntTotal))
