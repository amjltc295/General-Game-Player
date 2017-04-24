#!/usr/bin/env python
# python_example.py
# Author: Ben Goodrich
#
# This is a direct port to python of the shared library example from
# ALE provided in doc/examples/sharedLibraryInterfaceExample.cpp
import sys
from random import randrange
sys.path.append('/home/allen/tensorflow/DeepLearningFlappyBird/Arcade-Learning-Environment-0.5.1')
print (sys.path)
from ale_python_interface.ale_python_interface import ALEInterface
import pygame
import numpy as np
if len(sys.argv) < 2:
  print ('Usage:', sys.argv[0], 'rom_file')
  sys.exit()

ale = ALEInterface()

# Get & Set the desired settings
ale.setInt('random_seed', 123)

# Set USthe code in the module will be executed, just as if you imported it, but with the __name__ set to "__main__". That means that by adding this code at the end of your module:

USE_SDL = False
if USE_SDL:
  if sys.platform == 'darwin':
    import pygame
    pygame.init()
  elif sys.platform.startswith('linux'):
    ale.setBool('sound', True)
  ale.setBool('display_screen', True)

# Load the ROM file
ale.loadROM(sys.argv[1])

# Get the list of legal actions
legal_actions = ale.getLegalActionSet()
print (len(legal_actions))
for each in legal_actions:
    print (each)

pygame.init()
size = width, height = ale.getScreenDims()
print ("Size:", size)
#size = width, height = 480, 640
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


# Play 10 episodes
for episode in xrange(10):
  total_reward = 0
  count = 0
  action_index = 1
  while not ale.game_over():
    count += 1
    if count % 60 == 0:
        action_index += 1
        
    print (action_index)
    a = legal_actions[action_index % len(legal_actions)]
    # Apply an action and get the resulting reward
    reward = ale.act(a);
    total_reward += reward
    screen_data = ale.getScreen()
    #screen_data = ale.getScreenRGB()
    screen_data = np.reshape(screen_data, (-1, width)).T
    #print (screen_data.shape)
    #bv = screen.get_buffer()
    #bv.write(screen_data.tostring(), 0)
    data = pygame.surfarray.make_surface(screen_data)
    screen.blit(data, (0,0))
    pygame.display.flip()
    clock.tick(30)
  print ('Episode', episode, 'ended with score:', total_reward)
  ale.reset_game()
