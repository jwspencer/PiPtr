import socket
import sys
import code
from io import StringIO
import contextlib
@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old

class sockInt(code.InteractiveConsole):
    def __init__(self,connection, locals=None, filename="<<<Socket>>>"):
        self.connection = connection
        code.InteractiveConsole.__init__(self,locals=locals,filename=filename)
    def write (self,data) :
        """ send the data out the socket
        """
        try:
            self.connection.sendall(bytes(data,'UTF-8'))
        except:
            self.connection.close()
            raise EOFError
    def raw_input(self,prompt) :
        self.write(prompt)
        try:
            line = self.connection.recv(1024).decode("utf-8").rstrip()
            return(line)
        except:
            print("Exception in raw input")
            self.connection.close()
            raise EOFError
    def runcode(self,code) :
        """copied from code.py with a twist to capture the output
        """
        try:
            with stdoutIO() as s:
                exec(code, self.locals)
            self.write(s.getvalue())
        except SystemExit:
            return
        except:
            self.showtraceback()
 
 
class socketPython:
    def __init__(self,locals) :
        self.locals = locals
        # Create a TCP/IP socket
        self.portNum = 62222
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to the address given on the command line
        #server_name = sys.argv[1]
        #server_address = (server_name, 10000)
        self.hostname = socket.gethostname()
        self.server_address = ('', self.portNum)
    def run(self):
        self.sock.bind(self.server_address)
        self.sock.listen(1)
        while True:
            print ('waiting for debug connection on port %d' % self.portNum)
            self.connection, client_address = self.sock.accept()
            interp = sockInt(self.connection,locals=self.locals)
            try:
                print('client connected:', client_address)
                interp.interact(banner="Hello Socket Python")
                print("interp exit")
                self.connection.close()
                #break
            except:
                print(" got exeption in run")
                self.connection.close()
                #break
            finally:
                print(" got exeption in run finally")
                self.connection.close()
                #break
    def bye(self):
        self.connection.close()
