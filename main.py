from agent import sig, relu
import pygame as pg
import cv2
import random
from random import randint as ri
from numpy.random import uniform as u
import time
import math
import numpy as np
from operator import itemgetter

old_time = time.time()
delta_time = 1 # time.time() to 60 fps

DEBUG = True

FPS = 60

# не трогать
distance = 2 # 1000/1 <-- растояние луча в пикселях *** чем больше тем меньше область видемости dino ***
distance_i = 100 # сколько мы должны сделать шагов для луча --точность-- *** чем больше тем меньше производительность ***
# не трогать

# *** \|/ *** #
dino_count = 10 # сколько dino в обучении *** чем больше тем меньше производительность ***

mutashen_procent = 3 # процент мутации dino 0% - 100% *** в основном не больше 5% ***
# *** /|\ *** #

epoch = 1

WIDTH = 1000
HEIGHT = 500

sc = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE)

old_WIDTH, old_HEIGHT = sc.get_size()

clock = pg.time.Clock()
pg.display.set_caption("DinoBrain")

rect = [pg.Rect(0, 500-25, 9999, 9999)]

luch_coli = [] # dino_count == 1 --> [[], [], []]
for i in range(dino_count):
	luch_coli.append([[], [], []])
luch_break = [False, False, False]

pg.font.init()
font_ComicSansMS = pg.font.Font("Fonts/ComicSansMS.ttf", 16) # 16 - размер шрифта

speed = 6 # скорость кактусов

# *** defs *** #

def get_w():
	ws = []
	for d in range(len(dinos)):
		w = []
		for x in range(8):
			for y in range(3):
				w.append(dinos[d].agent.w[0][x][y])
		for x in range(4):
			for y in range(8):
				w.append(dinos[d].agent.w[1][x][y])
		for x in range(1):
			for y in range(4):
				w.append(dinos[d].agent.w[2][x][y])
		ws.append(w)
	return ws


def uspex_dino():
	dino_ochky = []
	for d in range(len(dinos)):
		dino_ochky.append(dinos[d].kill_time-start_time)

	for e in range(len(dinos)):
		dinos[e].time += dinos[e].kill_time-start_time

	dino_rand = []
	for d in range(len(dino_ochky)):
		dino_rand.append(dino_ochky[d]/sum(dino_ochky))

	dino_w = get_w()

	new_w = []

	for i in range(len(dino_w)):
		delta_w = random.choices(range(len(dino_w)), weights=dino_rand, k=len(dino_w[0]))
		new_w.append([])
		for x in range(len(delta_w)):
			if random.random()*100 <= mutashen_procent:
				new_w[i].append(ri(-1*10000000, 1*10000000)/10000000)
			else:
				new_w[i].append(dino_w[i][delta_w[x]])

	ws = []
	for d in range(len(dinos)):
		w = []
		w.append([])
		for x in range(8):
			w[0].append([])
			for y in range(3):
				w[0][x].append(new_w[d][(x+1)*(y+1)-1])
		w.append([])
		for x in range(4):
			w[1].append([])
			for y in range(8):
				w[1][x].append(new_w[d][24+(x+1)*(y+1)-1])
		w.append([])
		for x in range(1):
			w[2].append([])
			for y in range(4):
				w[2][x].append(new_w[d][32+24+(x+1)*(y+1)-1])
		ws.append(w)

	return ws


def update_dino_w():
	global epoch, start_time
	new_w = uspex_dino()
	for i in range(len(dinos)):
		dinos[i].agent.w = new_w[i]
		dinos[i].kill_time = None
	epoch += 1
	start_time = time.time()


def update_caktoos():
	global speed
	for g in range(1, len(rect)):
		rect[g].x -= speed
		speed += delta_time*0.0005
		if rect[g].x < -100:
			del rect[g]
			caktoos()
			update_caktoos()
			break


def caktoos():
	rect.append(pg.Rect(WIDTH, 500-150-25, 75, 150))


def get_dino():
	
	dino = cv2.imread("Assets/dino.png", cv2.IMREAD_UNCHANGED)
	color = [ri(0, 255), ri(0, 255), ri(0, 255), 255]
	for y in range(len(dino)):
		for x in range(len(dino[y])):
			if dino[y][x][3] != 0:
				dino[y][x] = color
	dino = pg.image.frombuffer(dino.tostring(), dino.shape[1::-1], "RGBA")
	dino = pg.transform.scale(dino, (100, 100))
	
	return [dino, color]


# *** classes *** #

class Colision():
	def __init__(self):
		self.l1 = [1, 0]
		self.l2 = [0.5, 0.5]
		self.l3 = [0, 1]

		self.luch_break = [False, False, False]
		self.luch_coli = [[], [], []]

	def update(self, dino_xy, glob_y):
		self.luch_coli = [[], [], []]

		for i in range(1, distance_i+1):
			for q in range(len(rect)):
				if not self.luch_break[0] and rect[q].collidepoint([dino_xy[0]+self.l1[0]*1000/distance*i/distance_i, dino_xy[1]+self.l1[1]*1000/distance*i/distance_i-glob_y]):
					self.luch_break[0] = True
					self.luch_coli[0] = 1/i
				if not self.luch_break[1] and rect[q].collidepoint([dino_xy[0]+self.l2[0]*1000/distance*i/distance_i, dino_xy[1]+self.l2[1]*1000/distance*i/distance_i-glob_y]):
					self.luch_break[1] = True
					self.luch_coli[1] = 1/i
				if not self.luch_break[0] and rect[q].collidepoint([dino_xy[0]+self.l3[0]*1000/distance*i/distance_i, dino_xy[1]+self.l3[1]*1000/distance*i/distance_i-glob_y]):
					self.luch_break[2] = True
					self.luch_coli[2] = 1/i
		for i in range(len(self.luch_coli)):
			if type(self.luch_coli[i]) == list:
				self.luch_coli[i] = 1/distance_i
		self.luch_break = [False, False, False]

	def out(self):
		return self.luch_coli


class Agent():
	def __init__(self):
		self.time = time.time()

		self.w = []
		self.w.append(u(-1, 1, size=(8, 3)))
		self.w.append(u(-1, 1, size=(4, 8)))
		self.w.append(u(-1, 1, size=(1, 4)))

	def input(self, x1, x2, x3):
		self.x = [x1, x2, x3]

	def update(self):
		self.s1 = np.dot(self.w[0], self.x)
		self.s2 = np.dot(self.w[1], self.s1)
		self.res = np.dot(self.w[2], self.s2)

	def out(self):
		return sig(self.res)[0]


class Dino():
	def __init__(self, agent, colision, dino, plaer=False):
		self.x, self.y = 300, 475
		self.x_glaas = self.x-37
		self.y_glaas = self.y-110
		self.glob_y = 0

		self.is_jump = False
		self.jump_time = None

		self.agent = agent
		self.colision = colision
		self.dino = dino[0]
		self.color = dino[1]

		self.plaer = plaer

		self.kill_time = None
		self.time = 0

	def jump(self):
		if not self.jump_time:
			self.jump_time = time.time()
		if self.jump_time:
			self.glob_y = math.sin((time.time()-self.jump_time)*3)
			if self.glob_y < 0:
				self.glob_y = 0
				self.jump_time = None
				self.is_jump = False

	def input(self):
		if self.plaer:
			keys = pg.key.get_pressed()
			if self.is_jump == False:
				self.is_jump = keys[pg.K_SPACE]
		else:
			self.colision.update([self.x_glaas, self.y_glaas], self.glob_y*250)
			self.agent.input(*self.colision.out())
			self.agent.update()
			if self.is_jump == False:
				self.is_jump = round(self.agent.out()) == 1
		if self.is_jump:
			self.jump()

	def draw(self):
		sc.blit(self.dino, [self.x-self.dino.get_rect().w, self.y-self.dino.get_rect().h-self.glob_y*250])

	def kill(self):
		if not self.kill_time:
			self.kill_time = time.time()
			self.glob_y = 0

	def update(self):
		if pg.Rect(self.x-self.dino.get_rect().w, self.y-self.dino.get_rect().h-self.glob_y*250, self.dino.get_rect().w, self.dino.get_rect().h).colliderect(rect[1]):
			self.kill()
		if not self.kill_time:
			self.input()
			self.draw()

	def update_w(self):
		update_dino_w()


dinos = []
for i in range(dino_count):
	dinos.append(Dino(Agent(), Colision(), get_dino()))
start_time = time.time()
caktoos()

while True:
	# *** delta *** #

	delta_time = (time.time()-old_time)*60
	old_time = time.time()

	# *** проверки событий *** #

	keys = pg.key.get_pressed()

	for event in pg.event.get():
		if event.type == pg.QUIT:
			exit()
	if old_WIDTH != WIDTH or old_HEIGHT != HEIGHT:
		old_WIDTH, old_HEIGHT = sc.get_size()
	WIDTH, HEIGHT = sc.get_size()
	if DEBUG:
		if event.type == pg.KEYUP or keys[pg.K_z]:
			if keys[pg.K_SPACE]:
				pass
			if keys[pg.K_LEFT]:
				speed -= 1
				speed = max(speed, 1)
			if keys[pg.K_RIGHT]:
				speed += 1
		if keys[pg.K_SPACE]:
			jump = True
		else:
			jump = False

	sc.fill((24, 20, 37))

	out = False
	for i in range(len(dinos)):
		if not dinos[i].kill_time:
			out = True
	if out:
		for a in range(len(dinos)):
			dinos[a].update()
			text1 = font_ComicSansMS.render(str(round(dinos[a].time, 1)), True, dinos[a].color)
			sc.blit(text1, [30+(WIDTH-60)/dino_count*a, dinos[a].glob_y*-15+50-int(not not dinos[a].kill_time)*-30])
	else:
		update_dino_w()
		rect[1].x = 1000

	update_caktoos()
	for j in range(len(rect)): # кактусыыы кактусыыы
		pg.draw.rect(sc, (128, 255, 128), rect[j])

	pg.display.set_caption("fps: "+str(round(clock.get_fps()))+" | speed: "+str(round(speed, 2))+" | epoch: "+str(epoch))#+str(1/luch_coli[0][0][0]))
	pg.display.flip()
	clock.tick(FPS)