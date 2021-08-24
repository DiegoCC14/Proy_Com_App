from PyQt5 import uic #Carga la interfaz  grafica
from PyQt5.QtWidgets import QMainWindow , QApplication , QDialog

import SQL_get

class Ventana_Emergente_Categoria( QMainWindow ):
	def __init__(self):

		super().__init__()
		uic.loadUi( 'Ventana_Emergente_Categoria.ui' , self ) #Nombre de la ventana QT
		self.setFixedSize(502, 217) #Configuramos el tamanio de la ventana
		
		#------------------------>>>>> Configuraciones predeterminadas
		
		self.Cargar_Categorias()
		self.Button_Renombrar.setEnabled(False) #Boton Renombrar deshabilitado
		#------------------------>>>>>

		#------------------------>>>>> Acciones Buttons
		self.Button_Select_Categoria.currentTextChanged.connect( self.Deshabilitar_Button_Nueva_Categoria )
		self.Button_Nueva_Categoria.clicked.connect( self.Agregar_O_Renombrar_Categoria )
		#------------------------>>>>>

	def Cargar_Categorias(self):
		sql = SQL_get.Abrir_Conexion()
		Categorias = SQL_get.Ver_Tabla( sql , 'Categorias_Productos')
		SQL_get.Cerrar_Conexion( sql )
		lista_categorias = ['NUEVA CATEGORIA']
		for Cat in Categorias:
			lista_categorias.append( Cat['nombre'] )
		self.Button_Select_Categoria.addItems(lista_categorias) #Agregamos strings a select

	def Deshabilitar_Button_Nueva_Categoria(self):
		Select_Categoria = self.Button_Select_Categoria.currentText()
		if Select_Categoria=='NUEVA CATEGORIA':
			self.Button_Nueva_Categoria.setEnabled(True)
			self.Button_Renombrar.setEnabled(False)
		else:
			self.Button_Renombrar.setEnabled(True)
			self.Button_Nueva_Categoria.setEnabled(False)

	def Agregar_O_Renombrar_Categoria(self):
		Select_Categoria = self.Button_Select_Categoria.currentText() #Vemos en Select 
		if Select_Categoria == 'NUEVA CATEGORIA' :
			Nombre_Nueva_Categoria = self.Entrada_Nombre_Categoria.toPlainText().upper()
			if( len(Nombre_Nueva_Categoria)>0 ):
				sql = SQL_get.Abrir_Conexion()
				SQL_get.Insert_SQL( sql , 'Categorias_Productos' , {'nombre':Nombre_Nueva_Categoria} )
				SQL_get.Cerrar_Conexion( sql )
				
				self.Cargar_Categorias()

				self.Label_Estado_Operacion.setText( Nombre_Nueva_Categoria + " fue Agregado!" )
				self.Entrada_Nombre_Categoria.setText("")
			else:
				self.Label_Estado_Operacion.setText( "NOMBRE CATEGORIA VACIO, no agregado! " )
		
		else: #Renombrar Categoria Seleccionada
			#Ademas de renombrar la categoria , tambien todas las tablas que tienen conexion con esta
			pass