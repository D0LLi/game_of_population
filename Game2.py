import copy
import random
import pygame as pg


width_count, height_count = 100, 70
size = 10
resolution = width, height = width_count * size + 1, height_count * size + 1
FPS = 60


screen = pg.display.set_mode(resolution)
clock = pg.time.Clock()


next_blocks_stage = [[0 for _ in range(width_count)] for _ in range(height_count)]
blocks = [[random.choice([0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) for _ in range(width_count)] for _ in range(height_count)]
children = [[0 for _ in range(width_count)] for _ in range(height_count)]
parents = [[0 for _ in range(width_count)] for _ in range(height_count)]
#parents2 = [[0 for _ in range(width_count)] for _ in range(height_count)]


class Victim:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alive = True
        self.age = 0

    def get_neighbours(self, field, position):
        neighbors = 0

        self.x, self.y = position
        for xs in range(self.x - 1, self.x + 2):
            for ys in range(self.y - 1, self.y + 2):
                if field[ys][xs] == 1:
                    neighbors += 1
        return neighbors - 1

    def reproduction(self, field, position):
        self.x, self.y = position
        neighbors = self.get_neighbours(field, position)

        # Если у клетки меньше двух соседей, то она умирает
        if neighbors == 0:
            self.alive = False
            return 0

        elif neighbors < 2:
            self.alive = False
            return 0
        # Если у клетки больше 8 соседей, то она умирает от перенаселения
        if neighbors == 8:
            self.alive = False
            return 0

        # Если клетка мертва и у нее три живых соседа, она оживает
        if not self.alive and neighbors == 3:
            self.alive = True
            self.age = 0
            return 1

    # Если клетка жива и у нее больше 2 соседей, она продолжает жить
        if self.alive and (neighbors >= 2) and (neighbors <= 7):
            self.age += 1
            if self.age > 100:
                return 0
            return 1


    def die(self, field, position):

        self.x, self.y = position
        neighbors = self.get_neighbours(field, position)

        if neighbors == 0:
            self.alive = False
            return 0

        elif neighbors == 8 or neighbors == 7:
            self.alive = False
            return 0

        elif self.age == 100:
            self.alive = False
            return 0

        else:
            self.age += 1
            return 1



# class Predator:
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#         self.color = (30, 30, 30)
#
#     def kill_other(self, field, position):
#         self.x, self.y = position
#
#     def die_self(self, field, position):
#         self.x, self.y = position
#

def right_choice(x, y, field):
    for xs in range(x - 1, x + 2):
        for ys in range(y - 1, y + 2):
            if field[ys][xs] == 0:
                return y - ys, x - xs
            else:
                continue

    else:
        return 0, 0


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            quit()

    screen.fill(pg.Color('black'))

    [pg.draw.line(screen, (100, 1, 100), (x, 0), (x, height)) for x in range(0, width, size * 2)]
    [pg.draw.line(screen, (100, 1, 100), (0, y), (width, y)) for y in range(0, height, size * 2)]

    for x_block in range(1, width_count - 1):
        for y_block in range(1, height_count - 1):
            if blocks[y_block][x_block] == 1:
                pg.draw.rect(screen, (1, 250, 1), (x_block * size + 2, y_block * size + 2, size - 2, size - 2))
            elif blocks[y_block][x_block] == 0:
                pg.draw.rect(screen, (1, 1, 1), (x_block * size + 2, y_block * size + 2, size - 2, size - 2))
            pos = (x_block, y_block)

            #we need to form right coordinates

            dy, dx = right_choice(x_block, y_block, blocks)
            #print(dy, dx)

            children[y_block - dy][x_block - dx] = Victim(x_block, y_block).reproduction(blocks, pos)
            parents[y_block][x_block] = blocks[y_block][x_block]

            # блок кода, который отвечает за генерацию смерти
            # parents2 = parents
            #
            # parents2[y_block][x_block] = Victim(x_block, y_block).die(blocks, pos)
            #
            # if parents2[y_block][x_block] + parents[y_block][x_block] == 2:
            #     parents[y_block][x_block] = 1
            # else:
            #     parents[y_block][x_block] = 0

            if parents[y_block][x_block] + children[y_block][x_block] >= 1:
                next_blocks_stage[y_block][x_block] = 1
            else:
                next_blocks_stage[y_block][x_block] = 0

    blocks = copy.deepcopy(next_blocks_stage)

    #print(len(next_blocks_stage))

    clock.tick(FPS)
    pg.display.flip()
