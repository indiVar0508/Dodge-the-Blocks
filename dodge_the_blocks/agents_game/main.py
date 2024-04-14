import pygame
import numpy as np
from game.blocks import Block
from game.main import Player, Game


class Agent(Player):
    def __init__(
        self,
        window_width: int,
        window_height: int,
        num_blocks: int,
        radius: int,
        states: int,
        actions: int,
        lr=0.8,
        gamma=1,
    ):
        super().__init__(window_width, window_height, num_blocks, radius)
        self.states = states
        self.actions = actions
        self.lr = lr
        self.gamma = gamma
        self.q_table = np.zeros((states, actions))

    def act(self, state, gameNo):
        return np.argmax(
            self.q_table[state, :]
            + np.random.randn(1, self.actions) * (1 / (gameNo + 1))
        )

    # Q(s, a) += lr *(future best reward - Current known value)
    def learn(self, state, action, reward, stateDash):
        self.q_table[state, action] += self.lr * (
            reward
            + self.gamma * np.max(self.q_table[stateDash, :])
            - self.q_table[state, action]
        )


class AgentGame(Game):
    def __init__(self, window_width=800, window_height=600, agent_state=3):
        assert (
            agent_state == 3 or agent_state == 25
        ), "Agent can be only in 3 or 25 states"
        super().__init__(window_width, window_height)
        self.player = Agent(window_width // 2, window_height, 5, 10, agent_state, 3)
        self.num_states = agent_state
        # Block should run on half of screen
        self.blocks = Block(window_width // 2, window_height, number_of_blocks = 5, speed = 0.5)

    def check_crashed(self):
        if (
            self.player.y - self.player.radius
            > self.blocks.cords_block[0][1] + self.blocks.cords_block[0][3]
        ):
            return 0
        if (
            self.blocks.cords_block[self.blocks.safe_block_index][0]
            < self.player.x
            < self.blocks.cords_block[self.blocks.safe_block_index][0]
            + self.blocks.cords_block[self.blocks.safe_block_index][2]
        ):
            return 5
        self.player.dead = True
        return -30

    def getState(self):
        if self.num_states == 3:
            # if agent is to the right of safeblock need to move left                                                                              # for continous
            if (
                self.blocks.cords_block[self.blocks.safe_block_index][0]
                + self.blocks.cords_block[self.blocks.safe_block_index][2]
                <= self.player.x
            ):
                return 0
            # if agent is between safeBlock should stay
            if (
                self.blocks.cords_block[self.blocks.safe_block_index][0]
                < self.player.x
                < self.blocks.cords_block[self.blocks.safe_block_index][0]
                + self.blocks.cords_block[self.blocks.safe_block_index][2]
            ):
                return 1
            # if agent is to the left of safeblock should move right
            if (
                self.blocks.cords_block[self.blocks.safe_block_index][0]
                >= self.player.x
            ):
                return 2
        else:
            for i in range(5):
                if (
                    self.blocks.cords_block[i][0]
                    < self.player.x
                    < self.blocks.cords_block[i][0] + self.blocks.cords_block[i][2]
                ):
                    return i * 5 + self.blocks.safe_block_index

    def showState(self):
        table = self.player.q_table
        xpos, ypos = 480, 120
        colours = [[255, 0, 0], [0, 255, 0], [0, 0, 255]]
        self.say_message("*  LEFT         STAY       RIGHT", loc=(xpos, ypos))
        ypos += 40
        xpos = 520
        for row in table:
            for val in row:
                if val < 0:
                    color = colours[0]
                elif val == 0:
                    color = colours[1]
                elif val > 0:
                    color = colours[2]
                if self.num_states == 3:
                    self.say_message(f"{val:.2f}", loc=(xpos-20, ypos), color=color)
                else:
                    # FIXME: 25 number system becomes expensive for rendering numbers as we 
                    #        format and render 25*3=>75 numbers on the screen
                    pygame.draw.rect(self.game_display, color, (xpos-10, ypos, 10, 5))
                xpos += 80
            ypos += 20 if self.num_states == 3 else 15
            xpos = 520

    def start_game(self, episode):
        left = right = False
        state = self.getState()  # 0, 1, 2
        while not self.player.dead:
            reward = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        return True

            action = self.player.act(state, episode)  # 0, 1, 2
            if action == 0:
                left = True
            elif action == 1:
                left = right = False  # stay
            elif action == 2:
                right = True

            if left:
                self.player.moveLeft()
                reward -= 1
                left = False
            elif right:
                self.player.moveRight()
                reward -= 1
                right = False

            stateDash = self.getState()  # new state of agent

            self.game_display.fill((51, 51, 51))  # RGB
            self.player.drawPlayer(self.game_display)
            self.blocks.display_blocks(self.game_display)
            self.showState()
            self.say_message("Score : " + str(self.score), loc=((self.window_width // 2)+80, 10))  # (10, 10)
            self.say_message("Episode : " + str(episode), loc=((self.window_width // 2)+80, 30))
            crossed = self.blocks.drop_blocks()
            if crossed:
                self.score += 1
                reward += 10
                if self.score % 3 == 0 and self.blocks.speed < 10:
                    self.blocks.speed += 1
            reward += self.check_crashed()
            self.player.learn(state, action, reward, stateDash)
            state = stateDash
            pygame.display.update()
        return False

if __name__ == "__main__":
    game = AgentGame()
    for episode in range(50):
        gracefully_close = game.start_game(episode)
        if gracefully_close is True:
            break
        game.reset()
