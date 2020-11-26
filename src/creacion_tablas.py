import pyodbc

##################################################################################
##################################################################################
#############           Borrado y creación de tablas           ###################
##################################################################################
##################################################################################
#
#	Documentación de pyodbc: https://github.com/mkleehammer/pyodbc/wiki/Objects
#


def borrar_tablas(c):
	
	print('Borrando las tablas...')

	cursor = c.cursor()


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

	print('Fin de borrado de tablas.\n')
	
	c.commit()


def crear_tablas(c):

	print('Creando las tablas...')
	cursor = c.cursor()

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
	except:
		print('Error no identificado en la creación de tablas.')

	c.commit()
	print('Fin de creación de tablas.\n')


def insertar_tuplas_iniciales(c):
	print('Insertando tuplas...')
	cursor = c.cursor()

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
	except:
		print('Error no identificado en la creación de tablas.')

	c.commit()

	print('Fin de inserción de tuplas.\n')


