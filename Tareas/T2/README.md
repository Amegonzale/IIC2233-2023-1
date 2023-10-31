# Tarea 2: DCCazafantasmas 👻🧱🔥


## Consideraciones generales :octocat:

Ojala disfrutes el juego ;w;<3 pues lo hice con amor.

Los nombres de los archivos de sounds y sprites deben ser los mismos que los entregados para hacer la tarea, ademas deben estar en la misma carpeta que la T2 :D ademas al comenzar una partida el timer se demora 1 segundo en cargar.

### Cosas implementadas y no implementadas 
#### Ventanas: 27 pts (27%)
##### ✅ Ventana de Inicio
En esta ventana se muestran los elementos minimos pedidos:
- Espacio editable
- Selector de mapas
- Boton de inicio
- Boton de salida

Una vez se apreta iniciar se envia al backend_inicio la info para checkear que sea valido el nombre (alnum y que este dentro de los min y max caracteres), si no se cumple abre una ventana de error. Si no cumple con ninguna parte avisando que no es alfanumerico luego va con los otros requerimientos. Asi el usuario va arreglando sus errores de a poco.

Se puede seleccionar un mapa predeterminado o 'Modo constructor'. Si se selecciona uno predeterminado comienza al tiro el juego, si se selecciona el modo constructor se abre la ventana del constructor.

Si se aprieta salir, cierra la ventana y cierra el programa.

- 'senal_procesar_user' linea 31 del main se usa para procesar el nombre.
-'senal_valid_username' linea 32 del main es la info del user procesado.

- 'senal_info' linea 35 del main se envia ssi el user era valido y comienza el juego

- En la linea 57 en Frontend inicio se encuentra la conexion con el boton salir que cierra el programa

##### ✅ Ventana de Juego
Se muestra correctamente el mapa y los elementos en ello. No se superponen entre si a menos que los fantasmas se cruzen o pasen por encima de una estrella, que es lo que se espera uwu.

A medida que se pierden vidas o pasa el tiempo esto se actualiza en la esquina superior izquierda, esa info va del backend juego y se actualiza en el frontend cada 1 segundo.

Como se menciono antes, si se selecciona modo selector inicia un mapa vacio y si se selecciona uno prehecho inicia automaticamente ese.

- En las lineas 42 y 43 del main se encuentran las señales encargadas de jugar un mapa prehecho
- En las lineas 48 a 49 se encuentran las señales encargadas de jugar un mapa construido
- 'senal_update_time' linea 63 del main se encarga de actualizar el tiempo
- 'senal_update_vidas' linea 64 del main se encarga de actualizar las vidas

- En la linea 26 (para cuando ganas) y linea 80 (para cuando pierdes) se encuentra la conexion con el boton para cerrar el programa una vez finaliza el juego.
#### Mecánicas de juego: 47 pts (47%)
Cada vez que ocurre un movimiento se manda la senal 'senal_coords' y 'senal_update_map' que actualizan las coordenadas de los entes y actualiza el mapa (que usa esas coordenadas para construirse).

##### ✅ Luigi
Al colisionar con un fantasma o fuego luigi pierde una vida y vuelve al inicio del nivel y todos los elementos que se movieron vuelven a su posicion original.

Al colisionar con una roca luigi la empuja, si colisiona con una pared o el borde del mapa este no avanza. Luigi avanza con WASD.

- En las lineas 56 a 59 del main se encuentran las senales utilizadas para resetear todo cuando luigi se hace daño
-  En lineas 52 y 53 del main se encuentran las señales usadas para mover a luigi, primero se valida su mov en el backend y si es valido actualiza la info en el frontend. En el backend chequea tambien si esta frente una roca y la mueve si su mov es valido (en el metodo validar_mov_roca en Backend_juego)

##### ✅ Fantasmas
Todos los fantasmas se mueven de manera independiente, cada 0.1 segundo el mapa se actualiza y los fantasmas avanzan dependiendo de su velocidad y direccion, esta velocidad es decidida de manera aleatorea. 

Ambos fantasmas se implementan como deberian, es decir mueren al colisionar con fuego y se invierte su direccion si colisionan con una roca o pared. Un fantasma horizontal y vertical pueden cruzar caminos correctamente, y si un fantasma tiene una estrella enfrente solo pasa por encima, sin hacer a la estrella desaparecer.

- En el metodo update_fantasmas en la linea 203 en Backend_juego se checkea primero si el timer dentro de cada fantasma esta inactivo para hacer que se mueva y luego reactivar su timer. Cada fantasma tiene su propio QTimer ya que asi son construidos en la linea 23 de Backend_juego, el intervalo de tiempo en el que esta activo esta dado por la velocidad.
- Su velocidad se calcula en la linea 26 de Backend_juego

##### ✅ Modo Constructor
El constructor no permite poner dos elementos en una casilla, de intentarse se abre una ventana de error indicando que ya esta ocupada.

Este posee todos los elementos que se pueden posicionar junto con la cantidad disponible de cada uno para poner entre parentesis. Se puede seleccionar por categoria: Todos, bloques, personajes. Una vez se presiona iniciar la partida comienza automaticamente y se cierra la ventana del modo constructor. Los iconos de los personajes son estaticos en el boton y al soltarlos en el mapa.

Si se apreta el boton de jugar se verifica que este luigi y la estrella, de ser asi comienza el juego con el mapa construido.

- En las lineas 46 a 49 en el main se encuentran las señales encargadas de iniciar todo una vez se apreta el boton de jugar. El checkeo de si hay solo un luigi y una estrella se encuentra en la linea 193 en el Frontend_constructor

- Para ver la cantidad de elementos la tiene el atributo en la linea 27 en Frontend_constructor son cargadas desde la clase CargarInfo() en la linea 266 del mismo modulo

Cada elemento tiene 
##### ✅ Fin de ronda
Hay dos formas de finalizar la ronda: ganando o perdiendo. Uno gana si apreta G sobre la estrella y uno pierde si te quedas sin vidas o se acaba el tiempo.

Al finalizar se notifica al usuario del resultado indicando el nombre, el puntaje, tambien suena la musica correspondiente.

Bajo lo anterior hay dos botones, Play again para jugar el mapa denuevo y salir que cierra el programa.
- El puntaje se calcula en el metodo puntaje() en la linea 92 de Backend_juego
- Como se menciono, en la linea 26 (para cuando ganas) y linea 80 (para cuando pierdes) se encuentra la conexion con el boton para cerrar el programa una vez finaliza el juego.

#### Interacción con el usuario: 14 pts (14%)
##### ✅ Clicks
El usuario puede drag and drop los iconos de los elementos para construir el mapa a su disposicion siempre que pueda (hayan suficientes del que toma y no este ocupada la casilla).
##### 🟠 Animaciones
Se implementan los sprites de los personajes, es decir se ven animados pero cuando pasan de una casilla a otra el movimiento no es fluido.

#### Funcionalidades con el teclado: 8 pts (8%)
##### ✅ Pausa
El boton P pausa el juego tambien como apretar el boton de pausa en la ventana. Pausarlo inhabilita el mov de luigi y los fantasmas se quedan quietos, ningun personaje esta animado cuando se pausa.

- En la linea 69 en el main se encuentra la señal que pausa el juego
##### 🟠 K + I + L
Elimina todos los fantasmas del mapa pero solo si las teclas son presionadas al mismo tiempo

- En la 241 en Frontend_jugar 'senal_update_backend' se encarga de hacer update de las coordenadas una vez se eliminan todos los fantasmas.
##### 🟠 I + N + F
Entrega vidas y tiempo infinito pero solo si las teclas son presionadas al mismo tiempo

- En la linea 70 se encuentra la señal asociada.

#### Archivos: 4 pts (4%)
##### ✅ Sprites
En la la linea 44 en Frontend_jugar se encuentran los sprites de los fantasmas como un diccionario, 'H' y 'V' como las llaves que estan asociadas a una lista de sprites ('H' esta asociada a otro diccionario que tiene 'L' y 'R' como llaves ya que el sprite que tenga depende de la direccion). Cada vez que se actualiza el mapa en el metodo update_mapa linea 121 los sprites rotan ya que se suma uno al indice que elige uno de los tres.
##### ✅ Parametros.py
Parametros se importa en Frontend_final para el audio, Frontend_jugar y Frontend_inicio para los sprites, Backend_juego para el manejo de info y Backend_inicio para info respecto al nombre de ususario.

#### Bonus: 8 décimas máximo
##### ✅ Volver a Jugar
Existe un boton de volver a jugar una vez termina el juego, ya sea por ganar o perder.
##### ❌ Follower Villain
##### ✅ Drag and Drop
Se implementa el drag and drop de objetos en el constructor

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Además es necesario que 'mapas', 'sounds' y 'sprites' esten en la carpeta T2 del repositorio.



## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```pyqt5```
2. ```os```
3. ```sys```
4. ```random```

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```Backend_inicio```
2. ```Backend_juego```
3. ```Frontend_constructor```
4. ```Frontend_final```
5. ```Fronend_inicio```
6. ```Fronend_jugar```
7. ```parametros```


## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. \<https://www.pythonguis.com/faq/pyqt-drag-drop-widgets/ >: saque inspiracion de aqui para hacer el drag and drop, modifique las funiciones del dropEvent en la linea 163 en Frontend_constructor para que se adapte a lo que queria.

