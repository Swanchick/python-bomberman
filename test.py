class A:
    pos: str

    def __init__(self, pos: str):
        self.pos = pos


a = A("123")

print(getattr(a, "pos"))