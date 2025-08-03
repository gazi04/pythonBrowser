from tkinter import *

TITLE = "PyBrowser"
HSTEP, VSTEP = 13, 18
SCROLL_STEP = 100


class Browser:
    def __init__(self) -> None:
        self.window = Tk()
        self.window.title(TITLE)

        self.__setupWidgets()
        self.__setupKeyBindings()

        self.scroll: int = 0
        self.content: str
        self.document: list
        self.documentHeight: int

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

    def __render(self) -> None:
        self.canvas.delete("all")

        if not self.document:
            return

        canvasHeight = self.canvas.winfo_height()

        for x, y, paragraph in self.document:
            if y > self.scroll + canvasHeight:
                continue
            if y + VSTEP < self.scroll:
                continue

            # y = y + (VSTEP * 1.5)
            self.canvas.create_text(x, y - self.scroll, text=paragraph)

        self.__updateScrollbar(canvasHeight)

    def __layout(self) -> None:
        displayList = []

        width = self.canvas.winfo_width()
        cursor_x, cursor_y = HSTEP, VSTEP

        for character in self.content:
            displayList.append((cursor_x, cursor_y, character))
            cursor_x += HSTEP
            if cursor_x >= width - HSTEP:
                cursor_y += VSTEP
                cursor_x = HSTEP

        self.documentHeight = cursor_y + VSTEP
        self.document = displayList

    def __updateScrollbar(self, canvasHeight: int) -> None:
        if self.documentHeight <= canvasHeight:
            self.scrollbar.pack_forget()  # If document fits on screen remove scrollbar
        else:
            self.scrollbar.pack(side=RIGHT, fill=Y)

        self.scrollbar.config(command=self.canvas.yview)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def load(self, content: str) -> None:
        self.content = content
        self.__layout()
        self.__render()
        self.window.mainloop()

    def onMouseWheel(self, event) -> None:
        direction = -1 if event.delta < 0 else 1
        self.scroll += direction * SCROLL_STEP
        self.__render()

    def onResize(self, event) -> None:
        self.__layout()
        self.__render()

    def __scrollDown(self, event) -> None:
        self.__setScrollPosition(SCROLL_STEP)

    def __scrollUp(self, event) -> None:
        self.__setScrollPosition(-SCROLL_STEP)

    def __setScrollPosition(self, delta: int) -> None:
        """Helper method to adjust the scroll position, clamping it at boundaries."""
        new_scroll = self.scroll + delta
        canvas_height = self.canvas.winfo_height()
        max_scroll = max(0, self.documentHeight - canvas_height)

        self.scroll = max(0, min(new_scroll, max_scroll))
        self.__render()
