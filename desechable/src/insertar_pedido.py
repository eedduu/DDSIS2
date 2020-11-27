import pyodbc
import datetime

def insertar_pedido(c):

	print('Introduzca nuevo pedido:')
	cursor = c.cursor()

	cpedido = int(input('Código del Pedido: '))
	ccliente = int(input('Código del cliente: '))
	dia = int(input('Día: '))
	mes = int(input('Mes: '))
	anyo = int(input('Año: '))

	fecha = datetime.date(anyo,mes,dia)
	print(fecha)
	try:
		 cursor.execute('''INSERT INTO Pedido (Cpedido,Ccliente,FechaPedido)
						VALUES(?,?,TO_DATE(?,'YYYY-MM-DD'))''',(cpedido,ccliente,fecha))
	except pyodbc.Error as error:
		 print('Error insertando en la tabla Pedido:\n\t{}\n'.format(error))
	except:
		 print('Error no identificado insertando el pedido')


	print('Fin de introducción de pedido')
	c.commit()


