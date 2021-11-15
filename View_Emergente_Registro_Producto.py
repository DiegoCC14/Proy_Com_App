from PyQt5 import uic #Carga la interfaz  grafica
from PyQt5.QtWidgets import QMainWindow , QApplication , QDialog


import SQL_get
from datetime import datetime

class Ventana_Emergente_Registro_Producto( QMainWindow ):
	def __init__(self):

		super().__init__()
		uic.loadUi( 'Ventana_Emergente_Registro_de_Producto.ui' , self ) #Nombre de la ventana QT
		self.setFixedSize(440, 562) #Configuramos el tamanio de la ventana
		
		#------------------------>>>>> Configuraciones predeterminadas	
		self.Cargar_Categorias()

		#Si Boton Valido vallda el producto, Registra Producto
		self.Button_Registrar_PRD.setEnabled(False) #Boton registrar deshabilitado al principio,
		self.Button_Modificar_Producto.setEnabled(True) #Boton registrar deshabilitado al principio,
		#------------------------>>>>>

		#------------------------>>>>> Acciones Buttons
		self.Button_Validar_Producto.clicked.connect( self.Validar_Producto_Nuevo )
		self.Button_Modificar_Producto.clicked.connect( self.Modificar_Producto )
		self.Button_Limpiar_Datos.clicked.connect( self.Limpiar_Cajas_Input )
		self.Button_Registrar_PRD.clicked.connect( self.Registrar_Producto_en_DB )
		#------------------------>>>>>
	def Modificar_Producto(self):
		self.Estado_Campos_InputText_Select( True )
		self.Button_Registrar_PRD.setEnabled(False) #Boton registrar hibilitado
		self.Button_Modificar_Producto.setEnabled(False) #Boton modificar hibilitado
		self.Button_Validar_Producto.setEnabled(True) #Boton modificar deshibilitado

	def Estado_Campos_InputText_Select(self , Estado): #True y los campo se podran cambiar
		self.Entrada_Nombre_Producto.setReadOnly( not Estado )
		self.Entrada_Precio_Producto.setReadOnly( not Estado )
		self.Entrada_Fecha_de_Vencimiento.setReadOnly( not Estado )
		self.Entrada_Codigo_Barras_Producto.setReadOnly( not Estado )
		self.Button_Select_Categoria_Producto.setEnabled( Estado )

	def Cargar_Categorias(self):
		
		sql = SQL_get.Abrir_Conexion()
		Categorias = SQL_get.Ver_Tabla( sql , 'Categorias_Productos')
		SQL_get.Cerrar_Conexion( sql )

		lista_categorias = []
		for Cat in Categorias:
			lista_categorias.append( Cat['nombre'] )
		self.Button_Select_Categoria_Producto.addItems(lista_categorias) #Agregamos strings a select

	def Retorna_lista_de_Codigos_Barra( self ):
		
		Codigos_de_Barra = self.Entrada_Codigo_Barras_Producto.toPlainText()

		lista_codigos_barras = []
		barra = ""
		for car in Codigos_de_Barra:
			print( car )
			if car == "\n":
				if len(barra)>0:
					lista_codigos_barras.append( barra )
				barra = ""
			else:
				barra += car
		if len(barra)>0:
			lista_codigos_barras.append( barra )

		set_elementos = set( lista_codigos_barras )
		lista_codigos_barras = list(set_elementos)
		return lista_codigos_barras

	def Validar_Producto_Nuevo(self):
		
		Nombre_Producto = self.Entrada_Nombre_Producto.toPlainText().upper()
		Select_Categoria = self.Button_Select_Categoria_Producto.currentText() #Categoria seleccionada

		Precio_Producto = self.Entrada_Precio_Producto.toPlainText().upper()
		try:
			Precio_Producto = float(Precio_Producto)
			self.Label_Precio_Venta.setText( "Correcto" )
			Precio_Correcto = True
		except:
			self.Label_Precio_Venta.setText( "Valor Invalido, ejemplo: 14.50" )
			Precio_Correcto = False

		Fecha_Vencimiento_Correcto = True
		Fecha_Venc_Ingresado = self.Entrada_Fecha_de_Vencimiento.toPlainText().upper()
		if Fecha_Venc_Ingresado != "" and Fecha_Venc_Ingresado != " " and Fecha_Venc_Ingresado != "  ": #Que no ingreso espacios vacios
			try:
				Fecha_Venc_Ingresado += " 23:59:59" #Las fechas incluiran el dia completo como vencimiento
				Fecha_Venc_Ingresado = datetime.strptime( Fecha_Venc_Ingresado , '%d/%m/%y %H:%M:%S')
				if datetime.now()>Fecha_Venc_Ingresado: #Fecha de vencimiento sera mayor a la actual
					Fecha_Vencimiento_Correcto = False
					self.Label_Fecha_Vencimiento.setText('Fecha Vencida;' + ' d/m/a-ej: 22/6/21')
			except:
				Fecha_Vencimiento_Correcto = False
				self.Label_Fecha_Vencimiento.setText('Fecha Mal Ingresada ;' + ' d/m/a-ej: 22/6/21')

		lista_codigos_barra = self.Retorna_lista_de_Codigos_Barra()
		
		if len(lista_codigos_barra) > 0:
			self.Label_Stock_Producto.setText( str(len(lista_codigos_barra)) + " Productos Sin Repetir" )
		else:
			self.Label_Stock_Producto.setText( "0 Productos Sin Repetir - Ingrese un producto" )

		TextoGeneral = "Verifique Campo:"
		if Precio_Correcto == False:
			TextoGeneral += " Precio ;"
		if Fecha_Vencimiento_Correcto == False:
			TextoGeneral += " Fecha_Vencimiento ;"
		if len(lista_codigos_barra) == 0:
			TextoGeneral += " Stock ;"
		
		Nombre_Valido = True
		if Nombre_Producto == "" or Nombre_Producto== " " or Nombre_Producto== "  " or Nombre_Producto== "   ":
			Nombre_Valido = False
			TextoGeneral += " Nombre ;"

		if TextoGeneral == "Verifique Campo:": #Si no tenemos error, el string seguira igual
			TextoGeneral = "Correcto Para Ingresar"
		
		self.Label_Estado_Accion_Genearada.setText( TextoGeneral )

		if ( Precio_Correcto and Fecha_Vencimiento_Correcto and len(lista_codigos_barra)>0 and Nombre_Valido ): #Si todo esta bien entonces Registramos
			self.Button_Registrar_PRD.setEnabled(True) #Boton registrar hibilitado
			self.Button_Modificar_Producto.setEnabled(True) #Boton modificar hibilitado
			self.Button_Validar_Producto.setEnabled(False) #Boton modificar deshibilitado
			
			self.Estado_Campos_InputText_Select( False )

	def Registrar_Producto_en_DB( self ):
		
		Nombre_Producto = self.Entrada_Nombre_Producto.toPlainText().upper()
		Select_Categoria = self.Button_Select_Categoria_Producto.currentText() #Categoria seleccionada
		Precio_Producto = self.Entrada_Precio_Producto.toPlainText().upper()
		Fecha_Venc_Ingresado = self.Entrada_Fecha_de_Vencimiento.toPlainText().upper()
		lista_codigos_barra = self.Retorna_lista_de_Codigos_Barra()
		
		Dicc_Productos = {
		"nombre_de_producto": Nombre_Producto ,
		"precio_venta": Precio_Producto ,
		"stock": len(lista_codigos_barra) ,
		"categoria": Select_Categoria
		}

		sql = SQL_get.Abrir_Conexion()

		SQL_get.Insert_SQL( sql , 'Productos' , Dicc_Productos )

		Dicc_Ingreso_Productos = {
		#"ID_ingreso":, No necesario, autoincremental
		"stock": len(lista_codigos_barra),
		"fecha_de_ingreso": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
		"nombre_de_producto2": Nombre_Producto
		}
		if len(Fecha_Venc_Ingresado)>=6: #Se ingreso fecha de vencimiento
			Dicc_Ingreso_Productos["Fecha_de_vencimiento"] = Fecha_Venc_Ingresado
		
		SQL_get.Insert_SQL( sql , 'Ingreso_de_productos' , Dicc_Ingreso_Productos )
		id_ultimo_ingreso = SQL_get.Ultimo_Valor_Campo_Ingrsado( sql , 'Ingreso_de_productos' , 'ID_ingreso' )

		Dicc_Stock = {
			"id_ingreso2": id_ultimo_ingreso,
			"codigo_de_barras": lista_codigos_barra
		}
		
		SQL_get.Insert_SQL_mult_values( sql , 'Stock_disponible' , Dicc_Stock , 'codigo_de_barras' )

		SQL_get.Cerrar_Conexion( sql )

		self.Label_Estado_Accion_Genearada.setText( Nombre_Producto + " se ingreso correctamente " )
		self.Limpiar_Cajas_Input() #Limpiamos las cajas

	def Limpiar_Cajas_Input( self ):
		self.Entrada_Nombre_Producto.setText("")
		self.Entrada_Precio_Producto.setText("")
		self.Entrada_Fecha_de_Vencimiento.setText("")
		self.Entrada_Codigo_Barras_Producto.setText("")
		self.Estado_Campos_InputText_Select( True ) #Podremos modificar producto

