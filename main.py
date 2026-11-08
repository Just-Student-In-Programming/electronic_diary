from utils import continue_while, console_clear
from group_students import GroupStudents
from teacher import Teacher
import constants as const

group_obj = GroupStudents()
group_obj.load_from_file()
teacher_obj = Teacher()

# ВЫБОР РОЛИ
console_clear()
print("""╔══════════════════════════════════════════╗
║             ВХОД В СИСТЕМУ               ║
╚══════════════════════════════════════════╝""")
print("┌── Выберите вашу роль: ──────────────────┐")
print("│  1. Я Учитель                           │")
print("│  2. Я Ученик                            │")
print("└─────────────────────────────────────────┘\n")

while True:
    role = input("Введите номер роли (1 или 2): ").strip()
    if role in ("1", "2"):
        break
    print("❌ Ошибка: нужно ввести только цифру 1 или 2. Попробуйте еще раз.")

is_teacher = False

if role == "1":
    print("\n🔒 Требуется авторизация.")
    for attempt in range(1, 4):
        attempt_info = f" (Попытка {attempt} из 3)" if attempt > 1 else ""
        pwd = input(f"Введите пароль учителя{attempt_info}: ")
        
        if teacher_obj.check_password(pwd):
            is_teacher = True
            print("\n┌" + "─" * 42 + "┐")
            print("│ ✅ Доступ разрешен. Добро пожаловать!    │")
            print("└" + "─" * 42 + "┘\n")
            break
        else:
            attempts_left = 3 - attempt
            if attempts_left > 0:
                print(f"❌ Неверный пароль! Осталось попыток: {attempts_left}\n")
            else:
                print("\n┌" + "─" * 42 + "┐")
                print("│ ❌ Попытки исчерпаны! Вход как ученик.   │")
                print("└" + "─" * 42 + "┘\n")
    continue_while()

# --- ОСНОВНОЙ ЦИКЛ ПРОГРАММЫ ---
is_work = True

while is_work:
    console_clear()
    
    # Выводим нужное меню в зависимости от роли
    if is_teacher:
        print(const.MENU_TEACHER)
    else:
        print(const.MENU_STUDENT)

    try:
        select = int(input("Выберите операцию: "))
    except ValueError:
        print("Ошибка! Введите номер выбранной Вами операции(например: 1).")
        continue_while()
        continue

    # ЛОГИКА ДЛЯ УЧИТЕЛЯ
    if is_teacher:
        if select == const.OPTION_T_SHOW_ALL_STUDENTS:
            console_clear()
            group_obj.show_group()
        elif select == const.OPTION_T_ADD_STUDENT:
            console_clear()
            group_obj.add_student_in_group()
            group_obj.save_to_file()
        elif select == const.OPTION_T_DEL_STUDENT:
            console_clear()
            group_obj.del_student_in_group()
            group_obj.save_to_file()
        elif select == const.OPTION_T_ENTER_FOR_STUDENT:
            console_clear()
            student = group_obj.enter_for_student()
            if student is None:
                continue

            #  ПРОФИЛЬ УЧЕНИКА ДЛЯ УЧИТЕЛЯ 
            is_work_student = True
            while is_work_student:
                console_clear()
                student_info = f"Профиль: {student.full_name} {student.name} | {student.age} лет | {student.course} курс"
                border = "═" * len(student_info)
                print(f"\n╔═{border}═╗")
                print(f"║ {student_info} ║")
                print(f"╚═{border}═╝\n")

                print(f"{const.OPTION_STUDENT_ADD_ESTIMATION}. Выставить оценку")
                print(f"{const.OPTION_STUDENT_DEL_ESTIMATION}. Удалить оценку")
                print(f"{const.OPTION_STUDENT_SHOW_ESTIMATIONS_COMPLETELY}. Оценки по всем предметам")
                print(f"{const.OPTION_STUDENT_SHOW_ESTIMATIONS_BY_SUBJECT}. Оценки по выбранному предмету")
                print(f"{const.OPTION_STUDENT_SHOW_AVERAGE_SCORE_COMPLETELY}. Средний балл по всем предметам")
                print(f"{const.OPTION_STUDENT_SHOW_AVERAGE_SCORE_BY_SUBJECT}. Средний балл по выбранному предмету")
                print(f"{const.OPTION_STUDENT_EXIT_PROFILE}. Назад в главное меню\n")

                try:
                    action = int(input("Выполнить действие: "))
                except ValueError:
                    print("Ошибка! Введите номер операции(например: 3).")
                    continue_while()
                    continue

                console_clear()

                if action == const.OPTION_STUDENT_ADD_ESTIMATION:
                    teacher_obj.add_estimation_interactive(student)
                    group_obj.save_to_file()
                elif action == const.OPTION_STUDENT_DEL_ESTIMATION:
                    teacher_obj.del_estimation_interactive(student)
                    group_obj.save_to_file()
                elif action == const.OPTION_STUDENT_SHOW_ESTIMATIONS_COMPLETELY:
                    student.show_all_grades_interactive()
                elif action == const.OPTION_STUDENT_SHOW_ESTIMATIONS_BY_SUBJECT:
                    student.show_estimations_interactive()
                elif action == const.OPTION_STUDENT_SHOW_AVERAGE_SCORE_COMPLETELY:
                    student.show_average_score_in_all_subjects()
                elif action == const.OPTION_STUDENT_SHOW_AVERAGE_SCORE_BY_SUBJECT:
                    student.show_average_score_for_selected_subject()
                elif action == const.OPTION_STUDENT_EXIT_PROFILE:
                    is_work_student = False
                else:
                    print("Недоступная операция.")
                    continue_while()
                    
        elif select == const.OPTION_T_EXIT_PROGRAM:
            console_clear()
            group_obj.save_to_file() 
            is_work = False
            print("Программа завершена.\nДо встречи!")
        else:
            print("Выберите доступную операцию.")
            continue_while()

    # ЛОГИКА ДЛЯ УЧЕНИКА
    else:
        if select == const.OPTION_S_ENTER_FOR_STUDENT:
            console_clear()
            student = group_obj.enter_for_student()
            if student is None:
                continue

            # ПРОФИЛЬ УЧЕНИКА ДЛЯ УЧЕНИКА 
            is_work_student = True
            while is_work_student:
                console_clear()
                student_info = f"Профиль: {student.full_name} {student.name} | {student.age} лет | {student.course} курс"
                border = "═" * len(student_info)
                print(f"\n╔═{border}═╗")
                print(f"║ {student_info} ║")
                print(f"╚═{border}═╝\n")

                print(f"{const.OPTION_STUDENT_VIEW_ALL_GRADES}. Мои оценки по всем предметам")
                print(f"{const.OPTION_STUDENT_VIEW_SUBJECT_GRADES}. Мои оценки по предмету")
                print(f"{const.OPTION_STUDENT_VIEW_ALL_AVERAGE}. Мой общий средний балл")
                print(f"{const.OPTION_STUDENT_VIEW_SUBJECT_AVERAGE}. Мой средний балл по предмету")
                print(f"{const.OPTION_STUDENT_VIEW_EXIT}. Назад в главное меню\n")

                try:
                    action = int(input("Выполнить действие: "))
                except ValueError:
                    print("Ошибка! Введите номер операции(например: 1).")
                    continue_while()
                    continue

                console_clear()

                if action == const.OPTION_STUDENT_VIEW_ALL_GRADES:
                    student.show_all_grades_interactive()
                elif action == const.OPTION_STUDENT_VIEW_SUBJECT_GRADES:
                    student.show_estimations_interactive()
                elif action == const.OPTION_STUDENT_VIEW_ALL_AVERAGE:
                    student.show_average_score_in_all_subjects()
                elif action == const.OPTION_STUDENT_VIEW_SUBJECT_AVERAGE:
                    student.show_average_score_for_selected_subject()
                elif action == const.OPTION_STUDENT_VIEW_EXIT:
                    is_work_student = False
                else:
                    print("Недоступная операция.")
                    continue_while()

        elif select == const.OPTION_S_SHOW_MY_GROUP:
            console_clear()
            print("Введите свои данные, чтобы программа нашла вашу группу:\n")
            # Просим ученика авторизоваться
            student = group_obj.enter_for_student() 
            if student is not None:
                group_obj.show_my_group(student)  

        elif select == const.OPTION_S_EXIT_PROGRAM:
            console_clear()
            # Ученик тоже сохраняет данные при выходе, чтобы ничего не потерялось
            group_obj.save_to_file() 
            is_work = False
            print("Программа завершена.\nДо встречи!")

        else:
            print("Выберите доступную операцию.")
            continue_while()