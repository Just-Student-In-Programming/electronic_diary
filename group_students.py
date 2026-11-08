from utils import continue_while
from student import Student
import constants as const
import json

class GroupStudents:
    def __init__(self):
        self.list_students = []

    def save_to_file(self, filename="data.json"):
        data = []
        for s in self.list_students:
            data.append({
                "name": s.name,
                "full_name": s.full_name,
                "age": s.age,
                "course": s.course,
                "group_num": getattr(s, 'group_num', 1), # <--- ДОБАВИТЬ ЭТУ СТРОКУ
                "grades": s.grades
            })
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_from_file(self, filename="data.json"):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            return
            
        self.list_students = []
        for item in data:
            # Достаем group_num (если его нет в старом JSON, ставим 1)
            grp_num = item.get("group_num", 1) 
            
            # Передаем grp_num в Student
            student = Student(item["name"], item["full_name"], item["age"], item["course"], grp_num) 
            student.grades = item["grades"]
            student.update_cache()
            self.list_students.append(student)

    def _input_student_data(self):
    # Цикл для имени
        while True:
            name = input("Введите имя учащегося: ").capitalize().strip()
            if not name:
                print("Поле имя не может быть пустым. Попробуйте снова.")
                continue
            if len(name) > const.MAX_LEN_NAME:
                print(f"Поле имя содержит большое количество символов. (максимальная длина символов: {const.MAX_LEN_NAME}).")
                continue
            if any(ch.isdigit() for ch in name):
                print("В поле имя не должно быть цифр.")
                continue
            break

        # Аналогично для фамилии
        while True:
            full_name = input("Введите фамилию учащегося: ").capitalize().strip()
            if not full_name:
                print("Поле фамилия не может быть пустым. Попробуйте снова.")
                continue
            if len(full_name) > const.MAX_LEN_FULL_NAME:
                print(f"Поле фамилия содержит большое количество символов. (максимальная длина символов: {const.MAX_LEN_FULL_NAME}).")
                continue
            if any(ch.isdigit() for ch in full_name):
                print("В поле фамилия не должно быть цифр.")
                continue
            break

        # Цикл для возраста
        while True:
            try:
                age = int(input("Введите возраст учащегося: "))
            except ValueError:
                print("Ошибка! Введите возраст учащегося числом(например: 16).")
                continue

            if age < const.MIN_AGE or age > const.MAX_AGE:
                print(f"Возраст должен быть от {const.MIN_AGE} до {const.MAX_AGE} лет.")
                continue
            break

        # Цикл для курса
        while True:
            try:
                course = int(input("Введите курс учащегося: "))
            except ValueError:
                print("Ошибка! Введите курс учащегося числом(например: 2).")
                continue
            
            if course < const.MIN_COURSE or course > const.MAX_COURSE:
                print(f"Курс должен быть от {const.MIN_COURSE} до {const.MAX_COURSE}.")
                continue
            break

        return Student(name, full_name, age, course)

    def add_student_in_group(self):
        print("Вы выбрали добавить ученика.\n")

        student = self._input_student_data()
        if student is None:
            return False

        # ПРОВЕРКА на существование студента (__eq__ сам сработает)
        if student in self.list_students:         
            print("Такой студент уже есть в группе.")
            continue_while()
            return False

        self.list_students.append(student)

        # Вычисляем номер группы для добавленного студента
        group_number = (len(self.list_students) - 1) // const.MAX_STUDENTS_IN_GROUP + 1
        print("\n[+] " + "=" * 40)
        print(f"    👥 Студент успешно добавлен в группу №{group_number}")
        print("[+] " + "=" * 40 + "\n")
        continue_while()
        return True

    def del_student_in_group(self):
        if not self.list_students:
            print("Нужно добавить хотя бы одного учащегося.")
            continue_while()
            return False
        
        print("Вы выбрали исключить ученика.\n")

        # зачем мы тут передаем фолз? и потом еще проверяем это условие но эта переменная никак не менятся!!!
        student = self._input_student_data()
        if student is None:
            return False

        # Ищем в списке(заменил)
        try:
            # Python сам пройдется по списку, сравнит всех через ваш __eq__ 
            # и удалит нужного студента. Если его нет — вызовет ошибку ValueError.
            self.list_students.remove(student)
            print("\nУчащийся был исключен.\n")
            continue_while()
            return True
        except ValueError:
            print("\nУчащегося с такими данными нет в нашем учебном заведении.\n")
            continue_while()
            return False

    #Вход за ученика (возвращает объект Student или None)
    def enter_for_student(self):
        if not self.list_students:
            print("Нужно добавить хотя бы одного учащегося.")
            continue_while()
            return None
        
        print("Вы входите в журнал ученика.\n")

        student = self._input_student_data()
        if student is None:
            return None

        for s in self.list_students:
            if s == student:
                return s
        
        print("\nУчащегося с такими данными нет в нашем заведении.")
        continue_while()
        return None

    def show_group(self):
        if not self.list_students:
            print("Нужно добавить хотя бы одного учащегося.")
            continue_while()
            return None

        # Проходимся по всем возможным курсам (от 1 до 5)
        for course_num in range(const.MIN_COURSE, const.MAX_COURSE + 1):
            # Ищем студентов только этого курса
            students_on_course = [s for s in self.list_students if s.course == course_num]
            
            if students_on_course:
                header_text = f" > СПИСОК ГРУППЫ (КУРС) №{course_num}"
                lines_to_print = []
                
                for num, s in enumerate(students_on_course, 1):
                    lines_to_print.append(f"  {num}. {s.show_state()}")

                max_line_len = max(len(line) for line in lines_to_print)
                width = max(max_line_len, len(header_text)) + 4

                print("\n╔" + "═" * width + "╗")
                print(f"║{header_text.ljust(width)}║")
                print("╠" + "═" * width + "╣")
                for line in lines_to_print:
                    print(f"║{line.ljust(width)}║")
                print("╚" + "═" * width + "╝\n")

        continue_while()

    def show_my_group(self, student):
        """Показывает только группу (курс) выбранного студента."""
        students_on_course = [s for s in self.list_students if s.course == student.course]
        
        if not students_on_course:
            print("В вашей группе пока нет учащихся.")
            continue_while()
            return

        header_text = f" > МОЯ ГРУППА (КУРС №{student.course})"
        lines_to_print = []

        for num, s in enumerate(students_on_course, 1):
            suffix = " (Вы)" if s == student else ""
            lines_to_print.append(f"  {num}. {s.show_state()}{suffix}")

        max_line_len = max(len(line) for line in lines_to_print)
        width = max(max_line_len, len(header_text)) + 4

        print("\n╔" + "═" * width + "╗")
        print(f"║{header_text.ljust(width)}║")
        print("╠" + "═" * width + "╣")
        for line in lines_to_print:
            print(f"║{line.ljust(width)}║")
        print("╚" + "═" * width + "╝\n")
        continue_while()