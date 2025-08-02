from tkinter import *

TITLE = 'PyBrowser'
HSTEP, VSTEP = 13, 18
SCROLL_STEP = 100

class Browser:
    def __init__(self) -> None:
        self.window = Tk()
        self.window.title(TITLE)

        self.canvas = Canvas(self.window)
        self.canvas.pack(expand=True, fill="both")

        self.scrollbar = Scrollbar(self.canvas)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.scroll: int = 0
        self.content: str
        self.documentHeight: int

        self.canvas.bind("<Configure>", self.onResize)
        self.window.bind("<Button-5>", self.scrollDown)      # <Button-5> for using the mouse wheel in linux
        self.window.bind("<Button-4>", self.scrollUp)        # <Button-4> for using the mouse wheel in linux
        self.window.bind("<MouseWheel>", self.onMouseWheel)  # <MouseWheel> only works on Windows/MacOS
        self.window.bind("<Down>", self.scrollDown)
        self.window.bind("<Up>", self.scrollUp)

    def __render(self) -> None:
        self.canvas.delete("all")

        document = self.__layout()
        canvasHeight = self.canvas.winfo_height()

        for x, y, paragraph in document:
            if y > self.scroll + canvasHeight: continue
            if y + VSTEP < self.scroll: continue

            # y = y + (VSTEP * 1.5)
            self.canvas.create_text(x, y - self.scroll, text=paragraph)

        self.__updateScrollbar(canvasHeight)

    def __layout(self) -> list:
        display_list = []

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        cursor_x, cursor_y = HSTEP, VSTEP

        for character in self.content:
            display_list.append((cursor_x, cursor_y, character))
            cursor_x += HSTEP
            if cursor_x >= width - HSTEP:
                cursor_y += VSTEP
                cursor_x = HSTEP

        self.documentHeight = cursor_y + VSTEP
        return display_list

    def __updateScrollbar(self, canvasHeight: int) -> None:
        if self.documentHeight <= canvasHeight: 
            self.scrollbar.pack_forget()                # If document fits on screen remove scrollbar
        else:
            self.scrollbar.pack(side=RIGHT, fill=Y)

    def load(self, content: str) -> None:
        self.content = content
        self.__render()
        self.window.mainloop()

    def onMouseWheel(self, event) -> None:
        direction = -1 if event.delta < 0 else 1
        self.scroll += direction * SCROLL_STEP
        self.__render()

    def onResize(self, event) -> None:
        self.__render()

    def scrollDown(self, event) -> None:
        self.scroll += SCROLL_STEP
        self.__render()

    def scrollUp(self, event) -> None:
        if 0 >= self.scroll: self.scroll = 0
        else: self.scroll -= SCROLL_STEP
        self.__render()
