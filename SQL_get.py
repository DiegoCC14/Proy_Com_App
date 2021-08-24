import mysql.connector

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