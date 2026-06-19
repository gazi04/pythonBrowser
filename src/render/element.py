from typing import List, Optional


class Element:
    def __init__(self, tag: str, attributes: List, parent: Optional[str] = None) -> None:
        self.tag: str = tag
        self.parent = parent
        self.children: List = []
        self.attributes: List = attributes

    def __repr__(self) -> str:
        return "<" + self.tag + ">"
