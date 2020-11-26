import pyodbc
import datetime

print('Conectando a la base de datos...')

c = pyodbc.connect('DRIVER={Devart ODBC Driver for Oracle};Direct=True;Host=oracle0;Service Name=practbd.oracle0.ugr.es;User ID=x7147725;Password=x7147725')

c.autocommit = False

print("Se ha conectado satisfactoriamente.\n")


##################################################################################
##################################################################################
#############           Borrado y creación de tablas           ###################
##################################################################################
##################################################################################
#
#	Documentación de pyodbc: https://github.com/mkleehammer/pyodbc/wiki/Objects
#


def borrar_tablas():
	
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


def crear_tablas():

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


def insertar_tuplas_iniciales():
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


##################################################################################
##################################################################################
#############          Insertado de pedidos			            ###################
##################################################################################
##################################################################################
#

def insertar_pedido():

	print('Introduzca nuevo pedido:')
	cursor = c.cursor()

	cpedido = int(input('Código del Pedido: '))
	ccliente = int(input('Código del cliente: '))
	dia = int(input('Día: '))
	mes = int(input('Mes: '))
	anyo = int(input('Año: '))

	fecha = datetime.date(anyo,mes,dia).__str__()
	try:
		 cursor.execute('''INSERT INTO Pedido (Cpedido,Ccliente,FechaPedido)
						VALUES(?,?,TO_DATE(?,'YYYY-MM-DD'))''',(cpedido,ccliente,fecha))
	except pyodbc.Error as error:
		 print('Error insertando en la tabla Pedido:\n\t{}\n'.format(error))
	except:
		 print('Error no identificado insertando el pedido')


	print('Fin de introducción de pedido')
	c.commit()










































while True:

	print('Escoge una opción:')
	print(' 1.Borrado de tablas y creacion de tablas con 10 tuplas nuevas.')
	print(' 2.Dar de alta nuevo pedido.')
	print(' 3.Borrar un pedido.')
	print(' 4.Salir del programa y cerrar la conexion.')
	opc = int(input('\n Entrada: '))

	if opc==1:
		borrar_tablas()
		crear_tablas()
		insertar_tuplas_iniciales()
	elif opc==2:
		insertar_pedido()
		print('OPCION 2')
	elif opc==3:
		print('OPCION 3')
	elif opc==4:
		break
	else:
		print('Opcion no valida, vuelva a elegir.\n')


	
print('Desconectandose de la bases de datos...')
c.close()
print('Se ha desconectado satisfactoriamente.\n')
	
