import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Trouble")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

ORANGE = (255, 165, 0)
COLORS = {"Red": RED, "Blue": BLUE, "Green": GREEN, "Yellow": YELLOW}

# Fonts
font_title = pygame.font.Font(None, 48)
font_text = pygame.font.Font(None, 32)
font_i = pygame.font.Font(None, 14)
font_small = pygame.font.Font(None, 24)

#Game variables
#Board
BOARD_SIZE = 500  # Size of the board
MARGIN = 100  # Margin from the edge of the screen to the board

#Spaces
SPACE_RADIUS = 20  # Radius for each space on the board
SPACE_OFFSET = BOARD_SIZE / 7 #distance between each space
NUM_SPACES = 28 #number of spaces going around the board
QUARTER = NUM_SPACES / 4 #each side of the board
PEG_SPACES = 16 #number of spaces holding pegs initially
FIN_SPACES = 16 #number of spaces going to the finish line

#Popomatic + Dice
POPOMATIC_RADIUS = 50  # Radius for the Pop-O-Matic button
dice_roll = 0

#instructions
show_instructions = False
file = open('Instructions.txt', 'r')
lines = file.readlines()
for l in range(len(lines)):
    lines[l] = lines[l].strip()
file.close()

# Board positions
def calculate_square_positions(SCREEN_WIDTH, SCREEN_HEIGHT, BOARD_SIZE, NUM_SPACES, QUARTER):
    '''
        Calculates the positions of the main spaces the pegs will move on; 
        Returns list 'positions' which hold 28 elements, spaces on the board, each with a list holding it's position [x, y]
    '''

    positions = []
    start_x = (SCREEN_WIDTH - BOARD_SIZE) // 2
    start_y = (SCREEN_HEIGHT - BOARD_SIZE) // 2

    quart = QUARTER
    
    for i in range(NUM_SPACES):
        if i < quart:
            # Top side
            x = start_x + i * (BOARD_SIZE / quart)
            y = start_y
        elif i < quart*2:
            # Right side
            x = start_x + BOARD_SIZE
            y = start_y + (i - quart) * (BOARD_SIZE / quart)
        elif i < quart*3:
            # Bottom side
            x = start_x + (BOARD_SIZE - (i - quart*2) * (BOARD_SIZE / quart))
            y = start_y + BOARD_SIZE
        elif i < quart*4:
            # Left side
            x = start_x
            y = start_y + (BOARD_SIZE - (i - quart*3) * (BOARD_SIZE / quart))
        positions.append([x, y])
        
    #positions hold 28 elements each with a list [x, y]
    return positions

# Generate list of board space's positions (Spaces: 0 to 27)
board_spaces = calculate_square_positions(SCREEN_WIDTH, SCREEN_HEIGHT, BOARD_SIZE, NUM_SPACES, QUARTER)

#dictionary of board spaces (0 to 27) and their corressponding peg, if any
#board = {}
#for space in range(len(board_spaces)):
#    board[space] = ''

#player setup
players = {0: 'RED', 1: 'BLUE', 2: 'GREEN', 3: 'YELLOW'}
# 0 "Red"   : board_spaces[0]     # Top-left for Red
# 1 "Blue"  : board_spaces[7]     # Top-right for Blue
# 2 "Green" : board_spaces[14]    # Bottom-right for Green
# 3 "Yellow": board_spaces[21]    # Bottom-left for Yellow
player_start = {0: 0, 1: 7, 2: 14, 3: 21}

def calculate_inital_peg_positions(QUARTER, board_spaces, SPACE_OFFSET):
    q = QUARTER
    peg_pos = {}
    for space in range(4):
        pos = []
        if space == 0:
            #RED
            pos.append([board_spaces[0][0]                 , board_spaces[0][1] - SPACE_OFFSET])
            pos.append([board_spaces[0][0] +   SPACE_OFFSET, board_spaces[0][1] - SPACE_OFFSET])
            pos.append([board_spaces[0][0] + 2*SPACE_OFFSET, board_spaces[0][1] - SPACE_OFFSET])
            pos.append([board_spaces[0][0] + 3*SPACE_OFFSET, board_spaces[0][1] - SPACE_OFFSET])
            
        if space == 1:
            #BLUE
            pos.append([board_spaces[7][0] + SPACE_OFFSET, board_spaces[7][1]])
            pos.append([board_spaces[7][0] + SPACE_OFFSET, board_spaces[7][1] +   SPACE_OFFSET])
            pos.append([board_spaces[7][0] + SPACE_OFFSET, board_spaces[7][1] + 2*SPACE_OFFSET])
            pos.append([board_spaces[7][0] + SPACE_OFFSET, board_spaces[7][1] + 3*SPACE_OFFSET])
            
        if space == 2:
            #GREEN
            pos.append([board_spaces[14][0]                 , board_spaces[14][1] + SPACE_OFFSET])
            pos.append([board_spaces[14][0] -   SPACE_OFFSET, board_spaces[14][1] + SPACE_OFFSET])            
            pos.append([board_spaces[14][0] - 2*SPACE_OFFSET, board_spaces[14][1] + SPACE_OFFSET])
            pos.append([board_spaces[14][0] - 3*SPACE_OFFSET, board_spaces[14][1] + SPACE_OFFSET])
            
    
        if space == 3:
            #YELLOW
            pos.append([board_spaces[21][0] - SPACE_OFFSET, board_spaces[21][1]])
            pos.append([board_spaces[21][0] - SPACE_OFFSET, board_spaces[21][1] -   SPACE_OFFSET])
            pos.append([board_spaces[21][0] - SPACE_OFFSET, board_spaces[21][1] - 2*SPACE_OFFSET])
            pos.append([board_spaces[21][0] - SPACE_OFFSET, board_spaces[21][1] - 3*SPACE_OFFSET])
            
        peg_pos[space] =  pos
    #player color : [the 4 pegs positions]
    return(peg_pos)

#Generate peg positions
inital_peg_positions = calculate_inital_peg_positions(QUARTER, board_spaces, SPACE_OFFSET)

#players 0, 1, 2, 3 each have 4 pegs (0, 1, 2, 3) w/ a location
peg_positions = {}
for key in inital_peg_positions:
    rock = []
    for peg in range(4):
        rock.append(inital_peg_positions[key][peg])
    peg_positions[key] = rock

start_pos = [board_spaces[player_start[0]], board_spaces[player_start[1]], board_spaces[player_start[2]],board_spaces[player_start[3]]]

def draw_diagonal_circles(start_pos, color):
    """Draw 4 diagonal circles from the Start space to the Pop-O-Matic."""
    pos_dict = {}
    center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

    for i in range(4):
        pos_list = []
        dx = (center_x - start_pos[i][0]) / 5
        dy = (center_y - start_pos[i][1]) / 5
        for j in range(1, 5):
            circle_x = start_pos[i][0] + dx * j
            circle_y = start_pos[i][1] + dy * j
            pos_list.append([circle_x,circle_y])
            pygame.draw.circle(screen, color, (int(circle_x), int(circle_y)), SPACE_RADIUS, 2)
        pos_dict[i] = pos_list
    return(pos_dict)

digonal_positions = draw_diagonal_circles(start_pos, WHITE)

def draw_board():
    """Draw the Trouble game board for the first time."""
    #draw the main spaces
    for pos in board_spaces:
        pygame.draw.circle(screen, WHITE, pos, SPACE_RADIUS, 2)
    
    #draw player's inital pegs
    for space in peg_positions:
        for i in range(4):
            pygame.draw.circle(screen, players[space], peg_positions[space][i], SPACE_RADIUS)
                
    # Draw the Pop-O-Matic bubble
    center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
    pygame.draw.circle(screen, RED, (center_x, center_y), POPOMATIC_RADIUS)
    popomatic_text = font_text.render("Pop-O-Matic", True, WHITE)
    screen.blit(popomatic_text, (center_x - popomatic_text.get_width() // 2, center_y - popomatic_text.get_height() // 2))

    draw_diagonal_circles(start_pos, WHITE)

    rect_width, rect_height = 150, 50
    rect_x, rect_y = SCREEN_WIDTH - rect_width - 10, 10 
    pygame.draw.rect(screen, WHITE, (rect_x, rect_y, rect_width, rect_height), 2) 
    instructions_text = font_text.render("Instructions", True, WHITE) 
    screen.blit(instructions_text, (rect_x + 10, rect_y + 10)) 

    # Show instructions if flag is True 
    if show_instructions:
        pygame.draw.rect(screen, BLACK, (100, 100, 600, 650))
        pygame.draw.rect(screen, WHITE, (100, 100, 600, 650), 2)
        y_offset = 120 
        for line in lines: 
            text = font_i.render(line, True, WHITE)
            screen.blit(text, (120, y_offset))
            y_offset += 40


def roll_dice():
    '''returns random int 1 to 6'''
    return random.randint(1, 6)

def popomatic_click(mouse_pos):
    '''if clicked, return the dice roll'''
    distance = math.sqrt((mouse_pos[0] - SCREEN_WIDTH // 2) ** 2 + (mouse_pos[1] - SCREEN_HEIGHT // 2) ** 2)
    if distance <= POPOMATIC_RADIUS:
        dice_roll = roll_dice()
        print(f"Dice rolled: {dice_roll}")
        return(dice_roll)

def handle_instructions_click(mouse_pos):
    rect_width, rect_height = 150, 50 
    rect_x, rect_y = SCREEN_WIDTH - rect_width - 10, 10 
    if rect_x <= mouse_pos[0] <= rect_x + rect_width and rect_y <= mouse_pos[1] <= rect_y + rect_height: 
        return True
    return False

current_player = 0
turn_order = [0, 1, 2, 3]
#what space is the peg rn?

peg_space = {0: [-1 , -1, -1 , -1],
             1: [-1 , -1, -1 , -1],
             2: [-1 , -1, -1 , -1],
             3: [-1 , -1, -1 , -1]}

has_peg_hit_start = {0: [False , False, False , False],
             1: [False , False, False , False],
             2: [False , False, False , False],
             3: [False , False, False , False]}

win = {0: 0,
       1: 0,
       2: 0,
       3: 0}

def collison(player, peg):
    global peg_space
    
    if peg_space[player][peg] == player_start[player]:
        if has_peg_hit_start[player][peg]:
            peg_positions[player][peg] = digonal_positions[player][peg]
            peg_space[player][peg] = 100
            win[player] += 1

            if win[player] >= 4:
                print(f'Player {player + 1} You Win!')

        has_peg_hit_start[player][peg] = True


    for key in peg_space:
        for i in range(4):
            if peg_space[player][peg] == peg_space[key][i] and not (key == player and i == peg) and (peg_space[player][peg] != 100):
                peg_space[key][i] = -1
                peg_positions[key][i] = inital_peg_positions[key][i]
                has_peg_hit_start[key][i] = False
                break


def check_if_any_peg_at_home(player):
    if -1 in peg_space[player]:
        return(True)
    else:
        return(False)

def check_if_any_peg_on_board(player):
    res = False
    for peg in range(4):
        if peg_space[player][peg] != -1 and peg_space[player][peg] != 100:
            res = True
    return(res)

def move_player(current_player, dice_roll):
    """Move the current player based on the dice roll."""
    player = current_player
    peg = -1

    print('')
    print(f'Player {int(player) + 1} you rolled a {dice_roll}')
    

    if dice_roll == 6:
        is_at_home = check_if_any_peg_at_home(player)
        is_on_board = check_if_any_peg_on_board(player)

        if is_at_home: #if there is still a peg to bring out
            if is_on_board: #and also a peg on the board
                try:
                    choice = int(input('Press 0 if you would like to bring out a new peg\nOR\nPress 1 if you would like to move an existing peg\n'))
                except:
                    print('You entered something that is not an integer of 0 or 1')
                    choice = int(input('Try again with 0 or 1 only.\n'))

                if choice == 0: #bring out
                    peg = int(input('Which peg would you like to bring out? ')) - 1 #pick a peg
                    while peg_space[player][peg] != -1:
                        print('This peg is not at home.')
                        peg = int(input('Which peg would you like to bring out? ')) - 1

                    new_space = player_start[player] #new space for peg
                    peg_space[player][peg] = new_space #where is the peg now
                    peg_positions[player][peg] = board_spaces[new_space] #update the space the peg is in
                    
                    collison(player, peg)

                elif choice == 1:
                    peg = int(input('Which peg would you like to move? ')) - 1

                    while peg_space[player][peg] == -1 or peg_space[player][peg] == 100:
                        print('Please move a peg on the board.')
                        peg = int(input('Which peg would you like to move? ')) - 1
                    
                    new_space = (peg_space[player][peg] + dice_roll) % 28
                    #check if another peg is there already
                    #update the peg position
                    peg_space[player][peg] = new_space
                    peg_positions[player][peg] = board_spaces[new_space]
                    collison(player, peg)

            else: #if no pegs on the board, but peg at home
                peg = int(input('Which peg would you like to bring out? ')) - 1 #pick a peg
                while peg_space[player][peg] != -1:
                    print('This peg is not at home.')
                    peg = int(input('Which peg would you like to bring out? ')) - 1

                new_space = player_start[player] #new space for peg
                peg_space[player][peg] = new_space #where is the peg now
                peg_positions[player][peg] = board_spaces[new_space] #update the space the peg is in
                collison(player, peg)

        else: #if peg is not at home
            peg = int(input('Which peg would you like to move? ')) - 1

            while peg_space[player][peg] == -1 or peg_space[player][peg] == 100:
                print('Please move a peg on the board.')
                peg = int(input('Which peg would you like to move? ')) - 1
                    
                new_space = (peg_space[player][peg] + dice_roll) % 28
                #check if another peg is there already
                #update the peg position
                peg_space[player][peg] = new_space
                peg_positions[player][peg] = board_spaces[new_space]
            collison(player, peg)
    
    else:
        is_peg_on_board = check_if_any_peg_on_board(player)
        if is_peg_on_board:
            peg = int(input('Which peg would you like to move? ')) - 1
            while peg_space[player][peg] == -1 or peg_space[player][peg] == 100:
                print('Please move a peg on the board.')
                peg = int(input('Which peg would you like to move? ')) - 1
                        
            new_space = (peg_space[player][peg] + dice_roll) % 28
            #check if another peg is there already
            #update the peg position
            peg_space[player][peg] = new_space
            peg_positions[player][peg] = board_spaces[new_space]
            collison(player, peg)
        else:
            print('No pegs on the board. Please try again next turn.')

    

def next_player(current_player, dice_roll):
    """Switch to the next player unless a six was rolled."""
    if dice_roll != 6:  # If a six is not rolled, move to the next player
        current_player = (current_player + 1) % len(players)
    return(current_player)
                
    

# Main game loop
def game_loop(current_player):
    running = True
    current_player = current_player
    dice_roll = 'n/a'
    draw_board()

    while running:
        global show_instructions
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if handle_instructions_click(event.pos):
                    show_instructions = not show_instructions
                dice_roll = popomatic_click(event.pos) #roll the dice
                if dice_roll != None:  # Ensure a roll even happened
                    move_player(current_player, dice_roll)  # Move the current player based on the dice roll
                    current_player = next_player(current_player, dice_roll)  # Update to the next player if needed

        screen.fill(BLACK)
        draw_board() #draw the new board

        # Display dice roll
        dice_roll_text = font_text.render(f"Dice Roll: {dice_roll}", True, WHITE)
        screen.blit(dice_roll_text, (SCREEN_WIDTH // 2 - dice_roll_text.get_width() // 2, SCREEN_HEIGHT - 25))

        pygame.display.update()

game_loop(current_player)
