import socket
import ssl

from enums.ports import Port
from src.network.httpResponse import HttpResponse


class URL:
    def __init__(self, url="http://localhost:8080/browser/index.html") -> None:
        self.scheme: str
        self.host: str
        self.port: int
        self.path: str
        self.socket: socket
        self.is_file: bool = False
        self.is_data: bool = False
        self.__prepareUrl(url)

    def __prepareUrl(self, url: str) -> None:
        self.scheme, url = url.split(":", 1)
        assert self.scheme in ["http", "https", "file", "data"]
        if self.scheme != "data":
            url = url[2:]

        if self.scheme == "file":
            self.path = url
            self.is_file = True
            return
        elif self.scheme == "data":
            self.path = url
            self.is_data = True
            return

        # handles the case where the given url doens't provide the path
        if '/' in url: 
            self.host, url = url.split("/", 1)
        else: 
            self.host = url
            url = ''

        if ":" in self.host:
            self.host, port = self.host.split(":", 1)
            self.port = int(port)
        else:
            self.port = Port.HTTPS.value if self.scheme == "https" else Port.HTTP.value
        self.path = "/" + url

    def request(self) -> str:
        request: str = "GET {} HTTP/1.0\r\n".format(self.path)
        request = self.__prepareHeaders(request)

        self.socket.send(request.encode("utf8"))

        response = self.socket.makefile(mode="rb", encoding="utf8", newline="\r\n")
        response = HttpResponse(response)

        return response.getHtmlContent()

    def showContentWithoutHtml(self, html_content: str) -> None:
        """Print the html content of a response without the html tags"""
        cleaned_content: str = ""
        in_tag: bool = False
        for char in html_content:
            if char == "<":
                in_tag = True
            elif char == ">":
                in_tag = False
            elif not in_tag:
                cleaned_content += char
        print(cleaned_content.strip())

    def load(self) -> None:
        html_content = self.request()
        self.showContentWithoutHtml(html_content)

    def viewSource(self) -> None:
        print(self.request())

    def openConnection(self) -> socket:
        server = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP
        )
        server.connect((self.host, self.port))

        if self.scheme == "https":
            context = ssl.create_default_context()
            server = context.wrap_socket(server, server_hostname=self.host)

        return server
