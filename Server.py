import socket, time

from _thread import start_new_thread
import threading

from computer1 import  Computer1
from computer2 import  Computer2
from computer3 import  Computer3

import numpy as np, pickle

mutex = threading.Lock() 

class Server:

	def __init__(self, port, computer1, computer2, computer3):        
		self.port = port
		self.computer1 = computer1
		self.computer2 = computer2
		self.computer3 = computer3
	
	def ChooseComputer(self, c):
		result = []
		while True: 
			# data received from client 
			data = c.recv(4096) 
			if not data: 
				print('Bye') 
				
				# lock released on exit 
				mutex.release() 
				break
			else:
				matrixDecoded = pickle.loads(data)
				
				time.sleep(3)
				if(self.computer1.mutex1.locked() == False): 
					print('Computador 1 | Mutex 1')
					oi = self.computer1.scheduler(matrixDecoded, self.computer1.mutex1, 10)
					print(oi)
				elif(self.computer1.mutex2.locked() == False):	
					print('Computador 1 | Mutex 2')
					self.computer1.scheduler(matrixDecoded, self.computer1.mutex2, 2)
				elif(self.computer1.mutex3.locked() == False):
					print('Computador 1 | Mutex 3')
					self.computer1.scheduler(matrixDecoded, self.computer1.mutex3, 8)
				elif(self.computer1.mutex4.locked() == False):
					print('Computador 1 | Mutex 4')
					self.computer1.scheduler(matrixDecoded, self.computer1.mutex4, 7)
						
				elif(self.computer2.mutex1.locked() == False): 
					print('Computador 2 | Mutex 1')
					self.computer2.scheduler(matrixDecoded, self.computer2.mutex1, 5)
				elif(self.computer2.mutex2.locked() == False):
					print('Computador 2 | Mutex 2')	
					self.computer2.scheduler(matrixDecoded, self.computer2.mutex2, 2)
				elif(self.computer2.mutex3.locked() == False):
					print('Computador 2 | Mutex 3')
					self.computer2.scheduler(matrixDecoded, self.computer2.mutex3, 6)
						
				elif(self.computer3.mutex1.locked() == False): 
					print('Computador 3 | Mutex 1')
					self.computer3.scheduler(matrixDecoded, self.computer3.mutex1, 2)
				elif(self.computer3.mutex2.locked() == False):
					print('Computador 3 | Mutex 2')	
					self.computer3.scheduler(matrixDecoded, self.computer3.mutex2, 0)
			# send back reversed string to client
			matrixEncoded = pickle.dumps( result )
			c.sendall(matrixEncoded) 

		# connection closed 
		c.close() 


	def BindToClient(self): 
		host = "" 

		# reverse a port on your computer 
		# in our case it is 12345 but it 
		# can be anything 
		#port = 5003
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
		s.bind((host, self.port)) 
		print("socket binded to port", self.port) 

		# put the socket into listening mode 
		s.listen(5) 
		print("socket is listening") 

		# a forever loop until client wants to exit 
		while True: 

			# establish connection with client 
			c, addr = s.accept() 
		
			print('Connected to :', addr[0], ':', addr[1]) 

			# Start a new thread and return its identifier 
			start_new_thread(self.ChooseComputer, (c,)) 
		s.close() 


if __name__ == '__main__': 

	computer1 = Computer1("192.168.0.1")
	computer2 = Computer2("192.168.0.2")
	computer3 = Computer3("192.168.0.3")

	server = Server(5004, computer1, computer2, computer3) 
	server.BindToClient()