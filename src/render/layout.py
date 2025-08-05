from tkinter import Canvas
from tkinter.font import Font

from src.render.text import Text
from src.config import HORIZONTAL_STEP, VERTICAL_STEP


class Layout:
    def __init__(self, tokens: str, canvas: Canvas) -> None:
        self.tokens = tokens
        self.canvas = canvas

        self.renderList: tuple[int, int, str, Font] = []
        self.height: int

        self.cursor_x: int = HORIZONTAL_STEP
        self.cursor_y: int = VERTICAL_STEP

        self.fontCache: dict = {}
        self.fontSize: int = 16
        self.fontWeight: str = "normal"
        self.fontStyle: str = "roman"

        self.lineHeight: int = self.__getFont().metrics("linespace") * 1.25
        self.spaceWidth: int = self.__getFont().measure(" ")

        self.__prepareLayout()

    def __prepareLayout(self) -> None:
        for token in self.tokens:
            if isinstance(token, Text):
                self.__prepareLine(token)
            elif token.tag == "i":
                self.fontStyle = "italic"
            elif token.tag == "/i":
                self.fontStyle = "roman"
            elif token.tag == "b":
                self.fontWeight = "bold"
            elif token.tag == "/b":
                self.fontWeight = "normal"

        self.height = self.cursor_y + self.lineHeight

    def __prepareLine(self, token) -> None:
        for word in token.text.split():
            font = self.__getFont()

            wordWidth = font.measure(word)

            if self.cursor_x + wordWidth > self.canvas.winfo_width() - HORIZONTAL_STEP:
                self.cursor_y += self.lineHeight
                self.cursor_x = HORIZONTAL_STEP

            self.renderList.append((self.cursor_x, self.cursor_y, word, font))
            self.cursor_x += wordWidth + self.spaceWidth

    def __getFont(self) -> Font:
        key = (self.fontSize, self.fontWeight, self.fontStyle)

        if key not in self.fontCache:
            self.fontCache[key] = Font(
                size=self.fontSize,
                weight=self.fontWeight,
                slant=self.fontStyle,
            )

        return self.fontCache[key]
