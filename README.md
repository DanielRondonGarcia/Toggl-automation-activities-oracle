Toggl automation activities
===========================
[![Codacy Badge](https://public-assets.toggl.com/b/static/170105782f890706f19f7ebc2cde9c59/a14e0/icon-toggltrack.png)](www.toggl.com)

En el trabajo, hacemos un seguimiento de nuestras horas de trabajo en Toggl (www.toggl.com), así que creé este pequeño proyecto para automatizar el registro todas las actividades diarias a la base de datos SGI (oracle).

Deberá instalar las bibliotecas de python `requeriments` para poder usar esto.

Installation on Windows
-----------------------

* Si no tiene instalado Python, debe instalar Python 2.9^ desde [here](https://www.python.org/downloads/windows/)
* Abra el shell de comandos de Windows
* En el shell de comandos, ejecute los siguientes comandos

```
pip install -r requirements.txt
```

* Traer la Api desde [aqui](https://track.toggl.com/profile)
* Extraiga el archivo zip descargado
* Cambia tu clave API y conexiones de base de datos en `config.py` y quitar el `-example`.  Su token API de Toggl se puede encontrar en la configuración de su cuenta de Toggl.
* Descargue la versión de 64 bits de Oracle instantClient desde: [aqui](https://www.oracle.com/database/technologies/instant-client/winx64-64-downloads.html)
  * ![image](https://user-images.githubusercontent.com/61068392/176324441-f4fd17d0-d8d4-40c5-8687-6911c3fa1ba1.png)
* Copie los archivos dll en el directorio instantclient al directorio python, como se muestra a continuación
  * ![image](https://user-images.githubusercontent.com/61068392/176324506-82590467-6cca-4738-91b3-329c75f3e572.png)
  * ![image](https://user-images.githubusercontent.com/61068392/176324547-7e999176-11e9-41f0-b92d-9c3fea3823dd.png)
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
Client name: Daniel Gerardo Rondón García  Client ID: 8575225

==========================================================================  
Requerimiento: 76512
Etapa: 0
Actividad: 50
Descripción: Asistencia a la sexta versión de la reunión Test Ninjas ACTSIS.
Fecha de incio: 2022-06-24 20:01:09
Fecha de incio: 2022-06-24 22:42:19
Diff: 2:41:10  Diff in Hours: 2.7
==========================================================================

Total Hours: 6.8
Escribe el Numero 1 si quiere registrar el tiempo en el SGI, si no, solo oprima la tecla Enter. Tambien puedes ver mejor cada detalle en el archivo creado en la ruta: logs/data-24-06-2022.json
 
Escribió: 2
No se han guardado las actividades
```
# Example 2

#
![image](https://user-images.githubusercontent.com/61068392/178859085-5fc9ac7a-6b14-4744-894e-2848635586c1.png)

#
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
