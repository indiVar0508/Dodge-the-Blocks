import pygame

BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
class Player:
    
    def __init__(self, window_width: int, window_height: int, num_blocks: int, radius: int):
        self.game_window_width = window_width
        self.game_window_height = window_height
        self.num_blocks = num_blocks
        self.radius = radius
        self.x , self.y = (window_width // 2, window_height - 20)
        self.step = window_width // num_blocks
        self.dead = False
        self.color = BLUE

    def reset(self):
        self.dead = False
        self.x , self.y = (self.game_window_width // 2, self.game_window_height - 20)

    def drawPlayer(self, gameDisp):
        pygame.draw.circle(gameDisp, self.color, (self.x, self.y), self.radius)
        
    def moveLeft(self):
        self.x -= self.step
        if self.x < self.step // 2:
            self.x = self.step // 2
        
    def moveRight(self):
        self.x += self.step
        if self.x > self.game_window_width - self.step // 2: 
            self.x = self.game_window_width - self.step // 2
