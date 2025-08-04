import gzip
import io

from enums.httpStatus import HttpStatus
from src.render.tag import Tag
from src.render.text import Text


class HttpResponse:
    def __init__(self, raw_response: io.BufferedReader):
        self.response: io.BufferedReader = raw_response
        self.version: str
        self.status: int
        self.explenation: str
        self.headers: dict[str, str]
        self.html_content: str

        self.__parse()

    def __parse(self) -> None:
        status_line = self.response.readline().decode()
        self.version, status, self.explanation = status_line.split(" ", 2)

        # split() method returns a string even though the explicit typing in the constructor need to convert it to int
        self.status = int(status)
        self.headers = self.__readHeader()

        if self.status == HttpStatus.OK.value:
            # length has a default value of -1, in case the content length isn't provided read() method will read the response till the end
            length = int(self.headers.get("content-length", -1))
            if (
                "content-encoding" in self.headers
                and self.headers["content-encoding"] == "gzip"
            ):
                self.html_content = gzip.decompress(self.response.read(length)).decode()
            else:
                self.html_content = self.response.read(length).decode()

    def __readHeader(self) -> dict[str, str]:
        headers: dict[str, str] = {}
        while True:
            responseLine = self.response.readline()
            if responseLine == b"\r\n":
                break

            responseLine = responseLine.decode()

            if ":" not in responseLine:
                continue

            header, value = responseLine.split(":", 1)
            headers[header.casefold()] = value.strip()

        return headers

    def tokenize(self) -> list:
        out: list = []
        buffer: str = ""
        inTag: bool = False

        for character in self.html_content:
            if character == "<":
                inTag = True
                if buffer: out.append(Text(buffer))
                buffer = ""
            elif character == ">":
                inTag = False
                out.append(Tag(buffer))
                buffer = ""
            else:
                buffer += character

        if not inTag and buffer:
            out.append(Text(buffer))

        return out

    def showContentWithoutHtml(self) -> str:
        """Print the html content of a response without the html tags"""
        cleaned_content: str = ""
        in_tag: bool = False
        for char in self.html_content:
            if char == "<":
                in_tag = True
            elif char == ">":
                in_tag = False
            elif not in_tag:
                cleaned_content += char
        return cleaned_content.strip()
