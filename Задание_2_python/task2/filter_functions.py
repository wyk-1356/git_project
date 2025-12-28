"""
Задание 2: Функция фильтрации массива строк с использованием лямбда-функций.
"""

from typing import List, Callable


def filter_strings(filter_func: Callable[[str], bool], strings: List[str]) -> List[str]:
    """
    Фильтрует массив строк с помощью переданной функции.
    
    Args:
        filter_func (Callable[[str], bool]): Функция-фильтр, возвращает True для элементов,
                                             которые должны остаться в результате.
        strings (List[str]): Исходный список строк.
        
    Returns:
        List[str]: Отфильтрованный список строк.
        
    Examples:
        >>> filter_strings(lambda s: ' ' not in s, ["hello", "world", "hello world"])
        ['hello', 'world']
    """
    return [s for s in strings if filter_func(s)]


def main():
    """Демонстрация работы фильтров."""
    test_strings = [
        "apple",
        "banana",
        "apricot",
        "orange",
        "avocado",
        "blueberry",
        "a peach",
        "cherry",
        "ananas",
        "kiwi"
    ]
    
    print("Исходный список строк:")
    print(test_strings)
    print()
    
    # 1. Исключить строки с пробелами
    no_spaces_filter = lambda s: ' ' not in s
    result1 = filter_strings(no_spaces_filter, test_strings)
    print("1. Без строк с пробелами:")
    print(result1)
    print()
    
    # 2. Исключить строки, начинающиеся с буквы "а" (английской или русской)
    no_a_filter = lambda s: not s.lower().startswith(('а', 'a'))
    result2 = filter_strings(no_a_filter, test_strings)
    print("2. Без строк, начинающихся с 'а' или 'a':")
    print(result2)
    print()
    
    # 3. Исключить строки, длина которых меньше 5
    length_filter = lambda s: len(s) >= 5
    result3 = filter_strings(length_filter, test_strings)
    print("3. Без строк длиной меньше 5:")
    print(result3)
    print()
    
    # Комбинированный фильтр
    combined_filter = lambda s: (' ' not in s) and (not s.lower().startswith(('а', 'a'))) and (len(s) >= 5)
    result4 = filter_strings(combined_filter, test_strings)
    print("4. Комбинированный фильтр (без пробелов, не начинается с 'а', длина >= 5):")
    print(result4)


if __name__ == "__main__":
    main()