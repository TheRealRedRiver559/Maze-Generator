import random
import pygame

line_width = 1
cell_size = 20

delayed_generation = False
update_delay = 2

width = 800
height = 800
rows = (width//cell_size)
columns = (height//cell_size)
size = (width,height)
window = pygame.display.set_mode((width+line_width+1, height+line_width+1))

grid = []
active_cells = []

def generate_grid():
    window.fill([0,0,0])
    grid = ([[Cell(x, y) for y in range(rows)] for x in range(columns)])
    return grid

class Cell():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.top_wall = False
        self.right_wall = False
        self.bottom_wall = False
        self.left_wall = False
        self.wall_pos = []
        self.walls = []
        self.color = (123, 123, 244)

    def draw_walls(self):
        if self.top_wall:
            pygame.draw.line(window, (self.color), ((self.x*cell_size), (self.y*cell_size)), ((self.x*cell_size)+cell_size, (self.y*cell_size)), line_width)
        if self.right_wall:
            pygame.draw.line(window, (self.color), ((self.x*cell_size)+cell_size, (self.y*cell_size)), ((self.x*cell_size)+cell_size, (self.y*cell_size)+cell_size), line_width)
        if self.bottom_wall:
            pygame.draw.line(window, (self.color), ((self.x*cell_size)+cell_size, (self.y*cell_size)+cell_size), ((self.x*cell_size), (self.y*cell_size)+cell_size), line_width)
        if self.left_wall:
            pygame.draw.line(window, (self.color), ((self.x*cell_size), (self.y*cell_size)+cell_size), ((self.x*cell_size), (self.y*cell_size)), line_width)
    
    def add_walls(self):
        self.walls = []

        self.walls.append(((self.x*cell_size, self.y*cell_size), ((self.x*cell_size)+cell_size, (self.y*cell_size))))
        self.walls.append((((self.x*cell_size)+cell_size, self.y*cell_size), ((self.x*cell_size)+cell_size, ((self.y*cell_size)+cell_size))))
        self.walls.append(((self.x*cell_size, (self.y*cell_size)+cell_size), ((self.x*cell_size)+cell_size, ((self.y*cell_size)+cell_size))))
        self.walls.append(((self.x*cell_size, self.y*cell_size), (self.x*cell_size, ((self.y*cell_size)+cell_size))))

    def check_nighbors(self):
        self.nighbors = []

        if 0 < ((self.y-1)*cell_size) < height:
            self.nighbors.append(grid[self.x][self.y-1])

        if 0 < ((self.x+1)*cell_size) < width:
            self.nighbors.append(grid[self.x+1][self.y])

        if 0 < ((self.y+1)*cell_size) < height:
            self.nighbors.append(grid[self.x][self.y+1])
            
        if 0 < ((self.x-1)*cell_size) < height:
            self.nighbors.append(grid[self.x-1][self.y])
 
        if len(self.nighbors) > 0:
            self.nighbor = random.choice(self.nighbors)
            #self.nighbor.color = (204, 0, 0)
            self.edges = [edge for edge in self.walls if edge in self.nighbor.walls]

            if (list(self.walls).index(list(self.edges)[0])) == 0:
                self.top_wall = True
                self.nighbor.bottom_wall = True
            elif (list(self.walls).index(list(self.edges)[0])) == 1:
                self.right_wall = True
                self.nighbor.left_wall = True
            elif (list(self.walls).index(list(self.edges)[0])) == 2:
                self.bottom_wall = True
                self.nighbor.top_wall = True
            elif (list(self.walls).index(list(self.edges)[0])) == 3:
                self.left_wall = True
                self.nighbor.right_wall = True

            

fps_clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_1:
                grid = generate_grid()
                for x in range(columns):
                    for y in range(rows):
                        active_cells.append(grid[x][y])
                        obj = grid[x][y]
                        obj.draw_walls()
                        obj.add_walls()
                
                window.fill([0,0,0])
                pygame.draw.rect(window, ((127, 123, 232)), [(0, 0), (width+1, height+1)], 1)
                for _ in range(len(active_cells)):
                    obj = random.choice(active_cells)
                    active_cells.remove(obj)
                    #obj.color = (123, 0, 0)
                    obj.add_walls()
                    obj.check_nighbors()
                    obj.draw_walls()

                    if delayed_generation:
                        pygame.display.update()
                        pygame.time.wait(update_delay)

    fps_clock.tick(100)
    pygame.display.set_caption("Maze Generator: Algorithm 2 - FPS: {}".format(int(fps_clock.get_fps())))

    pygame.display.update()

pygame.quit()
