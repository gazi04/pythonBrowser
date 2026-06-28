from typing import List

from src.render.element import Element
from src.render.text import Text

SELF_CLOSING_TAGS = [
        "area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr",
        ]

HEAD_TAGS = [
        "base", "basefont", "bgsound", "noscript",
        "link", "meta", "title", "style", "script", 
        ]


class HtmlParser:
    def __init__(self, body: str) -> None:
        self.body: str = body
        self.unfinished: List[Element | Text] = []

    def parse(self) -> None:
        buffer: str = ""
        inTag: bool = False

        for character in self.body:
            if character == "<":
                inTag = True
                if buffer:
                    self.add_text(buffer)
                buffer = ""
            elif character == ">":
                inTag = False
                self.add_tag(buffer)
                buffer = ""
            else:
                buffer += character

        if not inTag and buffer:
            self.add_text(buffer)

        return self.finish()

    def add_text(self, text: str) -> None:
        if text.isspace() or not text:
            return

        parent = self.unfinished[-1]
        node = Text(text, parent)
        parent.children.append(node)

    def add_tag(self, tag: str) -> None:
        if tag.startswith("!"):
            return

        tag, attributes = self.get_attribute(tag)

        if tag.startswith("/"):
            if len(self.unfinished) == 1:
                return
            node = self.unfinished.pop()
            parent = self.unfinished[-1]
            parent.children.append(node)
        elif tag in SELF_CLOSING_TAGS:
            parent = self.unfinished[-1]
            node = Element(tag, parent=parent)
            parent.children.append(node)
        else:
            parent = self.unfinished[-1] if self.unfinished else None
            node = Element(tag, attributes, parent)
            self.unfinished.append(node)

    def get_attribute(self, text: str):
        parts = text.split()
        tag = parts[0].casefold()

        attributes = {}

        for attribute_pair in parts[1:]:
            if "=" in attribute_pair:
                key, value = attribute_pair.split('=', 1)

                if len(value) > 2 and value[0] in ["'", "\""]:
                    value = value[1:-1]
                attributes[key.casefold()] = value
            else:
                attributes[attribute_pair.casefold()] = ""

        return tag, attributes

    def finish(self) -> None:
        while len(self.unfinished) > 1:
            node = self.unfinished.pop()
            parent = self.unfinished[-1]
            parent.children.append(node)

        return self.unfinished.pop()
