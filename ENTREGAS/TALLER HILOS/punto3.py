import threading
import random
import math
import sys

def printvector(v):
    for i in range(len(v)):
        sys.stdout.write(str(v[i]))
        sys.stdout.write(" ")#esto es para imprimir sin el salto de linea al final del print

class MyThread(threading.Thread):
    def __init__(self, x, y):
        super(MyThread, self).__init__()
        self.u1 = x
        self.u2 = y
        self.total = 0

    def run(self):
        self.u1 = self.u1*self.u1
        self.u2 = self.u2*self.u2
        self.total = self.u1+self.u2



if __name__ == "__main__":
    threads = []
    vector = []
    for i in range(20):
        v = random.randrange(20)
        vector.append(v)
    i = 0
    while (i!=20):
        t = MyThread(vector[i], vector[i+1])
        t.start()
        threads.append(t)
        i += 2


    for t in threads:
        t.join()
    suma = 0

    for i in range(10):
        suma = suma+threads[i].total
    norma = math.sqrt(suma)
    print "La norma del vector: \n"
    printvector(vector)
    print "\n\nes "+str(norma)
