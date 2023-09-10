import agent
import pygame as pg
#import cv2
from random import randint as ri
from numpy.random import uniform as u
import time
import math
#from numba import njit
import numpy as np
from operator import itemgetter

old_time = time.time()
delta_time = 1 # time.time() to 60 fps

DEBUG = True

FPS = 60

distance = 2 # 1000/1 <-- растояние луча в пикселях *** чем больше тем меньше область видемости dino ***
distance_i = 100 # сколько мы должны сделать шагов для луча --точность-- *** чем больше тем меньше производительность ***

dino_count = 1 # сколько dino в обучении *** чем больше тем меньше производительность ***

WIDTH = 1000
HEIGHT = 500

sc = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE)

old_WIDTH, old_HEIGHT = sc.get_size()

clock = pg.time.Clock()
pg.display.set_caption("horrortayle")


rect = [pg.Rect(0, 500-25, 1000, 25)]


luch_coli = [] # dino_count == 1 --> [[], [], []]
for i in range(dino_count):
	luch_coli.append([[], [], []])
luch_break = [False, False, False]


def rand_dino():
	rand = ri(0, int(sum(uspex)*(10**7)))/(10**7)
	#print(rand, sum(uspex))
	#print(sum(uspex), rand)
	q = 0
	for i in range(len(agent_dino)):
		#print(q, rand, q+uspex[i])
		if q <= rand < q+uspex[i]:
			#print(i+1)
			proc[i] += 1
			break
		q += uspex[i]
	return i


def update_w():
	uspex = []
	
	for i in range(len(agent_dino)):
		if i == 2:
			time.sleep(5)
		uspex.append(agent_dino[i].kill())
	procent = 100/sum(uspex)#/100

	proc = [0, 0, 0, 0, 0]

	for i in range(1000):
		rand = ri(0, int(sum(uspex)*(10**7)))/(10**7)
		#print(rand, sum(uspex))
		#print(sum(uspex), rand)
		q = 0
		for i in range(len(agent_dino)):
			#print(q, rand, q+uspex[i])
			if q <= rand < q+uspex[i]:
				#print(i+1)
				proc[i] += 1
				break
			q += uspex[i]
	print(proc)


def update_caktoos():
	for g in range(1, len(rect)):
		rect[g].x -= 5*delta_time
		if rect[g].x < -100:
			del rect[g]
			caktoos()
			update_caktoos()
			break



def caktoos():
	rect.append(pg.Rect(1000, 500-150-25, 75, 150))


def rect_to(rect_cub):
	return rect_cub.x, rect_cub.y, rect_cub.w, rect_cub.y


def get_dino():
	"""
	dino = cv2.imread("dino.png", cv2.IMREAD_UNCHANGED) #pg.image.load('img/plaer/plaer.png')
	color = [ri(0, 255), ri(0, 255), ri(0, 255), 255]
	for y in range(len(dino)):
		for x in range(len(dino[y])):
			if dino[y][x][3] != 0:
				dino[y][x] = color
	dino = pg.image.frombuffer(dino.tostring(), dino.shape[1::-1], "BGRA")
	dino = pg.transform.scale(dino, (100, 100))
	"""
	return pg.Rect(0, 0, 75, 150) #dino


def delit(x):
	if x == 0:
		return 1
	else:
		return 1/x

#namba)
def post_coli():
	for i in range(dino_count):
		if len(luch_coli[i][0]) == 0:
			luch_coli[i][0] = [1000]
		if len(luch_coli[i][1]) == 0:
			luch_coli[i][1] = [1000]
		if len(luch_coli[i][2]) == 0:
			luch_coli[i][2] = [1000]

		if len(luch_coli[i][0]) >= 2:
			luch_coli[i][0] = [min(luch_coli[i][0])]
		if len(luch_coli[i][1]) >= 2:
			luch_coli[i][1] = [min(luch_coli[i][1])]
		if len(luch_coli[i][2]) >= 2:
			luch_coli[i][2] = [min(luch_coli[i][2])]


class Colision():
	def __init__(self):
		self.l1 = [1, 0]
		self.l2 = [0.5, 0.5]
		self.l3 = [0, 1]

		self.luch_break = [False, False, False]
		self.luch_coli = [[], [], []]

	def update(self, dino_xy, glob_y):
		self.luch_coli = [[], [], []]

		for i in range(distance_i):
			for q in range(len(rect)):
				if not self.luch_break[0] and rect[q].collidepoint([dino_xy[0]+self.l1[0]*1000/distance*i/distance_i, dino_xy[1]+self.l1[1]*1000/distance*i/distance_i]):
					pg.draw.circle(sc, [255, 0, 0], [dino_xy[0]+self.l1[0]*1000/distance*i/distance_i, dino_xy[1]+glob_y+self.l1[1]*1000/distance*i/distance_i])
					self.luch_break[0] = True
					luch_coli[0] = 1/i
				if not self.luch_break[1] and rect[q].collidepoint([dino_xy[0]+self.l2[0]*1000/distance*i/distance_i, dino_xy[1]+self.l2[1]*1000/distance*i/distance_i]):
					pg.draw.circle(sc, [255, 0, 0], [dino_xy[0]+self.l2[0]*1000/distance*i/distance_i, dino_xy[1]+glob_y+self.l2[1]*1000/distance*i/distance_i])
					self.luch_break[1] = True
					luch_coli[1] = 1/i
				if not self.luch_break[0] and rect[q].collidepoint([dino_xy[0]+self.l3[0]*1000/distance*i/distance_i, dino_xy[1]+self.l3[1]*1000/distance*i/distance_i]):
					pg.draw.circle(sc, [255, 0, 0], [dino_xy[0]+self.l3[0]*1000/distance*i/distance_i, dino_xy[1]+glob_y+self.l3[1]*1000/distance*i/distance_i])
					self.luch_break[2] = True
					luch_coli[2] = 1/i
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
		print(self.x)
	def out(self):
		return self.res


class Dino():
	def __init__(self, agent=Agent(), colision=Colision(), dino=get_dino(), plaer=False):
		self.x, self.y = 300, 475
		self.x_glaas = self.x+25
		self.y_glaas = self.y+75
		self.glob_y = 0

		self.is_jump = False
		self.jump_time = None

		self.agent = agent
		self.colision = colision
		self.dino = dino

		self.plaer = plaer

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
			self.colision.update([self.x_glaas, self.y_glaas], self.glob_y)
			self.agent.input(*self.colision.out())
			self.agent.update()
			print(self.agent.out())
			self.is_jump = round(self.agent.out()) == 1
		if self.is_jump:
			self.jump()

	def draw(self):
		pg.draw.rect(sc, [255, 255, 255], pg.Rect(self.x-self.dino.w, self.y-self.dino.h-self.glob_y*250, self.dino.w, self.dino.h))

	def update(self):
		self.input()
		self.draw()

dinos = []
for i in range(dino_count):
	dinos.append(Dino())


for i in range(2):
	caktoos()
	for j in range(250):
		update_caktoos()

#update_w()

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
		if keys[pg.K_SPACE]:
			jump = True
		else:
			jump = False

	sc.fill((24, 20, 37))

	for i in range(dino_count):
		dinos[i].update()

	for j in range(len(rect)): # кактусыыы кактусыыы
		pg.draw.rect(sc, (0, 255, 255), rect[j])

	update_caktoos()

	pg.display.set_caption(str(round(clock.get_fps())))#+str(1/luch_coli[0][0][0]))
	pg.display.flip()
	clock.tick(FPS)
"""



	for i in range(distance_i):
		if not collidepoint(agent_dino.x_glaas+1000/distance*i/distance_i, agent_dino.y_glaas+0/distance*i/distance_i, rect.x, rect.y, rect.w, rect.h):
			pg.draw.circle(sc, [255, 0, 0], (agent_dino.x_glaas+1000/distance*i/distance_i, agent_dino.y_glaas+0/distance*i/distance_i), 3)
		if not collidepoint(agent_dino.x_glaas+750/distance*i/distance_i, agent_dino.y_glaas+250/distance*i/distance_i, rect.x, rect.y, rect.w, rect.h):
			pg.draw.circle(sc, [255, 0, 0], (agent_dino.x_glaas+750/distance*i/distance_i, agent_dino.y_glaas+250/distance*i/distance_i), 3)
		if not collidepoint(agent_dino.x_glaas+500/distance*i/distance_i, agent_dino.y_glaas+500/distance*i/distance_i, rect.x, rect.y, rect.w, rect.h):
			pg.draw.circle(sc, [255, 0, 0], (agent_dino.x_glaas+500/distance*i/distance_i, agent_dino.y_glaas+500/distance*i/distance_i), 3)
		if not collidepoint(agent_dino.x_glaas+250/distance*i/distance_i, agent_dino.y_glaas+750/distance*i/distance_i, rect.x, rect.y, rect.w, rect.h):
			pg.draw.circle(sc, [255, 0, 0], (agent_dino.x_glaas+250/distance*i/distance_i, agent_dino.y_glaas+750/distance*i/distance_i), 3)
		if not collidepoint(agent_dino.x_glaas+0/distance*i/distance_i, agent_dino.y_glaas+1000/distance*i/distance_i, rect.x, rect.y, rect.w, rect.h):
			pg.draw.circle(sc, [255, 0, 0], (agent_dino.x_glaas+0/distance*i/distance_i, agent_dino.y_glaas+1000/distance*i/distance_i), 3)
"""