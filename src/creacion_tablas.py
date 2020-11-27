##################################################################################
##################################################################################
#############           Borrado y creación de tablas           ###################
##################################################################################
##################################################################################
#
#	Documentación de pyodbc: https://github.com/mkleehammer/pyodbc/wiki/Objects
#


import pyodbc

#
#	Borrado de tablas
#

def borrar_tablas(conexion):
	
	print('Borrando las tablas...')
	cursor = conexion.cursor()

	# Borrado de tabla DetallePedido
	try:
		cursor.execute('''DROP TABLE DetallePedido''')
	except pyodbc.Error as error:
		print('Error borrando la tabla DetallePedido:\n\t{}\n'.format(error))

	# Borrado de tabla Stock
	try:
		cursor.execute('''DROP TABLE Stock''')
	except pyodbc.Error as error:
		print('Error borrando la tabla Stock:\n\t{}\n'.format(error))

	# Borrado de tabla Pedido
	try:
		cursor.execute('''DROP TABLE Pedido''')
	except pyodbc.Error as error:
		print('Error borrando la tabla Pedido:\n\t{}\n'.format(error))

	print('Fin de borrado de tablas.\n')





#
# Creación de las tablas
#

def crear_tablas(conexion):

	print('Creando las tablas...')
	cursor = conexion.cursor()


	# Creacion de las tablas Stock, Pedido y DetallePedido
	try:
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

	except pyodbc.Error as error:
		print('Error creando las tablas:\n\t{}\n'.format(error))

	print('Fin de creación de tablas.\n')


#
# Insertar tuplas iniciales de stock
#
def insertar_tuplas_iniciales(conexion):

	print('Insertando tuplas...')
	cursor = conexion.cursor()

	# Insercción de tuplas 
	# En caso de error en mitad del try se ejecuta rollback 
	# y no se añade ninguna tupla
	try:
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
	except pyodbc.Error as error:
		print('Error creando las tablas:\n\t{}\n'.format(error))
		conexion.rollback()
	finally:
		conexion.commit()

	print('Fin de inserción de tuplas.\n')




