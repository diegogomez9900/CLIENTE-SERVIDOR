import json, socket
import threading
import random
from threading import Thread
from time import sleep
from datetime import datetime
import time
import logging

JugadorTurno = 0               #aqui va el codigo del jugador que esta en turno, puede ser 0,1,2,3
Finnn = True
ListaMovs = []


#DEFNICION DE FUNCIONES

def listastring(lista):
    listaenviar = ','.join(str(v) for v in lista)
    return listaenviar

def stringlista(cadena):
    listaenviar = cadena.split(',')
    for e in range(len(listaenviar)):
        aux = listaenviar[e]
        listaenviar[e] = int(aux)
    return listaenviar

def getTurno():
    global JugadorTurno
    return str(JugadorTurno)

def setTurno(valor):
    global JugadorTurno
    JugadorTurno = valor

def aumentarTurno():
    global JugadorTurno
    JugadorTurno = JugadorTurno + 1
    if JugadorTurno > 3:
        JugadorTurno = 0

def getFin():
    global Finnn
    return Finnn

def setFin():
    global Finnn
    Finnn = not Finnn

def getListaMovs():
    global ListaMovs
    return ListaMovs

def setListaMovs(NewLM):
    global ListaMovs
    ListaMovs = NewLM

class Cliente(Thread):
    """
    Objeto hijo de la libreria Thread
    """

    def __init__(self, conn, addr, id):
        # Inicializar clase padre.
        Thread.__init__(self)
        self.conn = conn #Conexion
        self.addr = addr #Addres de la conexion
        self.id_cliente = int(id)
        self.fin = 1
        self.turnisius = getTurno()
        self.retraso = 0

    def run(self):
        while self.fin == 1:
            if self.retraso < 2:
                print "registrar cliente"
                self.recibir()
            else:
                if self.id_cliente == int(getTurno()):
                    # Recibir datos del cliente.
                    print "iguales"
                    self.recibir()

                else:
                    print getTurno()
                    print self.id_cliente
                    print ""
                    print "no iguales"
                    self.cambiar()

    def cambiar(self):
        nada = self.conn.recv(1000)
        if getTurno() == self.turnisius:
            self.turnisius = getTurno()
        else:
            self.turnisius = getTurno()
            self.conn.send("turno finito".encode("ascii"))
            algo = peticion = self.conn.recv(1000)
            numero = getTurno()
            self.conn.send(numero.encode("ascii"))

        if getListaMovs() != []:
            aux = getListaMovs()
            print aux
            ls = aux[0]
            print aux[0]
            setListaMovs(aux.remove(aux[0]))

            self.conn.send("actualizar ficha".encode("ascii"))
            algo = peticion = self.conn.recv(1000)
            self.conn.send(ls.encode("ascii"))

        if getListaMovs() == []:
            self.conn.send("no cambio".encode("ascii"))

    def recibir(self):
        peticion = ""
        peticion = self.conn.recv(1000)
        peticion = peticion.decode("ascii") # Decodifica la peticion en ascii
        peticion = str(peticion)
        print peticion


        if self.retraso < 2:
            self.retraso =self.retraso + 1
        else:
            self.retraso = 3


        if peticion == "Soy un cliente":
            print "mi id es: "
            print self.id_cliente
            enviar = str(self.id_cliente)
            self.conn.send(enviar.encode("ascii"))
        if peticion == "terminar":
            print "Hasta Luego..."
            self.fin = 0
            self.conn.send("ok".encode("ascii"))
            setFin()#cambia el valor del fin del ciclo principal cuando un cliente se desconecta
        if peticion == "get turno":
            print "El turno es: "
            m = getTurno()
            print m
            self.conn.send(m.encode("ascii"))

        if peticion == "turno finito":
            print "Ok, cambiando turno"
            aumentarTurno()

            self.conn.send("ok, cambiando".encode("ascii"))
            algo = self.conn.recv(1000)
            numero = getTurno()
            self.conn.send(numero.encode("ascii"))
            algo = self.conn.recv(1000)


        if peticion == "registrar movimientos":
            print "Indique tipo de movimiento"
            self.conn.send("Indique tipo de movimiento".encode("ascii"))
            peticion2 = self.conn.recv(1000)
            peticion2 = peticion2.decode("ascii") # Decodifica la peticion en ascii
            peticion2 = peticion2
            if peticion2 == "salida":
                print "El movimiento es salida"
                self.conn.send("Datos de ficha".encode("ascii"))
                listaR = self.conn.recv(1000)
                self.conn.send("ok".encode("ascii"))
                print listaR
                aux = listaR.decode("ascii") # Decodifica la peticion en ascii
                print listaR
                listaaux = getListaMovs()
                listaaux.append(listaR)
                setListaMovs(listaaux)

            if peticion2 == "mov 1":
                print "Movimiento de ficha"
                self.conn.send("Datos de ficha".encode("ascii"))
                listaR = self.conn.recv(1000)
                self.conn.send("ok".encode("ascii"))
                print listaR
                aux = listaR.decode("ascii") # Decodifica la peticion en ascii
                print listaR
                listaaux = getListaMovs()
                listaaux.append(listaR)
                setListaMovs(listaaux)


    def responder(self, res):
        try:
            self.conn.send(res.encode("ascii"))
        except socket.error:
            print "error en el socket"


if __name__ == "__main__":

    host = "localhost" # Direccion IP
    port = 8006 # Puerto de practica

    # Creacion del socket
    mi_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (host, port)
    # Bind a el puerto del socket
    mi_socket.bind(server_address)
    mi_socket.listen(4)#el numero determina la cantidad de clientes que se pueden conectar simultaneamente
    print("Escuchando...")
    # public_url = ngrok.connect(port, "tcp", options={"remote_addr": "{}:{}".format(host, port)})
    # print('ngrok tunnel "{}" -> "tcp://127.0.0.1:{}/"'.format(public_url, port))
    hilos = []  # Se crea una lista de hilos vacia
    v = 1
    setTurno(v-1)
    fin = getFin()

    while fin:
        connection = None
        try:
            conexion, addr = mi_socket.accept()
            print("Nueva conexion establecida", addr)
            c = Cliente(conn=conexion, addr=addr,id= v-1)
            c.start()
            hilos.append(c)
            v = v + 1
            if v > 4:
                v = 1
        except KeyboardInterrupt:
            print(" Shutting down server.")
            for e in hilos:
                e.join()
            connection.close()
            setFin()
            break
        fin = getFin()

    for e in hilos:
        e.join()
    connection.close()
    mi_socket.close()
