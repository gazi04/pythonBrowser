from tkinter import Canvas
from tkinter.font import Font

from src.render.text import Text

HORIZONTAL_STEP, VERTICAL_STEP = 13, 18


class Layout:
    def __init__(self, tokens: str, canvas: Canvas) -> None:
        self.tokens = tokens
        self.canvas = canvas
        self.displayList = []
        self.height: int
        self.__prepareLayout()

    def __prepareLayout(self) -> None:
        canvasWidth = self.canvas.winfo_width()
        weight: str = "normal"
        style: str = "roman"

        lineHeight = Font().metrics("linespace") * 1.25
        spaceWidth = Font().measure(" ")

        cursor_x, cursor_y = HORIZONTAL_STEP, VERTICAL_STEP

        for token in self.tokens:
            if isinstance(token, Text):
                cursor_x, cursor_y = self.__prepareLine(
                    token,
                    cursor_x,
                    cursor_y,
                    weight,
                    style,
                    lineHeight,
                    spaceWidth,
                    canvasWidth,
                )
            elif token.tag == "i":
                style = "italic"
            elif token.tag == "/i":
                style = "roman"
            elif token.tag == "b":
                weight = "bold"
            elif token.tag == "/b":
                weight = "normal"

        self.height = cursor_y + lineHeight

    def __prepareLine(
        self,
        token,
        cursor_x,
        cursor_y,
        weight,
        style,
        lineHeight,
        spaceWidth,
        canvasWidth,
    ) -> tuple[int, int]:
        for word in token.text.split():
            font = Font(
                size=16,
                weight=weight,
                slant=style,
            )
            wordWidth = font.measure(word)

            if cursor_x + wordWidth > canvasWidth - HORIZONTAL_STEP:
                cursor_y += lineHeight
                cursor_x = HORIZONTAL_STEP

            self.displayList.append((cursor_x, cursor_y, word, font))
            cursor_x += wordWidth + spaceWidth

        return cursor_x, cursor_y
