import socket
import time
from datetime import datetime

def mes(m):
    if(m == 1):
        return "Enero"
    elif(m == 2):
        return "Febrero"
    elif(m == 3):
        return "Marzo"
    elif(m == 4):
        return "Abril"
    elif(m == 5):
        return "Mayo"
    elif(m == 6):
        return "Junio"
    elif(m == 7):
        return "Julio"
    elif(m == 8):
        return "Agosto"
    elif(m == 9):
        return "Septiembre"
    elif(m == 10):
        return "Octubre"
    elif(m == 11):
        return "Noviembre"
    elif(m == 12):
        return "Diciembre"


def ampm(h):
    if(h > 12):
        return [h-12, "PM"]
    else:
        return [h, "AM"]

if __name__ == '__main__':
    Mi_socket=socket.socket()
    Mi_socket.bind(("localhost", 8001))
    Mi_socket.listen(1)

    print ("Servidor iniciado")

    cli, addr=Mi_socket.accept()

    recibido = cli.recv(1024)# se recibe mensaje por el puerto 1024
    hora = datetime.now()
    am = ampm(hora.hour)
    print("conectado: "+recibido)

    cli.send("BIENVENIDO: "+recibido)
    cli.send("TE CONECTASTE DESDE: "+addr[0])
    cli.send("POR EL PUERTO: "+str(addr[1]))
    cli.send("FECHA: "+mes(hora.month)+" "+str(hora.day)+" de "+str(hora.year))
    cli.send("HORA: "+str(am[0])+" : "+str(hora.minute)+" "+am[1])

    cli.close()
    Mi_socket.close()
