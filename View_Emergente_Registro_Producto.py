from PyQt5 import uic #Carga la interfaz  grafica
from PyQt5.QtWidgets import QMainWindow , QApplication , QDialog

import SQL_get

class Ventana_Emergente_Registro_Producto( QMainWindow ):
	def __init__(self):

		super().__init__()
		uic.loadUi( 'Ventana_Emergente_Registro_de_Producto.ui' , self ) #Nombre de la ventana QT
		self.setFixedSize(440, 562) #Configuramos el tamanio de la ventana
		
		#------------------------>>>>> Configuraciones predeterminadas	
		self.Cargar_Categorias()
		self.Button_Registrar_PRD.setEnabled(False) #Boton Renombrar deshabilitado
		#------------------------>>>>>

		#------------------------>>>>> Acciones Buttons
		self.Button_Validar_Producto.clicked.connect( self.Validar_Producto_Nuevo )
		#------------------------>>>>>

	def Cargar_Categorias(self):
		
		sql = SQL_get.Abrir_Conexion()
		Categorias = SQL_get.Ver_Tabla( sql , 'Categorias_Productos')
		SQL_get.Cerrar_Conexion( sql )

		lista_categorias = []
		for Cat in Categorias:
			lista_categorias.append( Cat['nombre'] )
		self.Button_Select_Categoria_Producto.addItems(lista_categorias) #Agregamos strings a select

	def Validar_Producto_Nuevo(self):
		
		Nombre_Producto = self.Entrada_Nombre_Producto.toPlainText().upper()
		Precio_Producto = self.Entrada_Precio_Producto.toPlainText().upper()
		try:
			Precio_Producto = float(Precio_Producto)
			print(Precio_Producto)
			
		except:
			print("Solo numero y 1 punto[.]")

		Fecha_Producto = self.Entrada_Fecha_de_Vencimiento.toPlainText().upper()
		
		lista_codigos_barra = self.Retorna_lista_de_Codigos_Barra()
		
		print( lista_codigos_barra )
		
		Select_Categoria = self.Button_Select_Categoria_Producto.currentText() #Categoria seleccionada

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

		return lista_codigos_barras