# coding: utf-8

from math import sqrt
class Vector2D(object):
	"""Clase que representa un vector en R2."""
	
	def __init__(self, x=0.0, y=0.0):
		self.__x = x;
		self.__y = y;

	def setX(self, x):
		self.__x = x;

	def setY(self, y):
		self.__y = y;

	def getX(self):
		return self.__x;

	def getY(self):
		return self.__y;

	def __getitem__(self, clave):
		if (clave == 0):
			return self.__x;
		else:
			return self.__y;

	def __setitem__(self, clave, valor):
		if (clave == 0):
			self.__x = valor;
		else:
			self.__y = valor;

	def __cmp__(self, otro):
		if (self.__x == otro.__x and self.__y == otro.__y):
			return 0;
		elif ((self.__x > otro.__x) or (self.__x == otro.__x and self.__y > otro.__y)):
			return 1;
		else:
			return -1;

	def __add__(self, otro):
		c = Vector2D(self.__x + otro.__x, self.__y + otro.__y);
		return c;

	def __sub__(self, otro):
		c = Vector2D(self.__x - otro.__x, self.__y - otro.__y);
		return c;

	def __mult__(self, otro):
		"""Producto escalar."""
		return self.__x * otro.__x + self.__y * otro.__y;

	def __str__(self):
		return "(" + str(self.__x) + ", " + str(self.__y) + ")";

	def normalizar(self):
		tamano = self.tamano();
		self.__x = self.__x / tamano;
		self.__y = self.__y / tamano;

	def tamano(self):
		return sqrt(self.__x * self.__x + self.__y * self.__y);
