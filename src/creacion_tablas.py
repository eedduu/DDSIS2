import pyodbc

##################################################################################
##################################################################################
#############           Borrado y creación de tablas           ###################
##################################################################################
##################################################################################
#
#	Documentación de pyodbc: https://github.com/mkleehammer/pyodbc/wiki/Objects
#


print('Borrado y creación de la base de las tablas...')

# En UserID y Password cambiad los valores por los de vuestro DNI cuando lo useis
print("Conectando a la base de datos...")

conexion = pyodbc.connect('DRIVER={Devart ODBC Driver for Oracle};Direct=True;Host=oracle0;Service Name=practbd.oracle0.ugr.es;User ID=x7200029;Password=x7200029')

print("Se ha conectado satisfactoriamente.\n")


cursor = conexion.cursor()


print("Borrando tablas previamente creadas...")

try:
	cursor.execute('''DROP TABLE DetallePedido''')
except pyodbc.Error as error:
	print('Error borrando la tabla DetallePedido:\n\t{}\n'.format(error))
except:
	print('Error no identificado borrando la tabla DetallePedido.')

try:
	cursor.execute('''DROP TABLE Stock''')
except pyodbc.Error as error:
	print('Error borrando la tabla Stock:\n\t{}\n'.format(error))
except:
	print('Error no identificado borrando la tabla Stock.')

try:
	cursor.execute('''DROP TABLE Pedido''')
except pyodbc.Error as error:
	print('Error borrando la tabla Pedido:\n\t{}\n'.format(error))
except:
	print('Error no identificado borrando la tabla Pedido.')

print("Fin de borrado de tablas.\n")



print("Creando las tablas...")

cursor.execute('''
	CREATE TABLE Stock(
		Cproducto int,
		Cantidad int,
		PRIMARY KEY (Cproducto)
	)''')

cursor.execute('''
	CREATE TABLE Pedido(
		Cpedido int,
		Ccliente int,
		FechaPedido int,
		PRIMARY KEY (Cpedido)
	)''')


cursor.execute('''
	CREATE TABLE DetallePedido(
		Cpedido int,
		Cproducto int,
		Cantidad int,
		PRIMARY KEY (Cpedido,Cproducto),
		FOREIGN KEY (Cpedido) REFERENCES Pedido(Cpedido),
		FOREIGN KEY (Cproducto) REFERENCES Stock(Cproducto)
	)''')

print("Fin de creación de tablas.\n")

print("Insertando tuplas...\n")

cursor.execute('''INSERT INTO Stock VALUES (1,500)''')
cursor.execute('''INSERT INTO Stock VALUES (2,700)''')
cursor.execute('''INSERT INTO Stock VALUES (3,350)''')
cursor.execute('''INSERT INTO Stock VALUES (4,200)''')
cursor.execute('''INSERT INTO Stock VALUES (5,650)''')
cursor.execute('''INSERT INTO Stock VALUES (6,400)''')
cursor.execute('''INSERT INTO Stock VALUES (7,800)''')
cursor.execute('''INSERT INTO Stock VALUES (8,100)''')
cursor.execute('''INSERT INTO Stock VALUES (9,50)''')
cursor.execute('''INSERT INTO Stock VALUES (10,1000)''')


print("Fin de inserción de tuplas")

conexion.commit()


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

print("Desconectandose de la bases de datos...")
conexion.close()
print("Se ha desconectado satisfactoriamente.\n")
