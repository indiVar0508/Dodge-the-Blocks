import pygame

class Player:
    
    def __init__(self, windowWidth, windowHeight, n, rad):
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight
        self.n = n
        self.rad = rad
        self.x , self.y = (windowWidth // 2, windowHeight - 20)
        self.step = windowWidth // n
        self.dead = False

    def drawPlayer(self, gameDisp):
        pygame.draw.circle(gameDisp, (0, 0, 255), (self.x, self.y), self.rad) # display, color, pos, rad/size
        
    def moveLeft(self):
        self.x -= self.step
        if self.x < self.step // 2:
            self.x = self.step // 2
        
    def moveRight(self):
        self.x += self.step
        if self.x > self.windowWidth - self.step // 2: 
            self.x = self.windowWidth - self.step // 2
