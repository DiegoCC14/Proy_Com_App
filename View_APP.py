import os
import sys

from PyQt5.Qt import *

from PyQt5 import uic #Carga la interfaz  grafica
from PyQt5.QtWidgets import QMainWindow , QApplication , QDialog

from PyQt5.QtCore import QFile, QTextStream

import View_Emergente_Categoria , View_Emergente_Registro_Producto 

class Inicio_App( QMainWindow ): #Reemplazo de 'QMainWindow' por 'QDialog' no se la difeencia 

	def __init__(self):
		super().__init__()

		uic.loadUi( 'Interfaz_Mejorada.ui' , self )

		#MainWindow.setFixedSize(800, 600)
		#Botones Pestanias ----------------->>>>> 
		self.ButtonPestania_Productos.clicked.connect( self.Productos )
		self.ButtonPestania_VentaDeProductos.clicked.connect( self.Venta_de_Productos )
		self.ButtonPestania_EstadisticasDeVentas.setEnabled(False)
		#----------------------------------->>>>>

		#Botones Acciones ----------------->>>>>
		self.Button_Anadir_Renombrar_Categoria.clicked.connect( self.Anadir_o_Modificacar_Categoria )
		self.Button_Anadir_Producto.clicked.connect( self.Anadir_Producto )
		#---------------------------------->>>>>
	
	#Funciones Para Pestanias ============>>>>
	def Productos(self):
		self.ButtonPestania_Productos.setEnabled(False)
		self.ButtonPestania_VentaDeProductos.setEnabled(True)
		self.ButtonPestania_EstadisticasDeVentas.setEnabled(True)

		self.GroupBox_Productos.move( 20 , 80) #Cambiamos de lugar los group box, dando la ilucion de cambiar ventanas
		self.GruopBox_Venta_de_Productos.move( 980 , 80) #Cambiamos de lugar los group box, dando la ilucion de cambiar ventanas
		
	def Venta_de_Productos(self):
		self.ButtonPestania_VentaDeProductos.setEnabled(False)
		self.ButtonPestania_Productos.setEnabled(True)
		self.ButtonPestania_EstadisticasDeVentas.setEnabled(True)

		self.GroupBox_Productos.move( 980 , 80) #Cambiamos de lugar los group box, dando la ilucion de cambiar ventanas
		self.GruopBox_Venta_de_Productos.move( 20 , 80) #Cambiamos de lugar los group box, dando la ilucion de cambiar ventanas

	def Estadisticas_de_Ventas(self):
		self.ButtonPestania_EstadisticasDeVentas.setEnabled(False)
		self.ButtonPestania_VentaDeProductos.setEnabled(True)
		self.ButtonPestania_Productos.setEnabled(True)
	#Funciones Para Pestanias ============>>>>


	def Anadir_o_Modificacar_Categoria(self):
		self.ventana_categoria = View_Emergente_Categoria.Ventana_Emergente_Categoria( )
		self.ventana_categoria.show()

	def Anadir_Producto(self):
		self.ventana_producto = View_Emergente_Registro_Producto.Ventana_Emergente_Registro_Producto()
		self.ventana_producto.show()
	

app = QApplication( sys.argv )

Aplicacion = Inicio_App()
Aplicacion.setFixedSize(851, 882)
Aplicacion.show()

sys.exit( app.exec_() )



