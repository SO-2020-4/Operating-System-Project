from threading import Thread, Lock, Event
import time,queue
import numpy as np

class ComputerB:

    def __init__(self, ip):        
        self.ip = ip
        self.mutex1 = Lock()
        self.mutex2 = Lock()
        self.mutex3 = Lock()
        self.multMatrix = []

    def calculate_matrix(self, matrix1,matrix2):
        # Set server as busy
        #self.serverWorkingEvent.clear()
        result = []
        result = np.dot(matrix1, matrix2)
        
        return result

    def threaded(self, matrix1,matrix2, mutex, timeThread,q):
        mutex.acquire()
        try:        
            result = self.calculate_matrix(matrix1, matrix2)
            q.put(result)
            time.sleep(timeThread)   
        finally:
            mutex.release()
            return result
    
    def scheduler(self, matrixDecoded, mutex, timeThread):
        q = queue.Queue()
        t = Thread(target= self.threaded, args= (matrixDecoded[0],matrixDecoded[1], mutex, timeThread,q))
        t.start()
        return q.get()