import os

def console_clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def continue_while():
    input("Для продолжения нажмите Enter...")

def correct_round(x):
    # Округляет число к ближайшему целому, .5 – всегда вверх.
    if x >= 0:
        return int(x + 0.5)
    else:
        return int(x - 0.5)

#валидация числа
def safe_int_input(prompt):
    """Запрашивает целое число, обрабатывает ошибки и пустой ввод."""
    while True:
        try:
            value = input(prompt).strip()
            if not value:
                print("Поле не может быть пустым. Попробуйте снова.")
                continue
            return int(value)
        except ValueError:
            print("Ошибка! Введите номер предмета(например: 4).")
            continue_while()
        except KeyboardInterrupt:
            print("\nОперация отменена.")
            continue_while()
            return None

# работа с оценками в красивой рамке
def print_status_box(operation, subject_title, result_text):
    line1 = f"  ОПЕРАЦИЯ:  {operation}"
    line2 = f"  ПРЕДМЕТ:   «{subject_title}»"
    line3 = f"  РЕЗУЛЬТАТ: {result_text}"
    
    width = max(len(line1), len(line2), len(line3)) + 4

    print("\n┌" + "─" * width + "┐")
    print(f"│{line1.ljust(width)}│")
    print(f"│{line2.ljust(width)}│")
    print("├" + "─" * width + "┤")
    print(f"│{line3.ljust(width)}│")
    print("└" + "─" * width + "┘\n")