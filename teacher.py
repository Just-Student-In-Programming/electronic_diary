from utils import continue_while, print_status_box
import constants as const

class Teacher:
    def __init__(self, name="Учитель", password="1234"):
        self.name = name
        self.password = password

    def check_password(self, entered_password):
        """Проверяет, верный ли пароль."""
        return entered_password == self.password

    def add_estimation_interactive(self, student):
        """Учитель ставит оценку конкретному студенту."""
        subject = student._choose_subject("поставить оценку")
        if subject is None:
            continue_while()
            return False

        grade = student._input_grade("поставить")
        if grade is None:
            continue_while()
            return False

        student.add_grade(subject, grade)
        subject_title = const.SUBJECTS[subject]
        
        print_status_box("Учитель ставит оценку", subject_title, f"{student.full_name}: [{grade}]")
        continue_while()
        return True

    def del_estimation_interactive(self, student):
        """Учитель удаляет оценку у конкретного студента."""
        if not student.has_any_grade():
            print("У ученика пока нет оценок.")
            continue_while()
            return False

        subject = student._choose_subject("удалить оценку")
        if subject is None:
            continue_while()
            return False

        if not student.grades[subject]:
            print(f"У ученика нет оценок по предмету «{const.SUBJECTS[subject]}».")
            continue_while()
            return False

        grade = student._input_grade("удалить")
        if grade is None:
            continue_while()
            return False

        subject_title = const.SUBJECTS[subject]
        
        if student.del_grade(subject, grade):
            print_status_box("Учитель удаляет оценку", subject_title, f"{student.full_name}: [{grade}]")
        else:
            print_status_box("Ошибка удаления", subject_title, f"Оценки [{grade}] нет")
            
        continue_while()
        return True