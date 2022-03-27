import socket
import time

s = socket.socket()
s.connect(("localhost", 8001))
mensaje=input('ingresa tu nombre: ')

s.send(mensaje) #Se envia el mensaje

#se reciben los mensajes del serivodr por el puerto 1024
print(s.recv(1024))
print(s.recv(1024))
print(s.recv(1024))
print(s.recv(1024))
print(s.recv(1024))

s.close()
