import pyodbc
import config
cnxn = pyodbc.connect('DRIVER={Devart ODBC Driver for Oracle};Direct=True;Host='+ config.host +';Service Name=' + config.service + ';User ID=' + config.userid + ';Password=' +  config.password)
