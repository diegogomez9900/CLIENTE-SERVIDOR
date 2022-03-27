import threading

def potencia(x,y):
    b = x
    if not (y == 1):
        for a in range(1,y):
            x = x*b
    return x

class MyThread(threading.Thread):
    def __init__(self, x, y):
        super(MyThread, self).__init__()
        self.base = 2
        self.expini = x
        self.expfin = y
        self.total = 0

    def run(self):
        a = potencia(self.base, self.expini)
        b = potencia(self.base, self.expfin)
        print "el hilo tiene como total :"+str(a+b)
        self.total = a+b


if __name__ == "__main__":
    threads = []
    ini = 1
    fin = 2

    while (fin != 12):
        t = MyThread(ini, fin)
        t.start()
        threads.append(t)
        ini += 2
        fin += 2
        #print "\n\n"+str(fin)+"\n\n"

    suma = 0

    for t in threads:
        t.join()

    for i in range(5):
        suma = suma+threads[i].total
    print "\nla suma de los hilos es: "+str(suma)
