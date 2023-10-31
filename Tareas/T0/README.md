# Tarea 0: DCCeldas 💣🐢🏰

¡Bienvenido seas al reino de las tortugas! Donde abundan los microplasticos y las bombillas 🐢🐢 A continuacion encontraras informacion sobre el plan de defensa nacional, aka T0.

## Consideraciones generales :octocat:
Mi T0 cumple con lo que se pide, estan todas las funciones minimas implementadas de manera correcta y clara. Pero, es importante mencionar lo extremandamente lento que es cuando uno intenta resolver un tablero 7x7 o superior... MUY lento. A pesar de esto, dado el algoritmo utilizado para resolver el tablero se espera que la solucion sea correcta aun que tarde mucho en resolverlo.

## Consideranciones especificas
Estas consideraciones son mas pertinentes a la hora de correr el codigo:
1. El nombre del archivo debe tener el formato ```nombre_archivo.ext``` donde nombre_archivo es el nombre del archivo y ext es la extension del archivo.
2. Cuando se estan eligiendo las opciomes del menu, los numeros van sin [], las unicas opciones son 1, 2, 3, 4 o 0 de no ser asi se considera invalido.

### Cosas implementadas y no implementadas :white_check_mark: :x:
#### Menú de Inicio (5 pts) (7%)
##### ✅ Seleccionar Archivo
##### ✅ Validar Archivos
#### Menú de Acciones (11 pts) (15%) 
##### ✅ Opciones
##### ✅ Mostrar tablero 
##### ✅ Validar bombas y tortugas
##### ✅ Revisar solución
##### ✅ Solucionar tablero
##### ✅ Salir
#### Funciones (34 pts) (45%)
##### ✅ Cargar tablero
##### ✅ Guardar tablero
##### ✅ Valor bombas
##### ✅ Alcance bomba
##### ✅ Verificar tortugas
##### ✅ Solucionar tablero
#### General: (19 pts) (25%)
##### ✅ Manejo de Archivos
##### ✅ Menús
##### ✅ tablero.py
##### ✅ Módulos
##### ✅ PEP-8
#### Bonus: 6 décimas
##### ✅ Funciones atómicas
##### ❌ Regla 5

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py``` desde la carpeta ```T0```. Además los archivos que se quieren usar para probar el codigo deben estar en la carpeta ```Archivos``` que estara en la carpeta ```T0```. 

## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```os.path```: ```join()```,```exists()```


### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```functions```: Contiene todas las funciones minimas pedidas más otras que las complementan y facilitan su funcionamiento. 
2. ```tablero```: Se utilaza para graficar el tablero y que quede bonito <3

(Estan todos dentro de la carpeta ```T0```)

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. <Se asume que pueden haber celdas con una tortuga y una bomba y que estos no son validos por regla 3, pero no se espera recibir un tablero con un - y una bomba o un - y una tortuga en la misma celda. No se especifica su posibilidad en el enunciado asi que asumi que no se entregaran archivos asi. Por eso a la hora de chequear el valor de una bomba solo lo hace si esta sola.> 
2. <El codigo se vuelve muy ineficiente y poco optimo pasada cierta dimension, pero por como esta estructurado el algoritmo la solucion deberia encontrarse (o encontrar que no hay solucion) luego de cierto periodo de tiempo>
3. <Al intentar resolver un tablero ya resuelto se crea un archivo con el nombre archivo_sol_sol_.ext igual al archivo original, mi codigo no diferencia entre si se esta tratando de resolver algo ya resuelto o no>

PD: <El codigo se pone verdaderamente lento pasada cierta dimension de tablero (7x7) :c, pero en teoria funciona>


-------

## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. [Python Sudoku Solver - Computerphile](https://www.youtube.com/watch?v=G_UYXzGuqvM&ab_channel=Computerphile): de este video base el algoritmo de la recursion para resolver el tablero y está implementado alfinal de el archivo ```functions.py```. Su funcion es iterar todas las posibilidades para la solucionar del tablero y cada vez que hace la recursion chequea si el tablero es valido, de hacer todas las iteraciones y no encontrar nada retorna None.


## Agradecimientos
Mis dos gatitas lindas y [mi ultima neurona luego de escribir este README](https://www.youtube.com/watch?v=24yPYT5reo0&ab_channel=Vash)

