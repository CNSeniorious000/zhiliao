class IdGenerator:
    def __init__(self):
        self.now = -1

    def since(self, existed):
        self.now = max((self.now, *(int(i, 16) for i in existed)))

    def __call__(self):
        self.now += 1
        return hex(self.now)[2:]


def get_next_id(existed):
    getter = IdGenerator()
    getter.since(existed)
    return getter()
