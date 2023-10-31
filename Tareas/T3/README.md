# Tarea 3: Adiccion al juego y a apostar


## Consideraciones generales :octocat:
Ojala disfrute el juego <3 este tmb lo hice con amor.

### Cosas implementadas y no implementadas :white_check_mark: :x:

☆ Para anunciar en que lineas y donde se encuentran las cosas usare esta (☆) estrellita al inicio <3
#### Networking: 18 pts (16%)
##### ✅ Protocolo
EL socket del sv y del cliente se instancian como TCP/IP

☆ servidor/main.py: linea 28

☆ cliente/backend/backend.py: linea 36

##### ✅ Correcto uso de sockets
Para instanciar los sockets del cliente se usa un try/except en caso de que esto falle, se instancia en:

☆ cliente/backend/backend.py: linea 38

y se conecta en el metodo connect_to_server y escucha con el metodo listen y listen_thread en:

☆ cliente/backend/backend.py: linea 55 a linea 72

Para el caso del sv, este recibe las conecciones en el metodo accept_connections_thread en:

☆ servidor/main.py: linea 72

Las aplicaciones no se bloquean entre ellas por tratar de escuchar un socket y los escucha con el metodo listen_client_thread en:

☆ servidor/main.py: linea 116

##### ✅ Conexión
Tanto el cliente como el sv mantienen una conexion sostenida en el tiempo :D

##### ✅ Manejo de Clientes
Se pueden conectar multiples clientes de manera correcta, en la sala de inicio se mostraran hasta 4 players pero **pueden haber hasta 8 en total**, 4 dentro maximo y 4 en la cola maximo, esto es porque añadi 8 ids y nombres y total en el parametros.json del sv xD (no se me ocurrieron mas nombres).

##### ✅ Desconexión Repentina
- Si el sv se desconecta por KeyboardInterrupt o por OSError entonces los usuarios seran notificados al respecto y podran cerrar el programa.
- Si un cliente se desconecta no altera al resto de los clientes, en caso de estan en partida este sera descartado y los demas seguiran jugando saltando su turno.

#### Arquitectura Cliente - Servidor: 18 pts (16%)
##### ✅ Roles
El cliente solo utiliza cosas dentro de la carpeta cliente y el servidor solo utiliza cosas dentro de la carpeta servidor. Es mas, probe conectandome de otro compu con el sv y funciono :3 wahoo.

El cliente solo envia sus acciones realizadas en el frontend, recibe la info del sv y con eso actualiza su intefaz. Procesa los mensajes del sv y lo emite al frontend en la funcion procesar_mensaje en: 

☆ cliente/backend/backend.py: linea 75

Y todas las acciones se envian usando los metodos bajo:

☆ cliente/backend/backend.py: linea 130

El servidor se encarga de procesar y validar las cosas que llegan del cliente en la funcion procesar_info en:

☆ servidor/main.py: linea 148

Si uste esta usando vscode (ns si funciona eso en otros lados xd) puede mantener apretado ctrl y apretar sobre la funcion llamada al procesar el msg para que lo lleve a donde esta el metodo uwu
Bajo esos metodos es donde distribuye, actualiza y almacena la info que le llegue si es que corresponde.

##### ✅ Consistencia
El sv maneja la info de todos y la distribuye de manera tal que todos tengan actualizada su inteface de igual forma. El unico metodo que uso para mandar toda la informacion es metodo enviar_info en:

☆ cliente/backend/backend.py: linea 55

esta funcion utiliza un lock para mandar la informacion, de esa manera no ocurren errores con los threads y demases :p, es el unico lugar donde utilizo un lock.

##### ✅ Logs
Los logs permiten visualizar todo lo indicado por el enunciado

detalles menores que queria mencionar:
 El unico detalle de estos es que como decidi implementar algo que cerrara el sv cuando acaba la partida o cuando solo quedan bots es que al final, cuando alguien gana los logs se buguean un poquito y se ven asi xD, por ej:

☆ nantino gano ☆

----------------------------'

Comienza el turno de: nantino

☆ Se cerro el servidor uwu ☆

☆--------------------------☆

podria considerar que los logs acaban cuando anuncia al ganador y el resto ignorarlo ;3;

El unico caso donde el sv no se cierra (aun que no se pide por enunciado pero igual queria mencionarlo) es cuando uno juega con bots y te sales durante los turnos de los bots xd, no se cae el sv ni nada, solo que no se cierra :pp

#### Manejo de Bytes: 26 pts (22%)
Como se menciona en el enunciado que para esta parte se vera el cripto.py dentro de cliente entonces las referencias a las lineas de codigo las hare a ese arhivo (que en todo caso es igual al que tiene el sv xD)
##### ✅ Codificación
Se usa el metodo codificar_largo_mesaje para codificar los primeros 4 bytes del largo del contenido en:

☆ cliente/Scripts/cripto.py: linea 63

Se usa el metodo codificar_numero para codificar el num identificador de cada bloque en:

☆ cliente/Scripts/cripto.py: linea 69 nice

Se usa el metodo chunks para separarlo en bloques como se menciona en el enunciado en:

☆ cliente/Scripts/cripto.py: linea 75

##### ✅ Decodificación
Se usa el metodo desencriptar_largo para decodificar los primeros 4 bytes del largo del contenido en:

☆ cliente/Scripts/cripto.py: linea 124

El metodo decodificar_numero para decodificar el num identificador de cada bloque en:

☆ cliente/Scripts/cripto.py: linea 129

Como no encontre necesario tener que decoficar el numero identificador de los bloques (pq encontre que para obtener los mensajes del chunk podia ignorarlo) alfinal no utlice dicha funcion, pero ahi esta :p.

Se usa el metodo separar_chunks para unir el mensaje devuelta en:

☆ cliente/Scripts/cripto.py: linea 134

##### ✅ Encriptación
Se hace con el metodo mencionado luego de cambiar el enunciado, es decir, sin usar la seed, en:

☆ cliente/Scripts/cripto.py: linea 12

##### ✅ Desencriptación
Se realiza el metodo inverso en:

☆ cliente/Scripts/cripto.py: linea 26

Tanto aqui como para la encriptacion puse como condicion de que para hacer el swap el largo del mensaje debia ser mayor que el num, pues de no ser asi ocurrian errores :p

##### ✅ Integración
Se utiliza el metodo enviar para realizar todo el protocolo resumido en una funcion en:

☆ cliente/Scripts/cripto.py: linea 105

#### Interfaz Gráfica: 22 pts (19%)
##### ✅ Ventana de Inicio
Una vez iniciado el sv, se ve la ventana correctamente, con todos los elementos pedidos en el enunciado. Ademas la info se actualiza correctamente. Si alguien apreta el boton iniciar se llevan a esos 4 jugaores a la ventana de juego, si no se completan los 4 se llena con bots. 

Si la sala esta llena se notifica a quien quedo en cola con un popup, y como mencione antes, pueden haber max 4 personas en cola :D wahoo. Si la partida ya fue iniciada y alguien se conecta se le notifica que ya hay una partida en curso y que se espere

##### ✅ Ventana de juego
Se ven y actualizan correctamente todos los elementos pedidos en el enunciado. 
Los jugadores solo pueden ver sus propios dados, a menos que alguien dude (se veran de todos) o usen un poder (vera los suyos y los de quien uso el poder).

Los jugadores pueden cuando es su turno:
- Anunciar valor: luego de anunciar pasa al sig turno, al inicio de la ronda y hasta que alguien anuncie el valor maximo anunciado mostrara cero.
- Pasar turno: pasando al siguiente en sentido antihorario
- Cambiar sus dados: actualizandolos por unos nuevos, aveces les tocan los mismos, no es que el metodo no funcione, sino que tiene mala cuea xD
- Dudar: duda la accion del jugador anterior (pasar con/sin valor paso o anunciar valor), si es el primer turno de la ronda no puede dudar. Se verifica si dudo correctamente o no y comienza otra ronda
- Usar poder: se presiona el boton de usar poder, de ahi se muestra un combobox con los nombres de los jugadores sobre los que se puede usar el poder, se confirma el target, si el jugador poseia los dados entonces se aplica el poder, si no aparece un popup indicando que no se poseen los dados correctos.
Si no es su turno entonces los botones quedan deshabilitados

Cuando se finaliza una ronda se actualiza la inteface con las vidas correspondientes. La vidas las indico asi:
corazon_lleno = '♥'
corazon_vacio = '♡'
Cuando el corazon esta lleno eso significa una vida cuando esta vacio es pq perdio esa vida. Por ej, ♥♥♥♡ simbolizaria 3 vidas y ♡♡♡♡ 0 vidas. (Estimado ayudante, se que probablemente ya sabia y entendia eso xd pero nunca esta demas explicarlo <3)

La partida termina cuando queda un solo jugador con vidas, o cuando todos los demas se desconectan xD. Se indica mediante un popup la victoria o derrota y se pide que se cierre la ventana uwu

#### Reglas de DCCachos: 22 pts (19%)
##### ✅ Inicio del juego
Se asigna aleatoreamente el primer jugador de la primera ronda en:

☆ servidor/main.py: linea 245

Para los jugadores, al iniciar la partida se crea una lista con la informacion de todos, para respetar el otrden antihorario y los turnos de los jugadores se rota por la lista usando 
```
self.turno_actual = (self.turno_actual + 1) % self.max_players
player = self.players_info[self.turno_actual]
```

Para iniciar el juego se usa el metodo info_ini_partida en:

☆ servidor/metodos_auxiliares.py: linea 14

para instanciar los diccionarios que representan los jugadores utilizo el metodo random_dados que retorna una tupla de dos valores aleatoreos del 1 al 6 correspondientes a los dados del jugador, dicho metodo se encuentra en:

☆ servidor/metodos_auxiliares.py: linea 97

##### ✅ Bots
Los bots siguien las instrucciones indicadas por el enunciado. Se creo una clase en:

☆ servidor/bot.py

y se instancia solo uno en el sv para usar el metodo play del bot, que sigue el patron planteado en el enunciado.

##### ✅ Ronda
El metodo validar_dados donde se validan los dados anunciados se encuentra en:

☆ servidor/metodos_auxiliares.py: linea 74

retorna si es valido (bool) y un error si es que valido es False. De esta forma el anuncia el valor si es valido o manda el error para que se muestre sobre el qlineedit del cliente que intento anunciar en el metodo validar_valor en:

☆ servidor/main.py: linea 263

Si uno pasa el valor anunciado mas alto se mantiene.

Al dudar se verifica si el anterior jugador mentia (sobre el valor que anuncio o si paso con/sin valor paso) o no y se resta la vida a quien corresponda.

Una vez se apreta el boton de cambiar dados se cambian los dados del jugador y los botones de dudar y cambiar dados quedan deshabilitados por el resto del turno del jugador (se habilitan para el proximo turno).

El metodo usar_poder se encarga de revisar si el set de los dados del jugador corresponde a 1 y 2 para quitarle una vida al target o 1 y 3 para asignarle la vida al target en un valor entre 1 y vidas iniciales si no se posee la combinacion correcta alerta al usuario mediante un popup, el metodo esta en:

☆ servidor/main.py: linea 309

##### ✅ Termino del juego
Se asigna como ganador a aquel jugador con vidas restantes o si es el ultimo jugador conectado (habiendo muerto los bots o sin bots si la sala esta llena inicialmente). :3

#### Archivos: 10 pts (9%)
##### ✅ Parámetros (JSON)
Todos los parametros y rutas de sprites utilizados estan dentro de alguno de los archivos parametros.json (donde corresponde).

En el sv los parametros se cargan con el metodo server_info en:

☆ servidor/main.py: linea 50

En el cliente los parametros se cargan con el metodo client_info en:

☆ cliente/backend/backend.py: linea 50

##### ✅ main.py
El sv se corre desde la carpeta T3 como:

python servidor/main.py port

donde port es un numero de puerto valido o tambien accepta:

python servidor/main.py

Eso es posible por el codigo en:

☆ servidor/main.py: linea 394 a linea 397 (asies vivo al limite B))
sdfgfhnbfghbnfgnbf

El cliente se corre desde la carpeta T3 como:

python cliente/main.py port

donde port es un numero de puerto valido o tambien accepta:

python cliente/main.py

Eso es posible por el codigo en:

☆ cliente/main.py: linea 94 a linea 97

(tengo entendido que el / depende del sistema operativo asi que use el que corresponda con el suyo uwu)

##### ✅ Cripto.py
Este modulo (que es igual tanto para sv como cliente) tiene dos metodos, enviar y recibir que resumen toda la encriptacion + codificacion y decoficacion + desencriptacion respecivamente en un solo metodo, que luego se llama para enviar o recibir informacion en el cliente y sv.
El metodo enviar esta en:

☆ .../Scripts/cripto.py: linea 105

El metodo recibir esta en:

☆ .../Scripts/cripto.py: linea 178


En el sv el metodo enviar se usa en el metodo enviar_info dentro del sv en:

☆ servidor/main.py: linea 55

y el metodo recibir se usa dentro del metodo listen_client_thread especificamente en:

☆ servidor/main.py: linea 141


En el cliente el metodo enviar se usa en el metodo enviar_info dentro del backend en:

☆ cliente/backend/backend.py: linea 131

y el metodo recibir se usa dentro del metodo listen_thread especificamente en:

☆ cliente/backend/backend.py: linea 69


#### Bonus: 4 décimas máximo
##### ❌ Cheatcodes
##### ❌ Turno con tiempo
hell nah

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py``` que esta dentro de la carpeta servidor para abrir el servidor xd y ```main.py``` que esta dentro de la carpeta cliente para abrir un cliente... Deben correrse desde la carpeta T3 como se menciono en la seccion de main.py un poco mas arriba :3

 Además se debe añadir:
1. La carpeta```Sprites``` que venia con la tarea en la carpeta ```cliente``` 



## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```socket```
2. ```json```
3. ```os```
4. ```sys```
5. ```threading```
6. ```time```: para usar sleep de forma que los bots se sientan mas realistas xD
7. ```random```
8. ```PyQt5```

nada ilegal xD y nada q ud deba descargar (asumiendo que tiene PyQt5)

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```metodos_auxiliares.py```: Creado para ~~que el main.py del sv no llegue a 400 lineas~~ poder (valga la redundancia) tener todos los metodos auxiliares al main.py del sv en un mismo lugar.
2. ```bot.py```:  Contiene a ```Bot``` que tiene la logica del bot :D
3. ```cripto.py```: cositas de encriptacion codificacion desencriptacion y decodificacion


## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1.**importante** las ventanas son 1080x1080 la de inicio y 1280x720 la de juego y no estan fixed, pls corregir con una pantalla grande ;W;
2. la cola de espera del inicio no supera los 4 clientes pues no quedan nombres disponibles 
3. NO SE DESCONECTE UN CLIENTE (apretando la cruz de arriba) MIENTRAS LOS BOTS ESTAN EN SU TURNO, pueden si es turno propio o de otro cliente
4. los main.py se corren desde la carpeta T3 uwu
5. cuando un jugador se desconecta asigna sus vidas a cero, entonces al pasar la ronda ese jugador aparecera con cero vidas (no es un bug)
6. cuando muestra que el valor ingresado no es valido el tipo de error sale sobre el Qlineedit en blanquito uwu
7. Si aun no se anuncia valor arriba en la interfase saldra que este es cero uwu
8. El numero de turno se resetea cuando comienza una nueva ronda
9. cuando se usa el poder hay 3 segundos donde se muestran los dados de quien ataco :D paciencia

PD: porfavor no se desconecte de la partida si esta jugando con bots y es turno de uno de ellos u.u


-------

## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. La ayudantia 10: La parte donde se conectan y escuchan los sockets, le hice ciertas modificaciones pero el codigo hecho en base a la ayudantia esta en:

☆ cliente/backend/backend.py: linea 40 a linea 48 y linea 55 a linea 75

☆ servidor/main.py: linea 45 a linea 48, linea 55 a linea 107 y linea 116 a linea 146



## Extra uwu

Bueno esta es la ultima tarea, queria darle muchas gracias ayudante por su trabajo <3 Ademas queria mostrarle los iconos que habia hecho para el juego pero que lei que no podia añadir :c ojala le gusten.

Morochita y chocolate son mis gatitas lindas y nantino es el gatito de mi pololo jiji, aqui estan los iconos:
![iconos](https://i.imgur.com/vbVa62d.jpg)

y la ui wonita:
![ui](https://i.imgur.com/2cxHvEW.jpg)

[Muchas gracias por todo <3](https://youtube.com/shorts/Fgi-Xnj433c?feature=share)