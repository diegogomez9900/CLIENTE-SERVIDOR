import zmq
import json
import os.path as path
import os

def aumentarTurno(JugadorTurno):
    JugadorTurno = JugadorTurno + 1
    if JugadorTurno > 3:
        JugadorTurno = 0
    return JugadorTurno

if __name__ == "__main__":

    context = zmq.Context()

    s1 = context.socket(zmq.REP)
    s2 = context.socket(zmq.REP)
    s3 = context.socket(zmq.REP)
    s4 = context.socket(zmq.REP)

    ROUTE1 = "tcp://*:8080"
    ROUTE2 = "tcp://*:8081"
    ROUTE3 = "tcp://*:8082"
    ROUTE4 = "tcp://*:8083"

    s1.bind(ROUTE1)
    s2.bind(ROUTE2)
    s3.bind(ROUTE3)
    s4.bind(ROUTE4)

    turno = 0 # si se quiere el turno aleatorio, hacer que esto sea igual a un random

    print('--- ESPERANDO SOLICITUD ---')
    Msg=s1.recv_string()
    s1.send_string("0")
    Msg=s1.recv_string()
    s1.send_string(str(turno))

    Msg=s2.recv_string()
    s2.send_string("1")
    Msg=s2.recv_string()
    s2.send_string(str(turno))

    Msg=s3.recv_string()
    s3.send_string("2")
    Msg=s3.recv_string()
    s3.send_string(str(turno))

    Msg=s4.recv_string()
    s4.send_string("3")
    Msg=s4.recv_string()
    s4.send_string(str(turno))



    if turno == 0:
        s = s1
    if turno == 1:
        s = s2
    if turno == 2:
        s = s3
    if turno == 3:
        s = s4

    while True: # Recibo de segmentacion

        #Imprime en pantalla los datos del comando
        funcion = s.recv_string()#Se recibe la funcion
        print("CLIENTE: ", turno+1)
        print("FUNCION RECIBIDA: ",funcion)
        if funcion == "nada":
            print("Ok, esperando")
            s.send_string("ok")
        if funcion == "registrar movimientos": # Funcion de subir
            print("registrando movimientos")
            s.send_string("necesito datos movimiento")

            idficha = s.recv_string()
            s.send_string("recibido")
            casillaficha = s.recv_string()
            s.send_string("recibido")
            casillasficha = s.recv_string()
            s.send_string("recibido")
            pasosficha = s.recv_string()
            s.send_string("recibido")
            posxficha = s.recv_string()
            s.send_string("recibido")
            posyficha = s.recv_string()
            s.send_string("recibido")
            player = s.recv_string()

            print("se recibe lo siguiente:")
            print(idficha,casillaficha,casillasficha,pasosficha,posxficha,posyficha,player)

            s.send_string("lista recibida")
            if turno == int(player):
                if turno == 0:
                    print("quien registra es el cliente 1")
                    algo = s2.recv_string()
                    s2.send_string("actualizar ficha")
                    algo = s2.recv_string()

                    ss = s2

                    ss.send_string(idficha)
                    something = ss.recv_string()
                    ss.send_string(casillaficha)
                    something = ss.recv_string()
                    ss.send_string(casillasficha)
                    something = ss.recv_string()
                    ss.send_string(pasosficha)
                    something = ss.recv_string()
                    ss.send_string(posxficha)
                    something = ss.recv_string()
                    ss.send_string(posyficha)
                    something = ss.recv_string()
                    ss.send_string(player)
                    #Fin de envio de partes de la lista recibida

                    algo = s3.recv_string()
                    s3.send_string("actualizar ficha")
                    algo = s3.recv_string()
                    ss = s3

                    ss.send_string(idficha)
                    something = ss.recv_string()
                    ss.send_string(casillaficha)
                    something = ss.recv_string()
                    ss.send_string(casillasficha)
                    something = ss.recv_string()
                    ss.send_string(pasosficha)
                    something = ss.recv_string()
                    ss.send_string(posxficha)
                    something = ss.recv_string()
                    ss.send_string(posyficha)
                    something = ss.recv_string()
                    ss.send_string(player)
                    #Fin de envio de partes de la lista recibida

                    algo = s4.recv_string()
                    s4.send_string("actualizar ficha")
                    algo = s4.recv_string()
                    ss = s4

                    ss.send_string(idficha)
                    something = ss.recv_string()
                    ss.send_string(casillaficha)
                    something = ss.recv_string()
                    ss.send_string(casillasficha)
                    something = ss.recv_string()
                    ss.send_string(pasosficha)
                    something = ss.recv_string()
                    ss.send_string(posxficha)
                    something = ss.recv_string()
                    ss.send_string(posyficha)
                    something = ss.recv_string()
                    ss.send_string(player)
                    #Fin de envio de partes de la lista recibida
                if turno == 1:
                    print("quien registra es el cliente 2")
                    algo = s1.recv_string()
                    s1.send_string("actualizar ficha")
                    algo = s1.recv_string()
                    ss = s1

                    ss.send_string(idficha)
                    something = ss.recv_string()
                    ss.send_string(casillaficha)
                    something = ss.recv_string()
                    ss.send_string(casillasficha)
                    something = ss.recv_string()
                    ss.send_string(pasosficha)
                    something = ss.recv_string()
                    ss.send_string(posxficha)
                    something = ss.recv_string()
                    ss.send_string(posyficha)
                    something = ss.recv_string()
                    ss.send_string(player)
                    #Fin de envio de partes de la lista recibida

                    algo = s3.recv_string()
                    s3.send_string("actualizar ficha")
                    algo = s3.recv_string()
                    ss = s3

                    ss.send_string(idficha)
                    something = ss.recv_string()
                    ss.send_string(casillaficha)
                    something = ss.recv_string()
                    ss.send_string(casillasficha)
                    something = ss.recv_string()
                    ss.send_string(pasosficha)
                    something = ss.recv_string()
                    ss.send_string(posxficha)
                    something = ss.recv_string()
                    ss.send_string(posyficha)
                    something = ss.recv_string()
                    ss.send_string(player)
                    #Fin de envio de partes de la lista recibida

                    algo = s4.recv_string()
                    s4.send_string("actualizar ficha")
                    algo = s4.recv_string()
                    ss = s4

                    ss.send_string(idficha)
                    something = ss.recv_string()
                    ss.send_string(casillaficha)
                    something = ss.recv_string()
                    ss.send_string(casillasficha)
                    something = ss.recv_string()
                    ss.send_string(pasosficha)
                    something = ss.recv_string()
                    ss.send_string(posxficha)
                    something = ss.recv_string()
                    ss.send_string(posyficha)
                    something = ss.recv_string()
                    ss.send_string(player)
                    #Fin de envio de partes de la lista recibida
                if turno == 2:
                    print("quien registra es el cliente 3")
                    algo = s1.recv_string()
                    s1.send_string("actualizar ficha")
                    algo = s1.recv_string()
                    ss = s1

                    ss.send_string(idficha)
                    something = ss.recv_string()
                    ss.send_string(casillaficha)
                    something = ss.recv_string()
                    ss.send_string(casillasficha)
                    something = ss.recv_string()
                    ss.send_string(pasosficha)
                    something = ss.recv_string()
                    ss.send_string(posxficha)
                    something = ss.recv_string()
                    ss.send_string(posyficha)
                    something = ss.recv_string()
                    ss.send_string(player)
                    #Fin de envio de partes de la lista recibida

                    algo = s2.recv_string()
                    s2.send_string("actualizar ficha")
                    algo = s2.recv_string()
                    ss = s2

                    ss.send_string(idficha)
                    something = ss.recv_string()
                    ss.send_string(casillaficha)
                    something = ss.recv_string()
                    ss.send_string(casillasficha)
                    something = ss.recv_string()
                    ss.send_string(pasosficha)
                    something = ss.recv_string()
                    ss.send_string(posxficha)
                    something = ss.recv_string()
                    ss.send_string(posyficha)
                    something = ss.recv_string()
                    ss.send_string(player)
                    #Fin de envio de partes de la lista recibida

                    algo = s4.recv_string()
                    s4.send_string("actualizar ficha")
                    algo = s4.recv_string()
                    ss = s4

                    ss.send_string(idficha)
                    something = ss.recv_string()
                    ss.send_string(casillaficha)
                    something = ss.recv_string()
                    ss.send_string(casillasficha)
                    something = ss.recv_string()
                    ss.send_string(pasosficha)
                    something = ss.recv_string()
                    ss.send_string(posxficha)
                    something = ss.recv_string()
                    ss.send_string(posyficha)
                    something = ss.recv_string()
                    ss.send_string(player)
                    #Fin de envio de partes de la lista recibida
                if turno == 3:
                    print("quien registra es el cliente 4")
                    algo = s1.recv_string()
                    s1.send_string("actualizar ficha")
                    algo = s1.recv_string()
                    ss = s1

                    ss.send_string(idficha)
                    something = ss.recv_string()
                    ss.send_string(casillaficha)
                    something = ss.recv_string()
                    ss.send_string(casillasficha)
                    something = ss.recv_string()
                    ss.send_string(pasosficha)
                    something = ss.recv_string()
                    ss.send_string(posxficha)
                    something = ss.recv_string()
                    ss.send_string(posyficha)
                    something = ss.recv_string()
                    ss.send_string(player)
                    #Fin de envio de partes de la lista recibida

                    algo = s2.recv_string()
                    s2.send_string("actualizar ficha")
                    algo = s2.recv_string()
                    ss = s2

                    ss.send_string(idficha)
                    something = ss.recv_string()
                    ss.send_string(casillaficha)
                    something = ss.recv_string()
                    ss.send_string(casillasficha)
                    something = ss.recv_string()
                    ss.send_string(pasosficha)
                    something = ss.recv_string()
                    ss.send_string(posxficha)
                    something = ss.recv_string()
                    ss.send_string(posyficha)
                    something = ss.recv_string()
                    ss.send_string(player)
                    #Fin de envio de partes de la lista recibida

                    algo = s3.recv_string()
                    s3.send_string("actualizar ficha")
                    algo = s3.recv_string()
                    ss = s3

                    ss.send_string(idficha)
                    something = ss.recv_string()
                    ss.send_string(casillaficha)
                    something = ss.recv_string()
                    ss.send_string(casillasficha)
                    something = ss.recv_string()
                    ss.send_string(pasosficha)
                    something = ss.recv_string()
                    ss.send_string(posxficha)
                    something = ss.recv_string()
                    ss.send_string(posyficha)
                    something = ss.recv_string()
                    ss.send_string(player)
                    #Fin de envio de partes de la lista recibida

        if funcion == "turno finito":
            print("informando turno a demas clientes")
            s.send_string(str(aumentarTurno(turno)))
            if turno == 0:
                print("quien informa es el cliente 1")
                algo = s2.recv_string()
                s2.send_string("turno finito")
                algo = s2.recv_string()
                s2.send_string(str(aumentarTurno(turno)))

                algo = s3.recv_string()
                s3.send_string("turno finito")
                algo = s3.recv_string()
                s3.send_string(str(aumentarTurno(turno)))

                algo = s4.recv_string()
                s4.send_string("turno finito")
                algo = s4.recv_string()
                s4.send_string(str(aumentarTurno(turno)))
            if turno == 1:
                print("quien informa es el cliente 2")
                algo = s1.recv_string()
                s1.send_string("turno finito")
                algo = s1.recv_string()
                s1.send_string(str(aumentarTurno(turno)))

                algo = s3.recv_string()
                s3.send_string("turno finito")
                algo = s3.recv_string()
                s3.send_string(str(aumentarTurno(turno)))

                algo = s4.recv_string()
                s4.send_string("turno finito")
                algo = s4.recv_string()
                s4.send_string(str(aumentarTurno(turno)))
            if turno == 2:
                print("quien informa es el cliente 3")
                algo = s1.recv_string()
                s1.send_string("turno finito")
                algo = s1.recv_string()
                s1.send_string(str(aumentarTurno(turno)))

                algo = s2.recv_string()
                s2.send_string("turno finito")
                algo = s2.recv_string()
                s2.send_string(str(aumentarTurno(turno)))

                algo = s4.recv_string()
                s4.send_string("turno finito")
                algo = s4.recv_string()
                s4.send_string(str(aumentarTurno(turno)))
            if turno == 3:
                print("quien informa es el cliente 4")
                algo = s1.recv_string()
                s1.send_string("turno finito")
                algo = s1.recv_string()
                s1.send_string(str(aumentarTurno(turno)))

                algo = s2.recv_string()
                s2.send_string("turno finito")
                algo = s2.recv_string()
                s2.send_string(str(aumentarTurno(turno)))

                algo = s3.recv_string()
                s3.send_string("turno finito")
                algo = s3.recv_string()
                s3.send_string(str(aumentarTurno(turno)))
            turno = aumentarTurno(turno)
            if turno == 0:
                s = s1
            if turno == 1:
                s = s2
            if turno == 2:
                s = s3
            if turno == 3:
                s = s4

        if funcion == "terminar":
            print("terminando todo")
            if turno == 0:
                algo = s2.recv_string()
                s2.send_string("terminar")
                algo = s2.recv_string()
                s2.send_string("la buena")

                algo = s3.recv_string()
                s3.send_string("terminar")
                algo = s3.recv_string()
                s3.send_string("la buena")

                algo = s4.recv_string()
                s4.send_string("terminar")
                algo = s4.recv_string()
                s4.send_string("la buena")
            if turno == 1:
                algo = s1.recv_string()
                s1.send_string("terminar")
                algo = s1.recv_string()
                s1.send_string("la buena")

                algo = s3.recv_string()
                s3.send_string("terminar")
                algo = s3.recv_string()
                s3.send_string("la buena")

                algo = s4.recv_string()
                s4.send_string("terminar")
                algo = s4.recv_string()
                s4.send_string("la buena")
            if turno == 2:
                algo = s1.recv_string()
                s1.send_string("terminar")
                algo = s1.recv_string()
                s1.send_string("la buena")

                algo = s2.recv_string()
                s2.send_string("terminar")
                algo = s2.recv_string()
                s2.send_string("la buena")

                algo = s4.recv_string()
                s4.send_string("terminar")
                algo = s4.recv_string()
                s4.send_string("la buena")
            if turno == 3:
                algo = s1.recv_string()
                s1.send_string("terminar")
                algo = s1.recv_string()
                s1.send_string("la buena")

                algo = s2.recv_string()
                s2.send_string("terminar")
                algo = s2.recv_string()
                s2.send_string("la buena")

                algo = s3.recv_string()
                s3.send_string("terminar")
                algo = s3.recv_string()
                s3.send_string("la buena")
            s.send_string("listo")
            break
