import threading
import random


class MyThread(threading.Thread):
    def __init__(self, o, x, y):
        super(MyThread, self).__init__()
        self.op = o
        self.a = x
        self.b = y
        self.total = 0

    def run(self):
        if (self.op == 1):
            self.total = self.a+self.b
            print "El resultado de sumar "+str(self.a)+" y "+str(self.b)+" es "+str(self.total)
        elif (self.op == 2):
            self.total = self.a-self.b
            print "El resultado de restar "+str(self.a)+" y "+str(self.b)+" es "+str(self.total)
        elif (self.op == 3):
            self.total = self.a*self.b
            print "El resultado de multiplicar "+str(self.a)+" y "+str(self.b)+" es "+str(self.total)
        elif (self.op == 4):
            self.a = float(self.a)
            self.b = float(self.b)
            self.total = self.a/self.b
            print "El resultado de dividir "+str(self.a)+" y "+str(self.b)+" es "+str("{:.5f}".format(self.total))



if __name__ == "__main__":
    threads = []

    for i in range(5):
        a = random.randrange(50)
        b = random.randrange(50)
        t = MyThread(i, a, b)
        t.start()
        threads.append(t)


    for t in threads:
        t.join()
