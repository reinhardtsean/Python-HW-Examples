# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_pos = []
ball_vel = []
paddle1_pos =  []
paddle1_vel = []
paddle2_pos =  []
paddle2_vel = []
P1_Score = 0
P2_Score = 0


# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    
    global ball_pos, ball_vel, LEFT, RIGHT # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    if direction == "right":
        ball_vel = [random.randrange(120,240)/60.0,-random.randrange(60,120)/60.0]
        LEFT = False
        RIGHT = True
    else:
        ball_vel = [-random.randrange(120,240)/60.0,-random.randrange(60,120)/60.0]
        LEFT = True
        RIGHT = False
        
  

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global P1_Score, P2_Score  # these are ints
    
    P1_Score = 0
    P2_Score = 0
    LR = random.randint(0,1)
    if LR == 1:
        spawn_ball("right")
    else:
        spawn_ball("left")
    paddle1_pos = [HALF_PAD_WIDTH, HEIGHT / 2]
    paddle1_vel = [0,0]
    paddle2_pos = [WIDTH - HALF_PAD_WIDTH, HEIGHT / 2]
    paddle2_vel = [0,0] 

def VEdgeCheck(side):
    global ball_vel, P1_Score, P2_Score
    if side == 'left':
        if ball_pos[1] > paddle1_pos[1] - HALF_PAD_HEIGHT and ball_pos[1] < paddle1_pos[1] + HALF_PAD_HEIGHT:
            # Reflect ball
            ball_vel[0] = ball_vel[0]*-1.1
            ball_vel[1] = ball_vel[1]*1.1
        else:
            P2_Score +=1
            spawn_ball("right")

    elif side == 'right':
        if ball_pos[1] > paddle2_pos[1] - HALF_PAD_HEIGHT and ball_pos[1] < paddle2_pos[1] + HALF_PAD_HEIGHT:
            # Reflect ball
            ball_vel[0] = ball_vel[0]*-1.1
            ball_vel[1] = ball_vel[1]*1.1
        else:
            P1_Score +=1
            spawn_ball("left")     

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    #Reflect off Floor and Ceiling
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT-BALL_RADIUS:
        ball_vel[1] = ball_vel[1]*-1
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "white", "white")
    
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_vel[1] < 0 and paddle1_pos[1] > HALF_PAD_HEIGHT:
        paddle1_pos[1] += paddle1_vel[1]
    elif paddle1_vel[1] > 0 and paddle1_pos[1] < HEIGHT-HALF_PAD_HEIGHT:
        paddle1_pos[1] += paddle1_vel[1]
    
    if paddle2_vel[1] < 0 and paddle2_pos[1] > HALF_PAD_HEIGHT:
        paddle2_pos[1] += paddle2_vel[1]
    elif paddle2_vel[1] > 0 and paddle2_pos[1] < HEIGHT-HALF_PAD_HEIGHT:
        paddle2_pos[1] += paddle2_vel[1]
    
    
    # draw paddles
    canvas.draw_polygon([[paddle1_pos[0] - HALF_PAD_WIDTH, 
                          paddle1_pos[1] -  HALF_PAD_HEIGHT],
                         [paddle1_pos[0] - HALF_PAD_WIDTH,
                          paddle1_pos[1] +  HALF_PAD_HEIGHT],
                          [paddle1_pos[0] + HALF_PAD_WIDTH, 
                          paddle1_pos[1] +  HALF_PAD_HEIGHT],
                         [paddle1_pos[0] + HALF_PAD_WIDTH,
                          paddle1_pos[1] -  HALF_PAD_HEIGHT]]
                          , 1, 'Red', 'Red')
    
    canvas.draw_polygon([[paddle2_pos[0] - HALF_PAD_WIDTH, 
                          paddle2_pos[1] -  HALF_PAD_HEIGHT],
                         [paddle2_pos[0] - HALF_PAD_WIDTH,
                          paddle2_pos[1] +  HALF_PAD_HEIGHT],
                          [paddle2_pos[0] + HALF_PAD_WIDTH, 
                          paddle2_pos[1] +  HALF_PAD_HEIGHT],
                         [paddle2_pos[0] + HALF_PAD_WIDTH,
                          paddle2_pos[1] -  HALF_PAD_HEIGHT]]
                        , 1, 'Blue', 'Blue')
    
    
    # Handle Vertical Edge
    if ball_pos[0] <= PAD_WIDTH + BALL_RADIUS:
        VEdgeCheck('left')
    elif ball_pos[0] >= WIDTH-PAD_WIDTH - BALL_RADIUS:
        VEdgeCheck('right')
    
    # draw scores
    canvas.draw_text("Player1: "+str(P1_Score), (PAD_WIDTH+2, 12), 16, 'Red')
    canvas.draw_text("Player2: "+str(P2_Score), (WIDTH-85, 12), 16, 'Blue')
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel[1] = -3
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel[1] = 3
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel[1] = -3
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel[1] = 3        
        
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel[1] = 0
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel[1] = 0
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel[1] = 0
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel[1] = 0       

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
reset_button = frame.add_button('Reset',new_game,100)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


# start frame
new_game()
frame.start()

