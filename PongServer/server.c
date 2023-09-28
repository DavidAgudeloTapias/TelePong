#include <stdio.h>
#include <netdb.h>
#include <netinet/in.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <pthread.h>
#include <unistd.h>

void function(int connection_fd){
    int n;
    char buff[n];
    while (1) 
    {
        bzero(buff,n);

        char remote[] = read(connection_fd,buff,sizeof(buff));

        char commanLine[] = *strtok(remote, ' ');

        char command = commanLine[0];

        /*if (command == 'hello'){
            send(connection_fd, buff, );
        }*/
    }
}

void main(){
    int socket_fd, connection_fd, len;

    struct sockaddr_in server_address , client;

    pthread_t thread;

    //creamos y verificamos el socket
    socket_fd = socket(AF_INET,SOCK_STREAM,0);
    if(socket_fd == -1){
        printf("Socket fail");
        exit(0);
    }
    else{
        printf("Socket succes");
    }

    bzero(&server_address,sizeof(server_address));
    
    server_address.sin_family = AF_INET;
    server_address.sin_addr.s_addr = htonl(INADDR_ANY);
    server_address.sin_port = htonl(10); // port es una de las cosntantes

    if((bind(socket_fd, (struct sockaddr*)&server_address, sizeof(server_address))) != 0){
        printf("Bind fail");
        exit(0);
    }
    else{
        printf("Bind success");
    }

    if (listen(socket_fd,5) != 0){
        printf("Failed to listen");
        exit(0);
    }
    else{
        printf("listening");
    }

    len = sizeof(client);

    //while (1){ este ciclo esta para los threads pero no estoy seguro de como crearlos
        connection_fd = accept(socket_fd, (struct sockaddr*)&client, &len);
        if (connection_fd < 0){
            printf("accept fail");
            exit(0);
        }
        else{
            printf("Accept client");
        }
        
    //}

    // lamar funcion 

    close(socket_fd);

}