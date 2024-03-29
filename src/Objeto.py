# coding: utf-8

import pygame;
from Vector2D import *;
from Mosaico import *;

class Objeto(object):
	"""Clase abastracta que representa un objeto genérico: posición, velocidad, modelo, ..."""

	ESCENARIO = None;

	def __init__(self):
		self.posicion = Vector2D();
		self.velocidad = Vector2D();
		self.aceleracion = Vector2D();
		self.rebote_horizontal = 1.0; # Entre 0 y 1 incluido (0 no rebota, 1 hace un rebote perfecto).
		self.rebote_vertical = 1.0;
		self.width = 0.0;
		self.height = 0.0;
		self.color = (255, 255, 255);
		self.mosaico = None;
		self.numImagen = 0.0;
		self.colisionado = False;

	def getRebote(self):
		return (self.rebote_horizontal+self.rebote_vertical)/2;

	def setRebote(self, rebote):
		self.rebote_horizontal = rebote;
		self.rebote_vertical = rebote;
		
	rebote = property(getRebote, setRebote);

	def actualizar(self, tiempoTranscurrido):
		tiempoTranscurrido = tiempoTranscurrido / 1000.0;
		self.velocidad = Vector2D(self.velocidad[0]+self.aceleracion[0]*tiempoTranscurrido, self.velocidad[1]+self.aceleracion[1]*tiempoTranscurrido);
		self.posicion = Vector2D(self.posicion[0]+self.velocidad[0]*tiempoTranscurrido, self.posicion[1]+self.velocidad[1]*tiempoTranscurrido);

		if self.__class__.ESCENARIO != None:
			if self.posicion[0]-self.width/2.0 < self.__class__.ESCENARIO[0]:
				self.posicion[0] = self.posicion[0] + (self.__class__.ESCENARIO[0] - self.posicion[0] + self.width/2.0) * (1 + self.rebote_horizontal);
				self.velocidad[0] = self.rebote_horizontal * abs(self.velocidad[0]);

			elif self.posicion[0]+self.width/2.0 > self.__class__.ESCENARIO[2]:
				self.posicion[0] = self.posicion[0] - (self.posicion[0] + self.width/2.0 - self.__class__.ESCENARIO[2]) * (1 + self.rebote_horizontal);
				self.velocidad[0] = self.rebote_horizontal * (1 if self.velocidad[0] < 0 else -1)*self.velocidad[0];

			if self.posicion[1]+self.height/2.0 > self.__class__.ESCENARIO[3]:
				self.posicion[1] = self.posicion[1] - (self.posicion[1] + self.height/2.0 - self.__class__.ESCENARIO[3]) * (1 + self.rebote_vertical);
				self.velocidad[1] = self.rebote_vertical * (1 if self.velocidad[1] < 1 else -1)*self.velocidad[1];
				self.colisionado = True;
				
			elif self.posicion[1]-self.height/2.0 < self.__class__.ESCENARIO[1] and self.colisionado:
				self.posicion[1] = self.posicion[1] + (self.__class__.ESCENARIO[1] - self.posicion[1] + self.height/2.0) * (1 + self.rebote_vertical);
				self.velocidad[1] = self.rebote_vertical * abs(self.velocidad[1]);

	def colisionan(self, otro):
		ei = self.posicion[0]-self.width/2;
		ed = self.posicion[0]+self.width/2;
		ea = self.posicion[1]-self.height/2;
		eb = self.posicion[1]+self.height/2;
		ei2 = otro.posicion[0]-otro.width/2;
		ed2 = otro.posicion[0]+otro.width/2;
		ea2 = otro.posicion[1]-otro.height/2;
		eb2 = otro.posicion[1]+otro.height/2;

		colisionan = False;

		# Comprobamos que el objeto colisionado (el que se recibe como parámetro) está dentro del escenario.
		# Suele ocurrir que las bolas explotan cuando ni siquiera están en pantalla (cayendo repentinamente sobre el jugador).
		if self.__class__.ESCENARIO[0] <= ei2 and ei2 <= self.__class__.ESCENARIO[2] and self.__class__.ESCENARIO[0] <= ed2 and ed2 <= self.__class__.ESCENARIO[2]:
			if self.__class__.ESCENARIO[1] <= ea2 and ea2 <= self.__class__.ESCENARIO[3] and self.__class__.ESCENARIO[0] <= eb2 and eb2 <= self.__class__.ESCENARIO[2]:
				# Comprobamos si los objetos colisionan.
				if (ea <= ea2 and ea2 <= eb) or (ea <= eb2 and eb2 <= eb) or (ea2 <= ea and ea <= eb2) or (ea2 <= eb and eb <= eb2):
					if (ei <= ei2 and ei2 <= ed) or (ei <= ed2 and ed2 <= ed) or (ei2 <= ei and ei <= ed2) or (ei2 <= ed and ed <= ed2):
						colisionan = True;

		return colisionan;

	def dibujar(self, superficie, tiempoTranscurrido):
		if self.mosaico != None:
			tiempoTranscurrido = tiempoTranscurrido / 1000.0;
			if tiempoTranscurrido > 0.0 and self.mosaico.duracion > 0.0 and self.mosaico.numImagenes > 0.0:
				cantidadImagenesTranscurridas = tiempoTranscurrido * (float(self.mosaico.numImagenes) / self.mosaico.duracion);
				self.numImagen = self.numImagen + cantidadImagenesTranscurridas;
			while self.numImagen > self.mosaico.numImagenes:
				self.numImagen = self.numImagen - self.mosaico.numImagenes;
			self.mosaico.dibujar(superficie, int(self.numImagen), (int(self.posicion[0])-self.width/2, int(self.posicion[1])-self.height/2));
			#superficie.blit(self.imagen, (int(self.posicion[0])-self.width/2, int(self.posicion[1])-self.height/2));
		else:
			pygame.draw.circle(superficie, self.color, (int(self.posicion[0]), int(self.posicion[1])), int(self.width+self.height)/4);