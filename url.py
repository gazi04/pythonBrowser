import socket
import ssl
import os

class URL:
    def __init__(self, url='http://localhost:8080/browser/index.html') -> None:
        self.__prepareUrl(url)

    def __prepareUrl(self, url) -> None:
        self.scheme, url = url.split(':', 1)
        assert self.scheme in ['http', 'https', 'file', 'data']
        if self.scheme != 'data': url = url[2:]
        if self.scheme == 'file':
            self.__handleFileSchema(url)
            return

        if self.scheme == 'data':
            self.__handleDataSchema(url)
            return

        self.__handleHttpSchema(url)

    def __prepareHeaders(self, request: str) -> str:
        request += 'Host: {}\r\n'.format(self.host)
        request += 'User-Agent: PyBrowser\r\n'
        request += 'Connection: keep-alive\r\n'
        request += '\r\n'

        return request

    def __handleFileSchema(self, path: str):
        if os.path.exists(path) == False:
            print(f"File not found.\nPyBrowser can't find the file at {path}")
            return
        
        directory = os.listdir(path)
        for item in directory:
            # DOESNT DIPSLAY HIDDEN FOLDERS
            if item[0] == '.': continue
            print(item)

    def __handleHttpSchema(self, url: str) -> None:
        self.host, url = url.split('/', 1)
        if ':' in self.host:
            self.host, port = self.host.split(':', 1)
            self.port = int(port)
        else:
            self.port = 443 if self.scheme == 'https' else 80
        self.path = '/' + url

        self.socket = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP
        )
        self.socket.connect((self.host, self.port))

        if self.scheme == 'https':
            context = ssl.create_default_context()
            self.socket = context.wrap_socket(self.socket, server_hostname=self.host)

    def __handleDataSchema(self, url: str) -> None:
        print(url)

    def request(self) -> str:

        request = 'GET {} HTTP/1.0\r\n'.format(self.path)
        request = self.__prepareHeaders(request)

        self.socket.send(request.encode('utf8'))

        response = self.socket.makefile(mode='rb', encoding='utf8', newline='\r\n')
        
        # STATUS LINE CONTAINS HTTP VERSION, STATUS AND EXPLENATION
        statusline = response.readline().decode()
        
        response_headers = {}
        while True:
            responseLine = response.readline()
            if responseLine == b'\r\n':
                break

            responseLine = responseLine.decode()

            if ':' not in responseLine: 
                continue

            header, value = responseLine.split(':', 1)
            response_headers[header.casefold()] = value.strip()


        content_length = int(response_headers['content-length'])
        body = response.read(content_length).decode()

        assert 'transfer-encoding' not in response_headers
        assert 'content-encoding' not in response_headers

        return body

    def show(self, body) -> None:
        cleaned_body = ''
        in_tag = False
        for char in body:
            if char == '<':
                in_tag = True
            elif char == '>':
                in_tag = False
            elif not in_tag:
                cleaned_body += char
        print(cleaned_body.strip())

    def load(self) -> None:
        body = self.request()
        self.show(body)

    def viewSource(self) -> None:
        print(self.request())
