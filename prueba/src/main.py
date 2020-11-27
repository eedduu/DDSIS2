import pyodbc
import config
import borrar_pedido
import creacion_tablas
import insertar_pedido

conexion = pyodbc.connect('DRIVER={Devart ODBC Driver for Oracle};Direct=True;Host='+ config.host +';Service Name=' + config.service + ';User ID=' + config.userid + ';Password=' +  config.password)

aux = conexion.cursor()

while True:

    print('Escoge una opción:')
    print(' 1.Borrado de tablas y creacion de tablas con 10 tuplas nuevas.')
    print(' 2.Dar de alta nuevo pedido.')
    print(' 3.Borrar un pedido.')
    print(' 4.Salir del programa y cerrar la conexion.')
    opc = int(input('\n Entrada: '))

    if opc==1:
        creacion_tablas.borrar_tablas(conexion)
        creacion_tablas.crear_tablas(conexion)
        creacion_tablas.insertar(conexion)
    elif opc==2:
        aux.execute("savepoint uno")
        
        print('Introduzca nuevo pedido:')
        
        cpedido = int(input('Código del pedido: '))
        ccliente = int(input('Código del cliente: '))
        dia = int(input('Día: '))
        mes = int(input('Mes: '))
        anyo = int(input('Año: '))

        fecha_correcta = True

        try:
            fecha = datetime.date(anyo,mes,dia).__str__()
        except:
            print("Fecha inválida.")
            fecha_correcta = False

        if fecha_correcta:
            err = insertar_pedido.insertar(conexion, cpedido, ccliente, fecha)
        else:
            err = not fecha_correcta

        if not err:
            while True:
                print('Escoge una opción:')
                print(' 1.Añadir detalle de producto.')
                print(' 2.Eliminar todos los detalles de producto.')
                print(' 3.Cancelar pedido.')
                print(' 4.Finalizar pedido.')
                opc2 = int(input('\n Entrada: '))

                if opc2==1:
                    aux.execute("savepoint dos")
                    cproducto = int(input('\n Código del producto: '))
                    cantidad = int(input('\n Cantidad: '))
                    insertar_pedido.insertar_detalle(conexion,cpedido,cproducto,cantidad)
                elif opc2==2:
                    aux.execute("rollback_to dos")
                    print('Detalles del pedido cancelados')
                elif opc2==3:
                    aux.execute("rollback_to uno")
                    print('Pedido cancelado')
                elif opc2==4:
                    aux.commit()
                    break
                else:
                    print('Opcion no valida, vuelva a elegir.\n')

    elif opc==3:
        cpedido = int(input('Código del pedido: '))
        borrar_pedido.borrar(conexion,cpedido)
    elif opc==4:
        break
    else:
        print('Opcion no valida, vuelva a elegir.\n')


conexion.commit()
print('Desconectandose de la bases de datos...')
conexion.close()
print('Se ha desconectado satisfactoriamente.\n')
