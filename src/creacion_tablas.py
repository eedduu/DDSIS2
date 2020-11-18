import pyodbc

##################################################################################
##################################################################################
#############           Borrado y creación de tablas           ###################
##################################################################################
##################################################################################
#
#	Documentación de pyodbc: https://github.com/mkleehammer/pyodbc/wiki/Objects
#


print("\nBorrado y creación de la base de las tablas...\n")

# En UserID y Password cambiad los valores por los de vuestro DNI cuando lo useis
print("Conectando a la base de datos...")

conexion = pyodbc.connect('DRIVER={Devart ODBC Driver for Oracle};Direct=True;Host=oracle0;Service Name=practbd.oracle0.ugr.es;User ID=x7036964;Password=x7036964')

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
		FechaPedido date,
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

conexion.commit()

print("Desconectandose de la bases de datos...")
conexion.close()
print("Se ha desconectado satisfactoriamente.\n")
