import os
import socket
import ssl

from enums.ports import Port

from .httpResponse import HttpResponse


class URL:
    def __init__(self, url='http://localhost:8080/browser/index.html') -> None:
        self.scheme: str
        self.host: str
        self.port: int
        self.path: str
        self.socket: socket
        self.__prepareUrl(url)

    def __prepareUrl(self, url: str) -> None:
        self.scheme, url = url.split(':', 1)
        assert self.scheme in ['http', 'https', 'file', 'data']
        if self.scheme != 'data': url = url[2:]

        if self.scheme == 'file':
            self.__handleFileSchema(url)
            return

        if self.scheme == 'data':
            self.__handleDataSchema(url)
            return

        # THE __handleHttpSchema METHOD HANDLES ALSO THE SECURED VERSION
        self.__handleHttpSchema(url)

    def __prepareHeaders(self, request: str) -> str:
        request += 'Host: {}\r\n'.format(self.host)
        request += 'User-Agent: PyBrowser\r\n'
        request += 'Connection: keep-alive\r\n'
        request += '\r\n'

        return request

    def __handleFileSchema(self, path: str):
        if os.path.exists(path) is False:
            print(f"File not found.\nPyBrowser can't find the file at {path}")
            return
        
        directory: list = os.listdir(path)
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
            self.port = Port.HTTPS.value if self.scheme == 'https' else Port.HTTP.value
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
        request: str = 'GET {} HTTP/1.0\r\n'.format(self.path)
        request = self.__prepareHeaders(request)

        self.socket.send(request.encode('utf8'))

        response = self.socket.makefile(mode='rb', encoding='utf8', newline='\r\n')
        response = HttpResponse(response)
        
        return response.getHtmlContent()

    def showContentWithoutHtml(self, html_content: str) -> None:
        """Print the html content of a response without the html tags"""
        cleaned_content: str = ''
        in_tag: bool = False
        for char in html_content:
            if char == '<':
                in_tag = True
            elif char == '>':
                in_tag = False
            elif not in_tag:
                cleaned_content += char
        print(cleaned_content.strip())

    def load(self) -> None:
        html_content = self.request()
        # print(body)
        self.showContentWithoutHtml(html_content)

    def viewSource(self) -> None:
        print(self.request())

