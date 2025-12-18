"""
Задание 4: Классы Студент и Аспирант.
"""

from typing import Optional, Union


class Person:
    """Базовый класс для человека."""
    
    def __init__(self, full_name: str, age: int):
        """
        Args:
            full_name (str): ФИО человека.
            age (int): Возраст человека.
        """
        self.full_name = full_name
        self.age = age
    
    def get_info(self) -> str:
        """Возвращает информацию о человеке."""
        return f"ФИО: {self.full_name}, Возраст: {self.age}"


class Student(Person):
    """Класс студента."""
    
    # Константы для стипендий
    EXCELLENT_STIPEND = 6000
    GOOD_STIPEND = 4000
    DEFAULT_STIPEND = 0
    
    def __init__(self, full_name: str, age: int, group_number: str, average_score: float):
        """
        Args:
            full_name (str): ФИО студента.
            age (int): Возраст студента.
            group_number (str): Номер группы.
            average_score (float): Средний балл (от 0 до 5).
        """
        super().__init__(full_name, age)
        
        if not 0 <= average_score <= 5:
            raise ValueError("Средний балл должен быть в диапазоне от 0 до 5")
        
        self.group_number = group_number
        self.average_score = average_score
    
    def calculate_stipend(self) -> int:
        """Вычисляет размер стипендии студента."""
        if self.average_score == 5:
            return self.EXCELLENT_STIPEND
        elif self.average_score < 5:
            return self.GOOD_STIPEND
        else:
            return self.DEFAULT_STIPEND
    
    def get_stipend_info(self) -> str:
        """Возвращает информацию о стипендии."""
        stipend = self.calculate_stipend()
        return f"Стипендия: {stipend} руб."
    
    def compare_stipend(self, other: Union['Student', 'GraduateStudent']) -> str:
        """
        Сравнивает стипендию с другим студентом/аспирантом.
        
        Returns:
            str: Результат сравнения.
        """
        my_stipend = self.calculate_stipend()
        other_stipend = other.calculate_stipend()
        
        if my_stipend > other_stipend:
            return f"{self.full_name} получает больше, чем {other.full_name}"
        elif my_stipend < other_stipend:
            return f"{self.full_name} получает меньше, чем {other.full_name}"
        else:
            return f"{self.full_name} получает столько же, сколько {other.full_name}"
    
    def __str__(self):
        return (f"Студент: {self.full_name}, "
                f"Группа: {self.group_number}, "
                f"Средний балл: {self.average_score}")


class GraduateStudent(Student):
    """Класс аспиранта."""
    
    # Константы для стипендий аспиранта
    EXCELLENT_STIPEND = 8000
    GOOD_STIPEND = 6000
    DEFAULT_STIPEND = 0
    
    def __init__(self, full_name: str, age: int, group_number: str, 
                 average_score: float, research_topic: str):
        """
        Args:
            full_name (str): ФИО аспиранта.
            age (int): Возраст аспиранта.
            group_number (str): Номер группы.
            average_score (float): Средний балл.
            research_topic (str): Тема научной работы.
        """
        super().__init__(full_name, age, group_number, average_score)
        self.research_topic = research_topic
    
    def __str__(self):
        return (f"Аспирант: {self.full_name}, "
                f"Группа: {self.group_number}, "
                f"Средний балл: {self.average_score}, "
                f"Тема работы: {self.research_topic}")


def main():
    """Демонстрация работы классов студента и аспиранта."""
    
    # Создаем студентов
    student1 = Student("Иванов Иван Иванович", 20, "ГР-101", 4.8)
    student2 = Student("Петров Петр Петрович", 21, "ГР-102", 5.0)
    
    # Создаем аспирантов
    grad_student1 = GraduateStudent("Сидорова Анна Сергеевна", 25, "АСП-201", 4.9, 
                                    "Исследование алгоритмов машинного обучения")
    grad_student2 = GraduateStudent("Козлов Алексей Дмитриевич", 26, "АСП-202", 5.0,
                                    "Разработка квантовых вычислений")
    
    people = [student1, student2, grad_student1, grad_student2]
    
    print("Информация о студентах и аспирантах:")
    print("=" * 60)
    
    for person in people:
        print(person)
        print(f"  {person.get_info()}")
        print(f"  {person.get_stipend_info()}")
        print()
    
    # Сравнение стипендий
    print("Сравнение стипендий:")
    print("-" * 40)
    
    comparisons = [
        (student1, student2),
        (grad_student1, grad_student2),
        (student1, grad_student1),
        (student2, grad_student2)
    ]
    
    for person1, person2 in comparisons:
        result = person1.compare_stipend(person2)
        print(result)


if __name__ == "__main__":
    main()