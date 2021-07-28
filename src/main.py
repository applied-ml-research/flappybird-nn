import ml
import replay

import sys

def main():
  try:
    action = sys.argv[1]
    file = sys.argv[2]
    if action == 'replay':
      epoch = sys.argv[3]
    elif action != 'learn':
      raise Exception
  except Exception as e:
    raise Exception('replay [file] [epoch] OR learn [file]') from e

  if action == 'learn':
    ml.run(file)
  else:
    replay.replay(file, int(epoch))

if __name__ == '__main__':
  main()
