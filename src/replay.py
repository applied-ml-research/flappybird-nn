import game

import sys
import tkinter

FPS = 30
EVERY = 1000//FPS

BACKGROUND = 'white'
BIRD_COLOR = 'black'
BIRD_COLOR_PRESSED = 'red'

canvas_buffer = []

def update(root, canvas, state_list):
  global canvas_buffer
  if not state_list:
    return 

  state = state_list[0]
  if state[game.STATE_FLYING]:
    color = BIRD_COLOR_PRESSED
  else:
    color = BIRD_COLOR

  bird_x = state[game.STATE_BIRD_X]
  bird_y = state[game.STATE_BIRD_Y]
  next_buffer=[]
  next_buffer.append(canvas.create_oval(bird_x - game.BIRD_RADIUS, bird_y - game.BIRD_RADIUS, bird_x + game.BIRD_RADIUS, bird_y + game.BIRD_RADIUS, fill=color))

  for pole in state[game.STATE_POLES]:
    pole_x = pole[game.STATE_POLE_X]
    pole_hole_top = pole[game.STATE_POLE_HOLE_TOP]
    next_buffer.append(canvas.create_line(pole_x, pole_hole_top, pole_x, 0))
    next_buffer.append(canvas.create_line(pole_x, pole_hole_top + game.POLE_HOLE_HEIGHT, pole_x, game.HEIGHT))
  canvas.delete(*canvas_buffer)
  canvas_buffer = next_buffer
  root.after(EVERY, update, root, canvas, state_list[1:]) 

def replay(root, canvas, state_list):
  update(root, canvas, state_list) 
