"""
Задание 3: Иерархия классов геометрических фигур.
"""

import math
from abc import ABC, abstractmethod
from typing import Union


class Shape(ABC):
    """Абстрактный базовый класс для геометрических фигур."""
    
    @abstractmethod
    def area(self) -> float:
        """Вычисляет площадь фигуры."""
        pass
    
    @abstractmethod
    def perimeter(self) -> float:
        """Вычисляет периметр фигуры."""
        pass
    
    def area_greater_than(self, other: 'Shape') -> bool:
        """
        Сравнивает площадь текущей фигуры с другой фигурой.
        
        Returns:
            bool: True если площадь текущей фигуры больше, иначе False.
        """
        return self.area() > other.area()
    
    def perimeter_greater_than(self, other: 'Shape') -> bool:
        """
        Сравнивает периметр текущей фигуры с другой фигурой.
        
        Returns:
            bool: True если периметр текущей фигуры больше, иначе False.
        """
        return self.perimeter() > other.perimeter()


class Rectangle(Shape):
    """Класс прямоугольника."""
    
    def __init__(self, width: float, height: float):
        """
        Args:
            width (float): Ширина прямоугольника.
            height (float): Высота прямоугольника.
        """
        if width <= 0 or height <= 0:
            raise ValueError("Размеры прямоугольника должны быть положительными числами")
        self.width = width
        self.height = height
    
    def area(self) -> float:
        """Площадь прямоугольника: width * height."""
        return self.width * self.height
    
    def perimeter(self) -> float:
        """Периметр прямоугольника: 2 * (width + height)."""
        return 2 * (self.width + self.height)
    
    def __str__(self):
        return f"Прямоугольник (ширина={self.width}, высота={self.height})"


class Square(Rectangle):
    """Класс квадрата (частный случай прямоугольника)."""
    
    def __init__(self, side: float):
        """
        Args:
            side (float): Длина стороны квадрата.
        """
        super().__init__(side, side)
        self.side = side
    
    def __str__(self):
        return f"Квадрат (сторона={self.side})"


class Triangle(Shape):
    """Класс треугольника."""
    
    def __init__(self, a: float, b: float, c: float):
        """
        Args:
            a, b, c (float): Длины сторон треугольника.
        """
        if a <= 0 or b <= 0 or c <= 0:
            raise ValueError("Длины сторон треугольника должны быть положительными числами")
        
        # Проверка неравенства треугольника
        if not (a + b > c and a + c > b and b + c > a):
            raise ValueError("Треугольник с такими сторонами не существует")
        
        self.a = a
        self.b = b
        self.c = c
    
    def area(self) -> float:
        """Площадь треугольника по формуле Герона."""
        p = self.perimeter() / 2  # полупериметр
        return math.sqrt(p * (p - self.a) * (p - self.b) * (p - self.c))
    
    def perimeter(self) -> float:
        """Периметр треугольника: a + b + c."""
        return self.a + self.b + self.c
    
    def __str__(self):
        return f"Треугольник (стороны={self.a}, {self.b}, {self.c})"


class Circle(Shape):
    """Класс круга."""
    
    def __init__(self, radius: float):
        """
        Args:
            radius (float): Радиус круга.
        """
        if radius <= 0:
            raise ValueError("Радиус круга должен быть положительным числом")
        self.radius = radius
    
    def area(self) -> float:
        """Площадь круга: π * r²."""
        return math.pi * self.radius ** 2
    
    def perimeter(self) -> float:
        """Периметр круга (длина окружности): 2 * π * r."""
        return 2 * math.pi * self.radius
    
    def __str__(self):
        return f"Круг (радиус={self.radius})"


def main():
    """Демонстрация работы классов фигур."""
    shapes = [
        Square(5),
        Rectangle(4, 6),
        Triangle(3, 4, 5),
        Circle(3)
    ]
    
    print("Демонстрация работы с геометрическими фигурами:")
    print("=" * 60)
    
    # Вывод информации о каждой фигуре
    for shape in shapes:
        print(f"{shape}")
        print(f"  Площадь: {shape.area():.2f}")
        print(f"  Периметр: {shape.perimeter():.2f}")
        print()
    
    # Сравнение фигур
    print("Сравнение фигур:")
    print("-" * 40)
    
    if len(shapes) >= 2:
        shape1, shape2 = shapes[0], shapes[1]
        print(f"Сравнение {shape1} и {shape2}:")
        print(f"  Площадь {shape1} > площади {shape2}? {shape1.area_greater_than(shape2)}")
        print(f"  Периметр {shape1} > периметра {shape2}? {shape1.perimeter_greater_than(shape2)}")


if __name__ == "__main__":
    main()