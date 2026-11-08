from utils import continue_while, correct_round, console_clear, safe_int_input, print_status_box
import constants as const

class Student:
    def __init__(self, name, full_name, age, course, group_num=1):
        self.name = name
        self.full_name = full_name
        self.age = age
        self.course = course
        self.group_num = group_num

        self.grades = {}
        for key in const.SUBJECTS:
            self.grades[key] = []

        self.cached_avg = 0.0 

    # Проверка наличия любых оценок
    def has_any_grade(self):
        return any(self.grades.values())

    def update_cache(self):
        """Пересчитывает и сохраняет средний балл в память."""
        total_sum = sum(sum(g) for g in self.grades.values())
        total_count = sum(len(g) for g in self.grades.values())
        self.cached_avg = total_sum / total_count if total_count > 0 else 0.0

    # Добавление (вызывает Учитель)
    def add_grade(self, subject, grade):
        """subject — ключ из const.SUBJECTS, grade — число."""
        self.grades[subject].append(grade)
        self.update_cache()

    # Удаление (вызывает Учитель)
    def del_grade(self, subject, grade):
        """Возвращает True, если оценка была и удалена."""
        if grade not in self.grades[subject]:
            return False
        self.grades[subject].remove(grade)
        self.update_cache()
        return True

    # Средний балл
    def average_by(self, subject):
        """Средний балл по предмету или None, если оценок нет."""
        grades = self.grades[subject]
        if not grades:
            return None
        return sum(grades) / len(grades)

    # Показ оценок
    def show_grades(self, subject):
        """Печатает оценки по предмету."""
        grades = self.grades[subject]
        title = const.SUBJECTS[subject]
        
        if not grades:
            print_status_box("Список оценок", title, "Оценок пока нет")
            return
            
        grades_str = ", ".join(str(g) for g in grades)
        print_status_box("Список оценок", title, grades_str)

    # Вспомогательный метод (нужен Учителю для запроса данных)
    def _input_grade(self, action="поставить"):
        grade = safe_int_input(f"Какую оценку {action}: ")
        if grade is None:
            return None
        if grade > const.MAX_ESTIMATION:
            print(f"Максимальная оценка: {const.MAX_ESTIMATION}.")
            return None
        if grade < const.MIN_ESTIMATION:
            print(f"Минимальная оценка: {const.MIN_ESTIMATION}.")
            return None
        return grade

    # Вспомогательный метод (нужен Учителю для запроса данных)
    def _choose_subject(self, action="выберите"):
        print("Доступные предметы:")
        for i, title in enumerate(const.SUBJECTS.values(), 1):
            print(f"  {i}. {title}")
        print()

        choice = safe_int_input(f"По какому предмету {action} (цифру): ")
        if choice is None:
            return None

        keys = list(const.SUBJECTS.keys())
        if not (1 <= choice <= len(keys)):
            print("Неверный номер предмета. Выберите доступный номер предмета.")
            return None
        return keys[choice - 1]

    # ИНТЕРАКТИВНЫй МЕТОД (только просмотр)
    def show_estimations_interactive(self):
        if not self.has_any_grade():
            print("Пока нет оценок.")
            continue_while()
            return False
        subject = self._choose_subject("показать оценки")
        if subject is None:
            continue_while()
            return False
        self.show_grades(subject)
        continue_while()
        return True

    def show_all_grades_interactive(self):
        if not self.has_any_grade():
            print("Пока нет оценок.")
            continue_while()
            return False
        for subject in const.SUBJECTS:
            self.show_grades(subject)
        continue_while()
        return True
    
    def show_average_score_in_all_subjects(self):
        if not self.has_any_grade():
            print("Пока нет оценок.")
            continue_while()
            return False

        for subject in const.SUBJECTS:
            self.show_grades(subject)
            print()
        continue_while()
        console_clear()

        print("\n📊 Средний балл по предметам:")
        print("─" * 45)
        
        for i, (subject, title) in enumerate(const.SUBJECTS.items(), 1):
            avg = self.average_by(subject)
            if avg is not None:
                print(f"  {i}. {title.ljust(15)} : {avg:.2f} (окр. до {correct_round(avg)})")
            else:
                print(f"  {i}. {title.ljust(15)} : нет оценок")
                
        print("─" * 45 + "\n")
        continue_while()
        console_clear()

        total_sum = 0
        total_count = 0
        for subject_grades in self.grades.values():   
            for grade in subject_grades: 
                total_sum += grade
                total_count += 1

        avg = total_sum / total_count
        print_status_box("ИТОГОВЫЙ БАЛЛ", "Все предметы", f"Общий средний: {avg:.2f}")
        continue_while()
        return True

    def show_average_score_for_selected_subject(self):
        if not self.has_any_grade():
            print("Пока нет оценок.")
            continue_while()
            return False

        subject = self._choose_subject("показать средний балл")
        if subject is None:
            continue_while()
            return False

        subject_title = const.SUBJECTS[subject]
        avg = self.average_by(subject)
        
        if avg is None:
            print_status_box("Средний балл", subject_title, "Оценок нет")
        else:
            result_text = f"{avg:.2f} (округлено до: {correct_round(avg)})"
            print_status_box("Средний балл", subject_title, result_text)
            
        continue_while()
        return True
        
    def show_state(self):
        return f"{self.full_name} {self.name}  |  {self.age} лет  |  {self.course} курс"
    
    def __eq__(self, other):
        if not isinstance(other, Student):
            return False
        return (self.name == other.name and
                self.full_name == other.full_name and
                self.age == other.age and
                self.course == other.course)