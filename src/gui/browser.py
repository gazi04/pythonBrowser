from tkinter import *
from tkinter.font import Font

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

        self.render: Render

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
        self.window.update()
        self.render = Render(
            self.canvas,
            self.scrollbar,
            tokens
        )
        self.render.draw()
        self.window.mainloop()

    def onMouseWheel(self, event) -> None:
        direction = -1 if event.delta < 0 else 1
        self.render.scroll += direction * SCROLL_STEP
        self.render.draw()

    def onResize(self, event) -> None:
        # The 'render' object is initialized in the `load()` method, not the constructor.
        # However, the `onResize` function can be triggered during initialization before the `load()` method is called.
        # The 'if' condition prevents the program from crashing by checking if the 'render' object exists before attempting to resize it.      
        if hasattr(self, 'render'):
            self.render.resize()
        
    def __scrollDown(self, event) -> None:
        self.render.setScrollPosition(SCROLL_STEP)

    def __scrollUp(self, event) -> None:
        self.render.setScrollPosition(-SCROLL_STEP)
