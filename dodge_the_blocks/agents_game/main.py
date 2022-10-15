import pygame
import numpy as np
from game.main import Player, Game

class Agent(Player):
    
    def __init__(self, windowWidth, windowHeight, n, rad, states, actions, lr = 0.8, gamma = 0.99):
        super().__init__(windowWidth, windowHeight, n, rad)
        self.states = states
        self.actions = actions
        self.lr = lr
        self.gamma = gamma
        self.Qtable = np.zeros((states, actions))

    def act(self, state, gameNo):
        return np.argmax(self.Qtable[state, :] + np.random.randn(1, self.actions) * (1 / (gameNo + 1))) # for continous comment noise out
    
    # Q(s, a) += lr *(future best reward - Current known value)
    def learn(self, state, action, reward, stateDash):
        self.Qtable[state, action] += self.lr * (reward + self.gamma * np.max(self.Qtable[stateDash, :]) - self.Qtable[state, action])
        
    def reset(self):
        self.x , self.y = (self.windowWidth // 2, self.windowHeight - 20)
        self.dead = False
    
    
    
class AgentGame(Game):
    
    def __init__(self, windowWidth = 800, windowHeight = 600, agent_state=3):
        super().__init__(windowWidth, windowHeight)
        assert agent_state == 3 or agent_state == 25, "Agent can be only in 3 or 25 states"
        self.player = Agent(windowWidth // 2, windowHeight, 5, 10, agent_state, 3)
        self.num_states = agent_state
        
    def checkCrashed(self):                 # y of block                   # height of block
        if self.player.y-self.player.rad > self.blocks.cordsBlock[0][1] + self.blocks.cordsBlock[0][3]: return 0
        if self.blocks.cordsBlock[self.blocks.safeBlockIndex][0] < self.player.x <\
        self.blocks.cordsBlock[self.blocks.safeBlockIndex][0] + \
        self.blocks.cordsBlock[self.blocks.safeBlockIndex][2]: return 1
        self.player.dead = True
        return -1
        
        
    def getState(self):
        if self.num_states == 3:
            # if agent is to the right of safeblock need to move left                                                                              # for continous
            if self.blocks.cordsBlock[self.blocks.safeBlockIndex][0] + self.blocks.cordsBlock[self.blocks.safeBlockIndex][2] <= self.player.x: return 0
            # if agent is between safeBlock should stay
            if self.blocks.cordsBlock[self.blocks.safeBlockIndex][0] < self.player.x < self.blocks.cordsBlock[self.blocks.safeBlockIndex][0] + self.blocks.cordsBlock[self.blocks.safeBlockIndex][2]: return 1
            # if agent is to the left of safeblock should move right
            if self.blocks.cordsBlock[self.blocks.safeBlockIndex][0] >= self.player.x: return 2
        else:
            for i in range(5):
                if self.blocks.cordsBlock[i][0] < self.player.x < self.blocks.cordsBlock[i][0] + self.blocks.cordsBlock[i][2]:
                    return i*5 + self.blocks.safeBlockIndex
    def showState(self):
        table = self.player.Qtable
        xpos, ypos = 480, 120
        colours = [[255,0,0],[0,255,0],[0,0,255]]
        self.sayMessage('*  LEFT         STAY       RIGHT',loc=(xpos,ypos))
        ypos += 40
        xpos = 520
        for row in table:
            for val in row:
                if val < 0:
                    pygame.draw.rect(self.gameDisplay, colours[0], (xpos, ypos, 10, 5))
                elif val == 0:
                    pygame.draw.rect(self.gameDisplay, colours[1], (xpos, ypos, 10, 5))
                elif val > 0:
                    pygame.draw.rect(self.gameDisplay, colours[2], (xpos, ypos, 10, 5))
                xpos += 80
            ypos += 10
            xpos = 520
        self.sayMessage('Green = Zero ',loc=(410, 450), color = (0, 255, 0))
        self.sayMessage('Red = Negative ',loc = (410, 480), color = (255, 0, 0))
        self.sayMessage('Blue = Positive ',loc = (410, 510), color = (0, 0, 255))
    
    def startGame(self, episode):
        left = right = False
        state = self.getState() # 0, 1, 2
        while not self.player.dead:
            reward = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                        
            action = self.player.act(state, episode) #0, 1, 2 
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
            self.showState()
            self.sayMessage("Score : " + str(self.score)) # (10, 10)
            self.sayMessage("Episode : " + str(episode), loc = (410, 30))
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
            
if __name__ == "__main__":
    game = AgentGame()
    for episode in range(50):
        game.startGame(episode)
        game.reset()


