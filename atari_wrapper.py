#!/usr/bin/env python
# python_example.py
# Author: Ben Goodrich
#
# This is a direct port to python of the shared library example from
# ALE provided in doc/examples/sharedLibraryInterfaceExample.cpp
import sys
from random import randrange
#from ale_python_interface import ALEInterface
sys.path.append('Arcade-Learning-Environment-0.5.1')
from ale_python_interface.ale_python_interface import ALEInterface
#import ALEInterface
import pygame
import numpy as np

def getActionNum(filename):
    ale = ALEInterface()
    ale.loadROM(filename)

    legal_actions = ale.getMinimalActionSet()
    actionNum =  len(legal_actions)
    print ("ActionNum:", actionNum)
    return actionNum
    
class GameState():
    def __init__(self, filename):
        self.ale = ALEInterface()
        self.ale.setInt('random_seed', 123)
        #self.ale.loadROM('roms/Breakout.bin')
        #self.ale.loadROM(sys.argv[1])
        print ("Load:" + filename)
        self.ale.loadROM(filename)

        self.legal_actions = self.ale.getMinimalActionSet()
        print ("Action size: ", len(self.legal_actions))

        pygame.init()
        self.size = self.width, self.height = self.ale.getScreenDims()
        print ("Window size:", self.size)
        i = raw_input("Press ENTER to continue")
        #size = width, height = 480, 640
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        

    def frame_step(self, input_actions):
        a = None
        if sum(input_actions) != 1:
            raise ValueError('Multiple input actions!')
        for i in range(len(input_actions)):
            if input_actions[i] == 1:
                a = self.legal_actions[i]
                break
        reward = self.ale.act(a);
        terminal = self.ale.game_over()
        if not terminal:
            if reward > 1: reward = 1
            elif reward < 1: reward = 0.1
            if reward < 0: reward = -1
        else: 
            reward = -1
            self.ale.reset_game()
    
        image_data = self.ale.getScreen()
        #screen_data = ale.getScreenRGB()
        image_data = np.reshape(image_data, (-1, self.width)).T
        data = pygame.surfarray.make_surface(image_data)
        self.screen.blit(data, (0,0))
        pygame.display.flip()
        self.clock.tick(30)
        image_data = pygame.surfarray.array3d(pygame.display.get_surface())
        return image_data, reward, terminal
"""
if len(sys.argv) < 2:
  print 'Usage:', sys.argv[0], 'rom_file'
  sys.exit()
ale = ALEInterface()

# Get & Set the desired settings
ale.setInt('random_seed', 123)

# Set USE_SDL to true to display the screen. ALE must be compilied
# with SDL enabled for this to work. On OSX, pygame init is used to
# proxy-call SDL_main.
USE_SDL = False
if USE_SDL:
  if sys.platform == 'darwin':
    import pygame
    pygame.init()
    ale.setBool('sound', False) # Sound doesn't work on OSX
  elif sys.platform.startswith('linux'):
    ale.setBool('sound', True)
  ale.setBool('display_screen', True)

# Load the ROM file
ale.loadROM(sys.argv[1])

# Get the list of legal actions
legal_actions = ale.getLegalActionSet()
print (len(legal_actions))
print legal_actions
for each in legal_actions:
    print each

pygame.init()
size = width, height = ale.getScreenDims()
print ("Size:", size)
#size = width, height = 480, 640
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


# Play 10 episodes
for episode in xrange(10):
  total_reward = 0
  while not ale.game_over():
    a = legal_actions[randrange(len(legal_actions))]
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
  print 'Episode', episode, 'ended with score:', total_reward
  ale.reset_game()
"""
