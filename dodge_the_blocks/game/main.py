import pygame
import time
from .blocks import Block
from .player import Player 

BACKGROUND_COLOR: tuple = (51, 51, 51)
class Game:
    
    def __init__(self, window_width: int = 400, window_height: int = 600):
        self.window_width = window_width
        self.window_height = window_height
        self.game_display = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption("Dodge the Blocks!")
        self.blocks = Block(window_width, window_height, n = 5, speed = 0.5)
        self.player = Player(window_width, window_height, 5, 10)
        self.score = 0
        
    def say_message(self, msg: str, loc: tuple, font_type = 'freesansbold.ttf', color = (255, 255, 255),
                   font_size = 15):
        myMsg = pygame.font.Font(font_type, font_size).render(msg, True, color)
        self.game_display.blit(myMsg, loc)  
        
    def check_crashed(self):                 # y of block                   # height of block
        if (self.player.y-self.player.radius > self.blocks.cordsBlock[0][1] + self.blocks.cordsBlock[0][3]) or (self.blocks.cordsBlock[self.blocks.safeBlockIndex][0] < self.player.x <\
        self.blocks.cordsBlock[self.blocks.safeBlockIndex][0] + \
        self.blocks.cordsBlock[self.blocks.safeBlockIndex][2]): return
        self.player.dead = True
        

    def reset(self):
        self.blocks.cordsBlock = self.blocks.buildCords()
        self.blocks.speed = 0.5 # correction forgot to add in video 
        self.score = 0
        self.player.dead = False
    
    
    def start_game(self):
        left = right = False
        while not self.player.dead:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        left = True
                    if event.key == pygame.K_RIGHT:
                        right = True
                    if event.key == pygame.K_q:
                        return
                    
            if left:
                self.player.moveLeft()
                left = False
            elif right:
                self.player.moveRight()
                right = False
                
            self.game_display.fill(BACKGROUND_COLOR) # RGB  
            self.player.drawPlayer(self.game_display)
            self.blocks.displayBlocks(self.game_display)
            self.say_message("Score : " + str(self.score), loc=(self.window_width-80, 10)) # (10, 10)
            crossed = self.blocks.dropBlocks()
            if crossed:
                self.score += 1
                # uncomment below line to increase speed of agent for wrt to speed of block
                # self.player.step += 1
                if self.score % 3 == 0 and self.blocks.speed < 10:
                    self.blocks.speed += 1
            self.check_crashed()
            pygame.display.update()            

    def play_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        self.reset()
                        self.start_game()
                    if event.key == pygame.K_q:
                        pygame.quit()
                        return
            
            self.game_display.fill(BACKGROUND_COLOR)
            self.say_message("Press `S` to start Game", loc=((self.window_width // 2)-120, self.window_height // 2 - 20), font_size=24)
            self.say_message("Press `Q` to close Game", loc=((self.window_width // 2)-120, self.window_height // 2 + 20), font_size=24)

            pygame.display.update()   
            
if __name__ == "__main__":
    game = Game()
    game.start_game()

