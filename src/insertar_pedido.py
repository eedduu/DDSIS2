##################################################################################
##################################################################################
#############          Insertado de pedidos y detalles         ###################
##################################################################################
##################################################################################


import pyodbc
import datetime

# Insertar tupla pedido
# return: True si se ha producido un error
#			 False si no se ha producido un error
def insertar_pedido(conexion,cpedido, ccliente, fecha):

    print('Insertando pedido...')

    cursor = conexion.cursor()
    # Variable que guarda si se ha producido un error
    err = False

    # Introducir pedido 
    try:
        cursor.execute('''INSERT INTO Pedido (Cpedido,Ccliente,FechaPedido) VALUES(?,?,TO_DATE(?,'YYYY-MM-DD'))''',(cpedido,ccliente,fecha))
    except pyodbc.Error as error:
        print('Error insertando en la tabla Pedido:\n\t{}\n'.format(error))
        # Se ha producido un error
        err = True

    print('Fin de introducción de pedido\n')
    return err

#
# Insertar detalle de un pedido
#
def insertar_detalle(conexion,cpedido, cproducto, cantidad):

    print('Insertando detalle de pedido...')

    if (cantidad < 1):
        print ('La cantidad debe ser positiva.')
        return

    cursor = conexion.cursor()
    # Busca la tupla del producto
    cursor.execute('''SELECT * FROM STOCK WHERE Cproducto = ?''',cproducto)

    # Tupla del producto
    producto = cursor.fetchone()

    # Si no existe un producto con ese codigo
    if producto == None:
        print ('No hay ningún producto con ese código.')
        return
    
    # Vemos la cantidad que queda
    stock_disponible = producto[1]
	
    # Vemos que queda suficiente stock
    if (stock_disponible < cantidad):
        print('Cantidad de producto no disponible, {} restantes.'.format(stock_disponible))
        return

    # Reinicio el cursor para hacer insercciones
    cursor = conexion.cursor()

    # Creo un savepoint en caso de fallo al actualizar la cantidad
    cursor.execute('SAVEPOINT Predetalle')

    # Inserto el detalle pedido
    try:
        cursor.execute('''INSERT INTO DetallePedido (Cpedido,Cproducto,Cantidad) VALUES(?,?,?)''',(cpedido,cproducto,cantidad))
    except pyodbc.Error as error:
        print('Error insertando el detalle:\n\t{}\n'.format(error))
        return 

    # Nueva cantidad de stock del producto
    nueva_cantidad = stock_disponible - cantidad

    # Actualizo la tupla producto con su nueva cantidad
    # Si falla la actualización cancelo el detallepedido completamente
    try:
        cursor.execute('''UPDATE Stock SET Cantidad = ? WHERE Cproducto = ?''',(nueva_cantidad, cproducto))
    except pyodbc.Error as error:
        print('Error actualizando la cantidad del producto en stock:\n\t{}\n'.format(error))
        cursor.execute('ROLLBACK TO Predetalle')
        return 

    print('Insertado detalle de pedido\n')

