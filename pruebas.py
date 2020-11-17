import pyodbc 

print("Conectando a la base de datos...")
cnxn = pyodbc.connect('DRIVER={Devart ODBC Driver for Oracle};Direct=True;Host=oracle0;Service Name=practbd.oracle0.ugr.es;User ID=x7036964;Password=x7036964')
print("Se ha conectado a la base de datos.")



print("Desconectandose de la bases de datos...")
cnxn.close()
print("Se ha desconectado de la base de datos.")
