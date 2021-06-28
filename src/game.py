import random

BIRD_X = 50
BIRD_START_Y = 300
GRAVITY = 0.8

POLE_HOLE_HEIGHT = 100
POLE_SPAWN_X = 800

class Bird:
  def __init__(self):
    self.x = BIRD_X
    self.y = BIRD_START_Y
    self.acceleration = GRAVITY
    self.y_velocity = 0

class Pole:
  def __init__(self, min_bot, max_top):
    try:
      self.hole_top = random.randint(min_bot + POLE_HOLE_HEIGHT, max_top)
    except ValueError as e:
      raise Exception("Pole creation failed: difference between max_top and min_bot is less than POLE_HOLE_HEIGHT").with_traceback(e.__traceback__) from None
    self.x = POLE_SPAWN_X
