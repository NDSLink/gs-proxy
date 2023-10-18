# zurgeg's magical customizable redirection proxy thing
# licensed under gpl ig
#   This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#   This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#   You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>. 
# there are a few reasons why you shouldn't use this:
# 1) it doesn't work with https
# 2) websites get confused as to why the host is different (EDIT: this is kinda fixed with replace_redirected_url = True)
# 3) Tu stultus es (this one's really important)
import socket
import threading
from uuid import uuid1
import socket

class CustomizableRedirector:
    '''
    magic redirect thingy
    '''
    def __init__(self, listen, backlog=30, recv_length=1024, redir={}, replace_redirected_url = True):
        '''
        make a magic redirect thingy
        '''
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(listen)
        self.server.listen(backlog)
        self._recv_length = recv_length
        self.redir = redir
        self.replace_redirected_url = replace_redirected_url
    def start(self):
        '''
        Do the thing!
        '''
        while True:
            (cl_sock, cl_addr) = self.server.accept() # grab the newest client
            client_thread = threading.Thread(name=str(uuid1()),
                                            target = self._handle_client, args=(cl_sock, cl_addr))
            client_thread.setDaemon(True)
            client_thread.start()
    def _handle_client(self, cl_sock, cl_addr):
        '''
        who is cl and why do we keep talking about his socks
        '''
        request = cl_sock.recv(self._recv_length)
        url = request.split(b'\n')[0].split(b' ')[1]
        http_pos = url.find(b"://") # find where the http is
        if not http_pos == -1:
            url = url[http_pos+3:] # get the address
        port_location = url.find(b":") # we need this later because sockets is a jackass and can't handle having a port and a domain in the same place
        port = url[port_location + 1:]
        try:
            port = int(port)
        except Exception as e:
            # port ain't an integer
            port = 80 # oh well let's hope this works then
            port_location = len(url) # split it at the end lol
        slash_location = url.find(b"/")
        if slash_location == -1: url = url[:port_location] 
        else:
            url = url[:slash_location]
        if self.replace_redirected_url:
            original_url = url[:] # copy url so we can replace any reference to it later
        url = self.redir.get(url, url) # get what we will actually connect to
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #print("we goin to", url, port)
        try:
            s.connect((url, port))
        except:
            print("smth ain't workin", url, port)
        if self.replace_redirected_url:
            # this makes sure the url we redirected to
            # is the one that's sent to the server
            # for instance, the browser GETs from ihateproxyprotocolso.much which redirects to example.com
            # so we replace any instance of the URL the browser sent with the redirect
            request = request.replace(original_url, url)
        s.sendall(request)
        while True:
            data = s.recv(self._recv_length)
            if len(data) > 0:
                if self.replace_redirected_url:
                    # same thing here, but inverse
                    data = data.replace(url, original_url)
                cl_sock.send(data)
            else:
                break
        s.close()
        cl_sock.close()
        del s
        del cl_sock

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80)) 
    ip_addr = s.getsockname()[0]
    s.close() # stolen from so: https://stackoverflow.com/a/166589
    print("Running zurgeg's magical customizable redirection proxy thing on 0.0.0.0:8080")
    print("i don't even know if this works")
    print("set your proxy to", ip_addr, "(might not be your real ip if you have a vpn) on port 8080")
    print("and then go to http://ihateproxyprotocolso.much and it should appear as example.com")
    redirector = CustomizableRedirector(("0.0.0.0", 8080), redir={b"ihateproxyprotocolso.much": b"example.com"})
    redirector.start()

