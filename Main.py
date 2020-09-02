import pygame
pygame.font.init()
import random
import numpy as np


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



class Player:
    
    def __init__(self, windowWidth, windowHeight, n, rad):
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight
        self.n = n
        self.rad = rad
        self.x , self.y = (windowWidth // 2, windowHeight - 20)
        self.step = windowWidth // n #3 for continous
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
            
class Agent(Player):
    
    def __init__(self, windowWidth, windowHeight, n, rad, states, actions, lr = 0.8, gamma = 0.99):
        super().__init__(windowWidth, windowHeight, n, rad)
        self.states = states
        self.actions = actions
        self.lr = lr
        self.gamma = gamma
        # S X A -- > 3 * 3
        try:
            self.Qtable = np.load("Brain.npy")
        except:
            self.Qtable = np.zeros((states, actions))
        
    def act(self, state, gameNo):
        return np.argmax(self.Qtable[state, :] + np.random.randn(1, self.actions) * (1 / (gameNo + 1))) # for continous comment noise out
    
    
    # Q(s, a) += lr *(future best reward - Current known value)
    def learn(self, state, action, reward, stateDash):
        self.Qtable[state, action] += self.lr * (reward + self.gamma * np.max(self.Qtable[stateDash, :]) - self.Qtable[state, action])
        
    def reset(self):
        self.x , self.y = (self.windowWidth // 2, self.windowHeight - 20)
        self.dead = False
        
    def saveAgent(self):
        np.save("Brain.npy", self.Qtable)
        
    
    
    
class Game:
    
    def __init__(self, windowWidth = 400, windowHeight = 600):
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight
        self.gameDisplay = pygame.display.set_mode((windowWidth, windowHeight))
        pygame.display.set_caption("Dodge the Blocks!")
        self.blocks = Block(windowWidth, windowHeight, n = 5, speed = 0.5)
        self.player = Agent(windowWidth, windowHeight, 5, 10, 3, 3)
        self.score = 0
        
    def sayMessage(self, msg, fontType = 'freesansbold.ttf', color = (255, 255, 255),
                   fontSize = 15, loc = (10, 10)):
        myMsg = pygame.font.Font(fontType, fontSize).render(msg, True, color)
        self.gameDisplay.blit(myMsg, loc)  
        
    def checkCrashed(self):                 # y of block                   # height of block
        if self.player.y-self.player.rad > self.blocks.cordsBlock[0][1] + self.blocks.cordsBlock[0][3]: return 0
        if self.blocks.cordsBlock[self.blocks.safeBlockIndex][0] < self.player.x <\
        self.blocks.cordsBlock[self.blocks.safeBlockIndex][0] + \
        self.blocks.cordsBlock[self.blocks.safeBlockIndex][2]: return 1
        self.player.dead = True
        return -1
        
        
    def getState(self):
        # if opening is to the left of Agent                                                                              # for continous
        if self.blocks.cordsBlock[self.blocks.safeBlockIndex][0] + self.blocks.cordsBlock[self.blocks.safeBlockIndex][2] <= self.player.x: return 0
        # if agent is between safeBlock
        if self.blocks.cordsBlock[self.blocks.safeBlockIndex][0] < self.player.x < self.blocks.cordsBlock[self.blocks.safeBlockIndex][0] + self.blocks.cordsBlock[self.blocks.safeBlockIndex][2]: return 1
        # if agent is to the left of safeblock
        if self.blocks.cordsBlock[self.blocks.safeBlockIndex][0] >= self.player.x: return 2
        

    def reset(self):
        self.player.reset()
        self.player.saveAgent()
        self.blocks.cordsBlock = self.blocks.buildCords()
        self.blocks.speed = 0.5 # correction forgot to add in video 
        self.score = 0
    
    
    def startGame(self, episode):
        left = right = False
        state = self.getState() #0 , 1, 2
        while not self.player.dead:
            reward = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        left = True
                    if event.key == pygame.K_RIGHT:
                        right = True
                        
            action = self.player.act(state, episode) #0 ,1, 2 
            if action == 0:
                left = True
            elif action == 1:
                left = right = False #stay
            elif action == 2:
                right = True
                    
            if left:
                self.player.moveLeft()
                left = False
            elif right:
                self.player.moveRight()
                right = False
                
            stateDash = self.getState() #new state of agent
                    
            
                
                
            self.gameDisplay.fill((51, 51, 51)) # RGB  
            self.player.drawPlayer(self.gameDisplay)
            self.blocks.displayBlocks(self.gameDisplay)
            self.sayMessage("Score : " + str(self.score)) # (10, 10)
            self.sayMessage("Episode : " + str(episode), loc = (10, 30))
            crossed = self.blocks.dropBlocks()
            #print(self.getState())
            if crossed:
                self.score += 1
                reward += 5
                # uncomment below line to increase speed of agent for wrt to speed of block
                # self.player.step += 1 # Correction 2
                if self.score % 3 == 0 and self.blocks.speed < 10:
                    self.blocks.speed += 1
            reward += self.checkCrashed()
            self.player.learn(state, action, reward, stateDash)
            state = stateDash
            pygame.display.update()            
        #pygame.quit()
            
game = Game()
for episode in range(50):
    game.startGame(episode)
    game.reset()
pygame.quit()

