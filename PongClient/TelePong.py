import pygame
pygame.init() # Initialize the things we gonna need

# Variables being in uppercase are considered constants that will not change
WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

FPS = 60

WHITE = (255,255,255)
BLACK= (0,0,0)

PADDLE_HEIGHT, PADDLE_WIDTH = 100, 20
BALL_RADIUS = 7

# This class will let us create both paddles of the gamers
class Paddle:
    COLOR = WHITE
    VEL = 4

    def __init__(self, x, y, widht, height):
        self.x = x
        self.y = y
        self.width = widht
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

# This class will let us create the ball
class Ball:
    MAX_VEL = 5
    COLOR = WHITE

    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

def draw(win, paddles, ball):
    win.fill(BLACK)

    for paddle in paddles: # Take both paddles to draw them in the window
        paddle.draw(win)

    for i in range(10, HEIGHT, HEIGHT//20):
        if i%2 == 1:
            continue
        pygame.draw.rect(win, WHITE, (WIDTH//2 - 5, i, 10, HEIGHT//20))

    ball.draw(win)
    pygame.display.update() # Update constantly the display to the color


# Function that receive the keys that are pressed to make both paddles to move
def handle_paddle_movement(keys, leftPaddle, rightPaddle):
    if keys[pygame.K_w] and leftPaddle.y - leftPaddle.VEL >= 0:
        leftPaddle.move(up=True)
    if keys[pygame.K_s] and leftPaddle.y + leftPaddle.VEL + leftPaddle.height <= HEIGHT:
        leftPaddle.move(up=False)

    if keys[pygame.K_UP] and rightPaddle.y - rightPaddle.VEL >= 0:
        rightPaddle.move(up=True)
    if keys[pygame.K_DOWN] and rightPaddle.y + rightPaddle.VEL + rightPaddle.height <= HEIGHT:
        rightPaddle.move(up=False)


# Event or main loop that display the window and draw something on it
def main():
    run = True # Flag to let the game to run

    clock = pygame.time.Clock()

    leftPaddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    rightPaddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)

    ball = Ball(WIDTH//2, HEIGHT//2, BALL_RADIUS)

    while run:
        clock.tick(FPS) # Maximum ticks or frames per second that the screen will show
        draw(WIN, [leftPaddle, rightPaddle], ball)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # If you press close button ...
                run = False
                break

        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, leftPaddle, rightPaddle)

        ball.move()

    pygame.quit()

if __name__ == '__main__':
    main()