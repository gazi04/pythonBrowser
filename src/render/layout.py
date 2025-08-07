from tkinter import Canvas
from tkinter.font import Font

from src.render.text import Text
from src.config import HORIZONTAL_STEP, VERTICAL_STEP


class Layout:
    def __init__(self, tokens: str, canvas: Canvas) -> None:
        self.tokens = tokens
        self.canvas = canvas

        self.render_list: tuple[int, int, str, Font] = []
        self.height: int

        self.cursor_x: int = HORIZONTAL_STEP
        self.cursor_y: int = VERTICAL_STEP

        self.font_cache: dict = {}
        self.font_size: int = 12
        self.font_weight: str = "normal"
        self.font_style: str = "roman"

        self.line_height: int = self.__getFont().metrics("linespace") * 1.25
        self.space_width: int = self.__getFont().measure(" ")

        self.line_buffer: list[int, str, Font] = []

        self.__prepareLayout()

    def __prepareLayout(self) -> None:
        for token in self.tokens:
            if isinstance(token, Text):
                self.__prepareLine(token)
            elif token.tag == "br" or token.tag == "/br":
                self.__flush()
                self.cursor_y += VERTICAL_STEP
                self.cursor_x = HORIZONTAL_STEP
            elif token.tag == "p" or token.tag == "/p":
                self.__flush()
                self.cursor_y += VERTICAL_STEP
            elif token.tag == "i":
                self.font_style = "italic"
            elif token.tag == "/i":
                self.font_style = "roman"
            elif token.tag == "b":
                self.font_weight = "bold"
            elif token.tag == "/b":
                self.font_weight = "normal"
            elif token.tag == "small":
                self.font_size -= 2
            elif token.tag == "/small":
                self.font_size += 2
            elif token.tag == "big":
                self.font_size += 4
            elif token.tag == "/big":
                self.font_size -= 4
            elif token.tag == "h1":
                self.__flush()
                self.font_size += 24
                self.font_weight = "bold"
            elif token.tag == "/h1":
                self.font_size -= 24
                self.font_weight = "normal"
            elif token.tag == "h2":
                self.__flush()
                self.font_size += 20
                self.font_weight = "bold"
            elif token.tag == "/h2":
                self.font_size -= 20
                self.font_weight = "normal"
            elif token.tag == "h3":
                self.__flush()
                self.font_size += 18
                self.font_weight = "bold"
            elif token.tag == "/h3":
                self.font_size -= 18
                self.font_weight = "normal"
            elif token.tag == "h4":
                self.__flush()
                self.font_size += 16
                self.font_weight = "bold"
            elif token.tag == "/h4":
                self.font_size -= 16
                self.font_weight = "normal"
            elif token.tag == "h5":
                self.__flush()
                self.font_size += 14
                self.font_weight = "bold"
            elif token.tag == "/h5":
                self.font_size -= 14
                self.font_weight = "normal"
            elif token.tag == "h6":
                self.__flush()
                self.font_size += 12
                self.font_weight = "bold"
            elif token.tag == "/h6":
                self.font_size -= 12
                self.font_weight = "normal"

        self.height = self.cursor_y + self.line_height

    def __prepareLine(self, token) -> None:
        for word in token.text.split():
            font = self.__getFont()

            word_width = font.measure(word)

            if self.cursor_x + word_width > self.canvas.winfo_width() - HORIZONTAL_STEP:
                self.__flush()
                self.cursor_x = HORIZONTAL_STEP

            self.line_buffer.append((self.cursor_x, word, font))
            self.cursor_x += word_width + self.space_width

    def __getFont(self) -> Font:
        key = (self.font_size, self.font_weight, self.font_style)

        if key not in self.font_cache:
            self.font_cache[key] = Font(
                size=self.font_size,
                weight=self.font_weight,
                slant=self.font_style,
            )

        return self.font_cache[key]

    def __flush(self) -> None:
        if not self.line_buffer: return
        metrics = [font.metrics() for x, word, font in self.line_buffer]
        max_ascent = max([metric["ascent"] for metric in metrics])

        baseline = self.cursor_y + 1.25 * max_ascent

        for x, word, font in self.line_buffer:
            y = baseline - font.metrics("ascent")
            self.render_list.append((x, y, word, font))

        max_descent = max([metric["descent"] for metric in metrics])
        self.cursor_y = baseline + 1.25 * max_descent
        self.cursor_x = HORIZONTAL_STEP
        self.line_buffer = []
