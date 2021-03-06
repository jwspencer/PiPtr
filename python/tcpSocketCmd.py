import socket
import sys
import threading
class tcpSocketCmd:
    def __init__(self,dict,q1,q2) :
        self.dict = dict
        self.q1 = q1
        self.q2 = q2
        self.portNum = 10100
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the address given on the command line
        self.hostname = socket.gethostname()
        self.server_address = ('', self.portNum)
        print ('starting up on %s port %s' % self.server_address)
        self.sock.bind(self.server_address)
        self.sock.listen(1)
    def getDict(self,startDict,path) :
        dict = startDict
        pathlist = path.split('.')
        while(len(pathlist) > 1) :
            dict = dict[pathlist.pop(0)].__dict__
        return(dict[pathlist.pop(0)])

    def setDict(self,startDict,path,value) :
        dict = startDict
        pathlist = path.split('.')
        while(len(pathlist) > 1) :
            dict = dict[pathlist.pop(0)].__dict__
        dict[pathlist.pop(0)] = value

    def isDict(self,startDict,path) :
        dict = startDict
        pathlist = path.split('.')
        while(len(pathlist) > 1) :
            dict = dict[pathlist.pop(0)].__dict__
        return(pathlist.pop(0) in dict)



    def run(self):
        while True:
            print ('waiting for a command line connection on port %d' % self.portNum)
            connection, client_address = self.sock.accept()
            try:
                print('client connected:', client_address)
                while True:
                    data = connection.recv(1024).decode("utf-8")
                    print ('received "%s"' % data)
                    if data:
                        words = data.split()
                        if(len(words) == 0) :
                            response = '?'
                        elif(words[0] == '?' or words[0] == 'h' or words[0] == 'help') :
                            response = 'cmd one of the following\n'
                            response = response + 'get <variable>\n'
                            response = response + 'set <variable> <value>\n'
                            response = response + 'tt <port> <sequence>\n'
                            response = response + 'save\n'
                            response = response + 'bye\n'
                        elif(words[0] == 'get') :
                            if(self.isDict(self.dict,words[1])):
                                result = self.getDict(self.dict,words[1])
                                response = str(result)
                            else:
                                response = 'Not Found'
                        elif(words[0] == 'set') : 
                            if(self.isDict(self.dict,words[1])):
                                result = self.getDict(self.dict,words[1])
                                response = 'OK was ' + str(result)
                                self.setDict(self.dict,words[1], words[2])
                            else:
                                response = 'Not Found'
                        elif(words[0] == 'tt') : 
                            if(words[1] == '1') :
                                self.q1.put(words[2])
                                self.q1.put(' ')
                                response = 'sent ' + words[2] + ' to port ' + words[1]
                            elif(words[1] == '2') :
                                self.q2.put(words[2])
                                self.q2.put(' ')
                                response = 'sent ' + words[2] + ' to port ' + words[1]
                            else:
                                response = "No such port %s must be either 1 or 2" % words[1]
                        elif(words[0] == 'save') :
                            f = self.dict['gui'].guiSave()
                            response = ("saved: %s" % f) 
                        elif(words[0] == 'bye') :
                            connection.close()
                            break
                        else :
                            response = "unknown command: %s"  % data
                        print("sending response: " + response)
                        response = response + "\n"
                        connection.sendall(bytes(response, 'UTF-8'))
                    else:
                        break
            finally:
                connection.close()
