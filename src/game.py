import random

WIDTH = 800
HEIGHT = 600

BIRD_X = 100
BIRD_START_Y = 300
BIRD_RADIUS = 10

GRAVITY = 0.8

POLE_HOLE_HEIGHT = 100
POLE_MARGIN = 50
POLE_MIN_BOT = HEIGHT - POLE_MARGIN
POLE_MAX_TOP = POLE_MARGIN
POLE_THRESHOLD = 500
POLE_VELOCITY_X = 7

STATE_BIRD_X = 0
STATE_BIRD_Y = 1
STATE_FLYING = 2
STATE_POLES = 3

STATE_POLE_X = 0
STATE_POLE_HOLE_TOP = 1

REWARD_SURVIVAL = 1
REWARD_DEATH = -100

class Bird:
  def __init__(self):
    self.x = BIRD_X
    self.y = BIRD_START_Y
    self.radius = BIRD_RADIUS
    self.acceleration = GRAVITY
    self.velocity_y = 0

  def update(self, flying):
    if flying:
      self.acceleration = -GRAVITY
    else:
      self.acceleration = GRAVITY
    self.velocity_y += self.acceleration
    self.y += self.velocity_y

    return not self.y <= 0 and not self.y >= HEIGHT

class Pole:
  def __init__(self):
    try:
      self.hole_top = random.randint(POLE_MAX_TOP, POLE_MIN_BOT - POLE_HOLE_HEIGHT)
    except ValueError as e:
      raise Exception("Pole creation failed: difference between POLE_MAX_TOP and POLE_MIN_BOT is less than POLE_HOLE_HEIGHT").with_traceback(e.__traceback__) from None
    self.x = WIDTH

  def update(self):
    self.x -= POLE_VELOCITY_X

class Game:
  def __init__(self):
    self.bird = Bird()
    self.poles = [Pole()]
    self.score = 0
    self.alive = True

    self.states = []
    self.__add_current_state(False)

  def __add_current_state(self, flying):
    self.states.append((
      self.bird.x,
      self.bird.y,
      flying,
      tuple(map(lambda pole: (pole.x, pole.hole_top), self.poles))
    ))

  def cleanup(self):
    del self.bird
    del self.poles

  def update(self, flying):
    self.score += 1
    bird = self.bird
    if not bird.update(flying):
      self.cleanup()
      self.alive = False
      return False
    for pole in self.poles:
      pole.update()
      if pole.x >= bird.x - bird.radius and pole.x <= bird.x + bird.radius:
        if pole.hole_top >= bird.y - bird.radius or pole.hole_top + POLE_HOLE_HEIGHT <= bird.y + bird.radius:
          self.cleanup()
          self.alive = False
          return False
    if self.poles[0].x <= bird.x:
      self.poles = self.poles[1:] 
    if self.poles[-1].x <= POLE_THRESHOLD:
      self.poles.append(Pole())
    self.__add_current_state(flying)
    return True

  def get_nn_inputs(self):
    reward = REWARD_SURVIVAL if self.alive else REWARD_DEATH
    return reward, self.alive, self.score
