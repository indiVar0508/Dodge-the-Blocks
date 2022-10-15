import pygame
import time
from .blocks import Block
from .player import Player 

class Game:
    
    def __init__(self, windowWidth = 800, windowHeight = 600):
        self.windowWidth = windowWidth // 2
        self.windowHeight = windowHeight
        self.gameDisplay = pygame.display.set_mode((windowWidth, windowHeight))
        pygame.display.set_caption("Dodge the Blocks!")
        self.blocks = Block(windowWidth // 2, windowHeight, n = 5, speed = 0.5)
        self.player = Player(windowWidth // 2, windowHeight, 5, 10)
        self.score = 0
        
    def sayMessage(self, msg, fontType = 'freesansbold.ttf', color = (255, 255, 255),
                   fontSize = 15, loc = (410, 10)):
        myMsg = pygame.font.Font(fontType, fontSize).render(msg, True, color)
        self.gameDisplay.blit(myMsg, loc)  
        
    def checkCrashed(self):                 # y of block                   # height of block
        if (self.player.y-self.player.rad > self.blocks.cordsBlock[0][1] + self.blocks.cordsBlock[0][3]) or (self.blocks.cordsBlock[self.blocks.safeBlockIndex][0] < self.player.x <\
        self.blocks.cordsBlock[self.blocks.safeBlockIndex][0] + \
        self.blocks.cordsBlock[self.blocks.safeBlockIndex][2]): return
        self.player.dead = True
        

    def reset(self):
        self.player.reset()
        self.blocks.cordsBlock = self.blocks.buildCords()
        self.blocks.speed = 0.5 # correction forgot to add in video 
        self.score = 0
    
    
    def startGame(self):
        left = right = False
        while not self.player.dead:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    time.sleep(2)
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        left = True
                    if event.key == pygame.K_RIGHT:
                        right = True
                    
            if left:
                self.player.moveLeft()
                left = False
            elif right:
                self.player.moveRight()
                right = False
                
            self.gameDisplay.fill((51, 51, 51)) # RGB  
            self.player.drawPlayer(self.gameDisplay)
            self.blocks.displayBlocks(self.gameDisplay)
            self.sayMessage("Score : " + str(self.score)) # (10, 10)
            crossed = self.blocks.dropBlocks()
            if crossed:
                self.score += 1
                # uncomment below line to increase speed of agent for wrt to speed of block
                # self.player.step += 1
                if self.score % 3 == 0 and self.blocks.speed < 10:
                    self.blocks.speed += 1
            self.checkCrashed()
            pygame.display.update()            

            
if __name__ == "__main__":
    game = Game()
    game.startGame()

