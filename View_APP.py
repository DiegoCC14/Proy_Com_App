import os
import sys

from PyQt5.Qt import *

from PyQt5 import uic , QtWidgets #Carga la interfaz  grafica
from PyQt5.QtWidgets import QMainWindow , QApplication , QDialog

from PyQt5.QtCore import QFile, QTextStream

import View_Emergente_Categoria , View_Emergente_Registro_Producto

import SQL_get 

class Inicio_App( QMainWindow ): #Reemplazo de 'QMainWindow' por 'QDialog' no se la difeencia 

	def __init__(self):
		super().__init__()

		uic.loadUi( 'Interfaz_Mejorada.ui' , self )

		#MainWindow.setFixedSize(800, 600)
		#Botones Pestanias ----------------->>>>> 
		self.ButtonPestania_Productos.clicked.connect( self.VerPestana_Productos )
		self.ButtonPestania_VentaDeProductos.clicked.connect( self.VerPestana_Venta_de_Productos )
		self.ButtonPestania_EstadisticasDeVentas.setEnabled(False)
		#----------------------------------->>>>>

		#Botones Acciones Ver Productos----------------->>>>>
		self.Button_Anadir_Renombrar_Categoria.clicked.connect( self.Anadir_o_Modificacar_Categoria )
		self.Button_Anadir_Producto.clicked.connect( self.Anadir_Producto )
		self.Button_Refrescar_Tabla_Productos.clicked.connect( self.VerListas_Productos )
		#self.Tabla_Productos.itemSelectionChanged()
		#---------------------------------->>>>>

		#Botones Acciones Venta Articulos ----------------->>>>>
		
		self.Botton_Buscar_Producto_Codigo_Barras.clicked.connect( self.Buscar_Producto_por_Codigo_Barras )
		#---------------------------------->>>>>

		self.VerListas_Productos()
	
	#Funciones PestanaProductos ==========>>>>
	def VerListas_Productos(self):
		sql = SQL_get.Abrir_Conexion()
		Productos = SQL_get.Ver_Tabla( sql , 'Productos' )
		print( Productos )
		SQL_get.Cerrar_Conexion(sql)

		self.Tabla_Productos.setRowCount(len(Productos))
		self.Tabla_Productos.setColumnCount(4)
		self.Tabla_Productos.setHorizontalHeaderLabels(['PRODUCTO','STOCK','PRECIO',''])
		contador = 0
		for producto in Productos:
			self.Tabla_Productos.setItem(contador ,0 , QTableWidgetItem( producto['nombre_de_producto'] ) )
			self.Tabla_Productos.setItem(contador ,1 , QTableWidgetItem(str(producto['stock'])) )
			self.Tabla_Productos.setItem(contador ,2 , QTableWidgetItem(str(producto['precio_venta']) ) )

			combox_lay = QtWidgets.QPushButton(self)
			combox_lay.setText(" Ver Producto ")
			self.Tabla_Productos.setCellWidget(contador ,3 , combox_lay )
			
			contador+=1
		
		self.Tabla_Productos.setColumnWidth(0, 400)
		self.Tabla_Productos.setColumnWidth(1, 90)

		#self.Tabla_Productos.setCheckable(False)
	#=======================================>>>>

	#Funciones Venta de Productos ==========>>>>
	def Buscar_Producto_por_Codigo_Barras(self):
		
		CodigoBarras = self.Entrada_Codigo_Barras.toPlainText()
		sql = SQL_get.Abrir_Conexion()
		Dicc_resultados_Stock = SQL_get.Buscar_Elementos_En_Tabla( sql , 'Stock_disponible' , 'codigo_de_barras' , CodigoBarras )
		print( Dicc_resultados_Stock[0] )
		if len( Dicc_resultados_Stock ) != 0:
			

			Dicc_resultados_Ingreso_Producto = SQL_get.Buscar_Elementos_En_Tabla( sql , 'Ingreso_de_productos' , 'ID_ingreso' , Dicc_resultados_Stock[0]['id_ingreso2'] )
			Dicc_resultado_Producto = SQL_get.Buscar_Elementos_En_Tabla( sql , 'Productos' , 'nombre_de_producto' , Dicc_resultados_Ingreso_Producto[0]['nombre_de_producto2'] )
			print(Dicc_resultado_Producto[0])
			SQL_get.Cerrar_Conexion(sql)
			
			Estado = CodigoBarras + " Encontrado !!!"
			Nombre_Producto = Dicc_resultado_Producto[0]['nombre_de_producto']
			CodigoBarras = CodigoBarras
			Precio_Producto = '$ 'str( Dicc_resultado_Producto[0]['precio_venta'] )
		else:
			Estado = CodigoBarras + " NO Encontrado !!!"
			Nombre_Producto = "Producto no encontrado"
			CodigoBarras = "Producto no encontrado"
			Precio_Producto = "Producto no encontrado"

		self.Texto_EstadoBusquedaProducto_Venta.setText( Estado )
		self.Texto_NombreProducto_Venta.setText( Nombre_Producto )
		self.Texto_Codigo_Barras_Venta.setText( Dicc_resultados_Stock[0]['codigo_de_barras'] )
		self.Texto_Precio_Venta.setText( Precio_Producto )

	#=======================================>>>>

	#Funciones Para Pestanias ============>>>>
	def VerPestana_Productos(self):
		self.ButtonPestania_Productos.setEnabled(False)
		self.ButtonPestania_VentaDeProductos.setEnabled(True)
		self.ButtonPestania_EstadisticasDeVentas.setEnabled(True)

		self.GroupBox_Productos.move( 20 , 80) #Cambiamos de lugar los group box, dando la ilucion de cambiar ventanas
		self.GruopBox_Venta_de_Productos.move( 980 , 80) #Cambiamos de lugar los group box, dando la ilucion de cambiar ventanas
		
	def VerPestana_Venta_de_Productos(self):
		self.ButtonPestania_VentaDeProductos.setEnabled(False)
		self.ButtonPestania_Productos.setEnabled(True)
		self.ButtonPestania_EstadisticasDeVentas.setEnabled(True)

		self.GroupBox_Productos.move( 980 , 80) #Cambiamos de lugar los group box, dando la ilucion de cambiar ventanas
		self.GruopBox_Venta_de_Productos.move( 20 , 80) #Cambiamos de lugar los group box, dando la ilucion de cambiar ventanas

	def VerPestana_Estadisticas_de_Ventas(self):
		self.ButtonPestania_EstadisticasDeVentas.setEnabled(False)
		self.ButtonPestania_VentaDeProductos.setEnabled(True)
		self.ButtonPestania_Productos.setEnabled(True)
	#=======================================>>>>

	#Funciones Para Pestanias Emergentes ============>>>>
	def Anadir_o_Modificacar_Categoria(self):
		self.ventana_categoria = View_Emergente_Categoria.Ventana_Emergente_Categoria( )
		self.ventana_categoria.show()

	def Anadir_Producto(self):
		self.ventana_producto = View_Emergente_Registro_Producto.Ventana_Emergente_Registro_Producto()
		self.ventana_producto.show()
	#=======================================>>>>

app = QApplication( sys.argv )

Aplicacion = Inicio_App()
Aplicacion.setFixedSize(851, 882)
Aplicacion.show()

sys.exit( app.exec_() )



