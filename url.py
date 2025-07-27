import socket

class URL:
    def __init__(self, url: str) -> None:
        self.schema, url = url.split('://', 1)
        assert self.schema == "http"

        self.host, url = url.split('/', 1)
        self.path = '/' + url

    def request(self):
        s = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP
        )

        s.connect((self.host, 8080))

        request = "GET {} HTTP/1.0\r\n".format(self.path)
        request += "Host: {}\r\n".format(self.host)
        request += "\r\n"
        s.send(request.encode("utf8"))

        response = s.makefile(mode='r', encoding='utf8', newline='\r\n')
        statusline = response.readline()
        version, status, explenation = statusline.split(" ", 2)

        response_headers = {}
        while True:
            line = response.readline()
            if line == "\r\n": break
            header, value = line.split(":", 1)
            response_headers[header.casefold()] = value.strip()

        assert 'transfer-encoding' not in response_headers
        assert 'content-encoding' not in response_headers

        content = response.read()
        s.close()
        return content

    def show(self, body):
        in_tag = False
        for char in body:
            if char == "<":
                in_tag = True
            elif char == ">":
                in_tag = False
            elif not in_tag:
                print(char, "")

    def load(self):
        body = self.request()
        self.show(body)

