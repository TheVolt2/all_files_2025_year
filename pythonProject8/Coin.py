import pygame as pg

class Coin:
    def __init__(self, size, pos, col, coin, coins):
        self.col = col
        self.size = size
        self.pos = pos
        self.coin = coin
        self.coins = coins
    def circle(self, coin, coins, screen, col, pos, size):
        coin = (screen, col, (pos[0], pos[1]), size)
        coins = [coin for i in range(20)]
    def spawn(self, coins):
        for coin in coins:
            pg.draw.circle(coin)