from tkinter import *

HSTEP, VSTEP = 13, 18
SCROLL_STEP = 100


class Render:
    def __init__(self, canvas, scrollbar, tokens, layoutHeight) -> None:
        self.canvas: Canvas = canvas
        self.scrollbar: Scrollbar = scrollbar
        self.tokens: list = tokens
        self.scroll: int = 0
        self.layoutHeight: int = layoutHeight

    def draw(self) -> None:
        self.canvas.delete("all")

        if not self.tokens:
            return

        canvasHeight = self.canvas.winfo_height()

        for x, y, token, font in self.tokens:
            if y > self.scroll + canvasHeight:
                continue
            if y + VSTEP < self.scroll:
                continue

            self.canvas.create_text(
                x, y - self.scroll, text=token, anchor="nw", font=font
            )

        self.__updateScrollbar(canvasHeight)

    def __updateScrollbar(self, canvasHeight: int) -> None:
        if self.layoutHeight <= canvasHeight:
            self.scrollbar.pack_forget()  # If document fits on screen remove scrollbar
        else:
            self.scrollbar.pack(side=RIGHT, fill=Y)

        self.scrollbar.config(command=self.canvas.yview)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
