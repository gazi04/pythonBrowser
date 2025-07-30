import io

from enums.httpStatus import HttpStatus


class HttpResponse:
    def __init__(self, raw_response: io.BufferedReader):
        self.response: io.BufferedReader = raw_response
        self.version: str
        self.status: int
        self.explenation: str
        self.response_headers: dict[str, str]
        self.html_content: str

        self.__parse()

    def __parse(self) -> None:
        status_line = self.response.readline().decode()
        self.version, status, self.explanation = status_line.split(" ", 2)

        # split() method returns a string even though the explicit typing in the constructor need to convert it to int
        self.status = int(status)
        self.headers = self.__readHeader()

        if self.status == HttpStatus.OK.value:
            length = int(self.headers.get("content-length", 0))
            self.html_content = self.response.read(length).decode()

    def __readHeader(self) -> dict:
        response_headers: dict = {}
        while True:
            responseLine = self.response.readline()
            if responseLine == b"\r\n":
                break

            responseLine = responseLine.decode()

            if ":" not in responseLine:
                continue

            header, value = responseLine.split(":", 1)
            response_headers[header.casefold()] = value.strip()

        return response_headers
