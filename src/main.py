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

	try:
		cursor.execute('''DROP TABLE Stock''')
	except pyodbc.Error as error:
		print('Error borrando la tabla Stock:\n\t{}\n'.format(error))

	try:
		cursor.execute('''DROP TABLE Pedido''')
	except pyodbc.Error as error:
		print('Error borrando la tabla Pedido:\n\t{}\n'.format(error))

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

	c.commit()

	print('Fin de inserción de tuplas.\n')


##################################################################################
##################################################################################
#############          Insertado de pedidos y detalles         ###################
##################################################################################
##################################################################################


def insertar_pedido(cpedido, ccliente, fecha):

	print('Insertando pedido...')

	cursor = c.cursor()
	err = False
	try:
		cursor.execute('''INSERT INTO Pedido (Cpedido,Ccliente,FechaPedido)
						VALUES(?,?,TO_DATE(?,'YYYY-MM-DD'))''',(cpedido,ccliente,fecha))
	except pyodbc.Error as error:
		print('Error insertando en la tabla Pedido:\n\t{}\n'.format(error))
		err = True


	print('Fin de introducción de pedido\n')
	c.commit()
	return err


def insertar_detalle(cpedido, cproducto, cantidad):
	
	print('Insertando detalle de pedido...')

	cursor = c.cursor()
	cursor.execute('''SELECT * FROM STOCK WHERE Cproducto = ?''',cproducto)

	if cursor.arraysize == 0:
		print('No existe ningún producto con ese código...')
		return 0
	
	stock_disponible = (cursor.fetchone())[1]	
	
	if (stock_disponible < cantidad):
		print('Cantidad de producto no disponible, {} restantes.'.format(stock_disponible))
		return 0

	cursor = c.cursor()

	try:
		cursor.execute('''INSERT INTO DetallePedido (Cpedido,Cproducto,Cantidad)
								VALUES(?,?,?)''',(cpedido,cproducto,cantidad))
	except pyodbc.Error as error:
		print('Error insertando el detalle:\n\t{}\n'.format(error))
		return 0
	

	nueva_cantidad = stock_disponible - cantidad

	try:
		cursor.execute('''UPDATE Stock SET Cantidad = ? 
					WHERE Cproducto = ?''',(nueva_cantidad, cproducto))
	except pyodbc.Error as error:
		print('Error actualizando la cantidad del producto en stock:\n\t{}\n'.format(error))
		return 0

	print('Insertado detalle de pedido\n')
	c.commit()




##################################################################################
##################################################################################
#############       			   Borrado de pedidos					###################
##################################################################################
##################################################################################


def borrar_pedido(cpedido):

	print('Borrando pedido y todos sus detalles...')
	cursor = c.cursor()

	try:
		cursor.execute('DELETE FROM DetallePedido WHERE Cpedido = {} '.format(cpedido))
	except pyodbc.Error as error:
		print('Error borrando las tuplas de la tabla DetallePedido:\n\t{}\n'.format(error))
		return 0

	try:
		cursor.execute('''DELETE FROM Pedido WHERE Cpedido={}'''.format(cpedido))
	except pyodbc.Error as error:
		print('Error borrando las tuplas de la tabla Pedidos:\n\t{}\n'.format(error))
		return 0

	c.commit()


###################################################################################
###################################################################################



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

		print('Introduzca nuevo pedido:')
		cpedido = int(input('Código del pedido: '))
		ccliente = int(input('Código del cliente: '))
		dia = int(input('Día: '))
		mes = int(input('Mes: '))
		anyo = int(input('Año: '))

		fecha_correcta = True		

		try:
			fecha = datetime.date(anyo,mes,dia).__str__()
		except:
			print("Fecha inválida.")
			fecha_correcta = False
	
		if fecha_correcta:
			err = insertar_pedido(cpedido, ccliente, fecha)
		else:
			err = not fecha_correcta

		if not err:
			while True:
				print('Escoge una opción:')
				print(' 1.Añadir detalle de producto.')
				print(' 2.Eliminar todos los detalles de producto.')
				print(' 3.Cancelar pedido.')
				print(' 4.Finalizar pedido.')
				opc2 = int(input('\n Entrada: '))				

				if opc2==1:
					cproducto = int(input('\n Código del producto: '))
					cantidad = int(input('\n Cantidad: '))
					insertar_detalle(cpedido,cproducto,cantidad)
				elif opc2==2:
					# Aqui va un rollback(Falta el savepoint)
					print('OPCION 2.2')
				elif opc2==3:
					#Aqui va otro rollback(Falta el savepoint)
					print('OPCION 2.3')
				elif opc2==4:
					#Aqui va un commit()
					break
				else:
					print('Opcion no valida, vuelva a elegir.\n')

	elif opc==3:
		cpedido = int(input('Código del pedido: '))
		borrar_pedido(cpedido)
	elif opc==4:
		break
	else:
		print('Opcion no valida, vuelva a elegir.\n')


c.commit()	
print('Desconectandose de la bases de datos...')
c.close()
print('Se ha desconectado satisfactoriamente.\n')
	
