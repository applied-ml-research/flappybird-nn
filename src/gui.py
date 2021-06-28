import tkinter

EVERY = 2000

def update(root):
  print("tick")
  root.after(EVERY, update, root) 

def main():
  root = tkinter.Tk()
  update(root)
  root.mainloop()

if __name__ == '__main__':
  main()
