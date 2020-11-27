######
###### PRUEBA CODIGO ELIMINAR Pedido
######

try:
	cursor.execute('''INSERT INTO Pedido VALUES (12345, 66666, 141)''')
	cursor.execute('''INSERT INTO Pedido VALUES (1234, 6666, 113)''')
	cursor.execute('''INSERT INTO DetallePedido VALUES (1234, 10, 5)''')
except pyodbc.Error as error:
	print('Error insertando tuplas de la tabla DetallePedido:\n\t{}\n'.format(error))
except:
	print('Error no identificado insertando las tuplas de la tabla DetallePedido.')


cod_pedido=1234
print('Borrando los detalles del pedido asociados al pedido: {}'.format(cod_pedido))

try:
	cursor.execute('''DELETE FROM DetallePedido WHERE Cpedido = {} '''.format(cod_pedido))
except pyodbc.Error as error:
	print('Error borrando las tuplas de la tabla DetallePedido:\n\t{}\n'.format(error))
except:
	print('Error no identificado borrando las tuplas de la tabla DetallePedido.')


print('Borrando los pedidos con código: {}'.format(cod_pedido))


try:
	cursor.execute('''DELETE FROM Pedido WHERE Cpedido={}'''.format(cod_pedido))
except pyodbc.Error as error:
	print('Error borrando las tuplas de la tabla Pedidos:\n\t{}\n'.format(error))
except:
	print('Error no identificado borrando las tuplas de la tabla Pedidos.')

print('Todos los cambios se han hecho correctamente, aplicando los cambios a la base de datos')
conexion.commit()

#####
##### FIN PRUEBA
#####

