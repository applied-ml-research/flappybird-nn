import game

import tkinter

FPS = 30
EVERY = 1000//FPS

BACKGROUND = 'white'
BIRD_COLOR = 'black'
BIRD_COLOR_PRESSED = 'red'

space_pressed = False
canvas_buffer = []

def main():
  root = tkinter.Tk()
  root.attributes('-type', 'dialog')
  canvas = tkinter.Canvas(root, bg=BACKGROUND, height=game.HEIGHT, width=game.WIDTH)
  canvas.pack()
  gm = game.Game() 
  root.bind('<KeyPress-Return>', handleKeyPress)
  root.bind('<KeyRelease-Return>', handleKeyRelease)
  update(root, canvas, gm)
  root.mainloop()

def update(root, canvas, gm):
  global space_pressed
  global canvas_buffer
  if not gm.update(space_pressed):
    gm = game.Game() 

  if space_pressed:
    color = BIRD_COLOR_PRESSED
  else:
    color = BIRD_COLOR
  next_buffer=[]
  bird = gm.bird
  next_buffer.append(canvas.create_oval(bird.x - bird.radius, bird.y - bird.radius, bird.x + bird.radius, bird.y + bird.radius, fill=color))

  for pole in gm.poles:
    next_buffer.append(canvas.create_line(pole.x, pole.hole_top, pole.x, 0))
    next_buffer.append(canvas.create_line(pole.x, pole.hole_top + game.POLE_HOLE_HEIGHT, pole.x, game.HEIGHT))
  canvas.delete(*canvas_buffer)
  canvas_buffer = next_buffer
  root.after(EVERY, update, root, canvas, gm) 

def handleKeyPress(event):
  global space_pressed
  space_pressed = True 

def handleKeyRelease(event):
  global space_pressed
  space_pressed = False 

if __name__ == '__main__':
  main()
