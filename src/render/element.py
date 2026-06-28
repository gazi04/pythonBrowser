from typing import Any, Dict, List, Optional


class Element:
    def __init__(self, tag: str, attributes: Optional[Dict[str, Any]] = None, parent: Optional[str] = None) -> None:
        self.tag: str = tag
        self.parent = parent
        self.children: List = []
        self.attributes: Dict = attributes


    def __repr__(self) -> str:
        return "<" + self.tag + ">"
