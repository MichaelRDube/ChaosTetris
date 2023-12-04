import pygame
from pygame import mixer
import random

pygame.init()
score = 0
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0, 255, 0)
blue = (0,0,255)
purple = (255, 0, 255)
deep_purple = (120, 3, 140)
yellow = (255, 255, 0)
teal = (0, 255, 255)
orange = (255, 165, 0)
brown = (150, 0, 0)
dark_grey = (90, 90, 90)
window_width = 800
window_height = 700
up = [0, -1]
down = [0, 1]
left = [-1, 0]
right = [1, 0]
score_sprite = pygame.image.load("Assets/score.png")
score_sprite = pygame.transform.scale(score_sprite, (115, 50))
wow_sprite = pygame.image.load("Assets/wow.png")
wow_sprite = pygame.transform.scale(wow_sprite, (200, 200))
game_over_sprite = pygame.image.load("Assets/game_over.png")
game_over_sprite = pygame.transform.scale(game_over_sprite, (500, 500))
show_wow_sprite = False
wow_message = pygame.USEREVENT+2
preview_x = 525
preview_y = 290
brick_health = 10

next_piece = 0
recent_pieces = [False, False]
next_preview = [0, 0, 0, 0]


spaces_window_x = 60
spaces_window_y = 80
spaces = [[False]*20 for _ in range(10)]

# create window
gameDisplay = pygame.display.set_mode((window_width, window_height))

pygame.draw.rect(gameDisplay, white, [0, 0, window_width, window_height])
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()




class Block:
    block_size = 30
    border_width = 2
    filler_color = 0
    space_x = 0
    space_y = 0
   
    def __init__(self, color):
        self.filler_color = color
       
    def __init__(self, x, y, color):
        self.filler_color = color
        self.space_x = x
        self.space_y = y
       
        if x < 10 and y < 20:
            spaces[x][y] = self
           
    def translate(self, direction):
        if self.space_x + direction[0] >= len(spaces) or self.space_x + direction[0] < 0:
            return
        elif self.space_y + direction[1] >= len(spaces[0]) or self.space_y + direction[1] < 0:
            return
        placeholder_x = self.space_x
        placeholder_y = self.space_y
        self.space_x += direction[0]
        self.space_y += direction[1]
        spaces[self.space_x][self.space_y] = self
        spaces[placeholder_x][placeholder_y] = False
       
    def can_translate(self, direction, blocks):
        if self.space_x + direction[0] > 9 or self.space_x + direction[0] < 0:
            return False
        if self.space_y + direction[1] > 19 or self.space_y + direction[1] < 0:
            return False
        if spaces[self.space_x + direction[0]][self.space_y + direction[1]] != False and spaces[self.space_x + direction[0]][self.space_y + direction[1]] not in blocks:
            return False
       
        return True
       
   
    def plot(self, x, y):
        pygame.draw.rect(gameDisplay, black, [x, y, self.block_size, self.block_size])
        pygame.draw.rect(gameDisplay, self.filler_color, [x+self.border_width, y+self.border_width, self.block_size-2*self.border_width, self.block_size-2*self.border_width])

class Brick(Block):
    health = 1
    def __init__(self, x, y, health):
        self.filler_color = dark_grey
        self.space_x = x
        self.space_y = y
        spaces[x][y] = self
        self.health = health
       
    def bonk(self):
        global score
        score += 1
        self.health -= 1
        if self.health <= 0:
            self.destroy()
       
    def destroy(self):
        spaces[self.space_x][self.space_y] = False
       
    def plot(self, x, y):
        pygame.draw.rect(gameDisplay, black, [x, y, self.block_size, self.block_size])
        pygame.draw.rect(gameDisplay, self.filler_color, [x+self.border_width, y+self.border_width, self.block_size-2*self.border_width, self.block_size-2*self.border_width])
        display_message(x+self.block_size//2, y+self.block_size//2, str(self.health), 20, white)

class Tetromino:
    blocks = [0, 0, 0, 0]
    set = False
    pivot_point = 0
    game_over = False
    def __init__(self, x, y, config):
        print("config:", config)
        if config == 0: #T tetromino
            print("creating T tetromino")
            if spaces[0+x][0+y] != False:
                self.game_over = True
            elif spaces[1+x][0+y] != False:
                self.game_over = True
            elif spaces[2+x][0+y] != False:
                self.game_over = True
            elif spaces[1+x][1+y] != False:
                self.game_over = True
            self.blocks[0] = Block(0+x, 0+y, green)        
            self.blocks[1] = Block(1+x, 0+y, green)
            self.blocks[2] = Block(2+x, 0+y, green)
            self.blocks[3] = Block(1+x, 1+y, green)
            self.pivot_point = self.blocks[1]
        elif config == 1: #L tetromino
            print("creating L tetromino")
            if spaces[0+x][0+y] != False:
                self.game_over = True
            elif spaces[0+x][1+y] != False:
                self.game_over = True
            elif spaces[0+x][2+y] != False:
                self.game_over = True
            elif spaces[1+x][2+y] != False:
                self.game_over = True
            self.blocks[0] = Block(0+x, 0+y, yellow)        
            self.blocks[1] = Block(0+x, 1+y, yellow)
            self.blocks[2] = Block(0+x, 2+y, yellow)
            self.blocks[3] = Block(1+x, 2+y, yellow)
            self.pivot_point = self.blocks[2]
        elif config == 2: #long tetromino
            print("creating long tetromino")
            if spaces[0+x][0+y] != False:
                self.game_over = True
            elif spaces[1+x][0+y] != False:
                self.game_over = True
            elif spaces[2+x][0+y] != False:
                self.game_over = True
            elif spaces[3+x][1+y] != False:
                self.game_over = True
            self.blocks[0] = Block(0+x, 0+y, red)        
            self.blocks[1] = Block(1+x, 0+y, red)
            self.blocks[2] = Block(2+x, 0+y, red)
            self.blocks[3] = Block(3+x, 0+y, red)
            self.pivot_point = self.blocks[2]
        elif config == 3: #Z tetromino
            print("creating Z tetromino")
            if spaces[0+x][0+y] != False:
                self.game_over = True
            elif spaces[1+x][0+y] != False:
                self.game_over = True
            elif spaces[1+x][1+y] != False:
                self.game_over = True
            elif spaces[2+x][1+y] != False:
                self.game_over = True
            self.blocks[0] = Block(0+x, 0+y, purple)        
            self.blocks[1] = Block(1+x, 0+y, purple)
            self.blocks[2] = Block(1+x, 1+y, purple)
            self.blocks[3] = Block(2+x, 1+y, purple)
            self.pivot_point = self.blocks[1]
        elif config == 4: #backwards L tetromino
            print("creating backwards L tetromino")
            if spaces[0+x][0+y] != False:
                self.game_over = True
            elif spaces[0+x][1+y] != False:
                self.game_over = True
            elif spaces[0+x][2+y] != False:
                self.game_over = True
            elif spaces[1+x][0+y] != False:
                self.game_over = True
            self.blocks[0] = Block(0+x, 0+y, blue)        
            self.blocks[1] = Block(0+x, 1+y, blue)
            self.blocks[2] = Block(0+x, 2+y, blue)
            self.blocks[3] = Block(1+x, 0+y, blue)
            self.pivot_point = self.blocks[0]
        elif config == 5: #backwards Z tetromino
            print("creating backwards Z tetromino")
            if spaces[0+x][1+y] != False:
                self.game_over = True
            elif spaces[1+x][0+y] != False:
                self.game_over = True
            elif spaces[1+x][1+y] != False:
                self.game_over = True
            elif spaces[2+x][0+y] != False:
                self.game_over = True
            self.blocks[0] = Block(0+x, 1+y, orange)        
            self.blocks[1] = Block(1+x, 0+y, orange)
            self.blocks[2] = Block(1+x, 1+y, orange)
            self.blocks[3] = Block(2+x, 0+y, orange)
            self.pivot_point = self.blocks[1]
        else: #square tetromino
            print("creating square tetromino")
            if spaces[0+x][0+y] != False:
                self.game_over = True
            elif spaces[0+x][1+y] != False:
                self.game_over = True
            elif spaces[1+x][0+y] != False:
                self.game_over = True
            elif spaces[1+x][1+y] != False:
                self.game_over = True
            self.blocks[0] = Block(0+x, 0+y, teal)        
            self.blocks[1] = Block(0+x, 1+y, teal)
            self.blocks[2] = Block(1+x, 0+y, teal)
            self.blocks[3] = Block(1+x, 1+y, teal)
       
    def can_translate(self, direction):
        for i in range(len(self.blocks)):
            if self.blocks[i].can_translate(direction, self.blocks) == False:
                return False
        return True
   
    def translate(self, direction):
        spaces[self.blocks[0].space_x][self.blocks[0].space_y] = False
        spaces[self.blocks[1].space_x][self.blocks[1].space_y] = False
        spaces[self.blocks[2].space_x][self.blocks[2].space_y] = False
        spaces[self.blocks[3].space_x][self.blocks[3].space_y] = False
       
        self.blocks[0].space_x += direction[0]
        self.blocks[1].space_x += direction[0]
        self.blocks[2].space_x += direction[0]
        self.blocks[3].space_x += direction[0]
           
        self.blocks[0].space_y += direction[1]
        self.blocks[1].space_y += direction[1]
        self.blocks[2].space_y += direction[1]
        self.blocks[3].space_y += direction[1]
       
        spaces[self.blocks[0].space_x][self.blocks[0].space_y] = self.blocks[0]
        spaces[self.blocks[1].space_x][self.blocks[1].space_y] = self.blocks[1]
        spaces[self.blocks[2].space_x][self.blocks[2].space_y] = self.blocks[2]
        spaces[self.blocks[3].space_x][self.blocks[3].space_y] = self.blocks[3]
   
    def rotate_left(self):
        if self.pivot_point == 0:
            return
       
        spaces[self.blocks[0].space_x][self.blocks[0].space_y] = False
        spaces[self.blocks[1].space_x][self.blocks[1].space_y] = False
        spaces[self.blocks[2].space_x][self.blocks[2].space_y] = False
        spaces[self.blocks[3].space_x][self.blocks[3].space_y] = False
       
        for block in self.blocks:
            x_displacement = self.pivot_point.space_x - block.space_x
            y_displacement = self.pivot_point.space_y - block.space_y
            block.space_x = self.pivot_point.space_x - y_displacement
            block.space_y = self.pivot_point.space_y + x_displacement
       
        for block in self.blocks:
            spaces[block.space_x][block.space_y] = block
           
    def rotate_right(self):
        if self.pivot_point == 0:
            return
       
        spaces[self.blocks[0].space_x][self.blocks[0].space_y] = False
        spaces[self.blocks[1].space_x][self.blocks[1].space_y] = False
        spaces[self.blocks[2].space_x][self.blocks[2].space_y] = False
        spaces[self.blocks[3].space_x][self.blocks[3].space_y] = False
       
        for block in self.blocks:
            x_displacement = self.pivot_point.space_x - block.space_x
            y_displacement = self.pivot_point.space_y - block.space_y
            block.space_x = self.pivot_point.space_x + y_displacement
            block.space_y = self.pivot_point.space_y - x_displacement
       
        for block in self.blocks:
            spaces[block.space_x][block.space_y] = block
           
    def can_rotate_right(self):
        if self.pivot_point == 0:
            return True
        for block in self.blocks:
            x_displacement = self.pivot_point.space_x - block.space_x
            y_displacement = self.pivot_point.space_y - block.space_y
           
            x_destination = self.pivot_point.space_x + y_displacement
            y_destination = self.pivot_point.space_y - x_displacement
            if x_destination < 0 or x_destination > 9:
                return False
            if y_destination < 0 or y_destination > 19:
                return False
            if spaces[x_destination][y_destination] != False and spaces[x_destination][y_destination] not in self.blocks:
                return False
        return True
   
    def can_rotate_left(self):
        if self.pivot_point == 0:
            return True
        for block in self.blocks:
            x_displacement = self.pivot_point.space_x - block.space_x
            y_displacement = self.pivot_point.space_y - block.space_y
           
            x_destination = self.pivot_point.space_x - y_displacement
            y_destination = self.pivot_point.space_y + x_displacement
            if x_destination < 0 or x_destination > 9:
                return False
            if y_destination < 0 or y_destination > 19:
                return False
            if spaces[x_destination][y_destination] != False and spaces[x_destination][y_destination] not in self.blocks:
                return False
        return True


def render_spaces():
    for i in range(len(spaces)):
        for j in range(len(spaces[i])):
            if spaces[i][j] != False:
                spaces[i][j].plot((i*Block.block_size+spaces_window_x), (j*Block.block_size+spaces_window_y))
       
       
def check_spaces():
    count = 0
    for i in range(20):
        for j in range(10):
            if spaces[j][i] == False or type(spaces[j][i]) == Brick:
                print("opening at: ", j, ", ", i)
                break
            if j == 9:
                print("line", i, "complete")
                global score
                score += 10 + 5*count
                count += 1
                if count == 4:
                    global show_wow_sprite
                    show_wow_sprite = True
                    global wow_message
                    pygame.time.set_timer(wow_message, 2000)
                for k in range(10):
                    spaces[k][i] = False
                shift_blocks_down(i)
                   
def shift_blocks_down(lineNum):
    for i in range(lineNum-1, -1, -1):
        for j in range(10):
            if spaces[j][i] != False:
                spaces[j][i].translate(down)
           
             
def display_message(x, y, message, size, color):
    font = pygame.font.Font('freesansbold.ttf', size)
    textBody = font.render(str(message), True, color)
    textRect = textBody.get_rect()
    textRect.center = (x, y)
    gameDisplay.blit(textBody, textRect)
   
   
def refresh_background():
    pygame.draw.rect(gameDisplay, white, [0, 0, window_width, window_height])
   
    pygame.draw.rect(gameDisplay, black, [spaces_window_x-10, spaces_window_y-10, 10*Block.block_size+20, 20*Block.block_size+20])
    pygame.draw.rect(gameDisplay, white, [spaces_window_x, spaces_window_y, 10*Block.block_size, 20*Block.block_size])
   
    pygame.draw.rect(gameDisplay, black, [preview_x - 5, preview_y - 5, 4*Block.block_size+10, 4*Block.block_size+10])
    pygame.draw.rect(gameDisplay, white, [preview_x, preview_y, 4*Block.block_size, 4*Block.block_size])
    display_message(585, preview_y - 30, "Next:", 25, black)
    for block in next_preview:
        block.plot(block.space_x, block.space_y)
       
    display_message(582, 195, "Level: " + str(brick_health//10), 25, black)
   
    gameDisplay.blit(score_sprite, (525, 70))
   
    display_message(582, 140, score, 25, black)
   
    global show_wow_sprite
    if show_wow_sprite:
        gameDisplay.blit(wow_sprite, (500, 450))


def set_bricks(health):
    for i in range(5, 20):
        for j in range(10):
            if spaces[j][i] == False:
                rando = random.randint(0, 30)
                print("rando = ", rando)
                if rando == 0:
                    Brick(j, i, random.randint(1, health))

def choose_next_piece():
    global next_piece
    global recent_pieces
    global next_preview
    next_piece = random.randint(0, 6)
    print("picking", next_piece)
    recent_pieces_placeholder = [recent_pieces[0], recent_pieces[1]]
   
    while next_piece in recent_pieces_placeholder:
        recent_pieces_placeholder.remove(next_piece)
        next_piece = random.randint(0, 6)
        print("repicking to", next_piece)
   
    recent_pieces[0] = recent_pieces[1]
    recent_pieces[1] = next_piece
    print("next_piece chosen:", next_piece)
   
    if next_piece == 0: #T tetromino
        print("previewing T tetromino")
        next_preview[0] = Block(preview_x + 0*Block.block_size, preview_y + 1*Block.block_size, green)        
        next_preview[1] = Block(preview_x + 1*Block.block_size, preview_y + 1*Block.block_size, green)
        next_preview[2] = Block(preview_x + 2*Block.block_size, preview_y + 1*Block.block_size, green)
        next_preview[3] = Block(preview_x + 1*Block.block_size, preview_y + 2*Block.block_size, green)
    elif next_piece == 1: #L tetromino
        print("previewing L tetromino")
        next_preview[0] = Block(preview_x + 1*Block.block_size, preview_y + 0*Block.block_size, yellow)        
        next_preview[1] = Block(preview_x + 1*Block.block_size, preview_y + 1*Block.block_size, yellow)    
        next_preview[2] = Block(preview_x + 1*Block.block_size, preview_y + 2*Block.block_size, yellow)    
        next_preview[3] = Block(preview_x + 2*Block.block_size, preview_y + 2*Block.block_size, yellow)    
    elif next_piece == 2: #long tetromino
        print("previewing long tetromino")
        next_preview[0] = Block(preview_x + 0*Block.block_size, preview_y + 1*Block.block_size, red)        
        next_preview[1] = Block(preview_x + 1*Block.block_size, preview_y + 1*Block.block_size, red)
        next_preview[2] = Block(preview_x + 2*Block.block_size, preview_y + 1*Block.block_size, red)
        next_preview[3] = Block(preview_x + 3*Block.block_size, preview_y + 1*Block.block_size, red)
    elif next_piece == 3: #Z tetromino
        print("previewing Z tetromino")
        next_preview[0] = Block(preview_x + 0*Block.block_size, preview_y + 1*Block.block_size, purple)      
        next_preview[1] = Block(preview_x + 1*Block.block_size, preview_y + 1*Block.block_size, purple)
        next_preview[2] = Block(preview_x + 1*Block.block_size, preview_y + 2*Block.block_size, purple)
        next_preview[3] = Block(preview_x + 2*Block.block_size, preview_y + 2*Block.block_size, purple)
    elif next_piece == 4: #backwards L tetromino
        print("previewing backwards L tetromino")
        next_preview[0] = Block(preview_x + 1*Block.block_size, preview_y + 0*Block.block_size, blue)    
        next_preview[1] = Block(preview_x + 1*Block.block_size, preview_y + 1*Block.block_size, blue)
        next_preview[2] = Block(preview_x + 1*Block.block_size, preview_y + 2*Block.block_size, blue)
        next_preview[3] = Block(preview_x + 2*Block.block_size, preview_y + 0*Block.block_size, blue)
    elif next_piece == 5: #backwards Z tetromino
        print("previewing backwards Z tetromino")
        next_preview[0] = Block(preview_x + 0*Block.block_size, preview_y + 2*Block.block_size, orange)
        next_preview[1] = Block(preview_x + 1*Block.block_size, preview_y + 1*Block.block_size, orange)
        next_preview[2] = Block(preview_x + 1*Block.block_size, preview_y + 2*Block.block_size, orange)
        next_preview[3] = Block(preview_x + 2*Block.block_size, preview_y + 1*Block.block_size, orange)
    else: #square tetromino
        print("previewing square tetromino")
        next_preview[0] = Block(preview_x + 1*Block.block_size, preview_y + 1*Block.block_size, teal)  
        next_preview[1] = Block(preview_x + 1*Block.block_size, preview_y + 2*Block.block_size, teal)
        next_preview[2] = Block(preview_x + 2*Block.block_size, preview_y + 1*Block.block_size, teal)
        next_preview[3] = Block(preview_x + 2*Block.block_size, preview_y + 2*Block.block_size, teal)
   


def pause():
    print("Game paused")
    pygame.draw.rect(gameDisplay, white, [0, 0, window_width, window_height])
    display_message(window_width//2, window_height//2, "PAUSED", 40, black)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE):
                print("Game unpaused")
                return False
            elif event.type == pygame.QUIT:
                return True

def game_loop():
    global next_piece
    global brick_health
    brick_health = 10
   
    drop = pygame.USEREVENT+1
    drop_timer = 1000
    pygame.time.set_timer(drop, drop_timer)
   
   
    gameExit = False
    choose_next_piece()
    t1 = Tetromino(4, 0, next_piece)
    choose_next_piece()
   
    while (gameExit == False):
        if t1.set:
            t1 = Tetromino(4, 0, next_piece)
            choose_next_piece()
            if t1.game_over == True:
                gameExit = True
       
        #do stuff
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                mouse_x -= spaces_window_x
                mouse_x //= Block.block_size
                mouse_y -= spaces_window_y
                mouse_y //= Block.block_size
                print(f"clicked at {mouse_x}, {mouse_y}")
                if mouse_x < 10 and mouse_y < 20 and type(spaces[mouse_x][mouse_y]) == Brick:
                    spaces[mouse_x][mouse_y].bonk()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gameExit = pause()
                elif event.key == pygame.K_d:
                    if t1.can_translate(right):
                        t1.translate(right)
                elif event.key == pygame.K_a:
                    if t1.can_translate(left):
                        t1.translate(left)
                elif event.key == pygame.K_s:
                    if t1.can_translate(down):
                        t1.translate(down)
                elif event.key == pygame.K_q:
                    if t1.can_rotate_left():
                        t1.rotate_left()
                elif event.key == pygame.K_e:
                    if t1.can_rotate_right():
                        t1.rotate_right()
            elif event.type == drop:
                if t1.can_translate(down):
                    t1.translate(down)
                else:
                    t1.set = True
            elif event.type == wow_message:
                global show_wow_sprite
                show_wow_sprite = False
               
        if t1.set:
            print("setting bricks")
            brick_health += 1
            set_bricks(brick_health//10)
            drop_timer -= 10
            if drop_timer <= 0:
                drop_timer = 5
            pygame.time.set_timer(drop, drop_timer)
           
            print("checking lines")
            check_spaces()
       
        refresh_background()
        render_spaces()
        pygame.display.update()
        clock.tick(60)

game_loop()
print("exiting loop")
pygame.draw.rect(gameDisplay, white, [0, 0, window_width, window_height])
gameDisplay.blit(game_over_sprite, (150, 100))
gameDisplay.blit(score_sprite, (350, 10))
display_message(405, 80, score, 25, black)

display_message(405, 650, "Great game!  Press any button to close", 35, black)
pygame.display.update()

pygame.time.delay(1500)
pygame.event.get()

stay = True
while stay:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.QUIT:
            stay = False
           
pygame.quit()