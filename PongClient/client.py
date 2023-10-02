import socket 
import constants

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

def main():
    print('client')
    client_socket.connect(("127.0.0.1",constants.PORT))
    local = client_socket.getsockname()

    print("Coneted from: ", local)

    to_send = input() # aqui se podria crear un arreglo con la informacion

    while to_send != constants.QUIT: 
        if to_send == '':

            print("Invalid comand")

            to_send = input()

        elif to_send == constants.DATA: 

            data_send = input('Input wjat you want: ')

            command_and_data = to_send + ' ' + data_send

            client_socket.send(bytes(command_and_data,constants.ENCONDING_FORMAT))

            recived = client_socket.recv(constants.RECV_BUFFER_SIZE)

            print(recived.decode(constants.ENCONDING_FORMAT))

            to_send = input()

        else:

            client_socket.send(bytes(to_send,constants.ENCONDING_FORMAT))

            recived = client_socket.recv(constants.RECV_BUFFER_SIZE)

            print(recived.decode(constants.ENCONDING_FORMAT))

            to_send = input()
    
    client_socket.send(bytes(to_send,constants.ENCONDING_FORMAT))

    recived = client_socket.recv(constants.RECV_BUFFER_SIZE)

    print(recived.decode(constants.ENCONDING_FORMAT))

    to_send = input()

    client_socket.close()

if __name__ == '__main__':
    main()