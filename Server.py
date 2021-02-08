import socket, time
    
from _thread import start_new_thread
import threading
    
from ComputerA import  ComputerA
from ComputerB import  ComputerB
from ComputerC import  ComputerC

import numpy as np, pickle

main_mutex = threading.Lock() 
    
class Server:

    def __init__(self, port, computerA, computerB, computerC,filename):        
        self.port = port
        self.computerA = computerA
        self.computerB = computerB
        self.computerC = computerC
        
    def write_meta_data(self,data):
        metadata= open('metadata.txt', 'a')
        metadata.write(data)
        metadata.close()
        
    def ChooseComputer(self, matrixDecoded):
        for i in range(len(matrixDecoded)):
            time.sleep(1)
            if(self.computerA.mutex1.locked() == False): 
                print('Computer A | Mutex 1 | Matrix:'+ str(i))
                result = self.computerA.scheduler(matrixDecoded[i], self.computerA.mutex1, 10)
                self.write_meta_data( '\n' + 'Computer A | Mutex 1 | Matrix:' + str(i)+ '\n' + str(result) + '\n' )
            
            elif(self.computerA.mutex2.locked() == False):	
                print('Computer A | Mutex 2 | Matrix:'+ str(i))
                result = self.computerA.scheduler(matrixDecoded[i], self.computerA.mutex2, 10)
                self.write_meta_data('\n' + 'Computer A | Mutex 2 | Matrix:' + str(i) + '\n' + str(result) + '\n' )
                
            elif(self.computerB.mutex1.locked() == False): 
                print('Computer B | Mutex 1 | Matrix:'+ str(i))
                result = self.computerB.scheduler(matrixDecoded[i], self.computerB.mutex1, 10)
                self.write_meta_data('\n' + 'Computer B | Mutex 1 | Matrix:' + str(i) + '\n' + str(result) + '\n' )

            elif(self.computerB.mutex2.locked() == False):
                print('Computer B | Mutex 2 | Matrix:'+ str(i))	
                result = self.computerB.scheduler(matrixDecoded[i], self.computerB.mutex2, 4)
                self.write_meta_data('\n' + 'Computer B | Mutex 2 | Matrix:' + str(i) + '\n' + str(result) + '\n' )
            
            elif(self.computerB.mutex3.locked() == False):
                print('Computer B | Mutex 3 | Matrix:'+ str(i))
                result = self.computerB.scheduler(matrixDecoded[i], self.computerB.mutex3, 8)
                self.write_meta_data('\n' + 'Computer B | Mutex 3 | Matrix:' + str(i) + '\n' + str(result) + '\n' )
                
            elif(self.computerC.mutex1.locked() == False): 
                print('Computer C | Mutex 1 | Matrix:'+ str(i))
                result = self.computerC.scheduler(matrixDecoded[i], self.computerC.mutex1, 8)
                self.write_meta_data('\n' + 'Computer C | Mutex 1 | Matrix:' + str(i) + '\n' + str(result) + '\n' )
                
            elif(self.computerC.mutex2.locked() == False):
                print('Computer C | Mutex 2 | Matrix:'+ str(i))	
                result = self.computerC.scheduler(matrixDecoded[i], self.computerC.mutex2, 2)
                self.write_meta_data('\n' + 'Computer C | Mutex 2 | Matrix:' + str(i) + '\n' + str(result) + '\n' )
            
            elif(self.computerC.mutex3.locked() == False):
                print('Computer C | Mutex 3 | Matrix:'+ str(i))
                result = self.computerC.scheduler(matrixDecoded[i], self.computerC.mutex3, 1)
                self.write_meta_data('\n' + 'Computer C | Mutex 3 | Matrix:' + str(i) + '\n' + str(result) + '\n' )
                                
            elif(self.computerC.mutex4.locked() == False):
                print('Computer C | Mutex 4 | Matrix:'+ str(i))
                result = self.computerC.scheduler(matrixDecoded[i], self.computerC.mutex4, 2)
                self.write_meta_data('\n' + 'Computer C | Mutex 4 | Matrix:' + str(i) + '\n' + str(result) + '\n' )
    	
    def main_thread(self, c):    
        while True: 
            data = c.recv(4096) 
            
            if not data: 
                print('Bye') 
                				
                main_mutex.release() 
                break
            else:
                matrixDecoded = pickle.loads(data)
                self.ChooseComputer(matrixDecoded)
            
                mensagem = pickle.dumps( "As matrizes foram calculadas com sucesso. Verifique o arquivo metadata" )
                c.sendall(mensagem)
        c.close()
                
       
    def BindToClient(self): 
        host = "" 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        s.bind((host, self.port)) 
        print("socket binded to port", self.port) 
        
        # put the socket into listening mode 
        s.listen(5) 
        print("socket is listening") 
        # a forever loop until client wants to exit 
        while True: 
            # lock acquired by client 
            main_mutex.acquire() 
            # establish connection with client 
            c, addr = s.accept() 
            print('Connected to :', addr[0], ':', addr[1]) 
            # Start a new thread and return its identifier 
            start_new_thread(self.main_thread, (c,)) 
            # s.close() 
    
    
if __name__ == '__main__': 
	computerA = ComputerA("192.168.0.1")
	computerB = ComputerB("192.168.0.2")
	computerC = ComputerC("192.168.0.3")

	server = Server(5004, computerA, computerB, computerC, 'metadata.txt') 
	server.BindToClient()