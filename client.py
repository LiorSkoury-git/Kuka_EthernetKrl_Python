import socket
import xml.etree.ElementTree as ET

  
class EkiClient:
    
    def __init__(self, ip, port, timeout = 1500):
        # ip address of the EKI server
        self.ip = str(ip)
        # port of the EKI server
        self.port = int(port)
        # socket to connect to the EKI server
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # spcket timeout
        self.sock.settimeout(timeout)
        
        self.name = "eki_client"
        self.connected = False
        
    # method connect() connects to the EKI server and returns true if the connection was successful
    def connect(self):
        # setup server address
        server_address = (self.ip, self.port)
        print('connecting to {} port {}'.format(*server_address))
        # try to connect to the server
        try:
            self.sock.connect(server_address)
            print('connected')
            self.connected=True
            # return true if connection was successful
            return True
        except:
            print('connection failed')
            # return false if connection was not successful
            return False
        
    # method send_data() sends the data to the EKI server
    def send_data(self, message):
        # send data
        self.sock.sendall(message.serialize())
        print ('data was sent')
        # receive data
        data = None
        # receive data or wait for timeout
        try:
            data = self.sock.recv(1024)
        # if timeout occurs, print timeout message
        except socket.timeout:
            print('no data received within timeout time')
        # if data is received, return it
        return data
        
    # method close() closes the connection to the EKI server
    def close(self):
        print('closing socket')
        self.connected=False
        self.sock.close()

#Root element object (Sensor) 
class RootElement:
    
    def __init__(self,Name):
        self.Name = Name
        self.Element = ET.Element(self.Name)
        self.NodeCount = 0
    
    def AddNode(self,node):
        self.Element.append(node)
        self.NodeCount+=1
    
    def printXML(self):
        print(ET.tostring(self.Element))
    
    def serialize(self):
        return ET.tostring(self.Element)

# Data element object (for text and tag)
class NodeElement:
    
    def __init__(self,Data,Name,Type):
        self.Data = Data
        self.Name = Name
        self.Type = Type
    
    def getNode(self):
        node = ET.Element(self.Name)
        if self.Type == "tag":    
            node.tag = self.stringDict()
        else:    
            node.text = str(self.Data)
        return node
    
    def serialize(self):
        return ET.tostring(self.getNode())
            
    def printXML(self):
        print(ET.tostring(self.getNode()))

#construct a XML message with an action to be send by the eki_client
def constructXML(var):

    root = RootElement("Sensor")
    root.AddNode(NodeElement(var, 'Action', "text").getNode())
    return root

#construct a XML message indicating for the client to wait for the execution of the sent task
def constructWaitXML():   

    waitForResponse = RootElement("Sensor")
    waitForResponse.AddNode(NodeElement(1,"WaitForResponse","text").getNode())
    return waitForResponse

# testing the connection
if __name__ == "__main__":

    t = constructXML("X")
    print (t.printXML())

    ip = '192.168.2.1'
    port = 54600
    
    eki_client = EkiClient(ip, port)
    eki_client.connect()
    eki_client.close()


