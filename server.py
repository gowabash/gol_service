#! /usr/bin/env python 
from flask import Flask
from flask import jsonify
from flask import request
import random

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/gol/<size>")
def create(size):
	size = int(size)
	world = make_new_world(size)
	print request.args 
	print request.args.get('random')
	if request.args.get('random', '') != '':
		for i in range(size):
			for j in range(size):
				world[i][j] = random.randint(0,1)
	return jsonify(world)

@app.route("/gol", methods=['POST'])
def get_next_gen():
	val = request.get_json()
	print len(val)
	world = next_gen(val)
	return jsonify(world)

def make_new_world(size):
	world = [0]*size
	for i in range(size):
		world[i] = [0]*size
	return world

def next_gen(world):
	size = len(world)
	next_generation = make_new_world(size)
	for x in range(size):
		for y in range(size):
			n = num_live_neighbours(world, x,y)
			next_state = state_next_turn(n, world[x][y])
			next_generation[x][y] = next_state
	return next_generation

def state_next_turn(n,curr_state):
	if curr_state == 1:
		if n==2 or n==3 :
			return 1
	else:
		if n==3:
			return 1
	return 0

def num_live_neighbours(world, x,y):
	neighbours = 0
	if check_bounds(x,y, len(world)):
		if world[x-1][y-1] == 1:
			neighbours = neighbours + 1
		if world[x][y-1] == 1:
			neighbours = neighbours + 1
		if world[x+1][y-1] == 1:
			neighbours = neighbours + 1
		if world[x-1][y] == 1: 
			neighbours = neighbours + 1
		if world[x+1][y] == 1:
			neighbours = neighbours + 1
		if world[x-1][y+1] == 1:
			neighbours = neighbours + 1
		if world[x][y+1] == 1:
			neighbours = neighbours + 1
		if world[x+1][y+1] == 1:
			neighbours = neighbours + 1
	else:
		pass
	return neighbours

def check_bounds(x,y,size):
	if x==0 or x==(size -1) or y==0 or y==(size - 1):
		return False
	return True

if __name__ == "__main__":
    app.run(debug=True)

