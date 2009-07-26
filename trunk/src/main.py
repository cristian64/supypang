#! /usr/bin/env python
# coding: utf-8

__author__="cristian"
__date__ ="$03-jul-2009 20:09:44$"


import math;
import pygame;
from pygame.locals import *;
import os;
from random import randint, seed;
from Objeto import *;
from Mosaico import *;

os.environ['SDL_VIDEO_CENTERED'] = '1';

def main():

	###############################################################
	# Inicialización de los recursos del sistema.
	###############################################################
	pygame.init();
	width = 800;
	height = 600;
	margen = (10, 10, 10, 80);
	ventana = pygame.display.set_mode((width, height));
	pygame.display.set_caption('Supy Pang', "../resources/imagenes/icono16.png");
	pygame.display.set_icon(pygame.image.load("../resources/imagenes/icono16.png"));
	Objeto.ESCENARIO = (margen[0], margen[1], width-margen[2], height-margen[3]);
	seed(pygame.time.get_ticks());

	###############################################################
	# Cargando los mosaicos (tiles) y las imágenes del juego.
	###############################################################
	bender_parado_izq = Mosaico("../resources/imagenes/bender-parado-izq.png", 1, 1, 1, 0.0);
	bender_parado_der = Mosaico("../resources/imagenes/bender-parado-der.png", 1, 1, 1, 0.0);
	bender_corriendo_izq = Mosaico("../resources/imagenes/bender-corriendo-izq.png", 1, 4, 4, 0.25);
	bender_corriendo_der = Mosaico("../resources/imagenes/bender-corriendo-der.png", 1, 4, 4, 0.25);
	flecha_azul = Mosaico("../resources/imagenes/flecha.png", 1, 3, 3, 0.75);
	gancho_azul = Mosaico("../resources/imagenes/gancho.png", 1, 1, 1, 0.0);
	disparo_verde = Mosaico("../resources/imagenes/disparo.png", 1, 8, 8, 0.5);
	cambio_gancho = Mosaico("../resources/imagenes/obtener-gancho.png", 1, 6, 6, 0.5);
	cambio_pistola = Mosaico("../resources/imagenes/obtener-pistola.png", 1, 6, 6, 0.5);
	bola16 = Mosaico("../resources/imagenes/bola16.png", 6, 4, 24, 0.5);
	bola32 = Mosaico("../resources/imagenes/bola32.png", 6, 4, 24, 0.5);
	bola64 = Mosaico("../resources/imagenes/bola64.png", 6, 4, 24, 0.5);
	bola128 = Mosaico("../resources/imagenes/bola128.png", 6, 4, 24, 0.5);
	bola256 = Mosaico("../resources/imagenes/bola256.png", 6, 4, 24, 0.5);
	pancarta_nivel = pygame.image.load("../resources/imagenes/pancarta-nivel.png");
	bender_cabeza = pygame.image.load("../resources/imagenes/bender-cabeza.png");

	###############################################################
	# Cargando los sonidos del juego.
	###############################################################
	rompiendo_bola = pygame.mixer.Sound("../resources/sonidos/rompiendo-bola.wav");
	obteniendo_gancho = pygame.mixer.Sound("../resources/sonidos/obteniendo-gancho.wav");
	cambio_nivel = pygame.mixer.Sound("../resources/sonidos/cambio_nivel.wav");
	sonidos_herida = [];
	sonidos_herida.append(pygame.mixer.Sound("../resources/sonidos/muerto2.wav"));
	sonidos_herida.append(pygame.mixer.Sound("../resources/sonidos/muerto4.wav"));
	sonidos_disparo = [];
	sonidos_disparo.append(pygame.mixer.Sound("../resources/sonidos/disparo1.wav"));
	sonidos_muchos_disparos = [];
	sonidos_muchos_disparos.append(pygame.mixer.Sound("../resources/sonidos/disparo4.wav"));
	sonidos_muchos_disparos.append(pygame.mixer.Sound("../resources/sonidos/disparo9.wav"));
	sonido_bso = pygame.mixer.Sound("../resources/sonidos/bso.wav");
	sonido_bso.set_volume(0.2);
	sonido_bso.play(-1);

	###############################################################
	# Variables con el estado del juego.
	###############################################################
	puntuacion = 0;
	nivel = 1;
	bolas_destruidas = 0;
	vidas = 10;
	inmune = False;
	ultima_bola_colisiono = None;
	ultimo_mosaico = None;
	mostrar_nivel_inicial = mostrar_nivel = 3500;
	modo_disparo = "flechas";

	flechas = [];
	ganchos = [];
	ganchos_anclados = [];
	disparos = [];
	jugadores = [];
	bolas = [];

	obtener_gancho = None;
	obtener_pistola = None;

	velocidades_balas1 = [];
	velocidades_balas1.append(Vector2D(-100, -600));
	velocidades_balas1.append(Vector2D(100, -600));
	velocidades_balas1.append(Vector2D(50, -700));
	velocidades_balas1.append(Vector2D(-50, -700));
	velocidades_balas1.append(Vector2D(1, -750));

	velocidades_balas2 = [];
	velocidades_balas2.append(Vector2D(1, -620));
	velocidades_balas2.append(Vector2D(-1, 620));
	velocidades_balas2.append(Vector2D(620, -1));
	velocidades_balas2.append(Vector2D(-620, 1));
	velocidades_balas2.append(Vector2D(-100, -600));
	velocidades_balas2.append(Vector2D(-200, -550));
	velocidades_balas2.append(Vector2D(-300, -500));
	velocidades_balas2.append(Vector2D(-400, -400));
	velocidades_balas2.append(Vector2D(-500, -300));
	velocidades_balas2.append(Vector2D(-550, -200));
	velocidades_balas2.append(Vector2D(-600, -100));
	velocidades_balas2.append(Vector2D(100, -600));
	velocidades_balas2.append(Vector2D(200, -550));
	velocidades_balas2.append(Vector2D(300, -500));
	velocidades_balas2.append(Vector2D(400, -400));
	velocidades_balas2.append(Vector2D(500, -300));
	velocidades_balas2.append(Vector2D(550, -200));
	velocidades_balas2.append(Vector2D(600, -100));
	velocidades_balas2.append(Vector2D(100, 600));
	velocidades_balas2.append(Vector2D(200, 550));
	velocidades_balas2.append(Vector2D(300, 500));
	velocidades_balas2.append(Vector2D(400, 400));
	velocidades_balas2.append(Vector2D(500, 300));
	velocidades_balas2.append(Vector2D(550, 200));
	velocidades_balas2.append(Vector2D(600, 100));
	velocidades_balas2.append(Vector2D(-100, 600));
	velocidades_balas2.append(Vector2D(-200, 550));
	velocidades_balas2.append(Vector2D(-300, 500));
	velocidades_balas2.append(Vector2D(-400, 400));
	velocidades_balas2.append(Vector2D(-500, 300));
	velocidades_balas2.append(Vector2D(-550, 200));
	velocidades_balas2.append(Vector2D(-600, 100));
	
	jugador = Objeto();
	jugador.mosaico = bender_parado_der;
	jugador.width = jugador.mosaico.tamanoColumna+1;
	jugador.height = jugador.mosaico.tamanoFila+1;
	jugador.posicion = Vector2D(Objeto.ESCENARIO[2]/2, math.floor(Objeto.ESCENARIO[3]-jugador.height/2.0));
	jugador.aceleracion[1] = 5000;
	jugador.rebote = 0.0;
	jugadores.append(jugador);

	###############################################################
	# Funciones auxiliares.
	###############################################################
	def insertarBola16():
		bola = Objeto();
		bola.width = bola.height = 16;
		bola.posicion = Vector2D(randint(50,600), randint(-bola.height,-bola.height/2));
		bola.velocidad[0] = (-1 if randint(0, 1) == 0 else 1) * randint(300,800);
		bola.velocidad[1] = randint(200,700);
		bola.aceleracion[1] = randint(200,410);
		bola.color = (250, 50, 50);
		bola.mosaico = bola16;
		bolas.append(bola);

	def insertarBola32():
		bola = Objeto();
		bola.width = bola.height = 32;
		bola.posicion = Vector2D(randint(50,600), randint(-bola.height,-bola.height/2));
		bola.velocidad[0] = (-1 if randint(0, 1) == 0 else 1) * randint(30,200);
		bola.velocidad[1] = randint(0,60);
		bola.aceleracion[1] = randint(30,210);
		bola.color = (250, 50, 50);
		bola.mosaico = bola32;
		bolas.append(bola);

	def insertarBola64():
		bola = Objeto();
		bola.width = bola.height = 64;
		bola.posicion = Vector2D(randint(50,600), randint(-bola.height,-bola.height/2));
		bola.velocidad[0] = (-1 if randint(0, 1) == 0 else 1) * randint(30,200);
		bola.velocidad[1] = randint(0,60);
		bola.aceleracion[1] = randint(30,210);
		bola.color = (250, 50, 50);
		bola.mosaico = bola64;
		bolas.append(bola);

	def insertarBola128():
		bola = Objeto();
		bola.width = bola.height = 128;
		bola.posicion = Vector2D(randint(50,600), randint(-bola.height,-bola.height/2));
		bola.velocidad[0] = (-1 if randint(0, 1) == 0 else 1) * randint(30,200);
		bola.velocidad[1] = randint(0,60);
		bola.aceleracion[1] = randint(30,210);
		bola.color = (250, 50, 50);
		bola.mosaico = bola128;
		bolas.append(bola);

	def insertarBola256():
		bola = Objeto();
		bola.width = bola.height = 256;
		bola.posicion = Vector2D(randint(50,600), randint(-bola.height,-bola.height/2));
		bola.velocidad[0] = (-1 if randint(0, 1) == 0 else 1) * randint(30,200);
		bola.velocidad[1] = randint(0,60);
		bola.aceleracion[1] = randint(30,210);
		bola.color = (250, 50, 50);
		bola.mosaico = bola256;
		bolas.append(bola);

	def bolaRota(pbola):
		if pbola.width > 16:
			bolaMosaico = bola128;
			if pbola.width == 32:
				bolaMosaico = bola16;
			elif pbola.width == 64:
				bolaMosaico = bola32;
			elif pbola.width == 128:
				bolaMosaico = bola64;

			velocidad_horizontal = randint(70, 150);
			velocidad_vertical = randint(250, 400);
			bola = Objeto();
			bola.width = bola.height = pbola.width/2;
			bola.posicion = pbola.posicion;
			bola.aceleracion = pbola.aceleracion;
			bola.velocidad = Vector2D(-velocidad_horizontal+pbola.velocidad[0], -velocidad_vertical);
			if abs(bola.velocidad[0])<100:
				bola.velocidad[0] = 100;
			bola.mosaico = bolaMosaico;
			bola.rebote_vertical = 0.3 if randint(0, 30) == 0 else 1.0;
			bola.colisionado = True;
			bola.color = (250, 50, 50);
			bolas.append(bola);
			
			bola = Objeto();
			bola.width = bola.height = pbola.width/2;
			bola.posicion = pbola.posicion;
			bola.aceleracion = pbola.aceleracion;
			bola.velocidad = Vector2D(velocidad_horizontal+pbola.velocidad[0], -velocidad_vertical);
			if abs(bola.velocidad[0])<100:
				bola.velocidad[0] = 100;
			bola.mosaico = bolaMosaico;
			bola.rebote_vertical = 0.3 if randint(0, 30) == 0 else 1.0;
			bola.colisionado = True;
			bola.color = (250, 50, 50);
			bolas.append(bola);

	###############################################################
	# Variables de control de la ejecución.
	###############################################################
	salir = False;
	tiempoUltimaActualizacion = pygame.time.get_ticks();
	tiempoActualizacionGanchosAnclados = pygame.time.get_ticks();
	tiempoInsertarBola = pygame.time.get_ticks()-30000;
	tiempoObtenerGancho = pygame.time.get_ticks();
	tiempoObtenerPistola = pygame.time.get_ticks();
	tiempoObtenerFlecha = pygame.time.get_ticks();
	tiempoInmunidad = pygame.time.get_ticks();
	tiempoTranscurrido = 0.0;

	###############################################################
	# Inicio del juego.
	###############################################################
	while not salir:

		###############################################################
		# Procesamos los eventos y el estado del teclado.
		###############################################################
		eventos = pygame.event.poll();

		while eventos.type != NOEVENT and not salir:

			if eventos.type == QUIT:
				salir = True;

			elif eventos.type == KEYDOWN:

				if eventos.key == K_ESCAPE:
					salir = True;
				elif eventos.key == K_UP and jugador.velocidad[1] == 0:
					jugador.velocidad[1] = -1200;
				elif eventos.key == K_i:
					print "Número de bolas: " + str(len(bolas));
					print "Número de flechas: " + str(len(flechas));
					print "Número de ganchos: " + str(len(ganchos));
					print "Número de ganchos anclados: " + str(len(ganchos_anclados));
					print "Número de disparos: " + str(len(disparos));
				elif eventos.key == K_SPACE:
					reproducir_sonido = True;
					if modo_disparo == "flechas" and len(flechas) < nivel/2+3:
						flecha = Objeto();
						flecha.mosaico = flecha_azul;
						flecha.width = flecha.mosaico.tamanoColumna;
						flecha.height = 30;
						flecha.posicion = Vector2D(jugador.posicion[0], Objeto.ESCENARIO[3]-flecha.height/2);
						flecha.velocidad = Vector2D(0, -200 if jugador.velocidad[1] == 0 else -500);
						flechas.append(flecha);
					elif modo_disparo == "ganchos" and len(ganchos)+len(ganchos_anclados) < nivel/2+3:
						gancho = Objeto();
						gancho.mosaico = gancho_azul;
						gancho.width = gancho.mosaico.tamanoColumna;
						gancho.height = 30;
						gancho.posicion = Vector2D(jugador.posicion[0], Objeto.ESCENARIO[3]-gancho.height/2);
						gancho.velocidad = Vector2D(0, -200 if jugador.velocidad[1] == 0 else -500);
						ganchos.append(gancho);
					elif modo_disparo == "pistola":
						if jugador.velocidad[1] == 0:
							velocidades = velocidades_balas1;
						else:
							velocidades = velocidades_balas2;
						for i in velocidades:
							disparo = Objeto();
							disparo.mosaico = disparo_verde;
							disparo.colisionado = True;
							disparo.width = disparo.height = disparo.mosaico.tamanoColumna;
							disparo.posicion = Vector2D(jugador.posicion[0], jugador.posicion[1]);
							disparo.velocidad = i;
							disparo.rebote = 0.0;
							disparos.append(disparo);
						sonidos_muchos_disparos[randint(0, len(sonidos_muchos_disparos)-1)].play();
					else:
						reproducir_sonido = False;
					if reproducir_sonido and (len(flechas)==1 or len(ganchos)==1):
						sonidos_disparo[randint(0, len(sonidos_disparo)-1)].play();


			eventos = pygame.event.poll();

		# Restauramos la velocidad y mosaico del jugador.
		jugador.velocidad[0] = 0;
		if jugador.mosaico == bender_corriendo_der:
			jugador.mosaico = bender_parado_der;
		elif jugador.mosaico == bender_corriendo_izq:
			jugador.mosaico = bender_parado_izq;

		# Extraemos el estado del teclado.
		teclado = pygame.key.get_pressed();

		# Comprobamos hacia dónde está dirigiéndose el jugador.
		if teclado[K_RETURN]:
			velocidad = 600;
		else:
			velocidad = 400;
		if teclado[K_RIGHT]:
			jugador.velocidad[0] = velocidad;
			jugador.mosaico = bender_corriendo_der;
		if teclado[K_LEFT]:
			jugador.velocidad[0] = -velocidad;
			jugador.mosaico = bender_corriendo_izq;

		###############################################################
		# Actualizamos los objetos.
		###############################################################
		flechas_aux = [];
		for i in flechas:
			i.actualizar(tiempoTranscurrido);
			i.height = (Objeto.ESCENARIO[3]-i.posicion[1])*2
			if i.height<=Objeto.ESCENARIO[3]-Objeto.ESCENARIO[1]:
				flechas_aux.append(i);
		flechas = flechas_aux;
		ganchos_aux = [];
		for i in ganchos:
			i.actualizar(tiempoTranscurrido);
			i.height = (Objeto.ESCENARIO[3]-i.posicion[1])*2
			if i.height<=Objeto.ESCENARIO[3]-Objeto.ESCENARIO[1]:
				ganchos_aux.append(i);
			else:
				if len(ganchos_anclados) == 0:
					tiempoActualizacionGanchosAnclados = pygame.time.get_ticks();
				ganchos_anclados.insert(0, i);
		ganchos = ganchos_aux;
		if (pygame.time.get_ticks() - tiempoActualizacionGanchosAnclados > 3000):
			if len(ganchos_anclados) > 0:
				ganchos_anclados.pop();
			tiempoActualizacionGanchosAnclados = pygame.time.get_ticks();
		disparos_aux = [];
		for i in disparos:
			i.actualizar(tiempoTranscurrido);
			if i.velocidad[0]!=0 and i.velocidad[1]!=0:
				disparos_aux.append(i);
		disparos = disparos_aux;
		for i in jugadores:
			i.actualizar(tiempoTranscurrido);
		for i in bolas:
			i.actualizar(tiempoTranscurrido);

		###############################################################
		# Comprobamos colisiones entre bolas, jugadores y armas.
		###############################################################
		if obtener_gancho != None:
			obtener_gancho.actualizar(tiempoTranscurrido);
			if obtener_gancho.colisionan(jugador):
				obtener_gancho = None;
				modo_disparo = "ganchos";
				obteniendo_gancho.play();
				tiempoObtenerFlecha = pygame.time.get_ticks();
		if obtener_pistola != None:
			obtener_pistola.actualizar(tiempoTranscurrido);
			if obtener_pistola.colisionan(jugador):
				obtener_pistola = None;
				modo_disparo = "pistola";
				obteniendo_gancho.play();
				tiempoObtenerFlecha = pygame.time.get_ticks();
		if not inmune:
			jugador.height = jugador.height-30;
			jugador.width = jugador.width-30;
			for i in bolas:
				if jugador.colisionan(i):
					vidas = vidas - 1;
					jugador.posicion[1] = -100;
					jugador.colisionado = False;
					sonidos_herida[randint(0, len(sonidos_herida)-1)].play();
					inmune = True;
					tiempoInmunidad = pygame.time.get_ticks();
					ultima_bola_colisiono = i;
					ultimo_mosaico = i.mosaico;
					i.mosaico = None;
					break;
			jugador.height = jugador.height+30;
			jugador.width = jugador.width+30;

		###############################################################
		# Detectamos las colisiones entre flechas y bolas.
		###############################################################
		bolas_rotas = [];
		flechas_rotas = [];
		for i in flechas:
			for j in bolas:
				if i.colisionan(j):
					flechas_rotas.append(i);
					bolas_rotas.append(j);

		# Eliminamos las flechas rotas de la lista.
		flechas_aux = [];
		for i in flechas:
			if not(i in flechas_rotas):
				flechas_aux.append(i);
		flechas = flechas_aux;

		###############################################################
		# Detectamos las colisiones entre ganchos y bolas.
		###############################################################
		ganchos_rotos = [];
		for i in ganchos:
			for j in bolas:
				if i.colisionan(j):
					ganchos_rotos.append(i);
					bolas_rotas.append(j);

		# Eliminamos los ganchos rotos de la lista.
		ganchos_aux = [];
		for i in ganchos:
			if not(i in ganchos_rotos):
				ganchos_aux.append(i);
		ganchos = ganchos_aux;

		###############################################################
		# Detectamos las colisiones entre ganchos anclados y bolas.
		###############################################################
		ganchos_rotos = [];
		for i in ganchos_anclados:
			for j in bolas:
				if i.colisionan(j):
					ganchos_rotos.append(i);
					bolas_rotas.append(j);

		# Eliminamos los ganchos rotos de la lista.
		ganchos_aux = [];
		for i in ganchos_anclados:
			if not(i in ganchos_rotos):
				ganchos_aux.append(i);
		ganchos_anclados = ganchos_aux;

		###############################################################
		# Detectamos las colisiones entre disparos y bolas.
		###############################################################
		disparos_rotos = [];
		for i in disparos:
			for j in bolas:
				if i.colisionan(j):
					disparos_rotos.append(i);
					bolas_rotas.append(j);

		# Eliminamos las flechas rotas de la lista.
		disparos_aux = [];
		for i in disparos:
			if not(i in disparos_rotos):
				disparos_aux.append(i);
		disparos = disparos_aux;

		###############################################################
		# Eliminamos las bolas rotas de la lista e insertamos bolas más pequeñas.
		###############################################################
		bolas_aux = [];
		for i in bolas:
			if not(i in bolas_rotas):
				bolas_aux.append(i);
			else:
				bolaRota(i);
				bolas_destruidas = bolas_destruidas + 1;
				nuevo_nivel = bolas_destruidas / 30 + 1;
				if nuevo_nivel != nivel:
					nivel = nuevo_nivel;
					mostrar_nivel = mostrar_nivel_inicial;
					vidas = vidas + 1;
					cambio_nivel.play();
					#tiempoInsertarBola = pygame.time.get_ticks() + 15000;
				puntuacion = puntuacion + len(bolas)*((i.width/16)+nivel);
				rompiendo_bola.play();
		bolas = bolas_aux;

		###############################################################
		# Comprobamos si ha finalizado la inmunidad.
		###############################################################
		if pygame.time.get_ticks() - tiempoInmunidad > 5000:
			inmune = False;
			if ultima_bola_colisiono != None and ultimo_mosaico != None:
				ultima_bola_colisiono.mosaico = ultimo_mosaico;
			tiempoInmunidad = pygame.time.get_ticks();

		###############################################################
		# Insertamos más bolas.
		###############################################################
		if pygame.time.get_ticks() - tiempoInsertarBola > 3000:
			if len(bolas) < nivel+5 or vidas > 10:
				if nivel<10: insertarBola64();
				elif nivel<20: insertarBola128();
				else: insertarBola256() if randint(0, 10) == 0 else insertarBola128();
			if len(bolas) == 0:
				insertarBola64();
				insertarBola64();
			tiempoInsertarBola = pygame.time.get_ticks();

		###############################################################
		# Comprobamos qué arma tiene el jugador.
		###############################################################
		if pygame.time.get_ticks() - tiempoObtenerFlecha > max(10000, min(nivel*1000, 30000)):
			modo_disparo = "flechas";
			tiempoObtenerFlecha = pygame.time.get_ticks();

		if pygame.time.get_ticks() - tiempoObtenerGancho > 25000 and obtener_gancho == None:
			obtener_gancho = Objeto();
			obtener_gancho.width = obtener_gancho.height = 32;
			obtener_gancho.mosaico = cambio_gancho;
			obtener_gancho.posicion = Vector2D(randint(20, 720), -40);
			obtener_gancho.velocidad = Vector2D(0, 0);
			obtener_gancho.rebote = 0.3;
			obtener_gancho.aceleracion = Vector2D(0, 300);
			tiempoObtenerGancho = pygame.time.get_ticks();

		if pygame.time.get_ticks() - tiempoObtenerPistola > max(10000, min((50-nivel)*1000, 40000)) and obtener_pistola == None:
			obtener_pistola = Objeto();
			obtener_pistola.width = obtener_pistola.height = 32;
			obtener_pistola.mosaico = cambio_pistola;
			obtener_pistola.posicion = Vector2D(randint(20, 720), -40);
			obtener_pistola.velocidad = Vector2D(0, 0);
			obtener_pistola.rebote = 0.3;
			obtener_pistola.aceleracion = Vector2D(0, 300);
			tiempoObtenerPistola = pygame.time.get_ticks();

		###############################################################
		# Renderizamos la escena.
		###############################################################
		ventana.fill((90,140,245));
		pygame.draw.rect(ventana, (0, 0, 0), (margen[0], margen[1], width-margen[0]-margen[2], height-margen[1]-margen[3]), 1);
		for i in flechas:
			i.dibujar(ventana, tiempoTranscurrido);
		for i in ganchos:
			i.dibujar(ventana, tiempoTranscurrido);
		for i in ganchos_anclados:
			i.dibujar(ventana, tiempoTranscurrido);
		for i in disparos:
			i.dibujar(ventana, tiempoTranscurrido);
		if not inmune or randint(0,1) == 0:
			jugador.dibujar(ventana, tiempoTranscurrido);
		else:
			jugador.dibujar(pancarta_nivel.copy(), tiempoTranscurrido);
		for i in bolas:
			i.dibujar(ventana, tiempoTranscurrido);
		if obtener_gancho != None:
			obtener_gancho.dibujar(ventana, tiempoTranscurrido);
		if obtener_pistola != None:
			obtener_pistola.dibujar(ventana, tiempoTranscurrido);

		###############################################################
		# Dibujamos el marco.
		###############################################################
		pygame.draw.rect(ventana, (0, 0, 0), (10, 10, width-20, height-80), 1);
		color_marco = (100, 100, 100);
		pygame.draw.rect(ventana, color_marco, (0, 0, margen[1], height));
		pygame.draw.rect(ventana, color_marco, (0, 0, width, margen[0]));
		pygame.draw.rect(ventana, color_marco, (width-margen[2], 0, margen[2], height));
		pygame.draw.rect(ventana, color_marco, (0, height-margen[3], width, margen[3]));

		###############################################################
		# Mostramos la información de la franja inferior.
		###############################################################
		texto = pygame.font.Font("../resources/otros/futurama.ttf", 17).render('PUNTUACION: ' +  str(puntuacion), True, (0, 0, 0));
		ventana.blit(texto, (margen[0]+1, height-margen[3]+11));
		texto = pygame.font.Font("../resources/otros/futurama.ttf", 17).render('PUNTUACION: ' +  str(puntuacion), True, (255, 255, 255));
		ventana.blit(texto, (margen[0], height-margen[3]+10));

		texto = pygame.font.Font("../resources/otros/futurama.ttf", 17).render('NIVEL: ' +  str(nivel), True, (0, 0, 0));
		ventana.blit(texto, (margen[0]+1, height-margen[3]+31));
		texto = pygame.font.Font("../resources/otros/futurama.ttf", 17).render('NIVEL: ' +  str(nivel), True, (255, 255, 255));
		ventana.blit(texto, (margen[0], height-margen[3]+30));

		texto = pygame.font.Font("../resources/otros/futurama.ttf", 17).render('BOLAS DESTRUIDAS: ' +  str(bolas_destruidas), True, (0, 0, 0));
		ventana.blit(texto, (margen[0]+1, height-margen[3]+51));
		texto = pygame.font.Font("../resources/otros/futurama.ttf", 17).render('BOLAS DESTRUIDAS: ' +  str(bolas_destruidas), True, (255, 255, 255));
		ventana.blit(texto, (margen[0], height-margen[3]+50));

		ventana.blit(bender_cabeza, (width-bender_cabeza.get_width()-margen[0]-margen[2]-80, height-bender_cabeza.get_height()));

		texto = pygame.font.Font("../resources/otros/futurama.ttf", 25).render(str(vidas), True, (0, 0, 0));
		ventana.blit(texto, (width-margen[0]-margen[2]-80+1, height-margen[3]+31));
		texto = pygame.font.Font("../resources/otros/futurama.ttf", 25).render(str(vidas), True, (255, 248, 16) if vidas >= 0 else (250, 50, 50));
		ventana.blit(texto, (width-margen[0]-margen[2]-80, height-margen[3]+30));

		###############################################################
		# Mostramos la pancarta del nivel actual.
		###############################################################
		mostrar_nivel = mostrar_nivel - tiempoTranscurrido;
		if (mostrar_nivel > 0):
			pancarta_nivel_aux = pancarta_nivel.copy();
			texto = pygame.font.Font("../resources/otros/futurama.ttf", 30).render('NIVEL: ' +  str(nivel) if nivel < 100 else 'N: ' +  str(nivel), True, (0, 0, 0));
			pancarta_nivel_aux.blit(texto, (37+1, 37+1));
			texto = pygame.font.Font("../resources/otros/futurama.ttf", 30).render('NIVEL: ' +  str(nivel) if nivel < 100 else 'N: ' +  str(nivel), True, (255, 255, 255));
			pancarta_nivel_aux.blit(texto, (37, 37));

			ventana.blit(pancarta_nivel_aux, (width/2 - pancarta_nivel.get_width()/2, margen[1]+10));

		pygame.display.flip();

		###############################################################
		# Actualizamos los relojes.
		###############################################################
		tiempoTranscurrido = pygame.time.get_ticks() - tiempoUltimaActualizacion;
		tiempoUltimaActualizacion = pygame.time.get_ticks();

	pygame.quit();

if __name__ == "__main__":
	main();