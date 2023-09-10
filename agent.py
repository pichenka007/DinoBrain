import numpy as np
from random import randint as ri
from random import random as r
from numpy.random import uniform as u
import matplotlib.pyplot as plt
import time

# random.uniform(-1, 1)


def sig(x):
	list_sig = []
	for i in range(len(x)):
		list_sig.append(1/(1 + np.exp(-x[i])))
	return list_sig# если перед 1 поставить - то всё упадёт *практически


def relu(x):
	list_relu = []
	for i in range(len(x)):
		list_relu.append(max(0, x[i]))
	return list_relu


def get_bool(x):
	if x >= 0.5:
		return True
	else:
		return False


class Agent():
	def __init__(self, dino_img):
		self.x = 100+500
		self.y = 350-300

		self.x_glaas = self.x+55
		self.y_glaas = self.y+5

		self.dino = dino_img
		
		self.time = time.time()

		self.w = []
		self.w.append(u(-1, 1, size=(64, 3)))
		self.w.append(u(-1, 1, size=(32, 64)))
		self.w.append(u(-1, 1, size=(1, 32)))

	def rezult(self, n):
		self.neyron = n
		self.o1 = np.dot(self.w[0], self.neyron)
		self.o2 = np.dot(self.w[1], self.o1)
		self.o3 = sig(np.dot(self.w[2], self.o2))
		print(round(self.o3[0]))
		return self.o3

	def get_w(self):
		delta_w = []
		for i in range(len(self.w)):
			for j in range(len(self.w[i])):
				delta_w.append(w[i][j])
		return self.w


	def update_coordinates(self, x_y):
		self.x, self.y = x_y
		self.x_glaas, self.y_glaas = self.x+55, self.y+5

	def kill(self):
		self.time_kill = time.time() - self.time
		return self.time_kill