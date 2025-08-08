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

        self.tag_handlers = {
            "br": lambda: self.__breakLine,
            "/br": lambda: self.__breakLine,
            "p": lambda: self.__paragraphBreak,
            "/p": lambda: self.__paragraphBreak,
            "i": lambda: self.__setFontStyle("italic"),
            "/i": lambda: self.__setFontStyle("roman"),
            "b": lambda: self.__setFontWeight("bold"),
            "/b": lambda: self.__setFontWeight("normal"),
            "big": lambda: self.__setFontSize(4),
            "/big": lambda: self.__setFontSize(-4),
            "small": lambda: self.__setFontSize(-2),
            "/small": lambda: self.__setFontSize(2),
            "h1": lambda: self.__setHeading(24),
            "/h1": lambda: self.__resetHeading(24),
            "h2": lambda: self.__setHeading(20),
            "/h2": lambda: self.__resetHeading(20),
            "h3": lambda: self.__setHeading(18),
            "/h3": lambda: self.__resetHeading(18),
            "h4": lambda: self.__setHeading(16),
            "/h4": lambda: self.__resetHeading(16),
            "h5": lambda: self.__setHeading(14),
            "/h5": lambda: self.__resetHeading(14),
            "h6": lambda: self.__setHeading(12),
            "/h6": lambda: self.__resetHeading(12),
        }

        self.__prepareLayout()

    def __prepareLayout(self) -> None:
        for token in self.tokens:
            if isinstance(token, Text):
                self.__prepareLine(token)
            elif token.tag in self.tag_handlers:
                self.tag_handlers[token.tag]()

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

    def __setFontSize(self, size: int) -> None:
        self.font_size += size

    def __setFontWeight(self, weight: str) -> None:
        self.font_weight = weight

    def __setFontStyle(self, style: str) -> None:
        self.font_style = style

    def __breakLine(self) -> None:
        self.__flush()
        self.cursor_y += VERTICAL_STEP
        self.cursor_x = HORIZONTAL_STEP

    def __paragraphBreak(self) -> None:
        self.__flush()
        self.cursor_y += VERTICAL_STEP

    def __setHeading(self, size: int) -> None:
        self.__flush()
        self.__setFontSize(size)
        self.__setFontWeight("bold")

    def __resetHeading(self, size: int):
        self.__setFontSize(-size)
        self.__setFontWeight("normal")
