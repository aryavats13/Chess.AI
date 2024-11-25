import pygame
import sys

from const import *
class Main:
    def __init__(self):
        pygame.init()
        self.screen=pygame.display.set_mode((witdh,height))
        pygame.display.set_caption('chess')

    def mainloop(self):

        while True:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()  




            pygame.display.update()


main=Main()
main.mainloop()