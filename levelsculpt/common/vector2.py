import math
import copy

class Vector2:
    def __init__(self, x:float, y:float):
        self.x = x
        self.y = y
    
    def __copy__(self):
        return Vector2(self.x, self.y)
        
    def __deepcopy__(self, memo):
        return self.__copy__()

    def __str__(self):
        return f'{self.x}, {self.y}'
    
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        return Vector2(self.x / scalar, self.y / scalar)
    
    def dist(self, other):
        return math.sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)
    
    def distSq(self, other):
        return (other.x - self.x) ** 2 + (other.y - self.y) ** 2
    
    def mag(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def magSq(self):
        return self.x ** 2 + self.y ** 2