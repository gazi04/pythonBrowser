class Tag:
    def __init__(self, tag: str, parent) -> None:
        self.tag: str = tag
        self.parent = parent
        self.children: list = []

    def __repr__(self) -> str:
        return "<" + self.tag + ">"
