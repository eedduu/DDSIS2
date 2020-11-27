##################################################################################
##################################################################################
#############       			   Borrado de pedidos					###################
##################################################################################
##################################################################################


import pyodbc


#
# borra un pedido
#
def borrar_pedido(conexion, cod_pedido):

    cursor= conexion.cursor()
    print('...Borrando los detalles del pedido asociados al pedido: {}'.format(cod_pedido))

    cursor.execute('SAVEPOINT Preborrado')
 
    try:
        cursor.execute('''DELETE FROM DetallePedido WHERE Cpedido = {} '''.format(cod_pedido))
    except pyodbc.Error as error:
        conexion.rollback()
        print('...Error borrando las tuplas de la tabla DetallePedido:\n\t{}\n'.format(error))
        return

    print('...Borrando los pedidos con código: {}'.format(cod_pedido))

    try:
        cursor.execute('''DELETE FROM Pedido WHERE Cpedido={}'''.format(cod_pedido))
    except pyodbc.Error as error:
        print('...Error borrando las tuplas de la tabla Pedidos:\n\t{}\n'.format(error))
        cursor.execute('ROLLBACK TO Preborrado')
        return

    # Confirmar los cambios
    cursor.commit()
