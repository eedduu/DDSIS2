import pyodbc
import config
import borrar_pedido
import creacion_tablas
import insertar_pedido
import datetime


# Conexión con la base de datos
conexion = pyodbc.connect('DRIVER={Devart ODBC Driver for Oracle};Direct=True;Host='+ config.host +';Service Name=' + config.service + ';User ID=' + config.userid + ';Password=' +  config.password)

# Cursor para hacer transacciones
aux = conexion.cursor()

# Hasta salir del menú
while True:

    # Opción del menú
    print('#################################################################')
    print('# Escoge una opción:                                            #')
    print('# 1.Borrado de tablas y creacion de tablas con 10 tuplas nuevas.#')
    print('# 2.Dar de alta nuevo pedido.                                   #')
    print('# 3.Borrar un pedido.                                           #')
    print('# 4.Salir del programa y cerrar la conexion.                    #')
    print('#################################################################')
    opc = int(input('\n Entrada: '))




    # Borrado, creación e insercción de tablas
    if opc==1:
        creacion_tablas.borrar_tablas(conexion)
        creacion_tablas.crear_tablas(conexion)
        creacion_tablas.insertar_tuplas_iniciales(conexion)

    # Insertado de pedido
    elif opc==2:
        
        print('Introduzca nuevo pedido:')

        # Datos de la tabla pedido
        cpedido = int(input('   Código del pedido: '))
        ccliente = int(input('  Código del cliente: '))
        dia = int(input('   Día: '))
        mes = int(input('   Mes: '))
        anyo = int(input('  Año: '))

        
        fecha_correcta = True

        # Comprueba que la fecha es válida
        try:
            fecha = datetime.date(anyo,mes,dia).__str__()
        except:
            print("Fecha inválida.")
            fecha_correcta = False

        # Savepoint para cancelar el pedido
        aux.execute("SAVEPOINT Cancelarpedido")

        # Si la fecha es correcta, introducir el pedido
        if fecha_correcta:
            err = insertar_pedido.insertar_pedido(conexion, cpedido, ccliente, fecha)
        else:
            err = True

        # Savepoint para cancelar los detalles
        aux.execute("SAVEPOINT Cancelardetalles")

        # Si se ha introducido el pedido
        if not err:
            # Hasta que se elija salir
            while True:
                 
                # Elegir opción
                print('#############################################')
                print('# Escoge una opción:                        #')
                print('# 1.Añadir detalle de producto.             #')
                print('# 2.Eliminar todos los detalles de producto.#')
                print('# 3.Cancelar pedido.                        #')
                print('# 4.Finalizar pedido.                       #')
                print('#############################################')
                opc2 = int(input('\n Entrada: '))


                # Crea un detalle pedido dado un codigo de producto y la cantidad
                if opc2==1:
                    cproducto = int(input('\n Código del producto: '))
                    cantidad = int(input('\n Cantidad: '))
                    insertar_pedido.insertar_detalle(conexion,cpedido,cproducto,cantidad)

                # Hace un rollback a antes de crear los detalles
                elif opc2==2:
                    aux.execute("ROLLBACK TO Cancelardetalles")
                    print('Detalles del pedido cancelados')

                # Hace un rollback a antes de hacer el pedido y todos sus detalles
                elif opc2==3:
                    aux.execute("ROLLBACK TO Cancelarpedido")
                    print('Pedido cancelado')
                    break

                # Confirma todos los cambios
                elif opc2==4:
                    aux.commit()
                    break

                # Opción no válida
                else:
                    print('Opcion no valida, vuelva a elegir.\n')


    # Borra un pedido dado su código
    elif opc==3:
        cpedido = int(input('Código del pedido: '))
        borrar_pedido.borrar_pedido(conexion,cpedido)
    # Sale del menú
    elif opc==4:
        break
    # Opcion no valida
    else:
        print('Opcion no valida, vuelva a elegir.\n')


conexion.commit()

# Nos desconectamos 
print('Desconectandose de la bases de datos...')
conexion.close()
print('Se ha desconectado satisfactoriamente.\n')
