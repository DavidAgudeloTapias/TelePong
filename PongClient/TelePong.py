import pygame
pygame.init() # Initialize the things we gonna need

# Las variables al estar en mayúsculas se consideran como constantes que no cambiarán
WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

FPS = 60

WHITE = (255,255,255)
BLACK= (0,0,0)

PADDLE_HEIGHT, PADDLE_WIDTH = 100, 20

# This class will let us create both paddñes of the gamers
class Paddle:
    COLOR = WHITE
    def __init__(self, x, y, widht, height):
        self.x = x
        self.y = y
        self.width = widht
        self.height = height
    
    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))


def draw(win, paddles):
    win.fill(BLACK)

    for paddle in paddles: # Take both paddles to draw them in the window
        paddle.draw(win)

    pygame.display.update() # Update constantly the display to the color


# Event or main loop that display the window and draw something on it
def main():
    run = True # Flag to let the game to run
    
    clock = pygame.time.Clock()
    
    leftPaddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    rightPaddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)

    while run:
        clock.tick(FPS) # Maximum ticks or frames per second that the screen will show
        draw(WIN, [leftPaddle, rightPaddle])
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # If you press close button ...
                run = False
                break
    pygame.quit()

if __name__ == '__main__':
    main()