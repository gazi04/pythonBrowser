from tkinter import Canvas, Scrollbar
import tkinter as tk

from src.render.layout import Layout
from src.config import VERTICAL_STEP


class Render:
    def __init__(self, canvas, scrollbar, tokens) -> None:
        self.canvas: Canvas = canvas
        self.scrollbar: Scrollbar = scrollbar
        self.tokens: str = tokens
        self.layout: Layout = Layout(self.tokens, self.canvas)
        self.scroll: int = 0

    def draw(self) -> None:
        self.canvas.delete("all")

        if not self.layout.renderList:
            return

        canvasHeight = self.canvas.winfo_height()

        for x, y, word, font in self.layout.renderList:
            if y > self.scroll + canvasHeight:
                continue
            if y + VERTICAL_STEP < self.scroll:
                continue

            self.canvas.create_text(
                x, y - self.scroll, text=word, anchor="nw", font=font
            )

        self.__updateScrollbar(canvasHeight)

    def setScrollPosition(self, delta: int) -> None:
        """Helper method to adjust the scroll position, clamping it at boundaries."""
        new_scroll = self.scroll + delta
        canvas_height = self.canvas.winfo_height()
        max_scroll = max(0, self.layout.height - canvas_height)

        self.scroll = max(0, min(new_scroll, max_scroll))
        self.draw()

    def resize(self):
        if not self.tokens:
            return
        self.layout = Layout(self.tokens, self.canvas)
        self.draw()

    def __updateScrollbar(self, canvasHeight: int) -> None:
        if self.layout.height <= canvasHeight:
            self.scrollbar.pack_forget()  # If document fits on screen remove scrollbar
        else:
            self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.scrollbar.config(command=self.canvas.yview)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
