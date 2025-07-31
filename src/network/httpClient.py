import os

from src.network.httpResponse import HttpResponse
from src.network.url import URL


class HttpClient:
    def __init__(self, max_redirects: int = 5) -> None:
        self.max_redirects: int = max_redirects

    def __buildRequest(self, url: URL) -> str:
        request: str = "GET {} HTTP/1.0\r\n".format(url.path)
        request += "Host: {}\r\n".format(url.host)
        request += "User-Agent: PyBrowser\r\n"
        request += "Connection: keep-alive\r\n"
        request += "Cache-Control: max-age=300, must-revalidate\r\n"
        request += "Accept-Encoding: gzip\r\n"
        request += "\r\n"

        return request

    def __handleFile(self, path: str) -> str:
        if os.path.exists(path) is False:
            print(f"File not found.\nPyBrowser can't find the file at {path}")
            return

        directory: list = os.listdir(path)
        for item in directory:
            # doesn't dipslay hidden folders
            if item[0] == ".":
                continue
            print(item)

    def get(self, url: str, redirect_count: int = 0) -> HttpResponse:
        if redirect_count >= self.max_redirects:
            raise Exception("Too many redirects")

        parsed_url = URL(url)

        # Handle file:// or data:// separately
        if parsed_url.is_file:
            return self.__handleFile(parsed_url.path)
        if parsed_url.is_data:
            print(parsed_url.path)
            return None

        # Make HTTP request
        sock = parsed_url.openConnection()
        request = self.__buildRequest(parsed_url)
        sock.send(request.encode("utf8"))

        response = HttpResponse(sock.makefile("rb", encoding="utf8", newline="\r\n"))

        # Handle redirects (3xx)
        if 300 <= response.status < 400 and "location" in response.headers:
            location = response.headers["location"]
            if location.startswith("/"):
                location = f"{parsed_url.scheme}://{parsed_url.host}{location}"
            return self.get(location, redirect_count + 1)

        return response
