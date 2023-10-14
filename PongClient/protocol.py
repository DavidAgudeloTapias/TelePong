import socket
import constants

def createSocket():
    socketCliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socketCliente.sendto("CONNECT".encode(), (constants.SERVER_IP, constants.SERVER_PORT))
    print("Conectado al servidor")
    return socketCliente

def escucharMensajeJuego(socketCliente):
    data, _ = socketCliente.recvfrom(constants.BUFFER_SIZE)
    if data:
        data = data.decode()
    return data

def sendToServer(socketCliente, current_movement):
    socketCliente.sendto(current_movement.encode(), (constants.SERVER_IP, constants.SERVER_PORT))

def closeSocket(socketCliente):
    socketCliente.close()