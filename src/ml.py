import game
import replay

import pickle
import random
import torch

DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

def init_nn_1(learning_rate=0.1):
  model = torch.nn.Sequential(
    torch.nn.Linear(4, 8),
    torch.nn.ReLU(),
    torch.nn.Linear(8, 6),
    torch.nn.Sigmoid(),
    torch.nn.Linear(6, 2),
  ).to(DEVICE)
  return {
    'model': model,
    'loss': torch.nn.MSELoss(),
    'optimizer': torch.optim.SGD(model.parameters(), lr=learning_rate),
    'memory': [],
  }

def eval_nn_1(nn, gm):
  bird = gm.bird
  pole = gm.poles[0]
  evaluation = nn['model'](torch.FloatTensor([bird.y, bird.velocity_y, pole.x, pole.hole_top]).to(DEVICE))
  nn['memory'].append(evaluation)
  return evaluation[1] > evaluation[0]

def train_nn_1(nn, reward=1.0, death_reward=-100.0, reward_decay=0.9, sample_ratio=0.3):
  states = len(nn['memory'])
  sample = random.sample(range(states - 1), int(states * sample_ratio))

  def step(mem_idx, target):
    nn['optimizer'].zero_grad()
    loss = nn['loss'](nn['memory'][mem_idx], target)
    loss.backward()
    nn['optimizer'].step()

  step(-1, torch.tensor(death_reward).to(DEVICE))
  for idx in sample:
    step(sample[idx], reward + reward_decay * nn['memory'][sample[idx] + 1])

  nn['memory'] = []

def run(file, nn_params={'init': init_nn_1, 'eval': eval_nn_1, 'train': train_nn_1}, save_every=100, until=100000):
  nn = nn_params['init']()
  data = []
  for i in range(1, until + 1):
    gm = game.Game()
    game_end = False
    flying = False 
    while not game_end:
      flying = nn_params['eval'](nn, gm)
      game_end = gm.update(flying)
    data.append(gm.states)    
    nn_params['train'](nn)

    if i % save_every == 0:
      pickle.dump(data, open(file, 'wb'))
      print('saved (epoch %d)' % i)

def load_results(file):
  return pickle.load(open(file, 'rb'))
