# FEEDBACK T3

**Repositorio de _Amegonzale_**

## Resumen

| Puntaje Máximo | Puntaje Obtenido | Décimas Bonus | Décimas Descuento | Nota final |
| -------------- | ---------------- | ------------- | ----------------- | ---------- |
| 116            |  110              | 0,0            | 1,0                | **6.6**     |

## Comentario general 

Hola @Amegonzale!! Excelente tarea, y aún mejor README, fue un placer corregir esta tarea, lamentablemente hubo un par de errores menores, pero aparte de eso la tarea está muy bien hecha y completa. Felicitaciones por la nota y por el esfuerzo!

Espero que hayas disfrutado el curso :)



### Puntaje por sección

#### **Networking (18 pts)**

1. Protocolo: Correcto uso de TCP/IP.

| Puntaje Máximo | Puntaje Obtenido |
| -------------- | ---------------- |
| 2              | 2               |

Muy bien!

--------------


2. Correcto uso de sockets: Instancia y conecta los sockets de manera correcta.

| Puntaje Máximo | Puntaje Obtenido |
| -------------- | ---------------- |
| 2              | 2               |

Muy bien!

--------------


3. Correcto uso de sockets: Las aplicaciones pueden trabajar concurrentemente sin bloquearse por escuchar un socket.

| Puntaje Máximo | Puntaje Obtenido |
| -------------- | ---------------- |
| 3              | 3               |

Muy bien!

--------------


4. Conexión: La conexión es sostenida en el tiempo y de propósito general para todos los tipos de mensajes que pueden intercambiar.

| Puntaje Máximo | Puntaje Obtenido |
| -------------- | ---------------- |
| 3              | 3               |

Muy bien!

--------------


5. Manejo de Clientes: Se pueden conectar múltiples clientes sin afectar el funcionamiento del programa.

| Puntaje Máximo | Puntaje Obtenido |
| -------------- | ---------------- |
| 2              | 2               |

Muy bien!

--------------


6. Desconexión Repentina: Si el servidor se desconecta, se le advierte a los clientes con un mensaje y se les permite cerrar el programa.

| Puntaje Máximo | Puntaje Obtenido |
| -------------- | ---------------- |
| 3              | 0               |

Ocurre un error al desconectar el servidor con KeyboardInterrupt y no se notifica a los clientes

--------------


7. Desconexión Repentina: Si algún cliente se desconecta, se descarta su conexión sin afectar al resto de clientes. Si se desconecta en una partida, entonces seguirán jugando los que queden en la sala.

| Puntaje Máximo | Puntaje Obtenido |
| -------------- | ---------------- |
| 3              | 3               |

Muy bien!

--------------



> **Resumen puntaje**

| Puntaje Máximo | Puntaje Obtenido |
| -------------- | ---------------- |
| 18             | 15               |


#### **Arquitectura Cliente - Servidor (18 pts)**

1. Roles: Correcta separación de recursos entre Cliente y Servidor.

| Puntaje Máximo | Puntaje Obtenido |
| -------------- | ---------------- |
| 3              | 3               |

Muy bien!

--------------


2. Roles: Las responsabilidades de cada cliente son consistentes al enunciado.

| Puntaje Máximo | Puntaje Obtenido |
| -------------- | ---------------- |
| 3              | 3               |

Muy bien!

--------------


3. Roles: Las responsabilidades del servidor son consistentes al enunciado.

| Puntaje Máximo | Puntaje Obtenido |
| -------------- | ---------------- |
| 3              | 3               |

Muy bien!

--------------


4. Consistencia: Se mantiene coordinada y actualizada la información en todos los clientes y en el servidor.

| Puntaje Máximo | Puntaje Obtenido |
| -------------- | ---------------- |
| 2              | 2               |

Muy bien!

--------------


5. Consistencia: Se utilizan locks cuando es necesario.

| Puntaje Máximo | Puntaje Obtenido |
| -------------- | ---------------- |
| 3              | 0               |

Falta uso de locks, cada vez que se actualiza información del servidor se debería usar un lock para evitar que se actualice al mismo tiempo desde dos threads. No es necesario usar locks para mandar información ya que da lo mismo que dos threads manden información a sockets distintos al mismo tiempo, pero si que un socket reciba información de dos lugares distintos al mismo tiempo.

--------------


6. Logs: Se implementan logs del servidor, que permiten visualizar la información indicada en el enunciado.

| Puntaje Máximo | Puntaje Obtenido |
| -------------- | ---------------- |
| 4              | 4               |

Muy bien!

--------------


> **Resumen puntaje**

| Puntaje Máximo | Puntaje Obtenido |
| -------------- | ---------------- |
| 18             | 15               |

#### **Manejo de Bytes (26 pts)**

1. Codificación: Se utiliza little endian para codificar los primeros 4 bytes que contienen el largo del contenido.

| Puntaje Máximo | Puntaje Obtenido |
| -------------- | ---------------- |
| 1              | 1               |

Muy bien!

--------------


2. Codificación: Se utiliza big endian para codificar el número identificador de cada bloque a bytes.

| Puntaje Máximo | Puntaje Obtenido |
| -------------- | ---------------- |
| 1              | 1               |

Muy bien!

--------------


3. Codificación: El mensaje se separa en bloques de 128 bytes, donde los primeros 4 corresponden al largo del contenido del mensaje ya encriptado. Si el mensaje restante del último bloque no es múltiplo de 128, se rellena con ceros.

| Puntaje Máximo | Puntaje Obtenido |
| -------------- | ---------------- |
| 3              | 3               |

Muy bien!

--------------


4. Decodificación: Se utiliza little endian para decodificar los primeros 4 bytes que contienen el largo del contenido.

| Puntaje Máximo | Puntaje Obtenido |
| -------------- | ---------------- |
| 1              | 1               |

Muy bien!

--------------


5. Decodificación: Se utiliza big endian para decodificar el número identificador de cada bloque a bytes.

| Puntaje Máximo | Puntaje Obtenido |
| -------------- | ---------------- |
| 1              | 1               |

Muy bien!

--------------


6. Decodificación: El mensaje se separa en bloques de 128 bytes, donde los primeros 4 corresponden al largo del contenido del mensaje ya encriptado. Si el mensaje restante del último bloque no es múltiplo de 128, se quitan los ceros.

| Puntaje Máximo | Puntaje Obtenido |
| -------------- | ---------------- |
| 3              | 3               |

Muy bien!

--------------


7. Encriptación: Se logra mover el mensaje una cantidad n de espacios a la derecha. Este n es generado aleatoriamente dado la seed del id del jugador. Se intercambia el byte de la posición 0 por el de la posición n.

| Puntaje Máximo | Puntaje Obtenido |
| -------------- | ---------------- |
| 6              | 6               |

Todo bien con cambio de líneas

--------------


8. Desencriptación: Se logra desencriptar el mensaje, separando correctamente cada componente y sin perdida de información.

| Puntaje Máximo | Puntaje Obtenido |
| -------------- | ---------------- |
| 6              | 6               |

Todo bien con cambio de líneas

--------------


9. Integración: Utiliza correctamente el protocolo para el envío de mensajes.

| Puntaje Máximo | Puntaje Obtenido |
| -------------- | ---------------- |
| 4              | 4               |

Muy bien!

--------------


> **Resumen puntaje**

| Puntaje Máximo | Puntaje Obtenido |
| -------------- | ---------------- |
| 26              | 26              |


#### **Interfaz Gráfica (22 pts)**

1. Ventana de Inicio: Se visualiza correctamente la ventana. Se muestran todos los elementos solicitados, incluyendo jugadores y botones. La información se actualiza correctamente.

| Puntaje Máximo | Puntaje Obtenido |
| -------------- | ---------------- |
| 2              | 2               |

Muy bien!

--------------


2. Ventana de Inicio: Cuando un jugador selecciona la opción de comenzar partida, se redirige a la ventana de juego. En caso de que no se encuentren 4 jugadores, los restantes son rellenados con bots.

| Puntaje Máximo | Puntaje Obtenido |
| -------------- | ---------------- |
| 2              | 2               |

Muy bien!

--------------


3. Ventana de Inicio: Si la sala se encuentra llena o bien hay una partida en curso, el nuevo jugador que ingrese no accederá a la partida y se le informará que espere la próxima partida.

| Puntaje Máximo | Puntaje Obtenido |
| -------------- | ---------------- |
| 2              | 2               |

Muy bien!

--------------


4. Ventana de juego: Se visualiza correctamente la ventana del juego con todos los elementos solicitados en el enunciado. La información se actualiza correctamente para todos los clientes.

| Puntaje Máximo | Puntaje Obtenido |
| -------------- | ---------------- |
| 2              | 2               |

Muy bien!

--------------


5. Ventana de juego: Se visualizan los nombres y dados de todos los jugadores. Solo es visible los dados del jugador. Para los contrincantes, estos dados permantecen ocultos.

| Puntaje Máximo | Puntaje Obtenido |
| -------------- | ---------------- |
| 2              | 2               |

Muy bien!

--------------


6. Ventana de juego: Existe una forma para anunciar el dado en el turno del jugador.

| Puntaje Máximo | Puntaje Obtenido |
| -------------- | ---------------- |
| 1              | 1               |

Muy bien!

--------------


7. Ventana de juego: Existe la forma de pasar en el turno. Al momento de pasar, se salta el turno del siguiente jugador.

| Puntaje Máximo | Puntaje Obtenido |
| -------------- | ---------------- |
| 2              | 2               |

Muy bien!

--------------


8. Ventana de juego: Existe la forma de cambiar los dados. Al momento de cambiarlos, se actualizan los dados del jugador con unos nuevos.

| Puntaje Máximo | Puntaje Obtenido |
| -------------- | ---------------- |
| 1              | 1               |

Muy bien!

--------------


9. Ventana de juego: Existe la forma de dudar. Al momento de dudar, se verifican las condiciones del enunciado y comienza una nueva ronda.

| Puntaje Máximo | Puntaje Obtenido |
| -------------- | ---------------- |
| 2              | 2               |

Muy bien!

--------------


10. Ventana de juego: Existe la forma de usar un poder. El jugador es capaz de seleccionar al rival afectado.

| Puntaje Máximo | Puntaje Obtenido |
| -------------- | ---------------- |
| 2              | 2               |

Muy bien!

--------------


11. Ventana de juego: Se actualizan correctamente las vidas de los jugadores al finalizar cada ronda.

| Puntaje Máximo | Puntaje Obtenido |
| -------------- | ---------------- |
| 1              | 1               |

Muy bien!

--------------


12. Ventana de juego: Se finaliza el juego indicando al ganador.

| Puntaje Máximo | Puntaje Obtenido |
| -------------- | ---------------- |
| 3              | 3               |

Muy bien!

--------------


> **Resumen puntaje**

| Puntaje Máximo | Puntaje Obtenido |
| -------------- | ---------------- |
| 22              | 22              |


#### **Reglas de DCCachos (22 pts)**

1. Inicio del juego: Se asigna un partidor de la primera ronda de forma aleatoria.

| Puntaje Máximo | Puntaje Obtenido |
| -------------- | ---------------- |
| 1              | 1               |

Muy bien!

--------------


2. Inicio del juego: Se define un orden de los turnos de los jugadores. El orden se respeta durante todo el juego.

| Puntaje Máximo | Puntaje Obtenido |
| -------------- | ---------------- |
| 2              | 2               |

Muy bien!

--------------


3. Inicio del juego: Se asignan aleatoriamente todos los dados de los jugadores.

| Puntaje Máximo | Puntaje Obtenido |
| -------------- | ---------------- |
| 2              | 2               |

Muy bien!

--------------


4. Bots: Los Bots que juegan siguen las instrucciones indicadas en el enunciado.

| Puntaje Máximo | Puntaje Obtenido |
| -------------- | ---------------- |
| 3              | 3               |

Muy bien!

--------------


5. Al anunciar un valor, se respeta la condición de que sea estrictamente mayor al último valor anunciado.

| Puntaje Máximo | Puntaje Obtenido |
| -------------- | ---------------- |
| 2              | 2               |

Muy bien!

--------------


6. Ronda: Se puede pasar conservando el valor anunciado más alto por un jugador anterior.

| Puntaje Máximo | Puntaje Obtenido |
| -------------- | ---------------- |
| 2              | 2               |

Muy bien!

--------------


7. Ronda: Al momento de dudar se verifica que el jugador anterior tenga al menos un valor más alto del que anuncio.  El jugador que se equivoca pierde una vida. Lo mismo sucede si se duda el paso.

| Puntaje Máximo | Puntaje Obtenido |
| -------------- | ---------------- |
| 3              | 3               |

Muy bien!

--------------


8. Ronda: Se pueden cambiar los dados solo una vez por turno. Si se cambian los dados, no se puede dudar.

| Puntaje Máximo | Puntaje Obtenido |
| -------------- | ---------------- |
| 1              | 1               |

Muy bien!

--------------


9. Ronda: Se puede usar un poder únicamente si se tiene el valor de los dados para hacerlo.

| Puntaje Máximo | Puntaje Obtenido |
| -------------- | ---------------- |
| 4              | 4               |

Muy bien!

--------------


10. Termino del juego: Se asigna correctamente el jugador ganador al último jugador con vidas restantes.

| Puntaje Máximo | Puntaje Obtenido |
| -------------- | ---------------- |
| 2              | 2               |

Muy bien!

--------------


> **Resumen puntaje**

| Puntaje Máximo | Puntaje Obtenido |
| -------------- | ---------------- |
| 22              | 22              |


#### **Archivos (10 pts)**

1. Parámetros (JSON): Todos los parametros se encuentran en alguno de los parametros.json.

| Puntaje Máximo | Puntaje Obtenido |
| -------------- | ---------------- |
| 2              | 2               |

Muy bien!

--------------


2. Parámetros (JSON): Se utiliza y carga correctamente parametros.json. 

| Puntaje Máximo | Puntaje Obtenido |
| -------------- | ---------------- |
| 2              | 2               |

Muy bien!

--------------


3. main.py: Para ejecutar tanto el cliente como el servidor se pasa como argumento el puerto mediante la consola.

| Puntaje Máximo | Puntaje Obtenido |
| -------------- | ---------------- |
| 4              | 4               |

Muy bien!

--------------


4. Cripto.py: Se implementa y utiliza correctamente cripto.py.

| Puntaje Máximo | Puntaje Obtenido |
| -------------- | ---------------- |
| 2              | 2               |

Muy bien!

--------------


> **Resumen puntaje**

| Puntaje Máximo | Puntaje Obtenido |
| -------------- | ---------------- |
| 10             | 10                |


#### Bonus (4 **decimas**)

1. Cheatcodes: Cumple con todos los requisitos de este bonus.

| Décimas Máximas | Décimas Obtenidas |
| --------------- | ----------------- |
| 2               | 0                |

No implementado :C

--------------


2. Turno con tiempo: Cumple con todos los requisitos de este bonus.

| Décimas Máximas | Décimas Obtenidas |
| --------------- | ----------------- |
| 2               | 0                |

No implementado :C

--------------


> **Resumen décimas**

| Décimas Máximas | Décimas Obtenidas |
| --------------- | ----------------- |
| 4              | 0                |


#### **Descuentos generales (39 décimas)**

#####  Descuentos generales (máximo 10 décimas)

1. Se descuenta hasta 5 décimas si el README no indica archivos los archivos necesarios para ejecutar la tarea ni información relevante para la corrección.

| Descuento máximo | Descuento Obtenido |
| ---------------- | ------------------ |
| 5                | 0                 |

Excelente README!!! :D

--------------


2. Se descuentan hasta 4 décimas por no respetar PEP8

| Descuento máximo | Descuento Obtenido |
| ---------------- | ------------------ |
| 4                | 0                 |

Todo bien :D

--------------


3. Se descuentan hasta 5 décimas si no se sigue el formato de entrega.

| Descuento máximo | Descuento Obtenido |
| ---------------- | ------------------ |
| 5                | 0                 |

Todo bien :D

--------------


4. Se descuenta 5 décimas si uno o más archivos excede las 400 líneas de código.

| Descuento máximo | Descuento Obtenido |
| ---------------- | ------------------ |
| 5                | 0                 |

Todo bien :D

--------------


5.  Se descuentan hasta 5 décimas por no usar correctamente el `.gitignore`.

| Descuento máximo | Descuento Obtenido |
| ---------------- | ------------------ |
| 5                | 0                 |

Todo bien :D

--------------


6.  Se descuenta hasta 5 décimas por malas prácticas como: uso de `except Exception`, no usar señales para conectar frontend y backend, entre otros.

| Descuento máximo | Descuento Obtenido |
| ---------------- | ------------------ |
| 5                | 0                 |

Todo bien :D

--------------


7. Se descuentan 1-5 décimas por cambio de líneas.

| Descuento máximo | Descuento Obtenido |
| ---------------- | ------------------ |
| 5                | 1                 |

Cambio de líneas en ambos archivos cripto.py para dejar `num = num % largo` y así manejar los casos donde el N es mas grande que el largo del mensaje.

--------------


##### Descuentos por utilizar alguna librería o Built-in no autorizado (5 décimas)

1. Se descuentan 1- 5 décimas por utilizar alguna librería o Built-in no autorizado. Tal como dice en cada enunciado de tarea, no se permite ninguna librería a no ser que nosotros especifiquemos lo contrario.

| Descuento máximo | Descuento Obtenido |
| ---------------- | ------------------ |
| 5                | 0                 |

Todo bien :D

--------------


> **Resumen Descuento**

| Descuento máximo | Descuento Obtenido | Descuento Aplicados |
| ---------------- | ------------------ | ------------------- |
| 39               | 1                 | 1                  |
