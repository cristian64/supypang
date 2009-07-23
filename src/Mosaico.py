# coding: utf-8

import pygame;
from Vector2D import *;

class Mosaico:
	"""Representa un mosaico de imágenes que se obtienen desde un único fichero."""

	def __init__(self, nomFich, filas, columnas, numImagenes, duracion):
		"""Se indica el nombre del fichero origen, el número de filas y columnas que tiene el mosaico y el número total de imágenes (podría ser que la última fila del mosaico no estuviera completa)."""
		self.imagen = pygame.image.load(nomFich);
		self.nomFich = nomFich;
		self.filas = filas;
		self.columnas = columnas;
		self.numImagenes = numImagenes;
		self.duracion = duracion;
		self.tamanoFila = self.imagen.get_height()/self.filas;
		self.tamanoColumna = self.imagen.get_width()/self.columnas;

	def dibujar(self, superficie, numImagen, posicion):
		if self.imagen != None and self.numImagenes > numImagen:
			superficie.blit(self.imagen, (posicion[0], posicion[1]), ((numImagen%self.columnas)*self.tamanoColumna, (numImagen/self.columnas)*self.tamanoFila, self.tamanoColumna, self.tamanoFila));