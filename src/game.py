import random

WIDTH = 800
HEIGHT = 600

BIRD_X = 100
BIRD_START_Y = 300
GRAVITY = 0.8

POLE_HOLE_HEIGHT = 100
POLE_MIN_BOT = 0
POLE_MAX_TOP = 800

class Bird:
  def __init__(self):
    self.x = BIRD_X
    self.y = BIRD_START_Y
    self.acceleration = GRAVITY
    self.y_velocity = 0

class Pole:
  def __init__(self):
    try:
      self.hole_top = random.randint(POLE_MIN_BOT + POLE_HOLE_HEIGHT, POLE_MAX_TOP)
    except ValueError as e:
      raise Exception("Pole creation failed: difference between POLE_MAX_TOP and POLE_MIN_BOT is less than POLE_HOLE_HEIGHT").with_traceback(e.__traceback__) from None
    self.x = WIDTH
