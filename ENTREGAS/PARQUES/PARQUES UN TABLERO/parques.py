import pygame
import random
import socket
import time
from datetime import datetime
import gc

#version de parques 3, funciona con serverparques.py medianamente, se requiere comunicacion entre todos los jugadores, para saber que fichas se movieron

#PARAMETROS GLOBALES____________
ancho = 1000
alto = 700
#___________FIN DE PARAMETROS

#DEFINICION DE FUNCIONES______________________________________________

def imprimir(pos,color, texto,tamano = 32):
    fuente = pygame.font.Font(None,tamano)
    tx = fuente.render(texto,1,color)
    pantalla.blit(tx,pos)

def obtenersiguiente(lista, elemento):
    for e in range(len(lista)):
        if e == elemento:
            return lista[e+1]

def obtenersiguienten(lista, elemento, n):
    res = obtenerpos(lista, elemento)
    if (int(len(lista)) - int(res)) <= 0:
        return lista[len(lista)]
    else:
        return lista[res]

#________________________________________FIN DE DEFINICION DE FUNCIONES

#CREACION DE CLASES___________________________________________
class Ficha(pygame.sprite.Sprite):

    def __init__(self,cod,lm, pos, colorr,cas, cass, car):
        pygame.sprite.Sprite.__init__(self)
        self.lisimag = lm
        self.selec = 0
        self.id = cod
        self.image = self.lisimag[self.selec]
        self.rect = self.image.get_rect()
        self.rect.x=pos[0]
        self.rect.y=pos[1]
        self.color = colorr#0 para amarillo, 1 para azul, 2 para verde, 3 para rojo
        self.casillaa = cas
        self.casillaas = cass
        self.casillacar = car
        self.casillacars = cass
        self.pasos = 0
        self.poscas = 0#1,2,3 o 4 dependiendo la posicion en la casilla que ocupe
        self.poscarcel = pos

    def getpos(self):
        res = [self.rect.x,self.rect.y]
        return res

    def cselec(self):
        if self.selec == 0:
            self.selec = 1
        else:
            self.selec = 0

    def update(self):
        self.image = self.lisimag[self.selec]

    def setpasos(self,passo,lim):
        if passo >= lim:
            self.pasos = lim - 1
        else:
            self.pasos = passo

    def moverCarcel(self):
        self.casillaa = self.casillacar
        self.casillaas = self.casillacars
        self.pasos = 0
        self.poscas = 0
        self.rect.x = self.poscarcel[0]
        self.rect.y = self.poscarcel[1]


    def mover(self,pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class Casilla():

    def __init__(self,lspos,tpe, idd):#recibe una lista con las posiciones donde se ubicaran las fichas
        self.id = idd
        self.tipo = tpe      # 0 carcel, 1 horizontal,2 vertical, 3 horizontal pequena, 4 vertical pequena, 5 especial(las diagonales), 6 meta
        self.pos = lspos
        self.pos1 = [lspos[0],0]
        self.pos2 = [lspos[1],0]
        self.pos3 = [lspos[2],0]
        self.pos4 = [lspos[3],0]#lista de dos posiciones, primera, posicion donde ira la ficha, segunda, posicion ocupada o no?, 0 para no, 1 para si
        self.peso = 0

    def setestado(self,poss,estado):
        if poss == 0:
            self.pos1 = [self.pos1[0],estado]
        if poss == 1:
            self.pos2 = [self.pos2[0],estado]
        if poss == 2:
            self.pos3 = [self.pos3[0],estado]
        if poss == 3:
            self.pos4 = [self.pos4[0],estado]

    def liberar(self,poss):
        if poss == self.pos1[0]:
            self.pos1 = [self.pos1[0],0]
        if poss == self.pos2[0]:
            self.pos2 = [self.pos2[0],0]
        if poss == self.pos3[0]:
            self.pos3 = [self.pos3[0],0]
        if poss == self.pos3[0]:
            self.pos4 = [self.pos4[0],0]

    def ubicarficha(self):
        if self.pos1[1]==0:
            res = self.pos1[0]
            self.setestado(0,1)
        elif self.pos2[1]==0:
            res = self.pos2[0]
            self.setestado(1,1)
        elif self.pos3[1]==0:
            res = self.pos3[0]
            self.setestado(2,1)
        elif self.pos4[1]==0:
            res = self.pos4[0]
            self.setestado(3,1)
        else:
            n = random.randrange(4)
            if n == 0:
                res = self.pos1[0]
                res = [res[0]+5,res[1]+5]
            if n == 1:
                res = self.pos2[0]
                res = [res[0]+5,res[1]+5]
            if n == 2:
                res = self.pos3[0]
                res = [res[0]+5,res[1]+5]
            if n == 3:
                res = self.pos4[0]
                res = [res[0]+5,res[1]+5]
        return res

class Puesto(pygame.sprite.Sprite):

    def __init__(self,pos,lm,casilla):
        pygame.sprite.Sprite.__init__(self)
        self.lisimag = lm
        self.image = self.lisimag[0]
        self.rect = self.image.get_rect()
        self.rect.x=pos[0]
        self.rect.y=pos[1]
        self.visible = False
        self.casilla = casilla
        self.ficha = 33 #numero de la ficha en la casilla, si es 33 no tiene ficha

    def liberar(self):
        self.ficha = 33

    def ubicar(self):
        if self.ficha == 33:
            return [self.rect.x,self.rect.y]
        else:
            return [0,0]

    def update(self):
        if self.visible:
            self.image = self.lisimag[1]
        else:
            self.image = self.lisimag[0]

class Dado(pygame.sprite.Sprite):

    def __init__(self, lm, pos):
        pygame.sprite.Sprite.__init__(self)
        self.lisimag = lm
        self.con = 6
        self.con2 = 0
        self.valor = 5
        self.limite = 5
        self.image = self.lisimag[self.con]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.numero = 0
        self.lanzar = 0#0 para no lanzar, 1 para lanzar

    def update(self):
        if self.con2 < self.valor:
            self.con2 = self.con2 + 1
            if self.lanzar == 1:
                if self.con < self.limite:
                    self.con +=1
                else:
                    self.con = 0
        else:
            self.lanzar = 0
            self.valor = 0
            self.con2 = 0
        self.image=self.lisimag[self.con]

#______________________________________________FIN DE CREACION DE CLASES

#INICIO DEL CICLO PRINCIPAL____________________________________________________
if __name__ == '__main__':
#INICIALIZACION DE PYGAME, MIXER, Y PANTALLA_________________________________________________
    pygame.init()
    pantalla = pygame.display.set_mode([ancho,alto])
    #CARGA DE IMAGENES_____________________________________________________________________________________
    fondo = pygame.image.load('./RECURSOS/FONDO.png')

    ficha_verde= pygame.image.load('./RECURSOS/ficha_verde.png')
    ficha_azul= pygame.image.load('./RECURSOS/ficha_azul.png')
    ficha_roja= pygame.image.load('./RECURSOS/ficha_roja.png')
    ficha_amarilla= pygame.image.load('./RECURSOS/ficha_amarilla.png')

    ficha_verde_s= pygame.image.load('./RECURSOS/ficha_verde_s.png')
    ficha_azul_s= pygame.image.load('./RECURSOS/ficha_azul_s.png')
    ficha_roja_s= pygame.image.load('./RECURSOS/ficha_roja_s.png')
    ficha_amarilla_s= pygame.image.load('./RECURSOS/ficha_amarillo_s.png')

    cero = pygame.image.load('./RECURSOS/cero.png')
    uno = pygame.image.load('./RECURSOS/uno.png')
    dos= pygame.image.load('./RECURSOS/dos.png')
    tres= pygame.image.load('./RECURSOS/tres.png')
    cuatro= pygame.image.load('./RECURSOS/cuatro.png')
    cinco= pygame.image.load('./RECURSOS/cinco.png')
    seis= pygame.image.load('./RECURSOS/seis.png')

    boton= pygame.image.load('./RECURSOS/boton.png')
    boton2= pygame.image.load('./RECURSOS/boton2.png')

    puesto= pygame.image.load('./RECURSOS/puesto.png')
    puesto2= pygame.image.load('./RECURSOS/puesto2.png')
    #__________________________________________________________FIN DE CARGA DE IMAGENES

    #CREACION SPRITES__________________________________________________________________________________
    c = 0
    cf=0
        #grupos de sprites_____________________
    Dados = pygame.sprite.Group()
    Fichas = pygame.sprite.Group()
    FichasJugador = pygame.sprite.Group()
    FichasNoJugador = pygame.sprite.Group()
    Puestos = pygame.sprite.Group()

    Casillas = []
    Puestosl = []
        #___________________________fin de grupos de sprites
    #la lista siguiente contiene todas las posiciones de las carceles
    posiciones_carcel = ([575,600],[625,600],[575,650],[625,650],[575,50],[625,50],[575,100],[625,100],[50,50],[100,50],[50,100],[100,100],[50,600],[100,600],[50,650],[100,650])
    #posiciones_carcel = (0 amarillo,1 amarillo,2 amarillo,3 amarillo,4 azul,5 azul,6 azul,7 azul,8 verde, 9 verde, 10 verde, 11 verde, 12 rojo, 13 rojo, 14 rojo, 15 rojo)

    #CREACION DE CASILLAS Y PUESTOS____________________________________________________________
    #creando casillas carcel tipo 0:
    for e in range(4):
        cc = Casilla([posiciones_carcel[e*4],posiciones_carcel[e*4 + 1],posiciones_carcel[e*4 + 2],posiciones_carcel[e*4 + 3]],0,len(Casillas))

        p = Puesto(cc.pos[0],[puesto2, puesto], cc.id)
        Puestos.add(p)
        p = Puesto(cc.pos[1],[puesto2, puesto], cc.id)
        Puestos.add(p)
        p = Puesto(cc.pos[2],[puesto2, puesto], cc.id)
        Puestos.add(p)
        p = Puesto(cc.pos[3],[puesto2, puesto], cc.id)
        Puestos.add(p)

        Casillas.append(cc)

    #creando casillas horizontales tipo 1:
    for e in range(6):
        cc = Casilla([[415,679-e*25],[440,679-e*25],[485,679-e*25],[510,679-e*25]],1,len(Casillas))

        p = Puesto(cc.pos[0],[puesto2, puesto], cc.id)
        Puestos.add(p)
        p = Puesto(cc.pos[1],[puesto2, puesto], cc.id)
        Puestos.add(p)
        p = Puesto(cc.pos[2],[puesto2, puesto], cc.id)
        Puestos.add(p)
        p = Puesto(cc.pos[3],[puesto2, puesto], cc.id)
        Puestos.add(p)

        Casillas.append(cc)
    for e in range(6):
        cc = Casilla([[415,4+e*25],[440,4+e*25],[485,4+e*25],[510,4+e*25]],1,len(Casillas))

        p = Puesto(cc.pos[0],[puesto2, puesto], cc.id)
        Puestos.add(p)
        p = Puesto(cc.pos[1],[puesto2, puesto], cc.id)
        Puestos.add(p)
        p = Puesto(cc.pos[2],[puesto2, puesto], cc.id)
        Puestos.add(p)
        p = Puesto(cc.pos[3],[puesto2, puesto], cc.id)
        Puestos.add(p)

        Casillas.append(cc)
    for e in range(6):
        cc = Casilla([[165,4+e*25],[190,4+e*25],[235,4+e*25],[260,4+e*25]],1,len(Casillas))

        p = Puesto(cc.pos[0],[puesto2, puesto], cc.id)
        Puestos.add(p)
        p = Puesto(cc.pos[1],[puesto2, puesto], cc.id)
        Puestos.add(p)
        p = Puesto(cc.pos[2],[puesto2, puesto], cc.id)
        Puestos.add(p)
        p = Puesto(cc.pos[3],[puesto2, puesto], cc.id)
        Puestos.add(p)

        Casillas.append(cc)
    for e in range(6):
        cc = Casilla([[165,679-e*25],[190,679-e*25],[235,679-e*25],[260,679-e*25]],1,len(Casillas))

        p = Puesto(cc.pos[0],[puesto2, puesto], cc.id)
        Puestos.add(p)
        p = Puesto(cc.pos[1],[puesto2, puesto], cc.id)
        Puestos.add(p)
        p = Puesto(cc.pos[2],[puesto2, puesto], cc.id)
        Puestos.add(p)
        p = Puesto(cc.pos[3],[puesto2, puesto], cc.id)
        Puestos.add(p)

        Casillas.append(cc)

    #creando casillas verticales tipo 2:
    for e in range(6):
        cc = Casilla([[678-e*25,415],[678-e*25,440],[678-e*25,485],[678-e*25,510]],2,len(Casillas))

        p = Puesto(cc.pos[0],[puesto2, puesto], cc.id)
        Puestos.add(p)
        p = Puesto(cc.pos[1],[puesto2, puesto], cc.id)
        Puestos.add(p)
        p = Puesto(cc.pos[2],[puesto2, puesto], cc.id)
        Puestos.add(p)
        p = Puesto(cc.pos[3],[puesto2, puesto], cc.id)
        Puestos.add(p)

        Casillas.append(cc)
    for e in range(6):
        cc = Casilla([[678-e*25,165],[678-e*25,190],[678-e*25,235],[678-e*25,260]],2,len(Casillas))

        p = Puesto(cc.pos[0],[puesto2, puesto], cc.id)
        Puestos.add(p)
        p = Puesto(cc.pos[1],[puesto2, puesto], cc.id)
        Puestos.add(p)
        p = Puesto(cc.pos[2],[puesto2, puesto], cc.id)
        Puestos.add(p)
        p = Puesto(cc.pos[3],[puesto2, puesto], cc.id)
        Puestos.add(p)

        Casillas.append(cc)
    for e in range(6):
        cc = Casilla([[3+e*25,165],[3+e*25,190],[3+e*25,235],[3+e*25,260]],2,len(Casillas))

        p = Puesto(cc.pos[0],[puesto2, puesto], cc.id)
        Puestos.add(p)
        p = Puesto(cc.pos[1],[puesto2, puesto], cc.id)
        Puestos.add(p)
        p = Puesto(cc.pos[2],[puesto2, puesto], cc.id)
        Puestos.add(p)
        p = Puesto(cc.pos[3],[puesto2, puesto], cc.id)
        Puestos.add(p)

        Casillas.append(cc)
    for e in range(6):
        cc = Casilla([[3+e*25,415],[3+e*25,440],[3+e*25,485],[3+e*25,510]],2,len(Casillas))

        p = Puesto(cc.pos[0],[puesto2, puesto], cc.id)
        Puestos.add(p)
        p = Puesto(cc.pos[1],[puesto2, puesto], cc.id)
        Puestos.add(p)
        p = Puesto(cc.pos[2],[puesto2, puesto], cc.id)
        Puestos.add(p)
        p = Puesto(cc.pos[3],[puesto2, puesto], cc.id)
        Puestos.add(p)

        Casillas.append(cc)

    #creando casillas horizontales pequenas tipo 3:
    for e in range(8):
        cc = Casilla([[304,679-e*25],[329,679-e*25],[354,679-e*25],[379,679-e*25]],3,len(Casillas))

        p = Puesto(cc.pos[0],[puesto2, puesto], cc.id)
        Puestos.add(p)
        p = Puesto(cc.pos[1],[puesto2, puesto], cc.id)
        Puestos.add(p)
        p = Puesto(cc.pos[2],[puesto2, puesto], cc.id)
        Puestos.add(p)
        p = Puesto(cc.pos[3],[puesto2, puesto], cc.id)
        Puestos.add(p)

        Casillas.append(cc)
    for e in range(8):
        cc = Casilla([[304,4+e*25],[329,4+e*25],[354,4+e*25],[379,4+e*25]],3,len(Casillas))

        p = Puesto(cc.pos[0],[puesto2, puesto], cc.id)
        Puestos.add(p)
        p = Puesto(cc.pos[1],[puesto2, puesto], cc.id)
        Puestos.add(p)
        p = Puesto(cc.pos[2],[puesto2, puesto], cc.id)
        Puestos.add(p)
        p = Puesto(cc.pos[3],[puesto2, puesto], cc.id)
        Puestos.add(p)

        Casillas.append(cc)

    #creando casillas verticales pequenas tipo 4:
    for e in range(8):
        cc = Casilla([[3+e*25,304],[3+e*25,329],[3+e*25,354],[3+e*25,379]],4,len(Casillas))

        p = Puesto(cc.pos[0],[puesto2, puesto], cc.id)
        Puestos.add(p)
        p = Puesto(cc.pos[1],[puesto2, puesto], cc.id)
        Puestos.add(p)
        p = Puesto(cc.pos[2],[puesto2, puesto], cc.id)
        Puestos.add(p)
        p = Puesto(cc.pos[3],[puesto2, puesto], cc.id)
        Puestos.add(p)

        Casillas.append(cc)
    for e in range(8):
        cc = Casilla([[503+e*25,304],[503+e*25,329],[503+e*25,354],[503+e*25,379]],4,len(Casillas))

        p = Puesto(cc.pos[0],[puesto2, puesto], cc.id)
        Puestos.add(p)
        p = Puesto(cc.pos[1],[puesto2, puesto], cc.id)
        Puestos.add(p)
        p = Puesto(cc.pos[2],[puesto2, puesto], cc.id)
        Puestos.add(p)
        p = Puesto(cc.pos[3],[puesto2, puesto], cc.id)
        Puestos.add(p)

        Casillas.append(cc)

    #creando casillas especiales tipo 5:
    cc = Casilla([[404,521],[429,525],[454,529],[479,531]],5,len(Casillas))#_________________AMARILLAS
    p = Puesto(cc.pos[0],[puesto2, puesto], cc.id)
    Puestos.add(p)
    p = Puesto(cc.pos[1],[puesto2, puesto], cc.id)
    Puestos.add(p)
    p = Puesto(cc.pos[2],[puesto2, puesto], cc.id)
    Puestos.add(p)
    p = Puesto(cc.pos[3],[puesto2, puesto], cc.id)
    Puestos.add(p)
    Casillas.append(cc)
    cc = Casilla([[429,474],[449,484],[469,494],[489,504]],5,len(Casillas))#_________________AMARILLAS
    p = Puesto(cc.pos[0],[puesto2, puesto], cc.id)
    Puestos.add(p)
    p = Puesto(cc.pos[1],[puesto2, puesto], cc.id)
    Puestos.add(p)
    p = Puesto(cc.pos[2],[puesto2, puesto], cc.id)
    Puestos.add(p)
    p = Puesto(cc.pos[3],[puesto2, puesto], cc.id)
    Puestos.add(p)
    Casillas.append(cc)
    cc = Casilla([[474,429],[484,449],[494,469],[504,485]],5,len(Casillas))#_________________AMARILLAS
    p = Puesto(cc.pos[0],[puesto2, puesto], cc.id)
    Puestos.add(p)
    p = Puesto(cc.pos[1],[puesto2, puesto], cc.id)
    Puestos.add(p)
    p = Puesto(cc.pos[2],[puesto2, puesto], cc.id)
    Puestos.add(p)
    p = Puesto(cc.pos[3],[puesto2, puesto], cc.id)
    Puestos.add(p)
    Casillas.append(cc)
    cc = Casilla([[521,404],[525,429],[529,454],[531,479]],5,len(Casillas))#_________________AMARILLAS
    p = Puesto(cc.pos[0],[puesto2, puesto], cc.id)
    Puestos.add(p)
    p = Puesto(cc.pos[1],[puesto2, puesto], cc.id)
    Puestos.add(p)
    p = Puesto(cc.pos[2],[puesto2, puesto], cc.id)
    Puestos.add(p)
    p = Puesto(cc.pos[3],[puesto2, puesto], cc.id)
    Puestos.add(p)
    Casillas.append(cc)

    cc = Casilla([[404,162],[429,160],[454,156],[479,152]],5,len(Casillas))#_________________AZULES
    p = Puesto(cc.pos[0],[puesto2, puesto], cc.id)
    Puestos.add(p)
    p = Puesto(cc.pos[1],[puesto2, puesto], cc.id)
    Puestos.add(p)
    p = Puesto(cc.pos[2],[puesto2, puesto], cc.id)
    Puestos.add(p)
    p = Puesto(cc.pos[3],[puesto2, puesto], cc.id)
    Puestos.add(p)
    Casillas.append(cc)
    cc = Casilla([[429,209],[449,199],[469,189],[489,179]],5,len(Casillas))#_________________AZULES
    p = Puesto(cc.pos[0],[puesto2, puesto], cc.id)
    Puestos.add(p)
    p = Puesto(cc.pos[1],[puesto2, puesto], cc.id)
    Puestos.add(p)
    p = Puesto(cc.pos[2],[puesto2, puesto], cc.id)
    Puestos.add(p)
    p = Puesto(cc.pos[3],[puesto2, puesto], cc.id)
    Puestos.add(p)
    Casillas.append(cc)
    cc = Casilla([[474,254],[484,234],[494,214],[504,194]],5,len(Casillas))#_________________AZULES
    p = Puesto(cc.pos[0],[puesto2, puesto], cc.id)
    Puestos.add(p)
    p = Puesto(cc.pos[1],[puesto2, puesto], cc.id)
    Puestos.add(p)
    p = Puesto(cc.pos[2],[puesto2, puesto], cc.id)
    Puestos.add(p)
    p = Puesto(cc.pos[3],[puesto2, puesto], cc.id)
    Puestos.add(p)
    Casillas.append(cc)
    cc = Casilla([[521,279],[525,254],[529,229],[531,204]],5,len(Casillas))#_________________AZULES
    p = Puesto(cc.pos[0],[puesto2, puesto], cc.id)
    Puestos.add(p)
    p = Puesto(cc.pos[1],[puesto2, puesto], cc.id)
    Puestos.add(p)
    p = Puesto(cc.pos[2],[puesto2, puesto], cc.id)
    Puestos.add(p)
    p = Puesto(cc.pos[3],[puesto2, puesto], cc.id)
    Puestos.add(p)
    Casillas.append(cc)

    cc = Casilla([[204,152],[229,156],[254,160],[279,162]],5,len(Casillas))#_________________VERDES
    p = Puesto(cc.pos[0],[puesto2, puesto], cc.id)
    Puestos.add(p)
    p = Puesto(cc.pos[1],[puesto2, puesto], cc.id)
    Puestos.add(p)
    p = Puesto(cc.pos[2],[puesto2, puesto], cc.id)
    Puestos.add(p)
    p = Puesto(cc.pos[3],[puesto2, puesto], cc.id)
    Puestos.add(p)
    Casillas.append(cc)
    cc = Casilla([[194,179],[214,189],[234,199],[254,209]],5,len(Casillas))#_________________VERDES
    p = Puesto(cc.pos[0],[puesto2, puesto], cc.id)
    Puestos.add(p)
    p = Puesto(cc.pos[1],[puesto2, puesto], cc.id)
    Puestos.add(p)
    p = Puesto(cc.pos[2],[puesto2, puesto], cc.id)
    Puestos.add(p)
    p = Puesto(cc.pos[3],[puesto2, puesto], cc.id)
    Puestos.add(p)
    Casillas.append(cc)
    cc = Casilla([[174,194],[184,214],[194,234],[204,254]],5,len(Casillas))#_________________VERDES
    p = Puesto(cc.pos[0],[puesto2, puesto], cc.id)
    Puestos.add(p)
    p = Puesto(cc.pos[1],[puesto2, puesto], cc.id)
    Puestos.add(p)
    p = Puesto(cc.pos[2],[puesto2, puesto], cc.id)
    Puestos.add(p)
    p = Puesto(cc.pos[3],[puesto2, puesto], cc.id)
    Puestos.add(p)
    Casillas.append(cc)
    cc = Casilla([[151,204],[155,229],[159,254],[161,279]],5,len(Casillas))#_________________VERDES
    p = Puesto(cc.pos[0],[puesto2, puesto], cc.id)
    Puestos.add(p)
    p = Puesto(cc.pos[1],[puesto2, puesto], cc.id)
    Puestos.add(p)
    p = Puesto(cc.pos[2],[puesto2, puesto], cc.id)
    Puestos.add(p)
    p = Puesto(cc.pos[3],[puesto2, puesto], cc.id)
    Puestos.add(p)
    Casillas.append(cc)

    cc = Casilla([[204,531],[229,529],[254,525],[279,521]],5,len(Casillas))#_________________ROJAS
    p = Puesto(cc.pos[0],[puesto2, puesto], cc.id)
    Puestos.add(p)
    p = Puesto(cc.pos[1],[puesto2, puesto], cc.id)
    Puestos.add(p)
    p = Puesto(cc.pos[2],[puesto2, puesto], cc.id)
    Puestos.add(p)
    p = Puesto(cc.pos[3],[puesto2, puesto], cc.id)
    Puestos.add(p)
    Casillas.append(cc)
    cc = Casilla([[194,504],[214,494],[234,484],[254,474]],5,len(Casillas))#_________________ROJAS
    p = Puesto(cc.pos[0],[puesto2, puesto], cc.id)
    Puestos.add(p)
    p = Puesto(cc.pos[1],[puesto2, puesto], cc.id)
    Puestos.add(p)
    p = Puesto(cc.pos[2],[puesto2, puesto], cc.id)
    Puestos.add(p)
    p = Puesto(cc.pos[3],[puesto2, puesto], cc.id)
    Puestos.add(p)
    Casillas.append(cc)
    cc = Casilla([[174,485],[184,469],[194,449],[204,429]],5,len(Casillas))#_________________ROJAS
    p = Puesto(cc.pos[0],[puesto2, puesto], cc.id)
    Puestos.add(p)
    p = Puesto(cc.pos[1],[puesto2, puesto], cc.id)
    Puestos.add(p)
    p = Puesto(cc.pos[2],[puesto2, puesto], cc.id)
    Puestos.add(p)
    p = Puesto(cc.pos[3],[puesto2, puesto], cc.id)
    Puestos.add(p)
    Casillas.append(cc)
    cc = Casilla([[151,479],[155,454],[159,429],[161,404]],5,len(Casillas))#_________________ROJAS
    p = Puesto(cc.pos[0],[puesto2, puesto], cc.id)
    Puestos.add(p)
    p = Puesto(cc.pos[1],[puesto2, puesto], cc.id)
    Puestos.add(p)
    p = Puesto(cc.pos[2],[puesto2, puesto], cc.id)
    Puestos.add(p)
    p = Puesto(cc.pos[3],[puesto2, puesto], cc.id)
    Puestos.add(p)
    Casillas.append(cc)

    #creando casillas meta tipo 6:
    cc = Casilla([[342,467],[-25,-25],[-25,-25],[-25,-25]],6,len(Casillas))#_________________AMARILLAS
    p = Puesto(cc.pos[0],[puesto2, puesto], cc.id)
    Puestos.add(p)
    Casillas.append(cc)
    cc = Casilla([[467,342],[-25,-25],[-25,-25],[-25,-25]],6,len(Casillas))#_________________AZULES
    p = Puesto(cc.pos[0],[puesto2, puesto], cc.id)
    Puestos.add(p)
    Casillas.append(cc)
    cc = Casilla([[342,217],[-25,-25],[-25,-25],[-25,-25]],6,len(Casillas))#_________________VERDES
    p = Puesto(cc.pos[0],[puesto2, puesto], cc.id)
    Puestos.add(p)
    Casillas.append(cc)
    cc = Casilla([[217,342],[-25,-25],[-25,-25],[-25,-25]],6,len(Casillas))#_________________ROJAS
    p = Puesto(cc.pos[0],[puesto2, puesto], cc.id)
    Puestos.add(p)
    Casillas.append(cc)

    cc = Casilla([[367,367],[367,317],[317,317],[317,367]],7,999)#casilla final
    p = Puesto(cc.pos[0],[puesto2, puesto], cc.id)
    Puestos.add(p)
    p = Puesto(cc.pos[1],[puesto2, puesto], cc.id)
    Puestos.add(p)
    p = Puesto(cc.pos[2],[puesto2, puesto], cc.id)
    Puestos.add(p)
    p = Puesto(cc.pos[3],[puesto2, puesto], cc.id)
    Puestos.add(p)
    Casillas.append(cc)
    #_________________________________________________FIN DE CREACION DE CASILLAS Y PUESTOS

    #DEFINICION DE CAMINOS SEGUN COLOR DE JUGADOR________________________________________________
    camarillo = [0,4,5,6,7,8,9,84,85,86,87,33,32,31,30,29,28,83,34,35,36,37,38,39,91,90,89,88,15,14,13,12,11,10,60,16,17,18,19,20,21,92,93,94,95,45,44,43,42,41,40,68,46,47,48,49,50,51,99,98,97,96,27,26,25,24,23,22,52,53,54,55,56,57,58,59,100,999]
    cazul = [1,34,35,36,37,38,39,91,90,89,88,15,14,13,12,11,10,60,16,17,18,19,20,21,92,93,94,95,45,44,43,42,41,40,68,46,47,48,49,50,51,99,98,97,96,27,26,25,24,23,22,52,4,5,6,7,8,9,84,85,86,87,33,32,31,30,29,28,83,82,81,80,79,78,77,76,101,999]
    cverde = [2,16,17,18,19,20,21,92,93,94,95,45,44,43,42,41,40,68,46,47,48,49,50,51,99,98,97,96,27,26,25,24,23,22,52,4,5,6,7,8,9,84,85,86,87,33,32,31,30,29,28,83,34,35,36,37,38,39,91,90,89,88,15,14,13,12,11,10,60,61,62,63,64,65,66,67,102,999]
    crojo = [3,46,47,48,49,50,51,99,98,97,96,27,26,25,24,23,22,52,4,5,6,7,8,9,84,85,86,87,33,32,31,30,29,28,83,34,35,36,37,38,39,91,90,89,88,15,14,13,12,11,10,60,16,17,18,19,20,21,92,93,94,95,45,44,43,42,41,40,68,69,70,71,72,73,74,75,103,999]
    camino = []
    #___________________________________________________FIN DE DEFINICION DE CAMINOS SEGUN COLOR

    #Lista con imagenes de los dados
    listaimagenes = [uno,dos,tres,cuatro,cinco,seis,cero]
    #listas con imagenes de las fichas
    lisamarilla = [ficha_amarilla,ficha_amarilla_s]
    lisazul = [ficha_azul,ficha_azul_s]
    lisverde = [ficha_verde,ficha_verde_s]
    lisroja = [ficha_roja, ficha_roja_s]
    #creacion de dados____________________________
    dado1 = Dado(listaimagenes, [775,150])
    dado2 = Dado(listaimagenes, [875,150])
    Dados.add(dado1)
    Dados.add(dado2)
    #_______________________________fin de creacion de dados

    #creacion fichas en posicion carcel correspondiente________________________
    for f in posiciones_carcel:
        if(c%4 == 0):
            cf = cf + 1
            if(cf == 1):
                ff = Ficha(c,lisamarilla,f,1, 0, 8,0)
                Fichas.add(ff)
            if(cf == 2):
                ff = Ficha(c,lisazul,f,2, 1,38,1)
                Fichas.add(ff)
            if(cf == 3):
                ff = Ficha(c,lisverde,f,3, 2, 20,2)
                Fichas.add(ff)
            if(cf == 4):
                ff = Ficha(c,lisroja,f,4, 3, 50,3)
                Fichas.add(ff)
        else:
            if(cf == 1):
                ff = Ficha(c,lisamarilla,f,1, 0, 8,0)
                Fichas.add(ff)
            if(cf == 2):
                ff = Ficha(c,lisazul,f,2, 1,38,1)
                Fichas.add(ff)
            if(cf == 3):
                ff = Ficha(c,lisverde,f,3, 2, 20,2)
                Fichas.add(ff)
            if(cf == 4):
                ff = Ficha(c,lisroja,f,4, 3, 50,3)
                Fichas.add(ff)
        c = c + 1
    #________________________________________fin de creacion de fichas en posiciones

    #_________________________________FIN DE CREACION DE SPRITES

#____________________________FIN DE INICIALIZACION DE PYGAME, MIXER Y PANTALLA
    pygame.display.flip()#ACTUALIZACION DE PANTALLA
#CONEXION CON EL SERVIDOR__________________________________
    host = "localhost"
    port = 8001
    mi_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (host, port)
    mi_socket.connect(server_address)#conexion con el servidor
    mensaje = "Soy un cliente"
    mi_socket.send(mensaje.encode("ascii"))
    respuesta = mi_socket.recv(1000)
    respuesta = respuesta.decode("ascii")
    jugador = int(respuesta)
    print jugador
#________________________________________________FIN DE CONEXION CON EL SERVIDOR

#CAMBIO DE INTERFAZ SEGUN COLOR DEL JUGADOR________________________________________________
    if jugador == 0:
        cuadro = pygame.transform.scale(ficha_amarilla,(50, 50))
        camino = camarillo
    if jugador == 1:
        cuadro = pygame.transform.scale(ficha_azul,(50, 50))
        camino = cazul
    if jugador == 2:
        cuadro = pygame.transform.scale(ficha_verde,(50, 50))
        camino = cverde
    if jugador == 3:
        cuadro = pygame.transform.scale(ficha_roja,(50, 50))
        camino = crojo

    botons1 = boton #declaracion de los botones, luego podran cambiar dependiendo de si estan habilitados o no
    botons2 = boton
    botons3 = boton
    botons4 = boton
    cuadro2 = boton

    #llenado de listas para colisiones
    for f in Fichas:
        if f.id == jugador*4:
            FichasJugador.add(f)
        elif f.id == jugador*4+1:
            FichasJugador.add(f)
        elif f.id == jugador*4+2:
            FichasJugador.add(f)
        elif f.id == jugador*4+3:
            FichasJugador.add(f)
        else:
            FichasNoJugador.add(f)
    #fin de llenado de listas para colisiones
#_____________________________________________________________FIN DEL CAMBIO DE INTERFAZ
    #VARIABLES DEL CICLO_____________
    click = False
    fin = False
    reloj = pygame.time.Clock()

    fic = 0 #Numero de ficha seleccionada, 0 para no hacer nada
    select = 0 #habilitar o no los botonees

    #salida = 0#Habilitar proceso de primer salida de carcel
    salida = [0,0,0,0]
    finito = 1 # inidica si el lanzamiento de los dados termino
    movee = 0 #inidica si ya se realizo el movimiento
    habil = 1 #indica si se pueden lanzar los dados
    turno = jugador #turno indica de quien es el turno, hecho para jugar sin servidor
    repetir = 0 #indica si cayo un numero par, para dejar repetir turno

    casi = 1000 # numero de la casilla siguiente
    pasoskys = 0 # numero de pasos a sumar cuando se mueve una ficha
    totald = 0 #numero igual a la suma de los valores de los dados, si se mueve solo 5, se descuenta, hasta no estar en 0 no termina turno
    cassel = 0

    lanzamiento = []#lista que contendra informacion sobre si los dos dados han lanzado, sera [1,1]
    terminado = []#lista que informa cuando un dado termina de lanzar, sera [1,1]
    npos = [0,0] # nueva poscion, en el se guarda la posicion del puesto al que se clickea para mover la ficha
    vdados = [0,0] #lista con el valor de los dados, cada posicion es el valor de un dado
    #________________FIN VARIABLES CICLO

#CICLO PRINCIPAL____________________________________________________
    while not fin:

#GESTION DE EVENTOS_____________________________________________________________________
        for event in pygame.event.get():
        #EVENTO CERRAR VENTANA_______________
            if event.type == pygame.QUIT:
                fin=True
                mensaje = "terminar"
                mi_socket.send(mensaje.encode("ascii"))
                respuesta = mi_socket.recv(1000)
                mi_socket.close()
        #____________________FIN DE CERRAR VENTANA
        #EVENTO CLICK DE MOUSE__________________________________________________
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
            #evento click derecho____________________________
                if event.button == 1:

                    #click en posicion lanzar_________

                    if pos[0]<900 and pos[0]>800:
                        if pos[1]<275 and pos[1]>250:
                            if finito == 1 and habil == 1:
                                for e in Dados:
                                    e.lanzar = 1
                                    e.valor = random.randrange(30)+10
                                    lanzamiento.append(1)
                                    movee = 1
                                    if salida[jugador] == 5:
                                        habil = 0
                                    mensaje = "deme un numero"
                                    mi_socket.send(mensaje.encode("ascii"))
                                    respuesta = mi_socket.recv(1000)
                                    respuesta = respuesta.decode("ascii")

                                    print str(respuesta)


                    #________fin de accion de click en pos lanzar
                    if select == 0 and movee == 1 and salida[jugador] == 5:
                        #click en ficha 1_________________
                        if pos[0]<950 and pos[0]>750:
                            if pos[1]<405 and pos[1]>345:
                                botons1 = boton
                                botons2 = boton2
                                botons3 = boton2
                                botons4 = boton2
                                select = 1
                                fic = 1
                                for f in Fichas:
                                    if f.id == jugador*4:
                                        if f.pasos + vdados[0] > len(camino) - 1:
                                            c1 = camino[len(camino) - 1]
                                            pasoskys1 = 0   #debo cambiar lo de las fichas, no se pueden mover infinitamente
                                        else:               #con ese totald, si algo volver a parques1funca.py
                                            c1 = camino[f.pasos + vdados[0]]
                                            pasoskys1 = vdados[0]

                                        if f.pasos + vdados[1] > len(camino) - 1:
                                            c2 = camino[len(camino) - 1]
                                            pasoskys2=0
                                        else:
                                            c2 = camino[f.pasos + vdados[1]]
                                            pasoskys2 = vdados[1]

                                        if f.pasos + vdados[0] + vdados[1] > len(camino) - 1:
                                            c3 = camino[len(camino) - 1]
                                            pasoskys3 = 0
                                        else:
                                            c3 = camino[f.pasos + vdados[0] + vdados[1]]
                                            pasoskys3 = vdados[0] + vdados[1]
                                        for pu in Puestos:
                                            if pu.casilla == c1:
                                                if totald == vdados[0] or  totald == vdados[0]+vdados[1]:
                                                    if pu.casilla == 999:
                                                        pass
                                                    else:
                                                        pu.visible = True
                                                else:
                                                    pu.visible = False

                                            if pu.casilla == c2:
                                                if totald == vdados[1] or totald == vdados[0]+vdados[1]:
                                                    if pu.casilla == 999:
                                                        pass
                                                    else:
                                                        pu.visible = True
                                                else:
                                                    pu.visible = False
                                            if pu.casilla == c3:
                                                if totald == vdados[0] + vdados[1]:
                                                    if pu.casilla == 999:
                                                        pass
                                                    else:
                                                        pu.visible = True
                                                else:
                                                    pu.vidible = False
                                        f.cselec()

                        #__________________fin click en ficha 1
                        #click en ficha 2_________________
                        if pos[0]<950 and pos[0]>750:
                            if pos[1]<480 and pos[1]>420:
                                botons1 = boton2
                                botons2 = boton
                                botons3 = boton2
                                botons4 = boton2
                                select = 1
                                fic = 2
                                for f in Fichas:
                                    if f.id == jugador*4+1:
                                        if f.pasos + vdados[0] > len(camino) - 1:
                                            c1 = camino[len(camino) - 1]
                                            pasoskys1 = 0   #debo cambiar lo de las fichas, no se pueden mover infinitamente
                                        else:               #con ese totald, si algo volver a parques1funca.py
                                            c1 = camino[f.pasos + vdados[0]]
                                            pasoskys1 = vdados[0]

                                        if f.pasos + vdados[1] > len(camino) - 1:
                                            c2 = camino[len(camino) - 1]
                                            pasoskys2=0
                                        else:
                                            c2 = camino[f.pasos + vdados[1]]
                                            pasoskys2 = vdados[1]

                                        if f.pasos + vdados[0] + vdados[1] > len(camino) - 1:
                                            c3 = camino[len(camino) - 1]
                                            pasoskys3 = 0
                                        else:
                                            c3 = camino[f.pasos + vdados[0] + vdados[1]]
                                            pasoskys3 = vdados[0] + vdados[1]
                                        for pu in Puestos:
                                            if pu.casilla == c1:
                                                if totald == vdados[0] or  totald == vdados[0]+vdados[1]:
                                                    if pu.casilla == 999:
                                                        pass
                                                    else:
                                                        pu.visible = True
                                                else:
                                                    pu.visible = False

                                            if pu.casilla == c2:
                                                if totald == vdados[1] or totald == vdados[0]+vdados[1]:
                                                    if pu.casilla == 999:
                                                        pass
                                                    else:
                                                        pu.visible = True
                                                else:
                                                    pu.visible = False
                                            if pu.casilla == c3:
                                                if totald == vdados[0] + vdados[1]:
                                                    if pu.casilla == 999:
                                                        pass
                                                    else:
                                                        pu.visible = True
                                                else:
                                                    pu.vidible = False
                                        f.cselec()

                        #__________________fin click en ficha 2
                        #click en ficha 3_________________
                        if pos[0]<950 and pos[0]>750:
                            if pos[1]<555 and pos[1]>495:
                                botons1 = boton2
                                botons2 = boton2
                                botons3 = boton
                                botons4 = boton2
                                select = 1
                                fic = 3
                                for f in Fichas:
                                    if f.id == jugador*4+2:
                                        if f.pasos + vdados[0] > len(camino) - 1:
                                            c1 = camino[len(camino) - 1]
                                            pasoskys1 = 0   #debo cambiar lo de las fichas, no se pueden mover infinitamente
                                        else:               #con ese totald, si algo volver a parques1funca.py
                                            c1 = camino[f.pasos + vdados[0]]
                                            pasoskys1 = vdados[0]

                                        if f.pasos + vdados[1] > len(camino) - 1:
                                            c2 = camino[len(camino) - 1]
                                            pasoskys2=0
                                        else:
                                            c2 = camino[f.pasos + vdados[1]]
                                            pasoskys2 = vdados[1]

                                        if f.pasos + vdados[0] + vdados[1] > len(camino) - 1:
                                            c3 = camino[len(camino) - 1]
                                            pasoskys3 = 0
                                        else:
                                            c3 = camino[f.pasos + vdados[0] + vdados[1]]
                                            pasoskys3 = vdados[0] + vdados[1]
                                        for pu in Puestos:
                                            if pu.casilla == c1:
                                                if totald == vdados[0] or  totald == vdados[0]+vdados[1]:
                                                    if pu.casilla == 999:
                                                        pass
                                                    else:
                                                        pu.visible = True
                                                else:
                                                    pu.visible = False

                                            if pu.casilla == c2:
                                                if totald == vdados[1] or totald == vdados[0]+vdados[1]:
                                                    if pu.casilla == 999:
                                                        pass
                                                    else:
                                                        pu.visible = True
                                                else:
                                                    pu.visible = False
                                            if pu.casilla == c3:
                                                if totald == vdados[0] + vdados[1]:
                                                    if pu.casilla == 999:
                                                        pass
                                                    else:
                                                        pu.visible = True
                                                else:
                                                    pu.vidible = False
                                        f.cselec()

                        #__________________fin click en ficha 3
                        #click en ficha 4_________________
                        if pos[0]<950 and pos[0]>750:
                            if pos[1]<630 and pos[1]>570:
                                botons1 = boton2
                                botons2 = boton2
                                botons3 = boton2
                                botons4 = boton
                                select = 1
                                fic = 4
                                for f in Fichas:
                                    if f.id == jugador*4+3:
                                        if f.pasos + vdados[0] > len(camino) - 1:
                                            c1 = camino[len(camino) - 1]
                                            pasoskys1 = 0   #debo cambiar lo de las fichas, no se pueden mover infinitamente
                                        else:               #con ese totald, si algo volver a parques1funca.py
                                            c1 = camino[f.pasos + vdados[0]]
                                            pasoskys1 = vdados[0]

                                        if f.pasos + vdados[1] > len(camino) - 1:
                                            c2 = camino[len(camino) - 1]
                                            pasoskys2=0
                                        else:
                                            c2 = camino[f.pasos + vdados[1]]
                                            pasoskys2 = vdados[1]

                                        if f.pasos + vdados[0] + vdados[1] > len(camino) - 1:
                                            c3 = camino[len(camino) - 1]
                                            pasoskys3 = 0
                                        else:
                                            c3 = camino[f.pasos + vdados[0] + vdados[1]]
                                            pasoskys3 = vdados[0] + vdados[1]
                                        for pu in Puestos:
                                            if pu.casilla == c1:
                                                if totald == vdados[0] or  totald == vdados[0]+vdados[1]:
                                                    if pu.casilla == 999:
                                                        pass
                                                    else:
                                                        pu.visible = True
                                                else:
                                                    pu.visible = False

                                            if pu.casilla == c2:
                                                if totald == vdados[1] or totald == vdados[0]+vdados[1]:
                                                    if pu.casilla == 999:
                                                        pass
                                                    else:
                                                        pu.visible = True
                                                else:
                                                    pu.visible = False
                                            if pu.casilla == c3:
                                                if totald == vdados[0] + vdados[1]:
                                                    if pu.casilla == 999:
                                                        pass
                                                    else:
                                                        pu.visible = True
                                                else:
                                                    pu.vidible = False
                                        f.cselec()

                        #__________________fin click en ficha 4
                    else:#aca entra despues del primer click
                        if fic == 1:
                            #click en ficha 1_________________
                            if pos[0]<950 and pos[0]>750:
                                if pos[1]<405 and pos[1]>345:
                                    botons1 = boton
                                    botons2 = boton
                                    botons3 = boton
                                    botons4 = boton
                                    select = 0
                                    fic = 0
                                    pasoskys = 0
                                    for f in Fichas:
                                        if f.id == jugador*4:
                                            for pu in Puestos:
                                                pu.visible = False
                                            f.cselec()

                            #__________________fin click en ficha 1
                            #click en ficha 2_________________
                        if fic == 2:
                            if pos[0]<950 and pos[0]>750:
                                if pos[1]<480 and pos[1]>420:
                                    botons1 = boton
                                    botons2 = boton
                                    botons3 = boton
                                    botons4 = boton
                                    select = 0
                                    fic = 0
                                    pasoskys = 0
                                    for f in Fichas:
                                        if f.id == jugador*4+1:
                                            for pu in Puestos:
                                                pu.visible = False
                                            f.cselec()

                            #__________________fin click en ficha 2
                            #click en ficha 3_________________
                        if fic == 3:
                            if pos[0]<950 and pos[0]>750:
                                if pos[1]<555 and pos[1]>495:
                                    botons1 = boton
                                    botons2 = boton
                                    botons3 = boton
                                    botons4 = boton
                                    select = 0
                                    fic = 0
                                    pasoskys = 0
                                    for f in Fichas:
                                        if f.id == jugador*4+2:
                                            for pu in Puestos:
                                                pu.visible = False
                                            f.cselec()
                        if fic == 4:
                            if pos[0]<950 and pos[0]>750:
                                if pos[1]<630 and pos[1]>570:
                                    botons1 = boton
                                    botons2 = boton
                                    botons3 = boton
                                    botons4 = boton
                                    select = 0
                                    fic = 0
                                    pasoskys = 0
                                    for f in Fichas:
                                        if f.id == jugador*4+3:
                                            for pu in Puestos:
                                                pu.visible = False
                                            f.cselec()

                            #__________________fin click en ficha 3
                            #click en ficha 4_________________


                            #___________________fin de click ficha 4
                    for pu in Puestos:
                        if salida[jugador] == 5:
                            if pu.rect.x < pos[0] and pu.rect.x+16 > pos[0]:
                                if pu.rect.y < pos[1] and pu.rect.y+16 > pos[1]:
                                    if pu.visible:
                                        pu.visible = not pu.visible
                                        npos = [pu.rect.x,pu.rect.y]
                                        print npos
                                        print pu.casilla
                                        if pu.casilla == c1:
                                            casi = c1
                                            pasoskys = pasoskys1
                                            cassel = c1
                                        if pu.casilla == c2:
                                            casi = c2
                                            pasoskys = pasoskys2
                                            cassel = c2
                                        if pu.casilla == c3:
                                            casi = c3
                                            pasoskys = pasoskys3
                                            totald = 0
                                            cassel = 0

            #_________________________fin de evento click derecho
        #______________________FIN EVENTO CLICK DE MOUSE

#GESTION DEL JUEGO___________________________________________________________________
                #Lanzamiento de dados, obtencion de valor de ellos_________
        if lanzamiento == [1,1]:
            print "lanzando"
            for d in Dados:
                if d.lanzar == 0:
                    terminado.append(1)
                else:
                    terminado.append(0)
            t = terminado
            for e in t:
                if e == 0:
                    terminado = []
            if terminado == [1,1]:
                print "\nterminado"
                finito = 1
                auxdados = 0
                for d in Dados:
                    if d.lanzar == 0:
                        vdados[auxdados] = d.con+1
                        auxdados=auxdados+1
                print vdados
                totald = vdados[0] + vdados[1]
                if vdados[0] == vdados[1]:
                    if salida[jugador] != 5:
                        salida[jugador] = 1
                    else:
                        repetir = 1
                    lanzamiento = []
                    terminado = []
                else:
                    lanzamiento = []
                    terminado = []
                    repetir = 0
            else:
                finito = 0
                #_________________________fin del lanzamiento de los dados

                #inicio configuraciones de salida de carcel primer vez_____
        if salida[jugador] == 1:
            for f in Fichas:
                if f.id == jugador*4:
                    cassig = obtenersiguiente(camino, f.casillaas)
                    f.casillaa = f.casillaas
                    f.casillaas = cassig
                    encontrado = 0
                    aux = []
                    for pu in Puestos:
                        if f.casillaa == pu.casilla:
                            if encontrado == 0:
                                aux = pu.ubicar()
                                pu.ficha = f.id
                                if aux == [0,0]:
                                    pass
                                else:
                                    encontrado = 1
                                    f.mover(aux)
                                    f.pasos = 5
                                    salida[jugador] = 5
                if f.id == jugador*4+1:
                    cassig = obtenersiguiente(camino, f.casillaas)
                    f.casillaa = f.casillaas
                    f.casillaas = cassig
                    encontrado = 0
                    aux = []
                    for pu in Puestos:
                        if f.casillaa == pu.casilla:
                            if encontrado == 0:
                                aux = pu.ubicar()
                                pu.ficha = f.id
                                if aux == [0,0]:
                                    pass
                                else:
                                    encontrado = 1
                                    f.mover(aux)
                                    f.pasos = 5
                                    salida[jugador] = 5
                if f.id == jugador*4+2:
                    cassig = obtenersiguiente(camino, f.casillaas)
                    f.casillaa = f.casillaas
                    f.casillaas = cassig
                    encontrado = 0
                    aux = []
                    for pu in Puestos:
                        if f.casillaa == pu.casilla:
                            if encontrado == 0:
                                aux = pu.ubicar()
                                pu.ficha = f.id
                                if aux == [0,0]:
                                    pass
                                else:
                                    encontrado = 1
                                    f.mover(aux)
                                    f.pasos = 5
                                    salida[jugador] = 5
                if f.id == jugador*4+3:
                    cassig = obtenersiguiente(camino, f.casillaas)
                    f.casillaa = f.casillaas
                    f.casillaas = cassig
                    encontrado = 0
                    aux = []
                    for pu in Puestos:
                        if f.casillaa == pu.casilla:
                            if encontrado == 0:
                                aux = pu.ubicar()
                                pu.ficha = f.id
                                if aux == [0,0]:
                                    pass
                                else:
                                    encontrado = 1
                                    f.mover(aux)
                                    f.pasos = 5
                                    salida[jugador] = 5
            habil = 1
            movee = 0
            cassel = 0
            if repetir == 0:
                if jugador == 3:
                    jugador = 0
                else:
                    jugador = jugador + 1
            if jugador == 0:
                cuadro = pygame.transform.scale(ficha_amarilla,(50, 50))
                camino = camarillo
            if jugador == 1:
                cuadro = pygame.transform.scale(ficha_azul,(50, 50))
                camino = cazul
            if jugador == 2:
                cuadro = pygame.transform.scale(ficha_verde,(50, 50))
                camino = cverde
            if jugador == 3:
                cuadro = pygame.transform.scale(ficha_roja,(50, 50))
                camino = crojo

                #_____________________________fin configuraciones de salida

        if salida[jugador] == 5 :
            #salida igual a 5 indica que el jugador esta en moviendose entre puestos de casillas
            if finito == 1:
                if movee == 1:
                    for f in Fichas:
                        if fic == 0:
                            casi = 0
                        elif fic == 1:
                            if f.id == jugador*4:
                                if casi == 1000:
                                    pass
                                else:
                                    if npos == [0,0]:
                                        pass
                                    else:
                                        f.casillaa = casi

                                        print casi
                                        print "todo bien"

                                        f.casillaas = obtenersiguiente(camino, f.casillaa)
                                        f.mover(npos)
                                        f.pasos = f.pasos + pasoskys

                                        pasoskys = 0
                                        f.selec = 0
                                        fic = 0
                                        npos = [0,0]
                                        casi = 1000
                                        if totald == 0:
                                            habil = 1
                                            movee = 0
                                            cassel = 0
                                            if repetir == 0:
                                                if jugador == 3:
                                                    jugador = 0
                                                else:
                                                    jugador = jugador + 1
                                            if jugador == 0:
                                                cuadro = pygame.transform.scale(ficha_amarilla,(50, 50))
                                                camino = camarillo
                                            if jugador == 1:
                                                cuadro = pygame.transform.scale(ficha_azul,(50, 50))
                                                camino = cazul
                                            if jugador == 2:
                                                cuadro = pygame.transform.scale(ficha_verde,(50, 50))
                                                camino = cverde
                                            if jugador == 3:
                                                cuadro = pygame.transform.scale(ficha_roja,(50, 50))
                                                camino = crojo
                                        else:
                                            if cassel == c1:
                                                totald = totald - vdados[0]
                                                if totald == 0:
                                                    habil = 1
                                                    movee = 0
                                                    cassel = 0
                                                    if repetir == 0:
                                                        if jugador == 3:
                                                            jugador = 0
                                                        else:
                                                            jugador = jugador + 1
                                                    if jugador == 0:
                                                        cuadro = pygame.transform.scale(ficha_amarilla,(50, 50))
                                                        camino = camarillo
                                                    if jugador == 1:
                                                        cuadro = pygame.transform.scale(ficha_azul,(50, 50))
                                                        camino = cazul
                                                    if jugador == 2:
                                                        cuadro = pygame.transform.scale(ficha_verde,(50, 50))
                                                        camino = cverde
                                                    if jugador == 3:
                                                        cuadro = pygame.transform.scale(ficha_roja,(50, 50))
                                                        camino = crojo
                                            else:
                                                totald = totald - vdados[1]
                                                if totald == 0:
                                                    habil = 1
                                                    movee = 0
                                                    cassel = 0
                                                    if repetir == 0:
                                                        if jugador == 3:
                                                            jugador = 0
                                                        else:
                                                            jugador = jugador + 1
                                                    if jugador == 0:
                                                        cuadro = pygame.transform.scale(ficha_amarilla,(50, 50))
                                                        camino = camarillo
                                                    if jugador == 1:
                                                        cuadro = pygame.transform.scale(ficha_azul,(50, 50))
                                                        camino = cazul
                                                    if jugador == 2:
                                                        cuadro = pygame.transform.scale(ficha_verde,(50, 50))
                                                        camino = cverde
                                                    if jugador == 3:
                                                        cuadro = pygame.transform.scale(ficha_roja,(50, 50))
                                                        camino = crojo
                        elif fic == 2:
                            if f.id == jugador*4 + 1:
                                if casi == 1000:
                                    pass
                                else:
                                    if npos == [0,0]:
                                        pass
                                    else:
                                        f.casillaa = casi

                                        print casi
                                        print "todo bien"

                                        f.casillaas = obtenersiguiente(camino, f.casillaa)
                                        f.mover(npos)
                                        f.pasos = f.pasos + pasoskys

                                        pasoskys = 0
                                        f.selec = 0
                                        fic = 0
                                        npos = [0,0]
                                        casi = 1000
                                        if totald == 0:
                                            habil = 1
                                            movee = 0
                                            cassel = 0
                                            if repetir == 0:
                                                if jugador == 3:
                                                    jugador = 0
                                                else:
                                                    jugador = jugador + 1
                                            if jugador == 0:
                                                cuadro = pygame.transform.scale(ficha_amarilla,(50, 50))
                                                camino = camarillo
                                            if jugador == 1:
                                                cuadro = pygame.transform.scale(ficha_azul,(50, 50))
                                                camino = cazul
                                            if jugador == 2:
                                                cuadro = pygame.transform.scale(ficha_verde,(50, 50))
                                                camino = cverde
                                            if jugador == 3:
                                                cuadro = pygame.transform.scale(ficha_roja,(50, 50))
                                                camino = crojo
                                        else:
                                            if cassel == c1:
                                                totald = totald - vdados[0]
                                                if totald == 0:
                                                    habil = 1
                                                    movee = 0
                                                    cassel = 0
                                                    if repetir == 0:
                                                        if jugador == 3:
                                                            jugador = 0
                                                        else:
                                                            jugador = jugador + 1
                                                    if jugador == 0:
                                                        cuadro = pygame.transform.scale(ficha_amarilla,(50, 50))
                                                        camino = camarillo
                                                    if jugador == 1:
                                                        cuadro = pygame.transform.scale(ficha_azul,(50, 50))
                                                        camino = cazul
                                                    if jugador == 2:
                                                        cuadro = pygame.transform.scale(ficha_verde,(50, 50))
                                                        camino = cverde
                                                    if jugador == 3:
                                                        cuadro = pygame.transform.scale(ficha_roja,(50, 50))
                                                        camino = crojo
                                            else:
                                                totald = totald - vdados[1]
                                                if totald == 0:
                                                    habil = 1
                                                    movee = 0
                                                    cassel = 0
                                                    if repetir == 0:
                                                        if jugador == 3:
                                                            jugador = 0
                                                        else:
                                                            jugador = jugador + 1
                                                    if jugador == 0:
                                                        cuadro = pygame.transform.scale(ficha_amarilla,(50, 50))
                                                        camino = camarillo
                                                    if jugador == 1:
                                                        cuadro = pygame.transform.scale(ficha_azul,(50, 50))
                                                        camino = cazul
                                                    if jugador == 2:
                                                        cuadro = pygame.transform.scale(ficha_verde,(50, 50))
                                                        camino = cverde
                                                    if jugador == 3:
                                                        cuadro = pygame.transform.scale(ficha_roja,(50, 50))
                                                        camino = crojo
                        elif fic == 3:
                            if f.id == jugador*4+2:
                                if casi == 1000:
                                    pass
                                else:
                                    if npos == [0,0]:
                                        pass
                                    else:
                                        f.casillaa = casi

                                        print casi
                                        print "todo bien"

                                        f.casillaas = obtenersiguiente(camino, f.casillaa)
                                        f.mover(npos)
                                        f.pasos = f.pasos + pasoskys

                                        pasoskys = 0
                                        f.selec = 0
                                        fic = 0
                                        npos = [0,0]
                                        casi = 1000
                                        if totald == 0:
                                            habil = 1
                                            movee = 0
                                            cassel = 0
                                            if repetir == 0:
                                                if jugador == 3:
                                                    jugador = 0
                                                else:
                                                    jugador = jugador + 1
                                            if jugador == 0:
                                                cuadro = pygame.transform.scale(ficha_amarilla,(50, 50))
                                                camino = camarillo
                                            if jugador == 1:
                                                cuadro = pygame.transform.scale(ficha_azul,(50, 50))
                                                camino = cazul
                                            if jugador == 2:
                                                cuadro = pygame.transform.scale(ficha_verde,(50, 50))
                                                camino = cverde
                                            if jugador == 3:
                                                cuadro = pygame.transform.scale(ficha_roja,(50, 50))
                                                camino = crojo
                                        else:
                                            if cassel == c1:
                                                totald = totald - vdados[0]
                                                if totald == 0:
                                                    habil = 1
                                                    movee = 0
                                                    cassel = 0
                                                    if repetir == 0:
                                                        if jugador == 3:
                                                            jugador = 0
                                                        else:
                                                            jugador = jugador + 1
                                                    if jugador == 0:
                                                        cuadro = pygame.transform.scale(ficha_amarilla,(50, 50))
                                                        camino = camarillo
                                                    if jugador == 1:
                                                        cuadro = pygame.transform.scale(ficha_azul,(50, 50))
                                                        camino = cazul
                                                    if jugador == 2:
                                                        cuadro = pygame.transform.scale(ficha_verde,(50, 50))
                                                        camino = cverde
                                                    if jugador == 3:
                                                        cuadro = pygame.transform.scale(ficha_roja,(50, 50))
                                                        camino = crojo
                                            else:
                                                totald = totald - vdados[1]
                                                if totald == 0:
                                                    habil = 1
                                                    movee = 0
                                                    cassel = 0
                                                    if repetir == 0:
                                                        if jugador == 3:
                                                            jugador = 0
                                                        else:
                                                            jugador = jugador + 1
                                                    if jugador == 0:
                                                        cuadro = pygame.transform.scale(ficha_amarilla,(50, 50))
                                                        camino = camarillo
                                                    if jugador == 1:
                                                        cuadro = pygame.transform.scale(ficha_azul,(50, 50))
                                                        camino = cazul
                                                    if jugador == 2:
                                                        cuadro = pygame.transform.scale(ficha_verde,(50, 50))
                                                        camino = cverde
                                                    if jugador == 3:
                                                        cuadro = pygame.transform.scale(ficha_roja,(50, 50))
                                                        camino = crojo
                        elif fic == 4:
                            if f.id == jugador*4+3:
                                if casi == 1000:
                                    pass
                                else:
                                    if npos == [0,0]:
                                        pass
                                    else:
                                        f.casillaa = casi

                                        print casi
                                        print "todo bien"

                                        f.casillaas = obtenersiguiente(camino, f.casillaa)
                                        f.mover(npos)
                                        f.pasos = f.pasos + pasoskys

                                        pasoskys = 0
                                        f.selec = 0
                                        fic = 0
                                        npos = [0,0]
                                        casi = 1000
                                        if totald == 0:
                                            habil = 1
                                            movee = 0
                                            cassel = 0
                                            if repetir == 0:
                                                if jugador == 3:
                                                    jugador = 0
                                                else:
                                                    jugador = jugador + 1
                                            if jugador == 0:
                                                cuadro = pygame.transform.scale(ficha_amarilla,(50, 50))
                                                camino = camarillo
                                            if jugador == 1:
                                                cuadro = pygame.transform.scale(ficha_azul,(50, 50))
                                                camino = cazul
                                            if jugador == 2:
                                                cuadro = pygame.transform.scale(ficha_verde,(50, 50))
                                                camino = cverde
                                            if jugador == 3:
                                                cuadro = pygame.transform.scale(ficha_roja,(50, 50))
                                                camino = crojo
                                        else:
                                            if cassel == c1:
                                                totald = totald - vdados[0]
                                                if totald == 0:
                                                    habil = 1
                                                    movee = 0
                                                    cassel = 0
                                                    if repetir == 0:
                                                        if jugador == 3:
                                                            jugador = 0
                                                        else:
                                                            jugador = jugador + 1
                                                    if jugador == 0:
                                                        cuadro = pygame.transform.scale(ficha_amarilla,(50, 50))
                                                        camino = camarillo
                                                    if jugador == 1:
                                                        cuadro = pygame.transform.scale(ficha_azul,(50, 50))
                                                        camino = cazul
                                                    if jugador == 2:
                                                        cuadro = pygame.transform.scale(ficha_verde,(50, 50))
                                                        camino = cverde
                                                    if jugador == 3:
                                                        cuadro = pygame.transform.scale(ficha_roja,(50, 50))
                                                        camino = crojo
                                            else:
                                                totald = totald - vdados[1]
                                                if totald == 0:
                                                    habil = 1
                                                    movee = 0
                                                    cassel = 0
                                                    if repetir == 0:
                                                        if jugador == 3:
                                                            jugador = 0
                                                        else:
                                                            jugador = jugador + 1
                                                    if jugador == 0:
                                                        cuadro = pygame.transform.scale(ficha_amarilla,(50, 50))
                                                        camino = camarillo
                                                    if jugador == 1:
                                                        cuadro = pygame.transform.scale(ficha_azul,(50, 50))
                                                        camino = cazul
                                                    if jugador == 2:
                                                        cuadro = pygame.transform.scale(ficha_verde,(50, 50))
                                                        camino = cverde
                                                    if jugador == 3:
                                                        cuadro = pygame.transform.scale(ficha_roja,(50, 50))
                                                        camino = crojo



#______________________________________________________FIN DE GESTION DEL JUEGO

#____________________________________________________________FIN DE GESTION DE EVENTOS
#GESTION DE PANTALLA___________________________________________________________________
        pantalla.fill([220,220,220])#color de fondo
        pantalla.blit(fondo,[0,0])

        if finito == 1 and habil == 1:
            cuadro2 = boton

        else:
            cuadro2 = boton2

        if fic == 0:
            botons1 = boton
            botons2 = boton
            botons3 = boton
            botons4 = boton
            select = 0
            pasoskys = 0
            for pu in Puestos:
                pu.visible = False
        pantalla.blit(cuadro2,[800,250])

        pantalla.blit(pygame.transform.scale(botons1,(200, 60)),[749,345])
        pantalla.blit(pygame.transform.scale(botons2,(200, 60)),[749,420])
        pantalla.blit(pygame.transform.scale(botons3,(200, 60)),[749,495])
        pantalla.blit(pygame.transform.scale(botons4,(200, 60)),[749,570])

        pantalla.blit(cuadro,[750,350])
        pantalla.blit(cuadro,[750,425])
        pantalla.blit(cuadro,[750,500])
        pantalla.blit(cuadro,[750,575])

        imprimir([805,252],[0,0,0],"LANZAR")

    #DIBUJADO DE CLASES_____________________
        #update de clases_____________________
        Dados.update()

        Fichas.update()
        FichasJugador.update()
        FichasNoJugador.update()
        Puestos.update()
        #___________________fin de updates

        Dados.draw(pantalla)
        Fichas.draw(pantalla)
        FichasJugador.draw(pantalla)
        FichasNoJugador.draw(pantalla)
        Puestos.draw(pantalla)
    #____________FIN DE DIBUJADO DE CLASES
        reloj.tick(60)
        pygame.display.flip()
        gc.collect()


#        for f in Fichas:
#            FichasJugador = pygame.sprite.Group()
#            FichasNoJugador = pygame.sprite.Group()
#            if f.id == jugador*4:
#                FichasJugador.add(f)
#            elif f.id == jugador*4+1:
#                FichasJugador.add(f)
#            elif f.id == jugador*4+2:
#                FichasJugador.add(f)
#            elif f.id == jugador*4+3:
#                FichasJugador.add(f)
#            else:
#                FichasNoJugador.add(f)



#____________________________________FIN DE GESTION DE PANTALLA
#__________________________________FIN CICLO PRINCIPAL
