import numpy as np, socket, pickle

class Client:
    def __init__(self, name):
        self.name = name
        self.matrixlist = []
        self.host='127.0.0.1'
        self.port=5004
        
        
    def create_matrix(self, numRow, numCol, numMatrix):
        for i in range(numMatrix):
            m1=np.random.randint(2, size = (numRow, numCol))
            m2=np.random.randint(2, size = (numRow, numCol))
            self.matrixlist.append([m1,m2])

    def connect_to_serve(self): 
    	        
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
        s.connect((self.host,self.port))         
        print('conectado')
        
        while True: 
            matrixEncoded = pickle.dumps( self.matrixlist )
            s.sendall(matrixEncoded)
      
            # messaga received from server 
            #data = s.recv(4096)
            #dataDecoded = pickle.loads(data)

            # print the received message 
            # here it would be a reverse of sent message 
            #print('Received from the server :', str(dataDecoded)) 
      
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
    cliente1.create_matrix(3, 3, 15)
    
    cliente1.connect_to_serve()