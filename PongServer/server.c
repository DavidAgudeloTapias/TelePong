#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define SERVER_PORT 8080
#define BUFFER_SIZE 1024
#define CLIENT_COUNT 2

typedef struct {
    int dir_x;
    int dir_y;
} Ball;

typedef struct {
    int dir_y;
} Paddle;

int find_client_index(struct sockaddr_in *clientAddrs, struct sockaddr_in client)
{
    for (int i = 0; i < CLIENT_COUNT; i++){
        if (clientAddrs[i].sin_addr.s_addr == client.sin_addr.s_addr &&
clientAddrs[i].sin_port == client.sin_port)
        {
            return i;
        }
    }
    return -1;
}

int main()
{
    int sockfd;
    char buffer[BUFFER_SIZE];
    struct sockaddr_in serverAddr, clientAddr, clientAddrs[CLIENT_COUNT];
    int connected_clients = 0;
    socklen_t addr_size = sizeof(struct sockaddr_in);

    memset(clientAddrs, 0, sizeof(clientAddrs));

    if ((sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0){
        perror("Error al crear el socket");
        exit(EXIT_FAILURE);
    }

    memset(&serverAddr, 0, sizeof(serverAddr));
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(SERVER_PORT);
    serverAddr.sin_addr.s_addr = INADDR_ANY;

    if (bind(sockfd, (struct sockaddr *)&serverAddr, sizeof(serverAddr)) < 0)
    {
        perror("Error al enlazar");
        close(sockfd);
        exit(1);
    }

    printf("Esperando a que se conecten los clientes...\n");

    while (connected_clients < CLIENT_COUNT)
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
            }
        }
    }

    char start_msg[] = "START";
    for (int i = 0; i < CLIENT_COUNT; i++) {
        sendto(sockfd, start_msg, strlen(start_msg), 0, (struct sockaddr *)&clientAddrs[i], addr_size);
    }

    printf("Todos los clientes están conectados...\n");

    char initial_msg[] = "5 5 0 0";
    for (int i = 0; i < CLIENT_COUNT; i++) {
        sendto(sockfd, initial_msg, strlen(initial_msg), 0, (struct sockaddr *)&clientAddrs[i], addr_size);
    }

    Ball ball;
    Paddle paddle_1, paddle_2;

    while (1)
    {
        int bytesReceived = recvfrom(sockfd, buffer, BUFFER_SIZE, 0, (struct sockaddr *)&clientAddr, &addr_size);
        if (bytesReceived > 0)
        {
            buffer[bytesReceived] = '\0';

            int sendingClientIndex = find_client_index(clientAddrs, clientAddr);

            // Extrayendo datos del mensaje
            sscanf(buffer, "%d %d %d %d", &ball.dir_x, &ball.dir_y, &paddle_1.dir_y, &paddle_2.dir_y);

            // Reenviando datos a ambos clientes
            for (int clientIndex = 0; clientIndex < CLIENT_COUNT; clientIndex++)
            {
                char tempBuffer[256];
                if(clientIndex == sendingClientIndex){
                    // Primer paleta es la del cliente que envió el mensaje, la segunda es la del oponente
                    sprintf(tempBuffer, "%d %d %d %d", ball.dir_x, ball.dir_y, paddle_1.dir_y, paddle_2.dir_y);
                } else {
                    // Primera paleta es la del oponente, la segunda es la del cliente que envió el mensaje
                    sprintf(tempBuffer, "%d %d %d %d", ball.dir_x, ball.dir_y, paddle_2.dir_y, paddle_1.dir_y);
                }
                sendto(sockfd, tempBuffer, strlen(tempBuffer), 0, (struct sockaddr *)&clientAddrs[clientIndex], addr_size);
            }
        }
    }

    close(sockfd);
    return 0;
}