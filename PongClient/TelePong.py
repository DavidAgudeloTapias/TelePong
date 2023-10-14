import pygame
import constants
import protocol
import threading

pygame.init() # Initialize the things we gonna need
pygame.display.set_caption("Pong")

WIN = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))

SCORE_FONT = pygame.font.SysFont("comicsans", 50)
WINNING_SCORE = 3

comenzarJuego = False # Flag to know if both players are conected
run = True # Flag to let the game to run
leftScore = 0
rightScore = 0

# This class will let us create both paddles of the gamers
class Paddle:
    COLOR = constants.WHITE
    VEL = 4

    def __init__(self):
        self.x = self.original_x = 0
        self.y = self.original_y = constants.HEIGHT//2 - constants.PADDLE_HEIGHT//2
        self.width = constants.PADDLE_WIDTH
        self.height = constants.PADDLE_HEIGHT

    def drawing(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))


# This class will let us create the ball
class Ball:
    MAX_VEL = 5
    COLOR = constants.WHITE

    def __init__(self):
        self.x = 350
        self.y = 250
        self.radius = constants.BALL_RADIUS
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def drawing(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)


# Create both paddles and the ball this way, to access them in the necessary methods

leftPaddle = Paddle()
leftPaddle.x = 10
rightPaddle = Paddle()
rightPaddle.x = constants.WIDTH - 10 - constants.PADDLE_WIDTH
ball = Ball()


def actualizarPosicionesPantalla():
    WIN.fill(constants.BLACK)

    leftScoreText = SCORE_FONT.render(f"{leftScore}", 1, constants.WHITE)
    rightScoreText = SCORE_FONT.render(f"{rightScore}", 1, constants.WHITE)
    WIN.blit(leftScoreText, (constants.WIDTH//4 - leftScoreText.get_width()//2, 20))
    WIN.blit(rightScoreText, (constants.WIDTH * (3/4) - rightScoreText.get_width()//2, 20))

    leftPaddle.drawing(WIN)
    rightPaddle.drawing(WIN)
    ball.drawing(WIN)

    for i in range(10, constants.HEIGHT, constants.HEIGHT//20):
        if i%2 == 1:
            continue
        pygame.draw.rect(WIN, constants.WHITE, (constants.WIDTH//2 - 5, i, 10, constants.HEIGHT//20))

    pygame.display.update() # Update constantly the display to the color


def escucharMensajeServidor(socketCliente):
    global comenzarJuego
    global leftScore
    global rightScore
    while True:
        data = protocol.escucharMensajeJuego(socketCliente)
        if data == "START":
            comenzarJuego = True
            print("Los 2 jugadores ahora pueden jugar")
        else:
            data = data.split()
            ball.x, ball.y, leftPaddle.y, rightPaddle.y, leftScore, rightScore = map(int, data)

            print(f"BolaDirX: {ball.x} - BolaDirY: {ball.y} - PaletaIzqDirY: {leftPaddle.y} - PaletaIzqDirY: {rightPaddle.y} - MarcadorIzq: {leftScore} - MarcadorDer: {rightScore}")

        if not run:
            break
        actualizarPosicionesPantalla()


def mostrarMensaje(mensaje, y_offset = 0):
    superficieTexto = SCORE_FONT.render(mensaje, True, constants.WHITE)
    rectanguloTexto = superficieTexto.get_rect(center=(350, 250 + y_offset))
    WIN.blit(superficieTexto, rectanguloTexto)
    pygame.display.update()


# Event or main loop that display the window and draw something on it
def main():
    # Socket of each player is being created
    socketCliente = protocol.createSocket()

    # Thread of each pair of players is being created
    hiloJuego = threading.Thread(target=escucharMensajeServidor, args=(socketCliente,))
    hiloJuego.daemon = True
    hiloJuego.start()

    WIN.fill(constants.BLACK)
    mostrarMensaje("Bienvenido a Pong", -20)
    mostrarMensaje("Esperando por otro jugador", 20)

    while not comenzarJuego:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

    global run
    clock = pygame.time.Clock()
    current_movement = "0"

    while run:
        actualizarPosicionesPantalla()
        
        if leftScore == 3 or rightScore == 3:
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    current_movement = "-4"
                if event.key == pygame.K_s:
                    current_movement = "4"

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    current_movement = "0"

        protocol.sendToServer(socketCliente, current_movement)

        pygame.display.flip()
        clock.tick(constants.FPS)

    WIN.fill(constants.BLACK)
    if leftScore == 3:
        mostrarMensaje("Jugador izquierda gana", -20)
        pygame.time.wait(3000)
        pygame.display.update()
    else:
        mostrarMensaje("Jugador derecha gana", -20)
        pygame.time.wait(3000)
        pygame.display.update()

    pygame.quit()
    protocol.closeSocket(socketCliente)

if __name__ == '__main__':
    main()