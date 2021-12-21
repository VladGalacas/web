class Rectangle:

    lenght = None
    weight = None

    @staticmethod
    def area_static(a, b=None):
        if b == None:
            return a ** 2
        return a * b

    @classmethod
    def area_class(cls, a, b=None):
        if b == None:
            cls.lenght = a
            return cls.area_static(cls.lenght)
        cls.lenght = a
        cls.weight = b
        return cls.area_static(cls.lenght, cls.weight)


class Square(Rectangle):
    pass


a = Square()
print(a.area_class(4))

print(Square.area_static(5))

b = Rectangle()
print(b.area_class(3, 4))

print(Rectangle.area_static(5, 6))