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
        self.metadata=open(filename,'a')
        
    def write_meta_data(self,data):
        self.metadata.writelines(data)
        self.metadata.close()
        
        
    def ChooseComputer(self, matrixDecoded):
        for i in range(len(matrixDecoded)):
        
            if(self.computerA.mutex1.locked() == False): 
                print('Computador A | Mutex 1 | Matrix:'+ str(i))
                r=self.computerA.scheduler(matrixDecoded[i], self.computerA.mutex1, 15)
                print(r)
                #self.write_meta_data(['Computador A | Mutex 1 | Matrix:'+ str(i)+'\n',r])
           
                
            
            
            elif(self.computerA.mutex2.locked() == False):	
                print('Computador A | Mutex 2 | Matrix:'+ str(i))
                r=self.computerA.scheduler(matrixDecoded[i], self.computerA.mutex2, 10)
                print(r)
                #self.write_meta_data('Computador A | Mutex 2 | Matrix:'+ str(i),r)
                
            		
            elif(self.computerB.mutex1.locked() == False): 
                print('Computador B | Mutex 1')
                self.computerB.scheduler(matrixDecoded[i], self.computerB.mutex1, 10)
            
            elif(self.computerB.mutex2.locked() == False):
                print('Computador B | Mutex 2')	
                self.computerB.scheduler(matrixDecoded[i], self.computerB.mutex2, 0)
            
            elif(self.computerB.mutex3.locked() == False):
                print('Computador B | Mutex 3')
                self.computerB.scheduler(matrixDecoded[i], self.computerB.mutex3, 6)
                
            elif(self.computerC.mutex1.locked() == False): 
                print('Computador C | Mutex 1')
                self.computerC.scheduler(matrixDecoded[i], self.computerC.mutex1, 4)
                
            elif(self.computerC.mutex2.locked() == False):
                print('Computador C | Mutex 2')	
                self.computerC.scheduler(matrixDecoded[i], self.computerC.mutex2, 2)
            
            elif(self.computerC.mutex3.locked() == False):
                print('Computador C | Mutex 3')
                self.computerC.scheduler(matrixDecoded[i], self.computerC.mutex3, 1)
                                
            elif(self.computerC.mutex4.locked() == False):
                print('Computador C | Mutex 4')
                self.computerC.scheduler(matrixDecoded[i], self.computerC.mutex4, 4)
            """
        		# send back reversed string to client
        		matrixEncoded = pickle.dumps( result )
        		c.sendall(matrixEncoded) 
                # connection closed 
                c.close()
            """
    	
    def main_thread(self, c):
        result = []
    
        while True: 
            # data received from client 
            data = c.recv(8000) 
            
            if not data: 
                print('Bye') 
                				
                # lock released on exit 
                main_mutex.release() 
                break
            else:
                matrixDecoded = pickle.loads(data)
               
                self.ChooseComputer(matrixDecoded)
                
       
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
            s.close() 
    
    
if __name__ == '__main__': 

	computerA = ComputerA("192.168.0.1")
	computerB = ComputerB("192.168.0.2")
	computerC = ComputerC("192.168.0.3")

	server = Server(5004, computerA, computerB, computerC,'metadata1.txt') 
	server.BindToClient()