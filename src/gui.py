import tkinter

FPS = 30
EVERY = 1000//FPS

def update(root):
  print("tick")
  root.after(EVERY, update, root) 

def main():
  root = tkinter.Tk()
  update(root)
  root.mainloop()

if __name__ == '__main__':
  main()
