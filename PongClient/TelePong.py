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

SCORE_FONT = pygame.font.SysFont("comicsans", 50)
WINNING_SCORE = 3

# This class will let us create both paddles of the gamers
class Paddle:
    COLOR = WHITE
    VEL = 4

    def __init__(self, x, y, widht, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = widht
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y

# This class will let us create the ball
class Ball:
    MAX_VEL = 5
    COLOR = WHITE

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1


# This method is the one that draw everything in the game window
def draw(win, paddles, ball, leftScore, rightScore):
    win.fill(BLACK)

    leftScoreText = SCORE_FONT.render(f"{leftScore}", 1, WHITE)
    rightScoreText = SCORE_FONT.render(f"{rightScore}", 1, WHITE)
    win.blit(leftScoreText, (WIDTH//4 - leftScoreText.get_width()//2, 20))
    win.blit(rightScoreText, (WIDTH * (3/4) - rightScoreText.get_width()//2, 20))

    for paddle in paddles: # Take both paddles to draw them in the window
        paddle.draw(win)

    for i in range(10, HEIGHT, HEIGHT//20):
        if i%2 == 1:
            continue
        pygame.draw.rect(win, WHITE, (WIDTH//2 - 5, i, 10, HEIGHT//20))

    ball.draw(win)
    pygame.display.update() # Update constantly the display to the color


# This method
def handle_collision(ball, leftPaddle, rightPaddle):
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    if ball.x_vel < 0:
        if ball.y >= leftPaddle.y and ball.y <= leftPaddle.y + leftPaddle.height:
            if ball.x - ball.radius <= leftPaddle.x + leftPaddle.width:
                ball.x_vel *= -1

                middle_y = leftPaddle.y + leftPaddle.height/2
                difference_in_y = middle_y - ball.y
                reduction_factor = (leftPaddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel
    else:
        if ball.y >= rightPaddle.y and ball.y <= rightPaddle.y + rightPaddle.height:
            if ball.x + ball.radius >= rightPaddle.x:
                ball.x_vel *= -1

                middle_y = rightPaddle.y + rightPaddle.height/2
                difference_in_y = middle_y - ball.y
                reduction_factor = (rightPaddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel


# Method that receive the keys that are pressed to make both paddles to move
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

    leftScore = 0
    rightScore = 0

    while run:
        clock.tick(FPS) # Maximum ticks or frames per second that the screen will show
        draw(WIN, [leftPaddle, rightPaddle], ball, leftScore, rightScore)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # If you press close button ...
                run = False
                break

        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, leftPaddle, rightPaddle)

        ball.move()

        handle_collision(ball, leftPaddle, rightPaddle)
        
        if ball.x < 0:
            rightScore += 1
            ball.reset()
        elif ball.x > WIDTH:
            leftScore += 1
            ball.reset()

        won = False
        if leftScore >= WINNING_SCORE:
            won = True
            win_text = "El ganador de la Izquierda ha ganado el juego"
        elif rightScore >= WINNING_SCORE:
            won = True
            win_text = "El ganador de la Derecha ha ganado el juego"

        if won:
            text = SCORE_FONT.render(win_text, 1, WHITE)
            WIN.blit(text, (WIDTH//2 - text.get_widht()//2, HEIGHT//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset()
            leftPaddle.reset()
            rightPaddle.reset()
            leftScore = 0
            rightScore = 0

    pygame.quit()

if __name__ == '__main__':
    main()