import pyodbc


def borradoycreacion(conexion):
	print('Borrado y creación de la base de las tablas...')

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
	
	
	print("Fin de inserción de tuplas\n")
	
	

def borrar_pedido(conexion, cod_pedido):
    cursor= conexion.cursor()

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


print("Conectando a la base de datos...")

conexion = pyodbc.connect('DRIVER={Devart ODBC Driver for Oracle};Direct=True;Host=oracle0;Service Name=practbd.oracle0.ugr.es;User ID=x7147725;Password=x7147725')

print("Se ha conectado satisfactoriamente.\n")


print("Buenos dias, escoge una opcion de las siguientes:\n1.Borrado de tablas y creacion de tablas con 10 tuplas nuevas\n2.Dar de alta nuevo pedido\n3.Borrar un pedido\n4.Salir del programa y cerrar la conexion\nNº de opcion:")

opc = input()

while opc!="4":
	if opc=="1":
		borradoycreacion(conexion)
	elif opc=="2":
		print("Dando de alta nuevo pedido\n")
		cursor= conexion.cursor()
		cursor.execute('''INSERT INTO Pedido VALUES (1,1,TO_DATE('26/11/2020','dd/mm/yyyy'))''')
		
	elif opc=="3":
		print("Introduzca el codigo de pedido a borrar:\n")
		cod_pe=input()
		borrar_pedido(conexion,cod_pe)
	else:
		print("Opcion no valida, vuelva a insertar\n")
	
	print("Escoge una opcion de las siguientes:\n1.Borrado de tablas y creacion de tablas con 10 tuplas nuevas\n2.Dar de alta nuevo pedido\n3.Borrar un pedido\n4.Salir del programa y cerrar la conexion\nNº de opcion:")
	opc = input()

	
print("Desconectandose de la bases de datos...")
conexion.close()
print("Se ha desconectado satisfactoriamente.\n")
	
