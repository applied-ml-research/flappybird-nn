import game

import tkinter

FPS = 30
EVERY = 1000//FPS

space_pressed = False

def update(root, canvas, gm):
  canvas.delete('all')
  global space_pressed
  if not gm.update(space_pressed):
    gm = game.Game() 

  bird = gm.bird
  canvas.create_oval(bird.x - bird.radius, bird.y - bird.radius, bird.x + bird.radius, bird.y + bird.radius)

  for pole in gm.poles:
    canvas.create_line(pole.x, pole.hole_top, pole.x, 0)
    canvas.create_line(pole.x, pole.hole_top + game.POLE_HOLE_HEIGHT, pole.x, game.HEIGHT)
  root.after(EVERY, update, root, canvas, gm) 

def main():
  root = tkinter.Tk()
  root.attributes('-type', 'dialog')
  canvas = tkinter.Canvas(root, bg="white", height=game.HEIGHT, width=game.WIDTH)
  canvas.pack()
  gm = game.Game() 
  root.bind('<KeyPress-Return>', handleKeyPress)
  root.bind('<KeyRelease-Return>', handleKeyRelease)
  update(root, canvas, gm)
  root.mainloop()

def handleKeyPress(event):
  global space_pressed
  space_pressed = True 

def handleKeyRelease(event):
  global space_pressed
  space_pressed = False 

if __name__ == '__main__':
  main()
