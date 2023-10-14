#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <time.h>
#include <pthread.h>

#define BUFFER_SIZE 1024

FILE *logfd;

typedef struct
{
    int x_vel;
    int y_vel;
    int x;
    int y;
    int radius;
    int MAX_VEL;
    int puntuacion_1;
    int puntuacion_2;
} Ball;

void moveBall(Ball *ball)
{
    ball->x += ball->x_vel;
    ball->y += ball->y_vel;
}

void resetBall(Ball *ball)
{
    ball->x = 350;
    ball->y = 250;
    ball->x_vel = -(ball->x_vel);
    ball->y_vel = 0;
}

void score(Ball *ball)
{
    if (ball->x < 0)
    {
        resetBall(ball);
        ball->puntuacion_2 += 1;
    }
    if (ball->x >= 700)
    {
        resetBall(ball);
        ball->puntuacion_1 += 1;
    }
}

typedef struct
{
    int x;
    int y;
    int width;
    int height;
    int VEL;
    int dir_y;
} Paddle;

void movePaddle(Paddle *paddle)
{
    paddle->y += paddle->dir_y;
    if (paddle->y - paddle->VEL >= 0)
    {
        paddle->y -= paddle->VEL;
    }
    if (paddle->y + paddle->VEL + paddle->height <= 500)
    {
        paddle->y += paddle->VEL;
    }
}

void handle_collision(Ball *ball, Paddle *leftPaddle, Paddle *rightPaddle) {
    // Verificar colisiones con los bordes superior e inferior
    if (ball->y + ball->radius >= 500)
    {
        ball->y_vel *= -1;
    }
    else if (ball->y - ball->radius <= 0)
    {
        ball->y_vel *= -1;
    }

    // Verificar colisiones con las paletas
    if (ball->x_vel < 0)
    {  // Movimiento hacia la izquierda
        if (ball->y >= leftPaddle->y && ball->y <= leftPaddle->y + leftPaddle->height)
        {
            if (ball->x - ball->radius <= leftPaddle->x + leftPaddle->width)
            {
                ball->x_vel *= -1;

                int middle_y = leftPaddle->y + leftPaddle->height / 2;
                int difference_in_y = middle_y - ball->y;
                int reduction_factor = (leftPaddle->height / 2) / ball->MAX_VEL;
                int y_vel = difference_in_y / reduction_factor;
                ball->y_vel = -y_vel;
            }
        }
    }
    else
    {  // Movimiento hacia la derecha
        if (ball->y >= rightPaddle->y && ball->y <= rightPaddle->y + rightPaddle->height)
        {
            if (ball->x + ball->radius >= rightPaddle->x)
            {
                ball->x_vel *= -1;

                int middle_y = rightPaddle->y + rightPaddle->height / 2;
                int difference_in_y = middle_y - ball->y;
                int reduction_factor = (rightPaddle->height / 2) / ball->MAX_VEL;
                int y_vel = difference_in_y / reduction_factor;
                ball->y_vel = -y_vel;
            }
        }
    }
}

int find_client_index(struct sockaddr_in *clientAddrs, struct sockaddr_in client)
{
    for (int i = 0; i < 2; i++)
    {
        if (clientAddrs[i].sin_addr.s_addr == client.sin_addr.s_addr && clientAddrs[i].sin_port == client.sin_port)
        {
            return i;
        }
    }
    return -1;
}

void log_info(const char *message)
{
    fprintf(logfd, "[INFO] %s\n", message);
    fflush(logfd);
}

void log_error(const char *message)
{
    fprintf(logfd, "[ERROR] %s\n", message);
    fflush(logfd);
}

typedef struct
{
    int sockfd;
    struct sockaddr_in serverAddr, clientAddr, clientAddrs[2];
    int addr_size;

} GameThreadArgs;

void *handle_game(void *arg)
{
    GameThreadArgs *args = (GameThreadArgs *)arg;
    char start_msg[] = "START";
    for (int i = 0; i < 2; i++)
    {
        sendto(args->sockfd, start_msg, strlen(start_msg), 0, (struct sockaddr *)&args->clientAddrs[i], args->addr_size);
    }

    printf("Todos los clientes están conectados...\n");
    log_info("Todos los clientes están conectados...\n");

    Ball ball;

    ball.x = 350;
    ball.y = 250;
    ball.radius = 7;
    ball.x_vel = 5;
    ball.y_vel = 0;
    ball.MAX_VEL = 5;

    ball.puntuacion_1 = 0;
    ball.puntuacion_2 = 0;



    Paddle leftPaddle, rightPaddle;

    leftPaddle.x = 10;
    leftPaddle.y = 200;
    leftPaddle.height = 100;
    leftPaddle.width = 20;
    leftPaddle.VEL = 4;
    leftPaddle.dir_y = 0;

    rightPaddle.x = 670;
    rightPaddle.y = 200;
    rightPaddle.height = 100;
    rightPaddle.width = 20;
    rightPaddle.VEL = 4;
    rightPaddle.dir_y = 0;

    char buffer[BUFFER_SIZE];

    while (1)
    {
        int bytesReceived = recvfrom(args->sockfd, buffer, BUFFER_SIZE, 0, (struct sockaddr *)&args->clientAddr, &args->addr_size); //Escuchar los clientes del juego al que está asociado el hilo 
        if (bytesReceived > 0) // Si recibió algún mensaje
        {
            buffer[bytesReceived] = '\0'; //Cinvertir el mensaje a string

            int sendingClientIndex = find_client_index(args->clientAddrs, args->clientAddr); //Detectar qué  cliente fue el que envió
            char logMessage[256];
            sprintf(logMessage, "El cliente %d envía: %d.\n", sendingClientIndex, atoi(buffer));
            printf(logMessage);
            log_info(logMessage);

            if (sendingClientIndex == 0)
            {
                leftPaddle.dir_y = atoi(buffer);
            }
            else if (sendingClientIndex == 1)
            {
                rightPaddle.dir_y = atoi(buffer);
            }

            moveBall(&ball);
            score(&ball);
            movePaddle(&leftPaddle);
            movePaddle(&rightPaddle);
            handle_collision(&ball, &leftPaddle, &rightPaddle);

            // Reenviando datos a ambos clientes
            for (int clientIndex = 0; clientIndex < 2; clientIndex++)
            {
                char tempBuffer2[256];
                sprintf(tempBuffer2, "%d %d %d %d %d %d", ball.x, ball.y, leftPaddle.y, rightPaddle.y, ball.puntuacion_1, ball.puntuacion_2);
                sendto(args->sockfd, tempBuffer2, strlen(tempBuffer2), 0, (struct sockaddr *)&args->clientAddrs[clientIndex], args->addr_size);
            }
        }
    }
}

int main(int argc, char *argv[])
{
    if (argc != 3)
    {
        fprintf(stderr, "Uso: %s <PORT> <Log File>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    int port = atoi(argv[1]);
    char *logFile = argv[2];

    logfd = fopen(logFile, "a");
    if (logfd == NULL)
    {
        perror("Error al abrir el archivo de log");
        exit(EXIT_FAILURE);
    }

    int sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd < 0)
    {
        perror("socket creation failed");
        exit(EXIT_FAILURE);
    }

    struct sockaddr_in serverAddr;
    memset(&serverAddr, 0, sizeof(serverAddr));
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(port);
    serverAddr.sin_addr.s_addr = INADDR_ANY;

    if (bind(sockfd, (struct sockaddr *)&serverAddr, sizeof(serverAddr)) < 0)
    {
        perror("Error al enlazar");
        close(sockfd);
        exit(1);
    }

    printf("Esperando a que se conecten los clientes...\n");

    struct sockaddr_in clientAddr;
    socklen_t addr_size = sizeof(clientAddr);
    struct sockaddr_in clientAddrs[2];

    char buffer[BUFFER_SIZE];

    while (1)
    {
        int connected_clients = 0;
        while (connected_clients < 2)
        {
            int bytesReceived = recvfrom(sockfd, buffer, BUFFER_SIZE, 0, (struct sockaddr *)&clientAddr, &addr_size);
            if (bytesReceived > 0)
            {
                buffer[bytesReceived] = '\0';
                if (strcmp(buffer, "CONNECT") == 0 && find_client_index(clientAddrs, clientAddr) == -1)
                {
                    clientAddrs[connected_clients] = clientAddr;
                    connected_clients++;
                    printf("Cliente %d conectado desde %s:%d\n", connected_clients, inet_ntoa(clientAddr.sin_addr), ntohs(clientAddr.sin_port));
                    char log_message[256];
                    sprintf(log_message, "Cliente %d conectado desde %s:%d", connected_clients, inet_ntoa(clientAddr.sin_addr), ntohs(clientAddr.sin_port));
                    log_info(log_message);
                }
            }
        }

        if (connected_clients == 2)
        {
            pthread_t game_thread;
            GameThreadArgs *args = malloc(sizeof(GameThreadArgs));
            memcpy(args->clientAddrs, clientAddrs, sizeof(clientAddrs));
            args->sockfd = sockfd;
            args->addr_size = sizeof(clientAddrs[0]);
            pthread_create(&game_thread, NULL, handle_game, (void *)args);
            pthread_detach(game_thread);
        }
    }

    close(sockfd);
    return 0;
}