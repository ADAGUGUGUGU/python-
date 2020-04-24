# coding=gbk
from random import randint
import pygame
from pygame import (Rect)
from sys import exit
from pygame.locals import (K_DOWN, K_ESCAPE, K_LEFT,
                           K_RIGHT, K_UP, KEYDOWN, K_r,QUIT)

COLOR_R = [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
		240, 220, 200, 180, 160, 140, 120, 100, 80, 60, 40, 20, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240]
COLOR_G = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240,
		255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
		255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255]
COLOR_B = [0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240,
		255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
		255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
		240, 220, 200, 180, 160, 140, 120, 100, 80, 60, 40, 20, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
g_gradual_change_color = [(r,g,b) for r,g,b in zip(COLOR_R,COLOR_G,COLOR_B)]

class Game_snake_ex:
    def __init__(self, windowsize_x=500, windowsize_y=500):
        self.windowsize_x = windowsize_x
        self.windowsize_y = windowsize_y
        self.gameUnitsize = 16
        if (self.windowsize_x % self.gameUnitsize != 0):
            self.windowsize_x += self.gameUnitsize - self.windowsize_x % self.gameUnitsize
        if (self.windowsize_y % self.gameUnitsize != 0):
            self.windowsize_y += self.gameUnitsize - self.windowsize_y % self.gameUnitsize
        self.window = pygame.display.set_mode(
            [self.windowsize_x, self.windowsize_y])

        pygame.display.set_caption("Snake!")
        self.window.fill((0, 0, 0))
        pygame.font.init()
        self.font = pygame.font.SysFont("bahnschrift", 20)

        self.text = self.font.render(
            "Press Direction key to begin", True, (255, 255, 255))
        self.startTextRect = self.text.get_rect(
            center=(windowsize_x/2, windowsize_y/2))
        self.snake = [self.startSnake()]
        self.food = self.createFood()
        self.speed = self.gameUnitsize
        self.score = 0
        self.scoreText = self.font.render(
            f"Score: {self.score}", True, (255, 255, 255), None)
        self.snakeDirections = {
            'left': (-1, 0), 'right': (1, 0), 'up': (0, -1), 'down': (0, 1)}

        self.previousDirection = self.snakeDirections.get('left')
        self.readyScreen()
        self.gameLoop()

    def startSnake(self):
        snakeNodeX = self.window.get_width() / 2 - self.gameUnitsize
        if (snakeNodeX % self.gameUnitsize != 0):
            snakeNodeX -= snakeNodeX % self.gameUnitsize
        snakeNodeY = self.window.get_height() / 2 - self.gameUnitsize
        if (snakeNodeY % self.gameUnitsize != 0):
            snakeNodeY -= snakeNodeY % self.gameUnitsize

        snakeNodeRectangle = Rect(
            (snakeNodeX, snakeNodeY), (self.gameUnitsize, self.gameUnitsize))
        return snakeNodeRectangle

    def createFood(self):
        foodX = randint(0, self.window.get_width() - self.gameUnitsize)
        if (foodX % self.gameUnitsize != 0):
            foodX -= foodX % self.gameUnitsize
        foodY = randint(0, self.window.get_height() - self.gameUnitsize)
        if (foodY % self.gameUnitsize != 0):
            foodY -= foodY % self.gameUnitsize
        foodRectangle = Rect(
            (foodX, foodY), (self.gameUnitsize, self.gameUnitsize))
        return foodRectangle

    def moveFood(self):
        self.food.x = randint(0, self.window.get_width() - self.gameUnitsize)
        if (self.food.x % self.gameUnitsize != 0):
            self.food.x -= self.food.x % self.gameUnitsize
        self.food.y = randint(0, self.window.get_height() - self.gameUnitsize)
        if (self.food.y % self.gameUnitsize != 0):
            self.food.y -= self.food.y % self.gameUnitsize

    def createSnake(self):
        snakeNodeX = randint(0, self.window.get_width())
        if (snakeNodeX % self.gameUnitsize != 0):
            snakeNodeX -= snakeNodeX % self.gameUnitsize
        snakeNodeY = randint(0, self.window.get_height())
        if (snakeNodeY % self.gameUnitsize != 0):
            snakeNodeY -= snakeNodeY % self.gameUnitsize
        snakeNodeRectangle = Rect(
            (snakeNodeX, snakeNodeY), (self.gameUnitsize, self.gameUnitsize))
        return snakeNodeRectangle

    def appendSnake(self):
        # add node to tail
        newSnakeLink = Rect((self.snake[len(self.snake) - 1].x, self.snake[len(
            self.snake) - 1].y), (self.gameUnitsize, self.gameUnitsize))
        self.snake.append(newSnakeLink)

    def moveSnake(self, direction):
        x = 0
        y = 1
        self.snake[len(self.snake) - 1].x = self.snake[0].x + \
            direction[x] * self.speed
        self.snake[len(self.snake) - 1].y = self.snake[0].y + \
            direction[y] * self.speed
        self.snake.insert(0, self.snake.pop())
        self.previousDirection = direction


    def intersect(self):
        if self.snake[0].x == self.food.x and self.snake[0].y == self.food.y:
            return True
        return False

    def snakeCollidingWithWall(self):
        if self.snake[0].x >= self.windowsize_x or self.snake[0].x < 0 or self.snake[0].y >= self.windowsize_y or self.snake[0].y < 0:
            return True
        return False


    def snakeCollidingWithSelf(self):
        for link in self.snake:
            if (self.snake[0] is not link):
                if self.snake[0].x == link.x and self.snake[0].y == link.y:
                    return True
        return False

    def killSnake(self):
        return self._gameOverScreen()

    def _update(self):

        self.window.fill((0,0,0))

        if (self.intersect() == True):
            self.appendSnake()
            self.moveFood()
            self.score += 1

        elif (self.snakeCollidingWithWall() == True or self.snakeCollidingWithSelf() == True):
            return self.killSnake()

        for link in self.snake:
            pygame.draw.rect(self.window, (255,255,255), link)
        pygame.draw.rect(self.window, (102, 255, 51), self.food)

        self.scoreText = self.font.render(
            f"Score: {self.score}", True, (255, 255, 255))
        self.scoreTextRect = self.scoreText.get_rect(center=(40, 10))
        self.window.blit(self.scoreText, self.scoreTextRect)

        pygame.display.update()

    def _input(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit()
        keys = pygame.key.get_pressed()
        if (keys[K_LEFT] and self.previousDirection != self.snakeDirections.get('right')):
            self.moveSnake(self.snakeDirections.get('left'))
        elif (keys[K_RIGHT] and self.previousDirection != self.snakeDirections.get('left')):
            self.moveSnake(self.snakeDirections.get('right'))
        elif (keys[K_UP] and self.previousDirection != self.snakeDirections.get('down')):
            self.moveSnake(self.snakeDirections.get('up'))
        elif (keys[K_DOWN] and self.previousDirection != self.snakeDirections.get('up')):
            self.moveSnake(self.snakeDirections.get('down'))
        else:
            self.moveSnake(self.previousDirection)

    def readyScreen(self):
        while True:
            self.window.blit(self.text, self.startTextRect)
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        exit()
            keys = pygame.key.get_pressed()
            if (keys[K_LEFT]):
                self.previousDirection = self.snakeDirections.get('left')
                break
            if (keys[K_RIGHT]):
                self.previousDirection = self.snakeDirections.get('right')
                break
            if (keys[K_UP]):
                self.previousDirection = self.snakeDirections.get('up')
                break
            if (keys[K_DOWN]):
                self.previousDirection = self.snakeDirections.get('down')
                break
            pygame.display.update()

    def _gameOverScreen(self):
        while True:
            self.window.fill((0, 0, 0))
            self.text = self.font.render(
                f"Game Over, Score: {self.score}", True, (255, 255, 255))
            self.startTextRect = self.text.get_rect(
                center=(self.windowsize_x/2, self.windowsize_y/2))
            self.window.blit(self.text, self.startTextRect)

            keys = pygame.key.get_pressed()
            if (keys[K_r]):
                break
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                     exit()
            pygame.display.update()
        return 1

    def gameLoop(self):
        while True:
            pygame.time.delay(100)
            self._input()
            self._update()

class Snake():
    def __init__(self,windowX=500,windowY=500):
        self.normal_speed = 16
        self.snake_color_index = 0
        self.snake_color_list = []
        self.snake_color_rule = ''
        self.snake_color = (102, 255, 51)
        self.food_color = (102, 255, 51)
        self.background_color = (0,0,0)
        self.snake_deceleration_standard = 0
        self.windowsize_x = windowX
        self.windowsize_y = windowY
        self.gameUnitsize = 16
        if (self.windowsize_x % self.gameUnitsize != 0):
            self.windowsize_x += self.gameUnitsize - self.windowsize_x % self.gameUnitsize
        if (self.windowsize_y % self.gameUnitsize != 0):
            self.windowsize_y += self.gameUnitsize - self.windowsize_y % self.gameUnitsize

        self.window = pygame.display.set_mode([self.windowsize_x,self.windowsize_y])
        pygame.display.set_caption("Snake!")
        self.window.fill((255, 255, 255))

        pygame.font.init()
        self.font = pygame.font.SysFont("bahnschrift", 20)
        self.home_text = self.font.render(
            "Press Direction key to begin", True, (0, 0, 0))
        self.startTextRect = self.home_text.get_rect(
            center=(self.windowsize_x / 2, self.windowsize_y / 2))
        self.snake = [self.init_snake()]
        self.food = self.createFood()
        self.speed = 16
        self.score = 0
        self.over_text = self.font.render(
            f"Score: {self.score}", True, (0, 0, 0), None)
        self.snakeDirections = {
            'left': (-1, 0), 'right': (1, 0), 'up': (0, -1), 'down': (0, 1)}
        self.previousDirection = self.snakeDirections.get('left')


    def set_snake_color(self,color_list,rule:str):
        if rule == 'flower_updata':
            self.snake_color_list = color_list
            self.snake_color_rule = rule
        elif rule == 'when_eat_food':
            self.snake_color_list = color_list
            self.snake_color_rule = rule
        elif rule == 'never':
            self.snake_color_rule = rule
        else:
              try:
                  raise Warning
              except Exception as e:
                  print('参数错误，候选参数 :\nflower_updata：跟随刷新变色\nwhen_eat_food：吃掉食物变色\nnever:无意义')
                  exit(0)
    def set_food_color(self,color):
        self.food_color = color

    def set_homeview_text(self,color,text,place):
        self.home_text = self.font.render(
            text,True,color
        )
        self.startTextRect = self.home_text.get_rect(
            center=place
        )

    def set_edge_slow_down(self,bool,normal_speed = 16,snake_deceleration_standard=2):
        if bool is False:
            self.snake_deceleration_standard = 0
        else:
            self.snake_deceleration_standard = snake_deceleration_standard
            self.normal_speed  = normal_speed
            
    def set_background_color(self,color):
        self.background_color = color

    def init_snake(self):
        snakeNodeX = self.window.get_width() / 2 - self.gameUnitsize
        if (snakeNodeX % self.gameUnitsize != 0):
            snakeNodeX -= snakeNodeX % self.gameUnitsize
        snakeNodeY = self.window.get_height() / 2 - self.gameUnitsize
        if (snakeNodeY % self.gameUnitsize != 0):
            snakeNodeY -= snakeNodeY % self.gameUnitsize

        snakeNodeRectangle = Rect(
            (snakeNodeX, snakeNodeY), (self.gameUnitsize, self.gameUnitsize))
        return snakeNodeRectangle

    def createFood(self):
        foodX = randint(0, self.window.get_width() - self.gameUnitsize)
        if (foodX % self.gameUnitsize != 0):
            foodX -= foodX % self.gameUnitsize
        foodY = randint(0, self.window.get_height() - self.gameUnitsize)
        if (foodY % self.gameUnitsize != 0):
            foodY -= foodY % self.gameUnitsize
        foodRectangle = Rect(
            (foodX, foodY), (self.gameUnitsize, self.gameUnitsize))
        return foodRectangle

    def moveFood(self):
        self.food.x = randint(0, self.window.get_width() - self.gameUnitsize)
        if (self.food.x % self.gameUnitsize != 0):
            self.food.x -= self.food.x % self.gameUnitsize
        self.food.y = randint(0, self.window.get_height() - self.gameUnitsize)
        if (self.food.y % self.gameUnitsize != 0):
            self.food.y -= self.food.y % self.gameUnitsize

    def appendSnake(self):
        # add node to tail
        newSnakeLink = Rect((self.snake[len(self.snake) - 1].x, self.snake[len(
            self.snake) - 1].y), (self.gameUnitsize, self.gameUnitsize))
        self.snake.append(newSnakeLink)

    def moveSnake(self, direction):
        x = 0
        y = 1
        self.snake[len(self.snake) - 1].x = self.snake[0].x + \
                                            direction[x] * self.speed
        self.snake[len(self.snake) - 1].y = self.snake[0].y + \
                                            direction[y] * self.speed
        self.snake.insert(0, self.snake.pop())
        self.previousDirection = direction

    def intersect(self):
        # if self.snake[0].x == self.food.x and self.snake[0].y == self.food.y:
        #     return True
        if (self.food.x <= self.snake[0].x <= self.food.x + self.food.width
                and
                self.food.y <= self.snake[0].y <= self.food.y + self.food.height):
            return True
        elif (self.food.x <= self.snake[0].x + self.snake[0].width <= self.food.x + self.food.width
              and
              self.food.y <= self.snake[0].y <= self.food.y + self.food.height):
            return True
        elif (self.food.x <= self.snake[0].x <= self.food.x + self.food.width
              and
              self.food.y <= self.snake[0].y + self.snake[0].height <= self.food.y + self.food.height):
            return True
        elif (self.food.x <= self.snake[0].x + self.snake[0].width <= self.food.x + self.food.width
              and
              self.food.y <= self.snake[0].y + self.snake[0].height <= self.food.y + self.food.height):
            return True
        return False

    def snakeCollidingWithWall(self):
        if self.snake[0].x >= self.windowsize_x or self.snake[0].x < 0 or self.snake[0].y >= self.windowsize_y or \
                self.snake[0].y < 0:
            return True
        return False

    def snakeCollidingWithSelf(self):
        for link in self.snake:
            if (self.snake[0] is not link):
                if self.snake[0].x == link.x and self.snake[0].y == link.y:
                    return True
        return False

    def snake_Will_CollidingWithWall(self):
        if (int(self.windowsize_x) - int(self.snake[0].x) < self.gameUnitsize * self.snake_deceleration_standard):
            self.speed = 2
            return True
        if (int(self.snake[0].x < int(self.gameUnitsize * self.snake_deceleration_standard))):
            self.speed = 2
            return True
        if (int(self.windowsize_y) - int(self.snake[0].y) < self.gameUnitsize * self.snake_deceleration_standard):
            self.speed = 2
            return True
        if (int(self.snake[0].y) < int(self.gameUnitsize * self.snake_deceleration_standard)):
            self.speed = 2
            return True
        self.speed = self.normal_speed
        return False

    def killSnake(self):
        return self._gameOverScreen()

    def _update(self):
        self.window.fill(self.background_color)


        if (self.intersect() == True):
            if self.snake_color_rule == 'when_eat_food':
                self.snake_color_index += 1
                if self.snake_color_index > len(self.snake_color_list) - 1:
                    self.snake_color_index = 0
            self.appendSnake()
            self.moveFood()
            self.score += 1
        elif (self.snakeCollidingWithWall() == True or self.snakeCollidingWithSelf() == True):
            return self.killSnake()
        elif self.snake_deceleration_standard > 0:
            self.snake_Will_CollidingWithWall()


        if self.snake_color_rule == 'when_eat_food':
            for link in self.snake:
                pygame.draw.rect(self.window,self.snake_color_list[self.snake_color_index],link)
        elif self.snake_color_rule == 'flower_updata':
            for link in self.snake:
                pygame.draw.rect(self.window,self.snake_color_list[randint(0,len(self.snake_color_list)-1)],link)
        else:
            # print('here')
            for link in self.snake:
                pygame.draw.rect(self.window,self.snake_color,link)
        pygame.draw.rect(self.window, self.food_color, self.food)
        self.scoreText = self.font.render(
            f"score : {self.score}", True, (255, 255, 255))
        self.scoreTextRect = self.scoreText.get_rect(center=(40, 10))
        self.window.blit(self.scoreText, self.scoreTextRect)
        pygame.display.update()

    def _input(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit()
        keys = pygame.key.get_pressed()
        if (keys[K_LEFT] and self.previousDirection != self.snakeDirections.get('right')):
            self.moveSnake(self.snakeDirections.get('left'))
        elif (keys[K_RIGHT] and self.previousDirection != self.snakeDirections.get('left')):
            self.moveSnake(self.snakeDirections.get('right'))
        elif (keys[K_UP] and self.previousDirection != self.snakeDirections.get('down')):
            self.moveSnake(self.snakeDirections.get('up'))
        elif (keys[K_DOWN] and self.previousDirection != self.snakeDirections.get('up')):
            self.moveSnake(self.snakeDirections.get('down'))
        else:
            self.moveSnake(self.previousDirection)

    def readyScreen(self):
        while True:
            # print('readyScreen')
            self.window.blit(self.home_text, self.startTextRect)
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        exit()
            keys = pygame.key.get_pressed()
            if (keys[K_LEFT]):
                self.previousDirection = self.snakeDirections.get('left')
                break
            if (keys[K_RIGHT]):
                self.previousDirection = self.snakeDirections.get('right')
                break
            if (keys[K_UP]):
                self.previousDirection = self.snakeDirections.get('up')
                break
            if (keys[K_DOWN]):
                self.previousDirection = self.snakeDirections.get('down')
                break
            pygame.display.update()

    def _gameOverScreen(self):
        while True:
            self.window.fill((0, 0, 0))
            self.home_text = self.font.render(
                f"Game Over, Score: {self.score}", True, (255, 255, 255))
            self.startTextRect = self.home_text.get_rect(
                center=(self.windowsize_x / 2, self.windowsize_y / 2))
            self.window.blit(self.home_text, self.startTextRect)

            keys = pygame.key.get_pressed()
            if (keys[K_r]):
                break
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        exit()
            pygame.display.update()


    def gameLoop(self):
        while True:
            # print('gameLoop')
            pygame.time.delay(60)
            self._input()
            self._update()
            
    def show_fun(self):
        pass

    def run(self):
        self.set_background_color((139,131,134))
        self.set_edge_slow_down(True)
        self.set_food_color((150,100,205))
        # self.set_homeview_text((193,205,205),'ok let s play',(100,100))
        # color_list = ['#00CD66','#87CEFA','#ADFF2F','#8B7355','#D8BFD8','#EE9A00','#8B795E']
        self.set_snake_color(g_gradual_change_color,'when_eat_food')
        self.readyScreen()
        self.gameLoop()



def main():
    # print(len(COLOR_R),len(COLOR_G),len(COLOR_B))
    # game = Game_snake_ex(500, 500)
    game = Snake()
    game.run()


main()