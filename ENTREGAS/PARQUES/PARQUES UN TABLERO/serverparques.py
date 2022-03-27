import json, socket
import threading
import random
from threading import Thread
from time import sleep
from datetime import datetime
import time
import logging

# PETICIONES DE SALIDA
class Cliente(Thread):
    """
    Objeto hijo de la libreria Thread
    """

    def __init__(self, conn, addr, id):
        # Inicializar clase padre.
        Thread.__init__(self)
        self.conn = conn #Conexion
        self.addr = addr #Addres de la conexion
        self.id_cliente = id
        self.fin = 1

    def run(self):
        while self.fin == 1:
            try:
                # Recibir datos del cliente.
                self.recibir()
            except SyntaxError:
                print "Error de lectura."

    def recibir(self):
        peticion = self.conn.recv(1000)
        peticion = peticion.decode("ascii") # Decodifica la peticion en ascii
        peticion = str(peticion)
        print peticion
        if peticion == "Soy un cliente":
            print "mi id es: "
            print self.id_cliente
            self.responder(str(self.id_cliente))
        if peticion == "deme un numero":
            print str(random.randrange(4))
            self.responder(str(random.randrange(4)))
        if peticion == "terminar":
            self.fin = 0
            self.responder("ok")


    def responder(self, res):
        try:
            self.conn.send(res.encode("ascii"))
        except socket.error:
            print "error en el socket"
            pass


if __name__ == "__main__":

    host = "localhost" # Direccion IP
    port = 8001 # Puerto de practica

    # Creacion del socket
    mi_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (host, port)
    # Bind a el puerto del socket creado
    mi_socket.bind(server_address)
    mi_socket.listen(4)#el numero determina la cantidad de clientes que se pueden conectar simultaneamente
    print("Escuchando...")
    # public_url = ngrok.connect(port, "tcp", options={"remote_addr": "{}:{}".format(host, port)})
    # print('ngrok tunnel "{}" -> "tcp://127.0.0.1:{}/"'.format(public_url, port))
    hilos = []  # Se crea una lista de hilos vacia
    v = 1
    fin = True

    while fin:
        connection = None
        try:
            conexion, addr = mi_socket.accept()
            print("Nueva conexion establecida", addr)
            c = Cliente(conn=conexion, addr=addr,id= v-1)
            c.start()
            print "\n"
            print v
            print "\n"
            hilos.append(c)
            v = v + 1
            if v > 4:
                v = 1
        except KeyboardInterrupt:
            print(" Shutting down server.")
            for e in hilos:
                e.join()
            connection.close()

            break

    for e in hilos:
        e.join()
    connection.close()
    mi_socket.close()
