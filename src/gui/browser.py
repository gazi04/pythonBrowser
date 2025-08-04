from tkinter import *
from tkinter.font import Font

from src.render.layout import Layout
from src.render.render import Render

TITLE = "PyBrowser"
HSTEP, VSTEP = 13, 18
SCROLL_STEP = 100


class Browser:
    def __init__(self) -> None:
        self.window = Tk()
        self.window.title(TITLE)

        self.__setupWidgets()
        self.__setupKeyBindings()

        self.layout: Layout
        self.render: Render

        self.scroll: int = 0
        self.tokens: str
        self.document: list
        self.layoutHeight: int

    def __setupWidgets(self) -> None:
        frame = Frame(self.window)
        frame.pack(expand=True, fill=BOTH)

        self.scrollbar = Scrollbar(frame)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.canvas = Canvas(frame, yscrollcommand=self.scrollbar.set)
        self.canvas.pack(expand=True, fill=BOTH)

        self.scrollbar.config(command=self.canvas.yview)

    def __setupKeyBindings(self) -> None:
        self.canvas.bind("<Configure>", self.onResize)
        self.window.bind(
            "<Button-5>", self.__scrollDown
        )  # <Button-5> for using the mouse wheel in linux
        self.window.bind(
            "<Button-4>", self.__scrollUp
        )  # <Button-4> for using the mouse wheel in linux
        self.window.bind(
            "<MouseWheel>", self.onMouseWheel
        )  # <MouseWheel> only works on Windows/MacOS
        self.window.bind("<Down>", self.__scrollDown)
        self.window.bind("<Up>", self.__scrollUp)

    def load(self, tokens: str) -> None:
        self.tokens = tokens
        self.window.update()
        self.layout = Layout(tokens, self.canvas)
        self.render = Render(
            self.canvas, self.scrollbar, self.layout.displayList, self.layout.height
        )
        self.render.draw()
        self.window.mainloop()

    def onMouseWheel(self, event) -> None:
        direction = -1 if event.delta < 0 else 1
        self.scroll += direction * SCROLL_STEP
        self.render.draw()

    def onResize(self, event) -> None:
        if not self.tokens:
            return

        # self.window.update()
        self.layout = Layout(self.tokens, self.canvas)

        if hasattr(self, "render"):
            print("re-render")
            self.render.layout = self.layout
            self.render.draw()

    def __scrollDown(self, event) -> None:
        self.__setScrollPosition(SCROLL_STEP)

    def __scrollUp(self, event) -> None:
        self.__setScrollPosition(-SCROLL_STEP)

    def __setScrollPosition(self, delta: int) -> None:
        """Helper method to adjust the scroll position, clamping it at boundaries."""
        new_scroll = self.scroll + delta
        canvas_height = self.canvas.winfo_height()
        max_scroll = max(0, self.layout.height - canvas_height)

        self.scroll = max(0, min(new_scroll, max_scroll))
        self.render.draw()
