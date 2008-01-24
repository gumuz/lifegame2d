# game of life 2d - gumuz
# http://www.gumuz.nl
#
# Conway's game of life using pyglet/opengl
# http://en.wikipedia.org/wiki/Conway%27s_Game_of_Life

# pyglet imports
from pyglet.gl import *
from pyglet import window, clock, image
from pyglet.window import key

# stadard lib imports
from random import choice


def seed_grid():
    # populate the grid at random
    global grid
    for y in range(50):
        for x in range(50):
            grid[y][x] = (choice((0,0,0,1)), 0)

def evolve_grid():
    # evolve the grid
    global grid
    # empty working grid
    working_grid = [[(0,0)]*50 for i in [0]*50]
    
    for y in range(50):
        for x in range(50):
            # count the 9 neighbours
            offsets = [ (-1, -1), (-1, 0), 
                        (-1, 1), (0, -1), 
                        (0, 1), (1, -1), 
                        (1, 0), (1, 1)]
            neighbours = 0
            for a,b in offsets:
                ny,nx = (y+a)%50, (x+b)%50
                neighbours += grid[ny][nx][0]
                
            state, age = grid[y][x]
            if state: # if alive
                if neighbours in (2,3): # keep alive
                    working_grid[y][x] = 1,age+1
            else: # if dead
                if neighbours == 3: # new life!
                    working_grid[y][x] = 1,0
    
    # copy working_grid onto gid
    grid = working_grid

def draw_grid():
    # draw the grid squares
    global grid
    
    # opengl quad-mode
    glBegin(GL_QUADS)
    
    # square vertices
    square_verts = [    (0,0), (10,0), 
                        (10,10), (0,10)]
    for y in range(50):
        for x in range(50):
            state, age = grid[y][x]
            if state: 
                # alive, adjust color to age, downto 0.2
                age_col = 1-(0.04*age)
                if age_col < 0.2: age_col= 0.2
                
                glColor3f(0.1,0.1,age_col)
                for vx,vy in square_verts:
                    vx = vx +10 + (x*10)
                    vy = vy + 10 + (y*10)
                    glVertex2f(vx,vy)
    glEnd()

def draw_arena():
    # draw arena lines
    glColor3f(.5,.5,.5)
    
    # opengl line-mode
    glBegin(GL_LINES)
    
    # arena vertices
    arena_verts = [  (9,9), (511,9), (511,511), 
                    (9,511), (9,9) ]
    for i in range(len(arena_verts)-1):
        glVertex2f(*arena_verts[i])
        glVertex2f(*arena_verts[i+1])

    glEnd()
    

def draw_header():
    global header_img
    
    glColor3f(1,1,1)
    header_img.blit(10,520)
    
def draw_help():
    global controls_img
    
    glColor3f(1,1,1)
    controls_img.blit(100,200)

    
# The OpenGL context
win = window.Window(visible=False,width=520,height=570)
win.set_visible()

# some globals
header_img = image.load('header.png').texture
controls_img = image.load('controls.png').texture

show_help = True
evolving = False
painting = False


fps_limit = 20
clock.set_fps_limit(fps_limit)

# events
def on_key_press(symbol, modifiers):
    global evolving, fps_limit, grid, show_help
    if show_help:
        show_help = False
        return

    if symbol == key.H:
        # show help screen
        show_help = True
    if symbol == key.SPACE:
        # toggle evolving
        evolving = not evolving
    if symbol == key.R:
        # reseed grid
        seed_grid()
    if symbol == key.C:
        # clear grid
        grid = [[(0,0)]*50 for i in range(50)]
    if symbol == key.UP:
        fps_limit += 2
        if fps_limit > 40: fps_limit = 40
        clock.set_fps_limit(fps_limit)
    if symbol == key.DOWN:
        fps_limit -= 2
        if fps_limit < 2: fps_limit = 2
        clock.set_fps_limit(fps_limit)
win.on_key_press = on_key_press

def on_mouse_press(x, y, button, modifiers):
    if x<11 or x>509 or y<11 or y>509: return
    global grid, painting
    painting = True
    grid[(y-10)/10][(x-10)/10] = (1,0)
win.on_mouse_press = on_mouse_press

def on_mouse_release(x, y, button, modifiers):
    global painting
    painting = False
win.on_mouse_release = on_mouse_release
    
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if x<11 or x>509 or y<11 or y>509: return
    global grid
    grid[(y-10)/10][(x-10)/10] = (1,0)
win.on_mouse_drag = on_mouse_drag



# empty zero-filled grid
grid = [[(0,0)]*50 for i in range(50)]


while not win.has_exit:
    win.dispatch_events()
    dt = clock.tick()
    
    # set title framerate
    win.set_caption('Game of Life 2d - evolutions per second: %s' % round(clock.get_fps()))

    # clear
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    
    draw_header()
    draw_arena()
    if evolving and not painting and not show_help: evolve_grid()
    draw_grid()
    if show_help: draw_help()

    win.flip()