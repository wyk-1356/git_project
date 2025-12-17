#!/usr/bin/env python3
"""
Главный скрипт для запуска всех задач.
"""

import subprocess
import sys
import os


def run_task(task_dir: str, script_name: str = None):
    """Запускает Python скрипт из указанной директории."""
    if script_name is None:
        # Ищем все .py файлы в директории
        py_files = [f for f in os.listdir(task_dir) if f.endswith('.py')]
        if not py_files:
            print(f"В директории {task_dir} не найдено .py файлов")
            return
        script_name = py_files[0]
    
    script_path = os.path.join(task_dir, script_name)
    if not os.path.exists(script_path):
        print(f"Файл {script_path} не найден")
        return
    
    print(f"\n{'='*60}")
    print(f"Запуск: {script_path}")
    print(f"{'='*60}\n")
    
    try:
        # Запускаем скрипт
        result = subprocess.run([sys.executable, script_path], 
                               capture_output=True, text=True, timeout=10)
        print(result.stdout)
        if result.stderr:
            print("Ошибки:", result.stderr)
    except subprocess.TimeoutExpired:
        print(f"Скрипт {script_name} превысил время выполнения")
    except Exception as e:
        print(f"Ошибка при выполнении {script_name}: {e}")


def main():
    """Запускает все задачи по очереди."""
    tasks = [
        ("task1", "palindrome.py"),
        ("task2", "filter_functions.py"),
        ("task3", "shapes.py"),
        ("task4", "students.py"),
        ("task5", "timer_decorator.py")
    ]
    
    print("Запуск всех Python задач")
    print("=" * 60)
    
    for task_dir, script_name in tasks:
        if os.path.exists(task_dir):
            run_task(task_dir, script_name)
        else:
            print(f"Директория {task_dir} не существует")
    
    print("\n" + "="*60)
    print("Все задачи выполнены!")


if __name__ == "__main__":
    main()