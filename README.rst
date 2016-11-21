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

Requerimientos
--------------

Para poder ejecutar el cliente es necesario tener instalado Python 3 y el SDK
de LibreDTE para Python:

La instalación de Python 3 depende del sistema operativo, y en el caso de
GNU/Linux es probable que ya venga incluído.

Si utiliza Microsoft Windows deberá
`descargar e instalar Python 3 <https://www.python.org/downloads/windows>`_,
marcar la opción "Add Python to PATH". Además revisa la instalación de LXML
según se describe `aquí <https://github.com/LibreDTE/libredte-sdk-python#lxml-en-microsoft-windows>`_.

Una vez instalado Python 3 deberá instalar, usando PIP, el SDK de LibreDTE. En
GNU/Linux:

.. code:: shell

    $ sudo pip install libredte

En Microsoft Windows:

.. code:: shell

    > pip.exe install libredte

Instalación
-----------

Para instalar el cliente, se puede clonar directamente el proyecto:

.. code:: shell

    $ git clone https://github.com/LibreDTE/libredte-cliente

O puedes descargar el
`archivo ZIP <https://github.com/LibreDTE/libredte-cliente/archive/master.zip>`_
con el cliente comprimido.

Se recomienda agregar al PATH del sistema operativo la ruta absoluta hacia
libredte-cliente ya que en esta carpeta se encuentra el programa
"libredte-cliente.py" que es el comando principal que se debe ejecutar.

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

En caso de estar usando un servidor que no sea el oficial, utilizar la opción
``--url=`` para indicar la dirección del servidor al que se quiere conectar.

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

    $ libredte-cliente.py dte_generar --hash=1234 --json=dte.json --dir=resultado

Generar DTE a partir de entrada en XML:

.. code:: shell

    $ libredte-cliente.py dte_generar --hash=1234 --xml=dte.xml --dir=resultado

Generar DTE a partir de entrada en XML sin normalizar (el XML trae todos los datos):

.. code:: shell

    $ libredte-cliente.py dte_generar --hash=1234 --xml=dte.xml --dir=resultado --normalizar=0

Generar DTE a partir de entrada en otros formatos, ejemplo YAML:

.. code:: shell

    $ libredte-cliente.py dte_generar --hash=1234 --archivo=dte.yml --formato=yaml --dir=resultado

dte_estado
~~~~~~~~~~

Actualizar el estado de un envío de DTE al SII usando el servicio web del SII:

.. code:: shell

    $ libredte-cliente.py dte_estado --hash=1234 --rut=76192083 --dte=33 --folio=1

Actualizar el estado de un envío de DTE al SII usando el correo recibido desde el SII:

.. code:: shell

    $ libredte-cliente.py dte_estado --hash=1234 --rut=76192083 --dte=33 --folio=1 --metodo=email

dte_emitido_pdf
~~~~~~~~~~~~~~~

Descargar PDF y guardar en directorio donde se está llamando al comando con nombre por defecto:

.. code:: shell

    $ libredte-cliente.py dte_emitido_pdf --hash=1234 --rut=76192083 --dte=33 --folio=1

Descargar PDF y guardar en una ruta específica con un nombre de PDF personalizado:

.. code:: shell

    $ libredte-cliente.py dte_emitido_pdf --hash=1234 --rut=76192083 --dte=33 --folio=1 --pdf=/home/delaf/factura.pdf

Descargar PDF en papel contínuo y guardar en una ruta específica con un nombre de PDF personalizado:

.. code:: shell

    $ libredte-cliente.py dte_emitido_pdf --hash=1234 --rut=76192083 --dte=33 --folio=1 --pdf=/home/delaf/factura.pdf --papel=80
