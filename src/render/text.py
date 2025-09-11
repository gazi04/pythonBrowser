class Text:
    def __init__(self, text: str, parent) -> None:
        self.text: str = text
        self.parent = parent
        self.children: list = []

    def __repr__(self) -> str:
        return repr(self.text)
