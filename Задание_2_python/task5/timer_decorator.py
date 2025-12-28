"""
Задание 5: Декоратор для измерения времени выполнения функции.
"""

import time
import os
from functools import wraps
from typing import Callable, Any


def timer_decorator(func: Callable) -> Callable:
    """
    Декоратор, который измеряет время выполнения функции.
    
    Args:
        func (Callable): Декорируемая функция.
        
    Returns:
        Callable: Обернутая функция с измерением времени.
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.perf_counter()
        
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            print(f"Функция '{func.__name__}' выполнилась за {execution_time:.6f} секунд")
    
    return wrapper


# 1. Функция сложения двух чисел
@timer_decorator
def add_numbers(a: float, b: float) -> float:
    """Складывает два числа и выводит результат в консоль."""
    result = a + b
    print(f"{a} + {b} = {result}")
    return result


# 2. Функция чтения из файла, сложения и записи в файл
@timer_decorator
def process_file() -> None:
    """
    Читает числа из файла, складывает их и записывает результат в другой файл.
    """
    # Используем абсолютный путь для надежности
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(current_dir, "input.txt")
    output_file = os.path.join(current_dir, "output.txt")
    
    print(f"Ищу input.txt в директории: {current_dir}")
    print(f"Полный путь: {input_file}")
    
    # Проверяем существование файла
    if not os.path.exists(input_file):
        print(f"[ОШИБКА] Файл не найден: {input_file}")
        print("Список файлов в директории task5:")
        for file in os.listdir(current_dir):
            print(f"  - {file}")
        return
    
    print(f"[OK] Файл найден: {input_file}")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        print(f"Прочитано строк: {len(lines)}")
        
        results = []
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue
                
            print(f"Обработка строки {line_num}: '{line}'")
            
            try:
                # Разделяем строку на числа
                parts = line.split()
                if len(parts) != 2:
                    print(f"[ПРЕДУПРЕЖДЕНИЕ] Строка {line_num} содержит {len(parts)} чисел (требуется 2): '{line}'")
                    continue
                
                a, b = float(parts[0]), float(parts[1])
                result = a + b
                results.append((a, b, result))
                print(f"  {a} + {b} = {result}")
                
            except ValueError as e:
                print(f"[ОШИБКА] Ошибка в строке {line_num}: неверный формат числа в '{line}'")
        
        # Записываем результаты в файл
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("Результаты сложения:\n")
            f.write("=" * 30 + "\n")
            for a, b, result in results:
                f.write(f"{a} + {b} = {result}\n")
        
        print(f"[OK] Результаты записаны в файл: {output_file}")
        
    except Exception as e:
        print(f"[ОШИБКА] Непредвиденная ошибка: {e}")


def main():
    """Демонстрация работы декоратора."""
    print("Тестирование декоратора для измерения времени выполнения:")
    print("=" * 60)
    
    print("\n1. Тестирование функции сложения чисел:")
    print("-" * 40)
    
    # Тест 1: Простое сложение
    result1 = add_numbers(10, 20)
    
    # Тест 2: Сложение дробных чисел
    result2 = add_numbers(3.14, 2.86)
    
    # Тест 3: Сложение отрицательных чисел
    result3 = add_numbers(-5, 10)
    
    print("\n2. Тестирование функции работы с файлами:")
    print("-" * 40)
    
    # Обработка файла
    process_file()
    
    # Читаем и отображаем выходной файл
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(current_dir, "output.txt")
    
    try:
        with open(output_file, 'r', encoding='utf-8') as f:
            print("\n[ФАЙЛ] Содержимое файла output.txt:")
            print("-" * 30)
            print(f.read())
    except FileNotFoundError:
        print(f"\n[ПРЕДУПРЕЖДЕНИЕ] Файл {output_file} не найден")


if __name__ == "__main__":
    main()