# Create your models here.
class Diagram:
    def __init__(self, identifier, name, tables):
        self.id = identifier
        self.name = name
        self.tables = tables


class Table:
    def __init__(self, identifier, name, pos_x, pos_y, width, height):
        self.id = identifier
        self.name = name
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
