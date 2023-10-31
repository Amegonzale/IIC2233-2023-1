# Tarea 1: DCCavaCava 🏖⛏
*Inserte introduccion interesante que capte la atencion del lector*

## Consideraciones generales :octocat:
La tarea puede correr partidas nuevas, cargar partidas guardadas y simular un torneo completo, yipieee. Permite obtener la experiencia completa de DCCavaCava ^^ <3

(Para ello es importante que los archivos csv esten en una carpeta llamada Datos dentro de T1 y que exista una carpeta vacia llamada Partidas dentro de T1.)

### Cosas implementadas y no implementadas :white_check_mark: :x:


#### Programación Orientada a Objetos: 42 pts (35%)
##### ✅  Diagrama
El diagrama se encuentra en formato pdf dentro de la carpeta T1

![Diagrama](https://i.imgur.com/lb6IjmK.jpg)

##### ✅ Definición de clases, atributos, métodos y properties
Las cuatro grandes clases que incluye mi tarea son las siguientes:
- Torneo
- Arena
- Excavador
- Item

=================================================

Torneo esta correctamente modelado pues incluye los atributos y metodos mencionados en el enunciado mas unos adicionales que facilitan el flujo del programa.

Todas las clases de torneo instanciadas parten inicialmente vacias. Solo recibe toda la poblacion de arenas y excavadores posibles (extraidas de los archivos csv e instanciadas segun sus clases). Esto se realiza para que todo lo que ocurra en el objeto torneo se quede ahi. Es por eso que los atributos comienzan inicialmente vacios. Para cargar una clase torneo lo que se hace es sobreescribir los atributos vacios.

Los setters de los atributos estan ahi para que estos no se vayan fuera de los limites establecidos en el enunciado. Importante mencionar que se utilizo un guion bajo en vez de dos para evitar bugs con los setters, pero cumple la misma funcion.

Torneo posee los siguientes metodos:
- simular_dia()
- iniciar_evento()
- mostrar_estado_torneo()
- ver_mochila()
- abrir_tesoro()
cuyo funcionamiento esta explicado dentro del modulo.

=================================================

Arena esta bien modelado pues incluye los atributos y metodos mencionados en el enunciado y a la hora de crear las subclases de arena estas funcionan correctamente. Dentro de la Arena estan instanciados todos los items.

Arena posee los siguientes metodos:
- setter_caracteristicas()
- items_consumibles()
- items_tesoro()
- __ iter __()
cuyo funcionamiento esta explicado dentro del modulo.

Las subclases de Arena fueron modeladas correctamente, modificando los atributos pertinentes y creando el metodo nuevo_dia() para la arena magnetica.

=================================================

Excavador es una clase abstracta y esta modelada correctamente, pues incluye los atributos y metodos mencionados en el enunciado y a la hora de crear las subclases de arena estas funcionan correctamente.... Ademas posee metodos adicionales para facilitar el flujo del torneo y las cosas pedidas por enunciado, como un_dia_mas() :D

Excavador posee los siguientes metodos:
- setter_caracteristicas()
- dias_por_descansar()
- cavar()               abstractmethod
- gastar_energia()      abstractmethod
- descansar()
- encontrar_item()
- consumir()            abstractmethod
- un_dia_mas()
- __ iter __()
cuyo funcionamiento esta explicado dentro del modulo.

Las subclases de Excavador fueron modeladas correctamente, modificando los metodos pertinentes y modificando el setter para energia del excavador hibrido.

=================================================

Item es el mas simple de los cuatro, posee pocos atributos base y ningun metodo. Las subclases solo construyen sobre este. :P

##### ✅ Relaciones entre clases
La clase de Excavador corresponde a una clase abstracta, ya que de cierta forma corresponde al blueprint de las subclases que tiene, por ende cavar, consumir y gastar_energia son metodos abstractos de esta. Arena no lo es pues no posee metodos que haya que redefinir en sus subclases, lo mismo con items.

Relaciones:
- Herencia:
    - ExcavadorDocencio y ExcavadorTareo heredan de Excavador
    - ExcavadorHibrido hereda de ExcavadorDocencio y ExcavadorTareo
    - ArenaNormal, ArenaMojada y ArenaRocosa heredan de Arena
    - ArenaMagnetica hereda de ArenaMojada y ArenaRocosa
    - Consumibles y Tesoros heredan de Item

- Agregacion:
    - Hay una relacion de agregacion entre Item y Arena, ya que Arena acumula items pero ambas pueden existir por su cuenta.
    - Hay una relacion de agregacion entre Item y Torneo, por lo mismo, Torneo acumula Items (y sus subclases) en la mochila, pero ambas pueden existir por su cuenta. Torneo no depende de Items.

- Composicion:
    - Hay una relacion de agregacion entre Arena y Torneo, pues sin Arena Torneo no funciona y Arena no tiene sentido sin estar en un Torneo.
    - Hay una relacion de agregacion entre Excavador y Torneo, por lo mismo, Excavador no tiene sentido sin Torneo y Torneo no funciona sin estos.

No se muestra la relacion entre las clases Excavador y Arena pues estas interactuan dentro del torneo y ninguna acumula o depende de la otra para existir.

#### Preparación programa: 11 pts (9%)
##### ✅ Creación de partidas
Todo lo que es pertinente a leer archivos esta en el modulo de Archivos. Es aqui donde se leen los archivos 'arenas.csv', 'consumibles.csv', 'excavadores.csv', 'tesoros.csv' y se instancian dependiendo de la clase a la que pertenecen.
Luego, como se menciono anteriormente, dichos objetos instanciados se utilizan para instanciar torneo, asi permitiendo crear una partida.

#### Entidades: 22 pts (18%)
##### ✅ Excavador
La clase Excavador posee el metodo cavar, que utiliza la formula dada por el enunciado la cual es heredada a sus subclases. Esta se reescribe para excavador docencio pues es necesario sumar algunos parametros a sus atributos. Cada vez que cavan pierden energia dada por el metodo gastar_energia(), se reescribe cuando es hibrido.

Los metodos descansar(), un_dia_mas() y los atributos descansado y dias_por_descansar tienen el mero fin de encargarse de implementar la accion de descansar y que se respeten los dias de descanso.

Los excavadores tienen arena como parametro en el metodo encontrar_item(), asi respetan las probabilidades de cada arena. No solo son capaces de encontrar consumibles sino de consumirlos :D consumir() se define en Excavadores y se sobreescribe cuando es tareo, otorga los stats del item.

##### ✅ Arena
Posee un nivel de dificultad determinado como atributo de la clase, tanto arena normal y rocosa sobre escriben este metodo con la formula que les corresponde. Como se menciono anteriormente, cada vez que se simula un dia verifica si la arena es magnetica, si es asi, corre el metodo nuevo_dia() que randomiza los atributos humedad y dureza en un rango establecido.

##### ✅ Torneo
Al simular el dia el metodo iniciar_evento() se encarga de verificar si ocurrio o no un evento y elegir uno segun las probabilidades de estos dado en parametros, luego se aplica su efecto.

#### Flujo del programa: 31 pts (26%)
##### ✅ Menú de Inicio
Posee:
- Nueva partida
- Cargar partida
- Salir

Como se realizo el bonus cargar partida muestra todas las partidas dentro de la carpeta Partidas en T1. Nueva partida inicia una nueva instancia de la clase torneo.

##### ✅ Menú Principal
Muestra las opciones minimas :p

##### ✅ Simulación día Torneo
Muestra lo siguiente en consola:
- Total de metros cavados durante el dia
- Metros cavados por excavador
- Items encontrados y por quien
- En caso de un evento: muestra a que arena cambio y su efecto en el equipo
- Muestra que excavadores estan descansando, cuales comienzan a descansar y cuales terminan de descansar

##### ✅ Mostrar estado torneo
Muestra la info minima pedida en el enunciado :p Dia actual, tipo de arena, metros cavados y excavadores con sus stats.

##### ✅ Menú Ítems
Muestra todos los items de la mochila, permitiendo su seleccion y posterior uso (desapareciendo de la mochila). 

##### ✅ Guardar partida
Es posible guardar la partida con el nombre que el usuario desee, estos van directo a la carpeta Partidas. Se establece que los nombres validos solo incluyen letras y numeros, pueden estar separadas por espacios, pero no compuesto solo de espacios. Informa del guardado exitoso.

##### ✅ Robustez
Los menus tienen la opcion de volver y salir (a excepcion del menu de inicio que no lo necesita), solo aceptan las opciones mostradas en pantalla, de ingresarse cualquier otro input el programa informa al usuario y vuelve a preguntar.

#### Manejo de archivos: 14 pts (12%)
##### ✅ Archivos CSV 
Como se menciono anteriormente, los archivos csv son trabajados con exito, son abiertos de manera correcta (usando encoding utf-8 para acentos) en el modulo Archivos.

##### ✅ Archivos TXT
Los archivos txt son trabajados con exito, es posible guardar y cargar archivos con este formato. Si es que el usuario desea puede sobreescribir un archivo existente ingresando el mismo nombre este.

##### ✅ parametros.py
El modulo parametros.py posee los parametros mencionados en el enunciado y los paths correspondientes a los archivos csv y el path a la carpeta Partidas. Estos parametros son utilizados globalmente.

#### Bonus: 3 décimas máximo
##### ✅ Guardar Partida

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```Jugar.py``` desde la carpeta ```T1```, ahi se encuentra el menu_manager. Además se debe crear los siguientes directorios adicionales:
1. ```Partidas``` en ```T1```, es decir debe existir la carpeta ```Partidas``` dentro de la carpeta ```T1```

Los archivos 'arenas.csv', 'consumibles.csv', 'excavadores.csv', 'tesoros.csv' deben estar en la carpeta ```Datos``` dentro de la carpeta ```T1```.


## Librerías :books:
### Librerías externas utilizadas
Solo se utilizaron las siguientes librerias:
1. ```os.path```: ```join()```
2. ```random```
3. ```abc```: ```ABC```, ```abstractmethod```


### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```Item```: Contiene a ```Item```, ```Consumibles```,```Tesoros```.
2. ```Arena```: Contiene a ```Arena```, ```ArenaNormal```,```ArenaMojada```, ```ArenaRocosa```,```ArenaMagnetica```.
3. ```Excavador```: Contiene a ```Excavador```, ```ExcavadorDocencio```,```ExcavadorTareo```, ```ExcavadorHíbrido```.
4. ```Torneo```: Contiene a ```Torneo```
5. ```Archivos```: Hecha para el manejo de archivos, guardar y cargar partidas.
6. ```Jugar```: Hecha para el manejo de menus y poder simular DCCavaCava
7. ```parametros```: Hecha para almacenar los parametros constantes y los paths a los archivos 'arenas.csv', 'consumibles.csv', 'excavadores.csv', 'tesoros.csv' y la carpeta de ```Partidas``` para cargar y guardar partidas.

(Todos estan ubicados dentro de la carpeta ```T1```)

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Cuando se ingresan inputs no se utilizan caracteres de escape como ctrl + z (^Z), o cualquier otra letra (como z) ya que eso corta el programa, cualquier otro input debiera ser recibido correctamente y validado como corresponde.
2. No puede haber dos o mas items con el mismo nombre pero con distintos stats.
3. La carpeta de Partidas debe estar creada dentro de T1 y estar vacia
4. Todos los datos relevantes ('arenas.csv', 'consumibles.csv', 'excavadores.csv', 'tesoros.csv') estan en una carpeta llamada Datos dentro de T1.
5. La carpeta Partidas solo contendra partidas con el formato de guardado elaborado y con extension txt, comienza vacio
6. Como todas las arenas tienen todos los items es posible y correcto que se encuentre el mismo item varias veces de distintas arenas
7. Yo no escribo con tildes, disculpas de antemano xd
8. Es correcto que se encuentre el mismo item mas de una vez, esto es porque las arenas tienen los mismos items al inicio y se puede encontrar el mismo en arenas distintas.

PD: DEBE existir una carpeta llamada Partidas dentro de T1, debe estar vacia y es realmente necesario que los archivos esten en Datos (de no ser asi, cambiar correctamente el path dentro de parametros)


-------
GRACIAS POR LEER <3
==========
![puppycat](https://media.tenor.com/MpUwwdicjIAAAAAC/puppycat-swiming.gif)

