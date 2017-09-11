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
Comando para consultar las estadísticas de la aplicación web de LibreDTE

Este comando lo dí como tarea a alumnos de primer año del curso Programación I
de la Universidad Andrés Bello segundo semestre 2016. Los alumnos que enviaron
sus códigos para ser publicados y tuvieron mejor evaluación fueron:
- Patricio Hernández
- David Otarola
- Matías Torres
- Manfred Valenzuela
- Fernando Lizana
- Katherine Cabrera
- Ricardo Carilao
- José Soto
- Jorge Sepúlveda
- Tomás Edwards
Entre todos ellos se sacaron las funcionalidades de este comando. Por eso pueden
aparecer funciones diferentes, a pesar de que hacen algo muy similar. Por lo
anterior, este comando no pretende ser la solución óptima. Sólo cumple con el
objetivo de mostrar las estadísticas.

@author Esteban De La Fuente Rubio, DeLaF (esteban[at]sasco.cl)
@version 2016-12-10
"""

# opciones en formato largo
long_options = ['certificacion', 'csv=', 'cantidad=']

# función principal del comando
def main (Cliente, args, config) :
    certificacion, csv, cantidad = parseArgs(args)
    if certificacion :
        ambiente = 'certificacion'
    else :
        ambiente = 'produccion'
    respuesta = Cliente.get('/estadisticas/'+ambiente)
    if respuesta.status_code!=200 :
        print('Error al obtener los datos para la estadística: '+respuesta.json())
        return respuesta.status_code
    datos = respuesta.json()
    if csv :
        csvContribuyentesActivos(datos['contribuyentes_activos'], csv)
    else :
        statsContribuyentesActivos(datos['contribuyentes_activos'], cantidad)
    return 0

# función que procesa los argumentos del comando
def parseArgs(args) :
    certificacion = 0
    csv = 0
    cantidad = 5
    for var, val in args:
        if var == '--certificacion' :
            certificacion = 1
        if var == '--csv' :
            csv = val
        if var == '--cantidad' :
            cantidad = val
    return certificacion, csv, cantidad

# función que genera la estadísticas de los contribuyentes activos
def statsContribuyentesActivos(datos, cantidad) :
    print()
    print('Estadística de LibreDTE')
    print('=======================')
    print()
    total = len(datos)
    # 1-4: promedio, desviación estándar, máximo y mínimo
    print('Total de empresas: '+str(total))
    if total == 0 :
        return False
    print('Máximo de documentos totales: '+str(maximoDocumentosTotales(datos)))
    print('Mínimo documentos totales: '+str(minimoDocumentosTotales(datos)))
    print('Promedio de documentos totales: '+str(round(promedioDocumentosTotales(datos))))
    print('Desviación estándar de documentos totales: '+str(desviacionEstandarDocumentosTotales(datos)))
    print()
    # 5: contribuyentes que más emiten
    print('Contribuyentes que más documentos emiten:')
    contribuyentes = contribuyentesConMasEmision(datos, cantidad)
    for e in contribuyentes :
        print('  - '+e['razon_social']+' ('+str(e['emitidos'])+')')
    print()
    # 6: contribuyentes que más reciben
    print('Contribuyentes que más documentos reciben:')
    contribuyentes = contribuyentesConMasRecepcion(datos, cantidad)
    for e in contribuyentes :
        print('  - '+e['razon_social']+' ('+str(e['recibidos'])+')')
    print()
    # 7: contribuyentes que más emiten y reciben (total)
    print('Contribuyentes que más documentos emiten y reciben (total):')
    contribuyentes = contribuyentesConMasEmisionRecepcion(datos, cantidad)
    for e in contribuyentes :
        print('  - '+e['razon_social']+' ('+str(e['total'])+')')
    print()
    # 8: contribuyentes que están sobre la cuota
    print('Contribuyentes que están sobre la cuota:')
    contribuyentes = contribuyentesSobreCuota(datos)
    for e in contribuyentes :
        print('  - '+e['razon_social']+' ('+str(e['sobre_cuota'])+')')
    print()
    # 9: usuarios con más de un contribuyente registrado
    print('Usuarios con más de un contribuyente registrado:')
    usuarios = usuariosConIgualMayorCantidadContribuyentes(datos, 2)
    for u in usuarios :
        print('  - '+u['usuario']+' ('+str(u['contribuyentes'])+')')
    print()
    # 10: empresas que pertenecen a ciertos grupos
    print('Empresas que pertenecen a los siguientes grupos:')
    grupos = ['dte_plus', 'lce_plus', 'rrhh_plus', 'inventario_plus']
    for g in grupos :
        n = usuariosEnGrupo(datos, g)
        print('  - '+g+': '+str(n)+' de '+str(total)+' ('+str(round((n/total)*100,2))+'%)')
    print()

# función que genera un archivo CSV con los datos de los contribuyentes activos
# Va un contribuyente por línea con las columnas de datos ordenados de la siguiente forma:
#   rut, razón social, usuario, grupos, nombre, emitidos, recibidos, total, sobre la cuota
def csvContribuyentesActivos(datos, archivo, sep = ';') :
    print('Generando archivo '+archivo)
    archivo_csv=open(str(archivo),"w")
    archivo_csv=open(str(archivo),"a")
    archivo_csv.write('rut'+sep+'razon social'+sep+'usuario'+sep+'grupos'+sep+'nombre'+sep+'email'+sep+'emitidos'+sep+'recibidos'+sep+'total'+sep+'sobre la cuota'+"\n")
    for linea in datos:
        archivo_csv.write(str(linea["rut"])+sep)
        archivo_csv.write(linea["razon_social"]+sep)
        archivo_csv.write(linea["usuario"]+sep)
        grupos=" ".join(linea["grupos"]) if 'grupos' in linea else ''
        archivo_csv.write(grupos+sep)
        archivo_csv.write(linea["nombre"]+sep)
        email=linea["email"] if 'email' in linea and linea["email"] else ''
        archivo_csv.write (email+sep)
        emitidos=linea["emitidos"] if linea["emitidos"] else 0
        archivo_csv.write (str(emitidos)+sep)
        recibidos=linea["recibidos"] if linea["recibidos"] else 0
        archivo_csv.write(str(recibidos)+sep)
        total=linea["total"] if linea["total"] else 0
        archivo_csv.write(str(total)+sep)
        sobre_cuota=linea["sobre_cuota"] if linea["sobre_cuota"] else 0
        archivo_csv.write(str(sobre_cuota)+"\n")
    archivo_csv.close()

# función que entrega el máximo de los totales de documentos (emitidos y recibidos)
# retorna un número entero
def maximoDocumentosTotales(datos) :
    maximo = None
    total=[]
    for linea in datos:
        total.append(linea["total"])
    maximo=total[0]
    for m in total:
        if m > maximo:
            maximo = m
    return maximo

# función que entrega el mínimo de los totales de documentos (emitidos y recibidos)
# retorna un número entero
def minimoDocumentosTotales(datos) :
    listaMin=[]
    minimo = None
    for contribuyente in datos:
        listaMin.append(contribuyente['total'])
    return min(listaMin)

# función que entrega el promedio (o media) de los totales de documentos (emitidos y recibidos)
# retorna un número entero
def promedioDocumentosTotales(datos) :
    promedio = None
    lista=[]
    suma=0
    for cliente in datos:
        for dato in cliente:
            if dato=="total":
                lista.append(cliente[dato])
    for n in range(len(lista)):
        if lista[n]==None:
            lista[n]=0
    for número in lista:
        suma=suma+número
    promedio=round(suma/len(lista),3)
    return promedio

# función que entrega la desviación estándar de los totales de documentos (emitidos y recibidos)
# retorna un número entero
def desviacionEstandarDocumentosTotales(datos) :
    desviacion = None
    total=[]
    for linea in datos:
        total.append(linea["total"])
    suma=0
    for m in total:
       suma += int(m)
    promedio=int(suma/len(total))
    contador=0
    varianza=[]
    for n in total:
        v=(int(n)-promedio)**2
        varianza.append(v)
    suma_v=0
    for p in varianza:
        suma_v += int(p)
    desviacion=int((suma_v/len(varianza))**0.5)
    return desviacion

# función que entrega un arreglo con las contribuyentes que más documentos emiten
# retorna un arreglo de diccionarios con índices: razon_social y emitidos
# ordenados de mayor a menor emitidos. ejemplo:
# [{'razon_social': 'empresa 1', 'emitidos': 10}]
def contribuyentesConMasEmision(datos, cantidad) :
    from operator import itemgetter
    D={}
    arreglo=[]
    contribuyentes = []
    for cliente in datos:
        for dato in cliente:
            if dato=="razon_social":
                D[cliente[dato]]=cliente["emitidos"]
                # ahora debería tener: {razón social: emitidos}
    for i in D:
        if D[i]==None:
            D[i]=0
    Tupla=sorted(D.items(), key=itemgetter(1),reverse=True)
    # necesito ordenar diccionario
    for i in range(len(Tupla)):
        D2={}
        D2["razon_social"]=str(Tupla[i][0])
        D2["emitidos"]=int(Tupla[i][1])
        arreglo.append(D2)#[{ , }]
    if cantidad>len(arreglo):
        cantidad=len(arreglo)
    for a in range(0,cantidad):
        contribuyentes.append(arreglo[a])
    return contribuyentes

# función que entrega un arreglo con las contribuyentes que más documentos reciben
# retorna un arreglo de diccionarios con índices: razon_social y recibidos
# ordenados de mayor a menor recibidos. ejemplo:
# [{'razon_social': 'empresa 1', 'recibidos': 10}]
def contribuyentesConMasRecepcion(datos, cantidad) :
    contribuyentes = []
    datos = insertionSortMayorAMenor(datos, 'recibidos')
    for x in (datos):
	    contribuyentes.append(({'razon_social':x['razon_social'], 'recibidos': x['recibidos']}))
    if(cantidad):
        return contribuyentes[:int(cantidad)]
    else:
        return contribuyentes
    return contribuyentes

# función que entrega un arreglo con las contribuyentes que más documentos emiten
# y reciben (total)
# retorna un arreglo de diccionarios con índices: razon_social y total
# ordenados de mayor a menor totales. ejemplo:
# [{'razon_social': 'empresa 1', 'total': 10}]
def contribuyentesConMasEmisionRecepcion(datos, cantidad) :
    contribuyentes = []
    datos = insertionSortMayorAMenor(datos, 'total')
    for x in (datos):
        contribuyentes.append(({'razon_social':x['razon_social'], 'total': x['total']}))
    if(cantidad):
        return contribuyentes[:int(cantidad)]
    else:
        return contribuyentes

# función que entrega un arreglo con las contribuyentes que están sobre la cuota
# retorna un arreglo de diccionarios con índices: razon_social y sobre_cuota
# ordenados de mayor a menor sobre la cuota. ejemplo:
# [{'razon_social': 'empresa 1', 'sobre_cuota': 10}]
def contribuyentesSobreCuota(datos) :
    contribuyentes4 = []
    n=[]
    lista=[]
    lista2=[]
    indice=0
    for m in datos:
        n.append(m["sobre_cuota"])
        lista.append(m["razon_social"])
    for r in n:
        sc = r if r else 0
        lista2.append(sc)
    for cant in (range(len(lista2))):
        if lista2[cant] >= 1:
            indice=cant
            e={"razon_social":lista[indice],"sobre_cuota":lista2[indice]}
            contribuyentes4.append(e)
        else:
            pass
    return  contribuyentes4

# función que entrega un arreglo con los usuarios que tienen una cantidad igual
# o superior de contribuyentes registrados a la indicada
# retorna una arreglo de diccionarios con índices: usuario y contribuyentes
# ordenados de mayor a menor contribuyentes. ejemplo:
# [{'usuario': 'delaf', 'contribuyentes': 4}]
def usuariosConIgualMayorCantidadContribuyentes(datos, cantidad) :
    usuarios = []
    usuarios_a=[]
    a=0
    n=0
    jk=0
    eh=0
    w=0
    v=0
    t=[]
    t_2=[]
    contador=[]
    for i in datos:
        t_2.append(i["usuario"])
    for l in t_2:
        if l not in t:
            t.append(l)
    for z in t:
        contador.append(0)
    b=len(t_2)
    while a != b:
        if t_2[0] == t[n]:
            contador[n]+=1
            del t_2[0]
            a+=1
            n=0
        else:
            n+=1
    for h in t:
        usuarios_a.append(dict([("usuario", h),("contribuyentes", contador[jk])]))
        jk+=1
    contador.sort(reverse=True)
    while w != len(contador):
        if contador[w] == usuarios_a[v]["contribuyentes"]:
            usuarios.append(usuarios_a[v])
            del usuarios_a[v]
            w+=1
            v=0
        else:
            v+=1
    while eh != len(usuarios):
        if usuarios[eh]["contribuyentes"] >= cantidad:
            eh+=1
        else:
            del usuarios[eh]
    return usuarios

# función que cuenta la cantidad de usuarios que están en cierto grupo
# se cuenta al usuario tantas veces como contribuyentes existan
# retorna un número entero con la cantidad de coincidencias
def usuariosEnGrupo(datos, grupo) :
    cantidad = 0
    for diccionario in datos:
        if 'grupos' in diccionario :
            for x in diccionario['grupos']:
                if x == grupo:
                    cantidad += 1
    return cantidad

# Algoritmo Insertion Sort Mayor a Menor
# función extra creada por un alumno para ordenar los datos
def insertionSortMayorAMenor(datos, clave):
    for j in range(1,(len(datos))):
        key = datos[j]
        if key[clave] is None:
            key[clave] = 0
        i = j - 1
        if datos[i][clave] is None:
            datos[i][clave] = 0
        while i >= 0 and (datos[i][clave] < key[clave]):
            datos[i+1] = datos[i]
            i = i - 1
        datos[i+1] = key
    for x in (datos):
        if x[clave] == 0:
            x[clave] = None
    return datos
