import pyodbc
import config
import datetime

conexion = pyodbc.connect('DRIVER={Devart ODBC Driver for Oracle};Direct=True;Host=oracle0;Service Name=practbd.oracle0.ugr.es;User ID=x7036964;Password=x7036964')

cursor = conexion.cursor()


print("Introduzca nuevo pedido:\n")

print("Código del Pedido: ")
cpedido = input()

print("Código del cliente: ")
ccliente = input()

print("Fecha pédido (Formato númerico):\n")

print("Día:")
dia = input()
print("Mes:")
mes = input()
print("Año:")
anyo = input()

fecha = datetime.datetime(int(anyo),int(mes),int(dia))

try:
    cursor.execute("insert into Pedido (Cpedido,Ccliente,FechaPedido) values(?,?,?)",(cpedido, ccliente,fecha))
except pyodbc.Error as error:
    print('Error insertando en la tabla Pedido:\n\t{}\n'.format(error))
except:
    print('Error no identificado insertando el pedido')

print("Se ha introducido el pedido en la base de datos")
conexion.commit()


conexion.close()
