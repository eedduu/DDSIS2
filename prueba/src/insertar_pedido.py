import pyodbc
import datetime

def insertar(conexion,cpedido, ccliente, fecha):

    print('Insertando pedido...')

    cursor = c.cursor()
    err = False

    try:
        cursor.execute('''INSERT INTO Pedido (Cpedido,Ccliente,FechaPedido) VALUES(?,?,TO_DATE(?,'YYYY-MM-DD'))''',(cpedido,ccliente,fecha))
    except pyodbc.Error as error:
        print('Error insertando en la tabla Pedido:\n\t{}\n'.format(error))
        err = True

    print('Fin de introducción de pedido\n')
    return err

def insertar_detalle(conexion,cpedido, cproducto, cantidad):

    print('Insertando detalle de pedido...')

    cursor = conexion.cursor()
    cursor.execute('''SELECT * FROM STOCK WHERE Cproducto = ?''',cproducto)

    stock_disponible = (cursor.fetchone())[1]

    if (stock_disponible < cantidad):
        print('Cantidad de producto no disponible, {} restantes.'.format(stock_disponible))
        return 0

    cursor = conexion.cursor()

    try:
        cursor.execute('''INSERT INTO DetallePedido (Cpedido,Cproducto,Cantidad) VALUES(?,?,?)''',(cpedido,cproducto,cantidad))
    except pyodbc.Error as error:
        print('Error insertando el detalle:\n\t{}\n'.format(error))
        return 0


    nueva_cantidad = stock_disponible - cantidad

    try:
        cursor.execute('''UPDATE Stock SET Cantidad = ? WHERE Cproducto = ?''',(nueva_cantidad, cproducto))
    except pyodbc.Error as error:
        print('Error actualizando la cantidad del producto en stock:\n\t{}\n'.format(error))
        return 0

    print('Insertado detalle de pedido\n')

