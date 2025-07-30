import io

from enums.httpStatus import HttpStatus

class HttpResponse:
    def __init__(self, raw_response: io.BufferedReader):
        self.response: io.BufferedReader = raw_response
        self.version: str
        self.status: int
        self.explenation: str
        self.response_headers: dict
        self.html_content: str

        self.__prepareResponse(self.response)


    def __prepareResponse(self, response: io.BufferedReader) -> None:
        statusline: str = response.readline().decode()
        self.version, self.status, self.explenation = statusline.split(' ', 2)

        # split() method returns a string even though the explicit typing in the constructor need to convert it to int
        self.status = int(self.status)
        self.response_headers = self.__readHeader(response)

        assert 'transfer-encoding' not in self.response_headers
        assert 'content-encoding' not in self.response_headers
        assert 'content-length' in self.response_headers

        self.__handleHttpStatus()


    def __readHeader(self, response: str) -> dict:
        response_headers: dict = {}
        while True:
            responseLine = response.readline()
            if responseLine == b'\r\n':
                break

            responseLine = responseLine.decode()

            if ':' not in responseLine: 
                continue

            header, value = responseLine.split(':', 1)
            response_headers[header.casefold()] = value.strip()

        return response_headers

    def __handleHttpStatus(self) -> None:
        if self.status == HttpStatus.OK.value:
            content_length: int = int(self.response_headers['content-length'])
            self.html_content = self.response.read(content_length).decode()

        elif self.status == HttpStatus.MOVED_PERMANENTLY.value:
            assert 'location' in self.response_headers
            from .url import URL
            url = URL(self.response_headers['location'])
            url.load()

    def getHtmlContent(self) -> str:
        return self.html_content

    def getHeaders(self) -> dict:
        return self.response_headers
