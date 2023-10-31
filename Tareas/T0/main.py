import functions
import tablero as t
import solucion

# Se preguntara al usuario el nombre del archivo que desea abrir
print('--- Menu de Inicio ---\n')
nombre_archivo = input('Por favor ingrese nombre del archivo (no se olvide de la extension): ')


if functions.verificar_archivo(nombre_archivo):
    functions.menu()
    datos_archivo = nombre_archivo.split('.')
    nombre = datos_archivo[0]
    extension = datos_archivo[1]
    opcion = input('Indique su opcion (1, 2, 3, 4, 0): ')

    # Comprobamos que la opcion sea valida
    while opcion not in ['1', '2', '3', '4', '0']:
        print('\nOpcion invalida, intentelo denuevo.\n')
        opcion = input('Indique su opcion (1, 2, 3, 4, 0): ')

    # Ahora en base a la decision del usuario tomamos distintos caminos
    while opcion != '0':
        tablero = functions.cargar_tablero(nombre_archivo)

        # Mostrar el tablero
        if opcion == '1':
            print('\n--- Tablero ---\n')
            t.imprimir_tablero(tablero)
            print('')

        # Verificar la validez del de las tortugas y bombas
        elif opcion == '2':
            bombas_invalidas = functions.verificar_valor_bombas(tablero)
            tortugas_invalidas = functions.verificar_tortugas(tablero)
            print('\n--- Estado del Tablero ---')
            if bombas_invalidas == 0 and tortugas_invalidas == 0:
                print('\n  Bombas y Tortugas Validas\n')
            else:
                print('\n Bombas y Tortugas no Validas\n')

        # Verificar si se cumnplen las reglas del uno al cuatro
        elif opcion == '3':
            valido = functions.tablero_valido(tablero)

            print('\n--- Estado del Tablero ---')
            if valido:
                print('\n  El Tablero es Valido\n')
            else:
                print('\n El Tablero No es Valido\n')

        elif opcion == '4':
            sol = solucion.solucionar_tablero(tablero)
            print('\nCargando...\n')
            if sol is not None:
                print('Se encontro una solucion :D')
                print('\n--- Tablero ---\n')
                t.imprimir_tablero(sol)
                nombre_solucion = nombre + '_sol.' + extension
                functions.guardar_tablero(nombre_solucion, sol)
                print('')
            else:
                print('No se encontro una solucion :c\n')
        # Preguntamos al usuario si desea realizar otra accion
        functions.menu()
        opcion = input('Indique su opcion (1, 2, 3, 4, 0): ')

        # Comprobamos que la opcion sea valida
        while opcion not in ['1', '2', '3', '4', '0']:
            print('\nOpcion invalida, intentelo denuevo.\n')
            opcion = input('Indique su opcion (1, 2, 3, 4, 0): ')

    if opcion == '0':
        print('Save the world my final message, good bye')


else:
    print('Nombre de archivo invalido.')
