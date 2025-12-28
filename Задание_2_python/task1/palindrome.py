"""
Задание 1: Проверка строки на палиндром.
Палиндром - это строка, которая читается одинаково слева направо и справа налево.
"""

def is_palindrome(s: str) -> bool:
    """
    Проверяет, является ли строка палиндромом.
    
    Args:
        s (str): Входная строка
        
    Returns:
        bool: True если строка палиндром, иначе False
        
    Examples:
        >>> is_palindrome("radar")
        True
        >>> is_palindrome("hello")
        False
        >>> is_palindrome("А роза упала на лапу Азора")
        True
    """
    # Убираем пробелы и приводим к нижнему регистру
    cleaned = ''.join(char.lower() for char in s if char.isalnum())
    
    # Сравниваем строку с её перевёрнутой версией
    return cleaned == cleaned[::-1]


def main():
    """Примеры использования функции is_palindrome."""
    test_strings = [
        "radar",
        "hello",
        "А роза упала на лапу Азора",
        "Madam, I'm Adam",
        "12321",
        "not a palindrome"
    ]
    
    print("Проверка строк на палиндром:")
    print("=" * 40)
    
    for test_str in test_strings:
        result = is_palindrome(test_str)
        print(f"'{test_str}' -> {'Палиндром' if result else 'Не палиндром'}")


if __name__ == "__main__":
    main()