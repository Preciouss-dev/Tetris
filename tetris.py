import pygame
import random


# nitialize the game
pygame.init()
  

colors = [
    (0, 0, 0),(0, 255, 255),(100, 179, 179),(80, 34, 22),
    (80, 134, 22),(0, 0, 255),(128, 0, 128),
]


class Shapes:
    column = 0
    row = 0

    #shapes in grid formatt
    shapes = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ]



    def __init__(self, column, row):
        self.column = column
        self.row = row
        self.type = random.randint(0, len(self.shapes) - 1)
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shapes[self.type])

    def image(self):
        return self.shapes[self.type][self.rotation]

 



class Tetris:
    
   
    state = "start"
    score = 0
    field = []
    level = 2
    height = 700
    width = 800
    column = 100
    zoom = 25
    row = 60
    blocks = None

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.field = []
        self.score = 0
        self.state = "start"
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)



    def new_shape(self):
        self.blocks = Shapes(3, 0)

    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.blocks.image():
                    if i + self.blocks.row > self.height - 1 or \
                            j + self.blocks.column > self.width - 1 or \
                            j + self.blocks.column < 0 or \
                            self.field[i + self.blocks.row][j + self.blocks.column] > 0:
                        intersection = True
        return intersection



    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines ** 2




    def go_space(self):
        while not self.intersects():
            self.blocks.row += 1
        self.blocks.row -= 1
        self.freeze()





    def downwards(self):
        self.blocks.row += 1
        if self.intersects():
            self.blocks.row -= 1
            self.freeze()




    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.blocks.image():
                    self.field[i + self.blocks.row][j + self.blocks.column] = self.blocks.color
        self.break_lines()
        self.new_shape()
        if self.intersects():
            self.state = "Gameover"




    def on_the_side(self, x_axis):
        old_x = self.blocks.column
        self.blocks.column += x_axis
        if self.intersects():
            self.blocks.column = old_x




    def rotate(self):
        old_rotation = self.blocks.rotation
        self.blocks.rotate()
        if self.intersects():
            self.blocks.rotation = old_rotation



# colors defination
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
NAVY = (128, 128, 128)

size = (500, 600)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("TETRIS")







# Loop until the user clicks the close button.
close = False
clock = pygame.time.Clock()
flips = 25         
game = Tetris(20, 10)
counter = 0

pressing_down = False


while not close:
    if game.blocks is None:
        game.new_shape()
    counter += 1
    if counter > 800000:
        counter = 0

    if counter % (flips // game.level // 2) == 0 or pressing_down:
        if game.state == "start":
            game.downwards()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.rotate()
            if event.key == pygame.K_DOWN:
                pressing_down = True
            if event.key == pygame.K_LEFT:
                game.on_the_side(-1)
            if event.key == pygame.K_RIGHT:
                game.on_the_side(1)
            if event.key == pygame.K_SPACE:
                game.go_space()
            if event.key == pygame.K_ESCAPE:
                game.__init__(20, 10)

    if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False

    screen.fill(WHITE)




    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen, NAVY, [game.column + game.zoom * j, game.row + game.zoom * i, game.zoom, game.zoom], 1)
            if game.field[i][j] > 0:
                pygame.draw.rect(screen, colors[game.field[i][j]],
                                 [game.column + game.zoom * j + 1, game.row + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])




    if game.blocks is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.blocks.image():
                    pygame.draw.rect(screen, colors[game.blocks.color],
                                     [game.column + game.zoom * (j + game.blocks.column) + 1,
                                      game.row + game.zoom * (i + game.blocks.row) + 1,
                                      game.zoom - 2, game.zoom - 2])

    font = pygame.font.SysFont('Calibri', 25, True, False)
    font1 = pygame.font.SysFont('Calibri', 65, True, False)
    text = font.render("Score: " + str(game.score), True, BLACK)
    game_over = font1.render("Game Over", True, (BLACK))
    game_over1 = font1.render("Press ESC", True, (BLACK))

    screen.blit(text, [0, 0])
    if game.state == "Gameover":
        screen.blit(game_over, [20, 100])
        screen.blit(game_over1, [25, 265])

    pygame.display.flip()
    clock.tick(flips)

pygame.quit()