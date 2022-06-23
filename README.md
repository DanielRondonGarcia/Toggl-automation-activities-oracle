Toggl automation activities
===========================
[![Codacy Badge](https://public-assets.toggl.com/b/static/170105782f890706f19f7ebc2cde9c59/a14e0/icon-toggltrack.png)](www.toggl.com)

En el trabajo, hacemos un seguimiento de nuestras horas de trabajo en Toggl (www.toggl.com), así que creé este pequeño proyecto para calcular cuántas horas debo trabajar para lograr mis objetivos mensuales.

Deberá instalar las bibliotecas de python `requeriments` para poder usar esto.

Installation on Windows
-----------------------

* Si no tiene instalado Python, debe instalar Python 2.9^ desde [here]([https://www.python.org/downloads/windows/])
* Abra el shell de comandos de Windows
* En el shell de comandos, ejecute los siguientes comandos

```
easy_install pip
pip install python-dateutil requests
```

* Descargar toggl_target desde [aqui](https://github.com/mos3abof/toggl_target/archive/master.zip)
* Extraiga el archivo zip descargado
* Cambia tu clave API y conexiones de base de datos en `config.py` Su token API de Toggl se puede encontrar en la configuración de su cuenta de Toggl.
* Run `python main.py`

Uso
-----
* En toggl debes utilizar siempre este formato al crear el registro del tiempo `RQ[NoRequerimiento]ACT[NoEtapa-NoActividad]-Descripción`.
  * Ejemplo:
  ```
  RQ[76871]ACT[0-43]-Capacitación sobre creación de escenarios de uso
  ```
Para usar el script, ejecute el siguiente comando:
```
$ python main.py
```
La salida será algo como:
```
Hola
Comprobando la conectividad a Internet...
¡Internet parece estar bien!

Intentando conectarme a Toggl, ¡espera!

```
Support or Contact
------------------
Si tiene problemas para usar este código, puede comunicarse con daniel5232010@gmail.com y lo ayudaré a resolverlo si tengo suficiente tiempo :).


Bug Reports & Feature Requests
------------------------------

Para informar errores, problemas o solicitudes de funciones, use la Cola de problemas en este repositorio de Github para que me sea más fácil de mantener. Por favor, no los envíe a mi correo electrónico.



License
-------

```
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
```
