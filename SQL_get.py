import mysql.connector
from datetime import datetime

def Abrir_Conexion():
	#Conecta con la Base de Datos ( DB [Data Base])
	''' 
	-h brzq0rsktp2der07uwg0-mysql.services.clever-cloud.com 
	-P 3306 
	-u uney766i2wqkm0an 
	-DB brzq0rsktp2der07uwg0
	PASSWORD: pHCSKl7UIq57Di9Qurc1

	<<--CONEXION DESDE TERMINAL MYSQL-->>
	#mysql -h brzq0rsktp2der07uwg0-mysql.services.clever-cloud.com -P 3306 -u uney766i2wqkm0an -p brzq0rsktp2der07uwg0
	#Password: pHCSKl7UIq57Di9Qurc1
	'''
	return mysql.connector.connect(
		host="brzq0rsktp2der07uwg0-mysql.services.clever-cloud.com",
		password="pHCSKl7UIq57Di9Qurc1",
		user="uney766i2wqkm0an",
		port="3306",
		db="brzq0rsktp2der07uwg0"
		) #Retorna la conexion establecida

def Cerrar_Conexion( sql ):
	sql.close()

def Ver_Tablas_de_DB( sql ):
	# sql: mysql.cursor -> Siendo mysql la conexion con DB [primero>Abrir_Conexion()]
	# -->> Retorna un lista con el nombre de todas las tablas de DB
	cur = sql.cursor()
	cur.execute("SHOW TABLES;")
	
	Tablas = []
	for campo in cur.fetchall():
		Tablas.append(campo[0])
	return Tablas 

def Ver_Tabla( sql , Nombre_Tabla ):
	# sql: mysql.cursor -> Siendo mysql la conexion con DB [primero>Abrir_Conexion()]
	# Nombre_Tabla: Nombre de la Tabla a ver
	# -->> Retorna una tupla con todas las filas de DB

	cur = sql.cursor()
	Nombres_Campos_Tabla = Ver_Nombres_Campos_Tabla( sql , Nombre_Tabla )

	cur.execute("SELECT * FROM " + Nombre_Tabla)
	Tabla = []
	for fila in cur.fetchall():
		Diccionario = {}
		for x in range( len( Nombres_Campos_Tabla ) ):
			Diccionario[ Nombres_Campos_Tabla[x] ] = fila[x]  
		Tabla.append( Diccionario )
	return( Tabla ) #Retorna una lista con todas las filas de DB

def Ver_Campos_y_Atributos_Tabla( sql , Nombre_Tabla ):
	# Retorna los campos de la Tabla
	# sql: mysql.cursor -> Siendo mysql la conexion con DB [primero>Abrir_Conexion()]
	# Nombre_Tabla: Nombre de la Tabla a ver DESCRIPCION
	# -->> Retorna una lista con todas las filas de DB
	cur = sql.cursor()
	cur.execute("DESCRIBE " + Nombre_Tabla)
	return( cur.fetchall() ) #Retorna una lista con todos los Campos de DB

def Ver_Nombres_Campos_Tabla( sql , Nombre_Tabla ):
	#Retorna lista con los nombres de los campos de la Tabla 'Nombre_Tabla'
	Campos_Tabla = Ver_Campos_y_Atributos_Tabla( sql , Nombre_Tabla )
	Nombres_Campo_Tabla = []
	for campo in Campos_Tabla:
		Nombres_Campo_Tabla.append( campo[0] )
	return Nombres_Campo_Tabla

def Insert_SQL( sql , Nombre_Tabla , Diccionario_Campos ):
	#sql: objeto con conexion establecida en DB
	#Nombre_Tabla: Nombre de la tabla a Insertar
	#Diccionario_Campos: Diccionario para ingresar a la Tabla	
	cur = sql.cursor()

	Campos_Tabla = '('
	for Campo in Diccionario_Campos.keys():
		Campos_Tabla += Campo + ','

	Campos_Tabla = Campos_Tabla[0:len(Campos_Tabla)-1] + ')'
	if( len(Diccionario_Campos.values()) == 1 ):
		Consulta = "INSERT INTO " + Nombre_Tabla + Campos_Tabla + " VALUES " + str( tuple(Diccionario_Campos.values()) )
		Consulta = Consulta[0:len(Consulta)-2] + ')' #Nos sale una coma al final y la sacamos
		cur.execute( Consulta )
	else:
		cur.execute("INSERT INTO " + Nombre_Tabla + Campos_Tabla + " VALUES " + str( tuple(Diccionario_Campos.values()) ) )
	
	sql.commit() #Guardamos los cambios

def Insert_SQL_mult_values( sql , Nombre_Tabla , Diccionario_Campos , Atributo_List_Multiple ):
	#Genera declaracion de insert de varios values.
	
	Campos_Tabla = '('
	Campo_Values = "("
	for Campo in Diccionario_Campos.keys():
		if Campo != Atributo_List_Multiple:
			Campos_Tabla += Campo + ','
			if type(Diccionario_Campos[Campo]) == str:
				Campo_Values += "'{}'".format( Diccionario_Campos[Campo] ) + "," #Tipo String
			elif type(Diccionario_Campos[Campo]) == int or type(Diccionario_Campos[Campo]) == float:
				Campo_Values += str(Diccionario_Campos[Campo]) + "," #Tipo Float
			elif type(Diccionario_Campos[Campo]) == datetime:
				Campo_Values += "TO_DATE('{}','DD/MM/YYYY')".format( Diccionario_Campos[Campo] ) + "," #Tipo Date

	Campos_Tabla += Atributo_List_Multiple #Dejamos el atributo lista al final
		
	Campos_Tabla += ')'

	Consulta = "INSERT INTO " + Nombre_Tabla + Campos_Tabla + " VALUES "
	ValuesTotal = ""
	for Atributo_list in Diccionario_Campos[Atributo_List_Multiple]:
		if type(Atributo_list) == str:
			ValuesTotal += Campo_Values + "'{}'".format( Atributo_list ) +")," #Tipo String
		elif type(Atributo_list) == int or type(Diccionario_Campos[Campo]) == float:
 			ValuesTotal += Campo_Values + str(Atributo_list) +")," #Tipo Float
		elif type(Atributo_list) == datetime:
			ValuesTotal += Campo_Values + "TO_DATE('{}','DD/MM/YYYY')".format( Atributo_list ) +"),"

	ValuesTotal = ValuesTotal[0:len(ValuesTotal)-1]
	Consulta += ValuesTotal

	print(Consulta)

	cur = sql.cursor()
	cur.execute( Consulta )
	sql.commit() #Guardamos los cambios	
''''
Diccionario_Campos = {
	"stock":0,
	"Fecha_de_vencimiento": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
	"fecha_de_ingreso": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
	"nombre_de_producto2": "JORGITO 300g"
}
'''
Diccionario_Campos = {
	"id_ingreso2": 1,
	"codigo_de_barras": ["dsaddsadadasd","dasfddasdaasdadc","fasdasdadcdwdaa","vvdwdadasdadc4444","vcxfsfadasdadc"]
}
#print(Diccionario_Campos)
sql = Abrir_Conexion()
#Insert_SQL_mult_values( "'sql'" , "Productos" , Diccionario_Campos , "Lista_Stock" )

#print( Ver_Tablas_de_DB(sql) )
#['Categorias_Productos', 'Ingreso_de_productos', 'Productos', 'Stock_disponible']

#Insert_SQL_mult_values( sql , 'Stock_disponible' , Diccionario_Campos,"codigo_de_barras" ) #GUARDAMOS EL NOMBRE DEL PRODUCTO

#print( Ver_Nombres_Campos_Tabla( sql , 'Stock_disponible' ) )
print( Ver_Tabla( sql , 'Stock_disponible' ) )

Cerrar_Conexion( sql )
