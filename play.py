from __future__ import print_function
import pygame
pygame.init()
pygame.display.init() 
pygame.display.list_modes()
import tensorflow as tf
import sys
sys.path.append("game/")
import wrapped_flappy_bird as game
import random
import numpy as np
from collections import deque
def main():

    game_state=game.GameState()
    while "flappy bird" != "angry bird":
        if pygame.key.get_pressed()[pygame.K_UP]!=0:
            _,_,_=game_state.frame_step([0,1])
        else:
            _,_,_=game_state.frame_step([1,0])

if __name__ == "__main__":
    main()
