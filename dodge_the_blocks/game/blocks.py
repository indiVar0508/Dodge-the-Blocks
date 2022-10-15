import pygame
import random

class Block:
    
    def __init__(self, windowWidth, windowHeight, n, speed):
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight
        self.n = n
        self.speed = speed
        self.widthOfBlock = windowWidth // n
        self.heightOfBlock = windowHeight // 10
        self.cordsBlock = self.buildCords()
        
    def buildCords(self):
        cords = [[0, 0, self.widthOfBlock, self.heightOfBlock]]
        for i in range(1, self.n):
            cords.append([cords[i-1][0] + self.widthOfBlock, 0, self.widthOfBlock, self.heightOfBlock])
        self.safeBlockIndex = random.randint(0, self.n-1)
        return cords
    
    def displayBlocks(self, gameDisp):
        for idx, cord in enumerate(self.cordsBlock):
            if idx == self.safeBlockIndex: continue
            pygame.draw.rect(gameDisp, (200, 0, 0), cord)
            
    def dropBlocks(self):
        for cord in self.cordsBlock:
            cord[1] += self.speed
        if self.cordsBlock[0][1] > self.windowHeight:
            self.cordsBlock = self.buildCords()
            return True
        return False
