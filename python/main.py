import pygame as pg 
import sys 
import time

# Initialize variables
WIDTH = 400
HEIGHT = 400
BACKGROUND_COLOR = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
TEXT_COLOR = (0, 0, 0)
FPS = 30

# Grid and player's information 
grid_size = [[None] * 3 for _ in range(3)]
current_player =  'x'
current_winner = None
is_draw = False

# Initialize pygame
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT + 100))
pg.display.set_caption("Tic Tac Toe")
clock = pg.time.Clock()

# Function to draw the grid
def draw_grid():
    """Draw the grid"""
    screen.fill(BACKGROUND_COLOR)
    # Vertical grid
    pg.draw.line(screen, LINE_COLOR, (WIDTH // 3, 0), (WIDTH // 3, HEIGHT), 7)
    pg.draw.line(screen, LINE_COLOR, (2 * WIDTH // 3, 0), (2 * WIDTH // 3, HEIGHT), 7)
    # Horizontal grid
    pg.draw.line(screen, LINE_COLOR, (0, HEIGHT // 3), (WIDTH, HEIGHT // 3), 7)
    pg.draw.line(screen, LINE_COLOR, (0, 2 * HEIGHT // 3), (WIDTH, 2 * HEIGHT // 3), 7)
    draw_status()
    
def draw_status():
    """Draw status message"""
    output = f"{current_player}'s Turn" if not current_player else f"{current_winner} won"
    if is_draw:
        output = "It's a draw!"
        
    font = pg.font.Font(None, 36)
    text_surface = font.render(output, True, TEXT_COLOR)
    screen.fill((200, 200, 200), (0, HEIGHT, WIDTH, 100))
    screen.blit(text_surface, text_surface.get_rect(center=(WIDTH // 2, HEIGHT + 50)))
    pg.display.update()

def check_winner():
    """"Check winner or draw and handle game state"""
    global current_winner, is_draw 
    
    for x in range(3):
        # row checking
        if grid_size[x][0] == grid_size[x][1] == grid_size[x][2] and grid_size[x][0] is not None:
            current_winner = grid_size[x][0]
            pg.draw.line(screen, (250, 0, 0), (0,( x + 0.5)* HEIGHT // 3), (WIDTH, (x + 0.5) * HEIGHT // 3), 7)
            return 
        # column checking   
        
        if grid_size[0][x] == grid_size[1][x] == grid_size[2][x] and grid_size[0][x] is not None:
            current_winner = grid_size[0][x]
            pg.draw.line(screen, (250, 0, 0), ((x + 0.5)*WIDTH // 3, 0), ((x + 0.5)*WIDTH // 3, HEIGHT), 7)
            return
    # diagonal checking
    if  grid_size[0][0] == grid_size[1][1] == grid_size[2][2] and grid_size[0][0] is not None:
            current_winner = grid_size[0][0]
            pg.draw.line(screen, (250, 0, 0), (0, 0), (WIDTH, HEIGHT), 7)
            return
    if grid_size[0][2] == grid_size[1][1] == grid_size[2][0] and grid_size[0][2] is not None:
            current_winner = grid_size[0][2]
            pg.draw.line(screen, (250, 0, 0), (WIDTH, 0), (0, HEIGHT), 7)
            return
    # draw check
    if all(cell for row in grid_size for cell in row) and not current_winner:
        is_draw = True

def draw_move(row, col):
    """Draw the X or O move on the board"""
    global current_player

    axis_x = (col +0.5) * WIDTH // 3
    axis_y = (row + 0.5) * HEIGHT // 3
    if current_player == 'x':
        # draw x move
        offset = 50
        pg.draw.line(screen, LINE_COLOR, (axis_x - offset, axis_y - offset), (axis_x + offset, axis_y + offset), 7)
        pg.draw.line(screen, LINE_COLOR, (axis_x - offset, axis_y + offset), (axis_x + offset, axis_y - offset), 7)
        current_player = 'o'
    else:
        # draw o move
        radius = 50
        pg.draw.circle(screen, LINE_COLOR, (axis_x, axis_y), radius, 7)
        current_player = 'x'
    grid_size[row][col] = current_player
    pg.display.update()

def handle_click():
    """Handle mouse click"""
    global current_winner, is_draw

    i, j = pg.mouse.get_pos()
    if j < HEIGHT:
        row, col = j // (HEIGHT // 3), i // (WIDTH // 3)
        if grid_size[row][col] is None:
            draw_move(row, col)
            check_winner()

def reset_game():
    """Reset the game"""
    global grid_size, current_player, current_winner, is_draw
    time.sleep(10) # Pause the game for 10 second intervals after a win/draw cycle 
    grid_size = [[None] * 3 for _ in range(3)]
    current_player = 'x'
    current_winner = None
    is_draw = False
    draw_grid()

draw_grid()


# MAin game loop
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        elif event.type == pg.MOUSEBUTTONDOWN:
             if not current_winner and not is_draw:
                 handle_click()
             else:
                 reset_game()
    pg.display.update()
    clock.tick(FPS)