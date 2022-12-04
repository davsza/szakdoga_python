class Node:
    def __init__(self, id, type, cx, cy):
        self.id = id
        self.type = type
        self.cx = cx
        self.cy = cy

    def print(self):
        print(f"Node id: {self.id}, type: {self.type}, cx: {self.cx}, cy: {self.cy}")