def borrar_pedido(conexion, cod_pedido):
    cursor= conexion.cursor()

    print('Borrando los detalles del pedido asociados al pedido: {}'.cod_pedido)

    try:
        cursor.execute('''DELETE * FROM DetallePedido WHERE Cpedido=cod_pedido ''')
    except pyodbc.Error as error:
    	print('Error borrando las tuplas de la tabla DetallePedido:\n\t{}\n'.format(error))
    except:
    	print('Error no identificado borrando las tuplas de la tabla DetallePedido.')


    print('Borrando los pedidos con código: {}'.cod_pedido)


    try:
        cursor.execute('''DELETE * FROM Pedidos WHERE Cpedido=cod_pedido''')
    except pyodbc.Error as error:
    	print('Error borrando las tuplas de la tabla Pedidos:\n\t{}\n'.format(error))
    except:
    	print('Error no identificado borrando las tuplas de la tabla Pedidos.')

    print('Todos los cambios se han hecho correctamente, aplicando los cambios a la base de datos')
    conexion.commit()
