from __future__ import print_function
import pygame
import sys, os
sys.path.append("game/")
#import wrapped_flappy_bird as game
import atari_wrapper as game
import numpy as np
def main():

    #check if game exists
    gamePath = "roms/"+sys.argv[1]+".bin"
    if not os.path.exists(gamePath):
        print ('Error:'+gamePath+' does not exists.')
        gamePath = "roms/"+sys.argv[1]+".BIN"
        print ("Try "+gamePath)
        if not os.path.exists(gamePath):
            raise IOError('Error:'+gamePath+' does not exists.')

    print (2, pygame.K_2)
    #get how many legal actions in actionNum to initialize Neural Network
    game_state=game.GameState(gamePath)
    actionNum = len(game_state.legal_actions)
    while "flappy bird" != "angry bird":
        a_t = np.zeros(actionNum)
        a_t[0] = 1
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE] != 0:
            pygame.quit()
            sys.exit()

        for i in range(1, actionNum+1):
            if keys[i+48] != 0:
                print (i)
                a_t = np.zeros(actionNum)
                a_t[i-1] = 1
                image, r_t, terminal_=game_state.frame_step(a_t)

                break

        image, r_t, terminal_=game_state.frame_step(a_t)
        pygame.event.pump()



if __name__ == "__main__":
    main()
