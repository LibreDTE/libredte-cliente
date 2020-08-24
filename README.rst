Cliente para servicios web de LibreDTE
======================================

Este cliente permite realizar la integración con los servicios web de LibreDTE
desde cualquier aplicación, y en cualquier lenguaje, que pueda construir un
archivo JSON o bien un XML con los datos del documentos que se desea emitir.

La ejecución del cliente se hará a través de llamadas a los comandos del cliente
como si fuera cualquier otro programa de la terminal.

Licencia
--------

Este código está liberado bajo licencia `AGPL <http://www.gnu.org/licenses/agpl-3.0.en.html>`_.

Al ser un cliente que se ejecuta separado del programa que lo llama, puede ser
utilizado tanto desde software libre como software privativo.

Si se desea modificar o distribuir este cliente, se debe hacer bajo los términos
de la licencia AGPL.

Instalación
-----------

Instalar Python
~~~~~~~~~~~~~~~

Para poder ejecutar el cliente es necesario tener instalado Python 3
(versión 3.4 o superior).

La instalación de Python 3 depende del sistema operativo, y en el caso de
GNU/Linux es probable que ya venga incluído.

Si utiliza Microsoft Windows deberá
`descargar e instalar Python 3 <https://www.python.org/downloads/windows>`_,
marcar la opción "Add Python to PATH".

Descargar cliente de LibreDTE
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Para instalar el cliente, se puede clonar directamente el proyecto:

.. code:: shell

    $ git clone https://github.com/LibreDTE/libredte-cliente

O puedes descargar el
`archivo ZIP <https://github.com/LibreDTE/libredte-cliente/archive/master.zip>`_
con el cliente comprimido.

Se recomienda agregar al PATH del sistema operativo la ruta absoluta hacia
libredte-cliente ya que en esta carpeta se encuentra el programa
"libredte-cliente.py" que es el comando principal que se debe ejecutar.

Instalación de requerimientos adicionales
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

En GNU/Linux:

.. code:: shell

    $ sudo pip3 install -r requirements.txt

En Microsoft Windows:

.. code:: shell

    > pip.exe install -r requirements.txt

¿Cómo ejecuto el cliente?
-------------------------

La forma de ejecución dependerá del sistema operativo, algunos ejemplos son:

GNU/Linux:

.. code:: shell

    $ libredte-cliente.py                           # si está en el PATH y hay permisos ejecución
    $ libredte-cliente/libredte-cliente.py          # si no está en el PATH y hay permisos ejecución
    $ python libredte-cliente/libredte-cliente.py   # si no está en el PATH y no hay permisos de ejecución

Microsoft Windows:

.. code:: shell

    > python.exe libredte-cliente/libredte-cliente.py

Si todo fue ok en la ejecución del cliente, o sea, se recibió un código 200
desde el servicio web, entonces el retorno del cliente al sistema operativo será
0. En caso de cualquier problema será distinto de 0.

Autenticación
-------------

Para poder usar el cliente es necesario contar con el HASH del usuario y que
dicho usuario esté autorizado a operar con el contribuyente que se quiere
interactuar.

El HASH del usuario se obtiene de la página del
`perfil del usuario <https://libredte.cl/usuarios/perfil>`_.

Configurar los datos para autenticación en el archivo de configuración config.yml

Comandos disponibles
--------------------

Se adjunta la documentación y ejemplos de ejecución de los comandos existentes.

dte_generar
~~~~~~~~~~~

Este comando permite generar a partir de los datos en cierto formato,
típicamente un archivo JSON o XML, el DTE timbrado y firmado. Dejará 5 archivos
en el directorio que se le indique, estos archivos son:

- temporal.json respuesta del servicio web que crea el DTE temporal.
- emitido.json respuesta del servicio web que crea el DTE real (sin el XML) e incluye el ``track_id`` si el DTE fue enviado al SII.
- emitido.csv mismos datos que emitido.json, pero en un archivo plano separado por punto y coma.
- emitido.xml archivo XML del documento real (sólo si se pasó la opción ``--getXML`` al comando).
- emitido.pdf archivo PDF del documento real, con copia cedible por defecto.

Generar DTE a partir de entrada en JSON:

.. code:: shell

    $ libredte-cliente.py dte_generar --json=dte.json --dir=resultado

Generar DTE a partir de entrada en XML:

.. code:: shell

    $ libredte-cliente.py dte_generar --xml=dte.xml --dir=resultado

Generar DTE a partir de entrada en XML sin normalizar (el XML trae todos los datos):

.. code:: shell

    $ libredte-cliente.py dte_generar --xml=dte.xml --dir=resultado --normalizar=0

Generar DTE a partir de entrada en otros formatos, ejemplo YAML:

.. code:: shell

    $ libredte-cliente.py dte_generar --archivo=dte.yml --formato=YAML --dir=resultado

Generar DTE a partir de entrada en JSON y enviar automáticamente por correo:

.. code:: shell

    $ libredte-cliente.py dte_generar --hash=1234 --json=dte.json --dir=resultado --email

Es posible especificar la codificación del archivo que se leerá, y que sea transformado
automáticamente a UTF-8 por el cliente antes de enviar al servicio web de LibreDTE:

.. code:: shell

    $ libredte-cliente.py dte_generar --json=dte.json --dir=resultado --encoding=ISO-8859-1

Se puede cambiar el formato por defecto del PDF que se genera:

.. code:: shell

    $ libredte-cliente.py dte_generar --json=dte.json --dir=resultado --formato_pdf=general

Se pueden pasar datos extras al formato del PDF que se genera cuando el formato de datos no es JSON:

.. code:: shell

    $ libredte-cliente.py dte_generar --json=dte.json --dir=resultado --formato_pdf=general --extra=datos_extra.json

dte_estado
~~~~~~~~~~

Actualizar el estado de un envío de DTE al SII usando el servicio web del SII:

.. code:: shell

    $ libredte-cliente.py dte_estado --rut=76192083 --dte=33 --folio=1

Actualizar el estado de un envío de DTE al SII usando el correo recibido desde el SII:

.. code:: shell

    $ libredte-cliente.py dte_estado --rut=76192083 --dte=33 --folio=1 --metodo=email

dte_emitido_pdf
~~~~~~~~~~~~~~~

Descargar PDF y guardar en directorio donde se está llamando al comando con nombre por defecto:

.. code:: shell

    $ libredte-cliente.py dte_emitido_pdf --rut=76192083 --dte=33 --folio=1

Descargar PDF y guardar en una ruta específica con un nombre de PDF personalizado:

.. code:: shell

    $ libredte-cliente.py dte_emitido_pdf --rut=76192083 --dte=33 --folio=1 --pdf=/home/delaf/factura.pdf

Descargar PDF en papel contínuo y guardar en una ruta específica con un nombre de PDF personalizado:

.. code:: shell

    $ libredte-cliente.py dte_emitido_pdf --rut=76192083 --dte=33 --folio=1 --pdf=/home/delaf/factura.pdf --papel=80

Se puede cambiar el formato por defecto del PDF que se genera:

.. code:: shell

    $ libredte-cliente.py dte_emitido_pdf --rut=76192083 --dte=33 --folio=1 --formato_pdf=general

dte_crear_pdf
~~~~~~~~~~~~~

Crear un PDF localmente a partir del XML de un DTE, por el momento sólo se soportan boletas.

Crear PDF con 1 copia tributaria (por defecto):

.. code:: shell

    $ libredte-cliente.py dte_crear_pdf --xml=documento.xml --pdf=documento.pdf

Crear PDF con 2 copias tributarias:

.. code:: shell

    $ libredte-cliente.py dte_crear_pdf --xml=documento.xml --pdf=documento.pdf --copias_tributarias=2

imprimir
~~~~~~~~

Permite imprimir un archivo PDF directamente en la impresora.

En GNU/Linux se deberá instalar el paquete de desarrollo de CUPS y pycups:

.. code:: shell

    # apt-get install libcups2-dev
    # pip3 install pycups

En Microsoft Windows se deberá instalar el paquete `pywin32 <https://sourceforge.net/projects/pywin32/files/pywin32>`_.

Imprimir en la impresora por defecto:

.. code:: shell

    $ libredte-cliente.py imprimir --pdf=factura.pdf

Imprimir indicando la impresora:

.. code:: shell

    $ libredte-cliente.py imprimir --pdf=factura.pdf --impresora=Brother_DCP-9020CDN

dte_sincronizar
~~~~~~~~~~~~~

Enviar todos los archivos XML de un directorio al servidor de LibreDTE:

.. code:: shell

    $ libredte-cliente.py dte_sincronizar --dir=/ruta/a/xmls -vv

dte_masivos
~~~~~~~~~~~

Permite generar masivamente los DTE a partir de un archivo CSV.

.. code:: shell

    $ libredte-cliente.py dte_masivos --emisor=76192083-9 --dir=masivos --csv=emision_masiva.csv

El comando creará en el directorio especificado una carpeta por cada DTE a generar, los archivos
de la carpeta serán los mismos del comando dte_generar más un archivo solicitud.json que contiene
el JSON del DTE creado a partir de los datos del CSV.

El comando permite enviar directamente los DTE por correo, para esto ejecutar el comando así:

.. code:: shell

    $ libredte-cliente.py dte_masivos --emisor=76192083-9 --dir=masivos --csv=emision_masiva.csv --email

El comando permite generar sólo cotizaciones (documentos temporales) en vez de los reales, para esto
ejecutar el comando así:

.. code:: shell

    $ libredte-cliente.py dte_masivos --emisor=76192083-9 --dir=masivos --csv=emision_masiva.csv --cotizacion

monitor
~~~~~~~

Permite monitorear un directorio e ir creando automáticamente los DTE a medida que se van dejando
los archivos con las solicitudes de DTE (ya sea en JSON, XML, YAML u otro formato soportado).

.. code:: shell

    $ libredte-cliente.py monitor --emisor=76192083-9 --dir_entrada=/home/delaf/entrada --dir_salida=/home/delaf/salida

El formato por defecto de los archivos debe ser JSON, si se quiere usar otro, por ejemplo XML,
ejecutar con el nombre del formato (misma opción que comando dte_generar):

.. code:: shell

    $ libredte-cliente.py monitor --emisor=76192083-9 --formato=xml --dir_entrada=/home/delaf/entrada --dir_salida=/home/delaf/salida

Si el receptor tiene correo asociado se puede enviar automáticamente el DTE por correo, ejecutar así:

.. code:: shell

    $ libredte-cliente.py monitor --emisor=76192083-9 --dir_entrada=/home/delaf/entrada --dir_salida=/home/delaf/salida --email

Es posible enviar a imprimir directamente el PDF a la impresora por defecto del equipo de la siguiente manera:

.. code:: shell

    $ libredte-cliente.py monitor --emisor=76192083-9 --dir_entrada=/home/delaf/entrada --dir_salida=/home/delaf/salida --imprimir

Es posible especificar la codificación de los archivos que se leerán en el directorio que
se estará monitoreando. Con esto, cada archivo será transformado automáticamente a UTF-8
por el cliente antes de enviar al servicio web de LibreDTE:

.. code:: shell

    $ libredte-cliente.py monitor --emisor=76192083-9 --dir_entrada=/home/delaf/entrada --dir_salida=/home/delaf/salida --encoding=ISO-8859-1

El monitor se ejecutará infinitamente y cada 1 segundo revisará el directorio para comprobar si
debe generar algún DTE.

websocketd
~~~~~~~~~~

Permite crear un servidor de websockets para que la aplicación web de LibreDTE
se comunique con el computador local. Esto permite, por ejemplo, imprimir
directamente desde la aplicación web un DTE sin tener que bajar o abrir un PDF.

Imprimir en una impresora en red (PDF o usando ESCPOS para impresoras térmicas):

.. code:: shell

    $ libredte-cliente.py websocketd --printer_type=network --printer_uri=172.16.1.5

Imprimir en la impresora que el computador tenga configurada por defecto (sólo PDF):

.. code:: shell

    $ libredte-cliente.py websocketd --printer_type=system

Imprimir en una impresora específica que el computador tenga configurada (sólo PDF):

.. code:: shell

    $ libredte-cliente.py websocketd --printer_type=system --printer_uri=Brother_HL-2070N_series

Para la impresión en una impresora del computador se usa el comando
`imprimir <https://github.com/LibreDTE/libredte-cliente#imprimir>`_ y se deben
tener los mismos requerimientos.
