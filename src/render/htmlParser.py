from src.render.tag import Tag
from src.render.text import Text

class HtmlParser:
    def __init__(self, body: str) -> None:
        self.body: str = body
        self.unfinished: list = []

    def parse(self) -> None:
        buffer: str = ""
        inTag: bool = False

        for character in self.body:
            print("----------------------------------")
            print(f"list={self.unfinished}")
            if character == "<":
                inTag = True
                if buffer:
                    print(f"Text={buffer}")
                    self.add_text(buffer)
                buffer = ""
            elif character == ">":
                inTag = False
                print(f"Tag={buffer}")
                self.add_tag(buffer)
                buffer = ""
            else:
                buffer += character

        if not inTag and buffer:
            self.add_text(buffer)

        return self.finish()

    def add_text(self, text: str) -> None:
        if text.isspace() or not text: return

        parent = self.unfinished[-1]
        node = Text(text, parent)
        parent.children.append(node)

    def add_tag(self, tag: str) -> None:
        if tag.startswith("!"): return

        if tag.startswith('/'):
            if len(self.unfinished) == 1: return
            node = self.unfinished.pop()
            parent =  self.unfinished[-1]
            parent.children.append(node)
        else:
            parent = self.unfinished[-1] if self.unfinished else None
            node = Tag(tag, parent)
            self.unfinished.append(node)
            if parent: 
                parent.children.append(node)

    def finish(self) -> None:
        while len(self.unfinished) > 1:
            node = self.unfinished.pop()
            parent = self.unfinished[-1]
            parent.children.append(node)

        return self.unfinished.pop()
