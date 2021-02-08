import numpy as np, socket, pickle

class Client:
    def __init__(self, name):
        self.name = name
        self.matrix = []
        self.host='127.0.0.1'
        self.port=5004
        
        
    def create_matrix(self, numRow, numCol, numMatrix):
        for i in range(numMatrix):
            self.matrix.append(np.random.randint(2, size = (numRow, numCol)))

    def connect_to_serve(self): 
    	        
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
        s.connect((self.host,self.port))         
        print('conectado')
        message= self.name
        
        while True: 
            matrixEncoded = pickle.dumps( self.matrix )
            s.sendall(matrixEncoded)
      
            # messaga received from server 
            data = s.recv(4096)
            dataDecoded = pickle.loads(data)

            # print the received message 
            # here it would be a reverse of sent message 
            print('Received from the server :', str(dataDecoded)) 
      
            # ask the client whether he wants to continue 
            ans = input('\nDo you want to continue(y/n) :') 
            if ans == 'y': 
                continue
            else: 
                break
        # close the connection 
        s.close()
                
               
                #port_list.remove(port)
        
if __name__ == '__main__':
    
    cliente1 = Client('User1')
    cliente1.create_matrix(5, 5, 3)
    
    cliente1.connect_to_serve()