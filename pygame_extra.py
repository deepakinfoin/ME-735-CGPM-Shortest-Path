
#importing library

import pygame
import math
from queue import *

#defining widht of layout
layout_width = 1520

#defining layout
window = pygame.display.set_mode((layout_width, layout_width - 760))
pygame.display.set_caption("CGPM PROJECT path FINDER")

#defining class for first event
class Object:
    def __init__(self, rows, col, width, total_rows):
        self.rows = rows
        self.col = col
        self.x = rows * width
        self.y = col * width
        self.color = black
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    #defining methods for getting class variables

    def get_pos(self):
        return self.rows, self.col

    def is_blockage(self):
        return self.color == blockage

    def build_start(self):
        self.color = START

    def build_closed(self):
        self.color = neighbour

    def build_open(self):
        self.color = border

    def build_blockage(self):
        self.color = blockage

    def build_end(self):
        self.color = END

    def build_path(self):
        self.color = path

    #method for drawing objects on layout
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    #method for updating neighbours
    def update_neighbors(self, grid):
        self.neighbors = []

        # moving down for updation of neighbor point
        if self.rows < self.total_rows - 1 and not grid[self.rows + 1][self.col].is_blockage():
            self.neighbors.append(grid[self.rows + 1][self.col])

        # moving up for updation of neighbor point
        if self.rows > 0 and not grid[self.rows - 1][self.col].is_blockage():
            self.neighbors.append(grid[self.rows - 1][self.col])

        # moving right for updation of neighbor point
        if self.col < self.total_rows - 1 and not grid[self.rows][self.col + 1].is_blockage():
            self.neighbors.append(grid[self.rows][self.col + 1])

        # moving left for updation of neighbor point
        if self.col > 0 and not grid[self.rows][self.col - 1].is_blockage():
            self.neighbors.append(grid[self.rows][self.col - 1])

    def __lt__(self, other):
        return False

# defining grid
def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, gray, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, gray, (j * gap, 0), (j * gap, width))

#defining method for drawing grid
def draw(win, grid, rows, width):
    win.fill(black)

    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()

#defining color codes
neighbour = (90, 100, 100)
border = (90, 100, 100)
blockage = (180, 45, 45)
black = (0, 0, 0)
path = (20, 20, 255)
START = (255, 255, 0)
gray = (128, 128, 128)
END = (51, 255, 51)


#calculating distance
def calc_dist(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

#reconstructing path based on neighbor updation (shortest distance)
def reconstruct_path(prev_position, current, draw):
    while current in prev_position:
        current = prev_position[current]
        current.build_path()
        draw()

#using astar algorithm algorithm
def algo(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    prev_position = {}
    dis_score = {spot: float("inf") for rows in grid for spot in rows}
    dis_score[start] = 0
    dist1_score = {spot: float("inf") for rows in grid for spot in rows}
    dist1_score[start] = calc_dist(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(prev_position, end, draw)
            end.build_end()
            return True

        for neighbor in current.neighbors:
            temp_dis_score = dis_score[current] + 1

            if temp_dis_score < dis_score[neighbor]:
                prev_position[neighbor] = current
                dis_score[neighbor] = temp_dis_score
                dist1_score[neighbor] = temp_dis_score + calc_dist(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((dist1_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.build_open()

        draw()

        if current != start:
            current.build_closed()

    return False

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Object(i, j, gap, rows)
            grid[i].append(spot)

    return grid

# getting mouse clicked position
def get_mouse_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


# main executing code

win = window
width = layout_width
ROWS = 50
grid = make_grid(ROWS, width)

start1 = None
end = None

decision = True

# run while loop till decision = True
while decision:
    #execute the layout
    draw(win, grid, ROWS, width)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            decision = False
            
        # if left mouse button is pressed_spot the start and end
        if pygame.mouse.get_pressed()[0]:  
            pos = pygame.mouse.get_pos()
            x, y = get_mouse_pos(pos, ROWS, width)
            spot = grid[x][y]
            if not start1 and spot != end:
                start1 = spot
                start1.build_start()

            elif not end and spot != start1:
                end = spot
                end.build_end()

            elif spot != end and spot != start1:
                spot.build_blockage()

        # if s key from keyboard is pressed then the process starts
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s and start1 and end:
                for x in grid:
                    for spot in x:
                        spot.update_neighbors(grid)

                algo(lambda: draw(win, grid, ROWS, width), grid, start1, end)
                start1.build_start()

            # if n key from keyboard is pressed then the process starts
            elif event.key == pygame.K_n:
                start1 = None
                end = None
                grid = make_grid(ROWS, width)
pygame.quit()

