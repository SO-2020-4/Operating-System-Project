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
        result=matrix1*matrix2
        """
        for i in range(len(matrix)):
            if(i == 0):
                result = matrix[i]
            else:
                result =  np.dot(result, matrix[i])
        """
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
    """
    def schedulerOld(self, listMatrix, listMatrix2):      

        for i in range(len(listMatrix)):
            matrix1 = listMatrix[i]
            matrix2 = listMatrix2[i]
           
            if(self.mutex1.locked()==False):
                t1 = Thread(target = self.threaded, args = (matrix1, matrix2, self.mutex1))
                t1.start()
            elif(self.mutex2.locked()==False):
                t2 = Thread(target = self.threaded, args = (matrix1, matrix2, self.mutex2))
                t2.start()
            elif(self.mutex3.locked()==False):
                t3 = Thread(target = self.threaded, args = (matrix1, matrix2, self.mutex3))
                t3.start()
            else:
                print("\nTudo ocupado")
    """
    def scheduler(self, matrixDecoded, mutex, timeThread):
        q = queue.Queue()
        t = Thread(target= self.threaded, args= (matrixDecoded[0],matrixDecoded[1], mutex, timeThread,q))
        t.start()
        return q.get()