import pygame
import random

class Block:
    
    def __init__(self, window_width: int, window_height: int, number_of_blocks: int, speed: int):
        self.game_window_width = window_width
        self.game_window_height = window_height
        self.number_of_blocks = number_of_blocks
        self.speed = speed
        self.width_of_block = window_width // number_of_blocks
        self.height_of_block = window_height // 10
        self.cords_block = self.build_cords()
        
    def build_cords(self):
        cords = [[0, 0, self.width_of_block, self.height_of_block]]
        for i in range(1, self.number_of_blocks):
            cords.append([cords[i-1][0] + self.width_of_block, 0, self.width_of_block, self.height_of_block])
        self.safe_block_index = random.randint(0, self.number_of_blocks-1)
        return cords
    
    def display_blocks(self, game_disp):
        for idx, cord in enumerate(self.cords_block):
            if idx == self.safe_block_index: continue
            pygame.draw.rect(game_disp, (200, 0, 0), cord)
            
    def drop_blocks(self):
        for cord in self.cords_block:
            cord[1] += self.speed
        if self.cords_block[0][1] > self.game_window_height:
            self.cords_block = self.build_cords()
            return True
        return False
