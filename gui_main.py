import math

import customtkinter as ctk
import constants as const

from group_students import GroupStudents
from utils import correct_round
from tkinter import messagebox
from student import Student
from teacher import Teacher

# Настройка внешнего вида
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class DiaryApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.active_window = None
        
        self.title("Электронный дневник")
        self.configure(fg_color="#0f172a")
        
        # 1. Задаем нормальный стартовый размер
        self.geometry("1100x700")
        
        # 2. Безопасно разворачиваем на весь экран с небольшой задержкой
        self.after(100, lambda: self.state('zoomed'))

        self.group = GroupStudents()
        self.group.load_from_file()
        self.teacher = Teacher()
        
        self.is_teacher_mode = False
        self.current_frame = None

        self.show_login_screen()

    def center_window(self, window, width, height):
        """Центрирует дочернее окно относительно главного экрана"""
        self.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (width // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

    def clear_screen(self):
        """Удаляет все элементы с текущего экрана И закрывает всплывающие окна"""
        if self.current_frame is not None:
            self.current_frame.destroy()
            
        if self.active_window is not None and self.active_window.winfo_exists():
            self.active_window.destroy()
            self.active_window = None

    def exit_app(self):
        """Сохраняет все данные и закрывает программу"""
        self.group.save_to_file()
        self.destroy()

    def close_active_window(self, window):
        """Корректно закрывает окно и сбрасывает переменную"""
        self.active_window = None
        window.destroy()

    def show_login_screen(self):
        self.clear_screen()
        self.is_teacher_mode = False 
        
        self.current_frame = ctk.CTkFrame(self, fg_color="#0f172a")
        self.current_frame.pack(expand=True, fill="both")

        # --- КАРТОЧКА ВХОДА ---
        login_box = ctk.CTkFrame(self.current_frame, width=400, height=500, 
                                 fg_color="#1e293b", corner_radius=15)
        login_box.place(relx=0.5, rely=0.5, anchor="center")

        label = ctk.CTkLabel(login_box, text="Вход в систему", font=("Segoe UI", 32, "bold"), 
                             text_color="#f8fafc")
        label.pack(pady=(40, 10))

        label_sub = ctk.CTkLabel(login_box, text="Выберите вашу роль", font=("Segoe UI", 16), 
                                 text_color="#94a3b8")
        label_sub.pack(pady=(0, 30))

        btn_teacher = ctk.CTkButton(login_box, text="Войти как Учитель", font=("Segoe UI", 20, "bold"),
                                    width=300, height=60, fg_color="#3b82f6", hover_color="#2563eb", corner_radius=10,
                                    command=self.login_teacher)
        btn_teacher.pack(pady=15)

        btn_student = ctk.CTkButton(login_box, text="Войти как Ученик", font=("Segoe UI", 20, "bold"),
                                    width=300, height=60, fg_color="#22c55e", hover_color="#16a34a", corner_radius=10,
                                    command=self.login_student)
        btn_student.pack(pady=15)

        btn_exit = ctk.CTkButton(login_box, text="Выйти из программы", font=("Segoe UI", 16, "bold"),
                                 width=300, height=40, fg_color="transparent", border_color="#ef4444", 
                                 border_width=2, text_color="#ef4444", hover_color="#1e293b", corner_radius=10,
                                 command=self.exit_app)
        btn_exit.pack(pady=(30, 20))

    def login_teacher(self):
        if self.active_window is not None and self.active_window.winfo_exists():
            self.active_window.focus()
            return

        window = ctk.CTkToplevel(self)
        self.active_window = window
        window.title("Авторизация")
        self.center_window(window, 350, 260)
        window.configure(fg_color="#1e293b")
        window.attributes("-topmost", True)
        window.protocol("WM_DELETE_WINDOW", lambda: self.close_active_window(window))
        
        ctk.CTkLabel(window, text="Введите пароль учителя:", font=("Segoe UI", 16, "bold"), text_color="#f8fafc").pack(pady=(25, 10))

        entry_pwd = ctk.CTkEntry(window, width=250, show="*", fg_color="#0f172a", border_color="#3b82f6")
        entry_pwd.pack(pady=5)
        
        error_label = ctk.CTkLabel(window, text="", font=("Segoe UI", 12, "bold"), text_color="#ef4444")
        error_label.pack(pady=(5, 0))

        window.wait_visibility()
        entry_pwd.focus_set()

        def check_password(event=None):
            pwd = entry_pwd.get()
            if self.teacher.check_password(pwd):
                self.is_teacher_mode = True
                self.close_active_window(window)
                self.show_teacher_menu()
            else:
                error_label.configure(text="Неверный пароль!")
                entry_pwd.delete(0, "end")
                entry_pwd.focus_set()

        entry_pwd.bind("<Return>", check_password)

        btn_frame = ctk.CTkFrame(window, fg_color="transparent")
        btn_frame.pack(pady=15)

        ctk.CTkButton(btn_frame, text="Войти", width=100, fg_color="#3b82f6", hover_color="#2563eb", command=check_password).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Отмена", width=100, fg_color="transparent", border_color="#ef4444", border_width=1.5, text_color="#ef4444", hover_color="#0f172a", command=lambda: self.close_active_window(window)).pack(side="left", padx=10)

    def login_student(self):
        self.is_teacher_mode = False
        self.show_student_menu()

    def show_teacher_menu(self):
        self.clear_screen()
        # ИСПОЛЬЗУЕМ СЛОВАРЬ THEME
        self.configure(fg_color=const.THEME["main_bg"]) 
        
        self.current_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.current_frame.pack(pady=20, padx=40, fill="both", expand=True)

        label = ctk.CTkLabel(self.current_frame, text="Панель Учителя", font=("Segoe UI", 32, "bold"), text_color=const.THEME["text_main"])
        label.pack(pady=(0, 15))

        # Нижние кнопки
        bottom_frame = ctk.CTkFrame(self.current_frame, fg_color="transparent")
        bottom_frame.pack(side="bottom", pady=10)
        
        ctk.CTkButton(bottom_frame, text="➕ Добавить", font=("Segoe UI", 14, "bold"), fg_color="#3b82f6", hover_color="#1d4ed8", height=40, width=150, command=self.open_add_student_window).pack(side="left", padx=5)
        ctk.CTkButton(bottom_frame, text="🗑 Удалить", font=("Segoe UI", 14, "bold"), fg_color="transparent", border_color="#ef4444", border_width=1.5, text_color="#ef4444", height=40, width=150, command=self.open_delete_student_window).pack(side="left", padx=5)
        ctk.CTkButton(bottom_frame, text="↩ Сменить роль", font=("Segoe UI", 14, "bold"), fg_color="#475569", hover_color="#64748b", height=40, width=150, command=self.show_login_screen).pack(side="left", padx=5)
        ctk.CTkButton(bottom_frame, text="⏻ Выйти", font=("Segoe UI", 14, "bold"), fg_color="#dc2626", hover_color="#b91c1c", height=40, width=150, command=self.exit_app).pack(side="left", padx=5)

        # Поле поиска (используем цвета из THEME)
        search_entry = ctk.CTkEntry(
            self.current_frame, placeholder_text="🔍 Быстрый поиск ученика по имени...", 
            height=40, fg_color=const.THEME["card_bg"], border_color=const.THEME["border"], corner_radius=8
        )
        search_entry.pack(fill="x", padx=40, pady=(0, 10))

        # Контейнер для списка
        list_container = ctk.CTkFrame(self.current_frame, fg_color=const.THEME["card_bg"], corner_radius=12)
        list_container.pack(fill="both", expand=True, pady=10)

        list_frame = ctk.CTkScrollableFrame(
            list_container, fg_color=const.THEME["card_bg"], corner_radius=0, 
            scrollbar_fg_color=const.THEME["card_bg"], scrollbar_button_color=const.THEME["border"]
        )
        list_frame.pack(fill="both", expand=True, padx=2, pady=2)

        def render_list(query=""):
            for widget in list_frame.winfo_children():
                widget.destroy()

            if not self.group.list_students:
                ctk.CTkLabel(list_frame, text="Список учеников пуст.", font=("Segoe UI", 16), text_color=const.THEME["text_muted"]).pack(pady=40)
                return

            filtered_students = [s for s in self.group.list_students if query in s.full_name.lower() or query in s.name.lower()]
            if len(filtered_students) > 50:
                ctk.CTkLabel(list_frame, text="⚠️ Показаны первые 50 учеников. Уточните поиск.", text_color="#ef4444").pack(pady=10)
                filtered_students = filtered_students[:50]

            for course_num in range(const.MIN_COURSE, const.MAX_COURSE + 1):
                students_on_course = [s for s in filtered_students if s.course == course_num]
                
                if students_on_course:
                    course_label = ctk.CTkLabel(list_frame, text=f"🚀 {course_num} КУРС", font=("Segoe UI", 20, "bold"), text_color="#38bdf8")
                    course_label.pack(pady=(25, 5), anchor="w", padx=20)
                    
                    line = ctk.CTkFrame(list_frame, height=2, fg_color=const.THEME["border"])
                    line.pack(fill="x", padx=20, pady=(0, 15))
                    
                    for group_idx in range(1, 20):
                        group_students = [s for s in students_on_course if getattr(s, 'group_num', 1) == group_idx]
                        
                        if group_students:
                            group_label = ctk.CTkLabel(list_frame, text=f"📋 Группа {course_num}-{group_idx}", font=("Segoe UI", 14, "bold"), text_color=const.THEME["text_muted"])
                            group_label.pack(pady=(5, 8), anchor="w", padx=35)
                            
                            for student in group_students:
                                # ИСПОЛЬЗУЕМ КЭШ
                                avg_score = getattr(student, 'cached_avg', 0.0)
                                
                                if avg_score >= 4.5:
                                    text_color, badge_text = "#22c55e", f"★ {avg_score:.2f}"
                                elif avg_score >= 3.5:
                                    text_color, badge_text = "#eab308", f" {avg_score:.2f}"
                                elif avg_score > 0:
                                    text_color, badge_text = "#ef4444", f"⚠ {avg_score:.2f}"
                                else:
                                    text_color, badge_text = const.THEME["text_muted"], "нет оценок"

                                # Карточка с прозрачным фоном, чтобы работала подсветка
                                card = ctk.CTkFrame(list_frame, fg_color=const.THEME["main_bg"], corner_radius=8, cursor="hand2")
                                card.pack(fill="x", pady=4, padx=(35, 25))

                                display_text = f"  👤  {student.full_name} {student.name}  |  {student.age} лет"
                                student_label = ctk.CTkLabel(
                                    card, text=display_text, font=("Segoe UI", 15, "bold"), anchor="w",
                                    fg_color="transparent", text_color=const.THEME["text_main"]
                                )
                                student_label.pack(side="left", fill="x", expand=True, padx=10, pady=15)

                                score_label = ctk.CTkLabel(
                                    card, text=badge_text, font=("Segoe UI", 15, "bold"),
                                    text_color=text_color, fg_color="transparent", anchor="e", width=100
                                )
                                score_label.pack(side="right", padx=(10, 20))

                                # Подсветка при наведении
                                for widget in (card, student_label, score_label):
                                    widget.bind("<Button-1>", lambda event, s=student: self.show_student_profile(s, is_teacher=True))
                                    widget.bind("<Enter>", lambda event, c=card: c.configure(fg_color="#1e3a8a"))
                                    widget.bind("<Leave>", lambda event, c=card: c.configure(fg_color=const.THEME["main_bg"]))

        search_entry.bind("<KeyRelease>", lambda e: render_list(search_entry.get().strip().lower()))
        render_list()
        
    def open_calculator_window(self, student):
        if self.active_window is not None and self.active_window.winfo_exists():
            self.active_window.focus()
            return

        window = ctk.CTkToplevel(self)
        self.active_window = window
        window.title("Калькулятор оценки")
        self.center_window(window, 420, 450)
        window.configure(fg_color="#1e293b")
        window.attributes("-topmost", True)
        window.protocol("WM_DELETE_WINDOW", lambda: self.close_active_window(window))

        ctk.CTkLabel(window, text="🧮 Умный калькулятор оценки", font=("Segoe UI", 20, "bold"), text_color="#f8fafc").pack(pady=(20, 10))

        ctk.CTkLabel(window, text="Выберите предмет:", font=("Segoe UI", 13, "bold"), text_color="#cbd5e1").pack(anchor="w", padx=40, pady=(5, 2))
        combo_subject = ctk.CTkComboBox(window, values=list(const.SUBJECTS.values()), height=38, fg_color="#0f172a", border_color="#334155", state="readonly")
        combo_subject.pack(fill="x", padx=40)
        combo_subject.set(list(const.SUBJECTS.values())[0])

        ctk.CTkLabel(window, text="Желаемая оценка (например, 5 или 4.5):", font=("Segoe UI", 13, "bold"), text_color="#cbd5e1").pack(anchor="w", padx=40, pady=(15, 2))
        entry_target = ctk.CTkEntry(window, height=38, fg_color="#0f172a", border_color="#334155")
        entry_target.pack(fill="x", padx=40)

        result_label = ctk.CTkLabel(window, text="", font=("Segoe UI", 14), text_color="#22c55e", wraplength=340, justify="center")
        result_label.pack(pady=20, padx=20)

        def calculate():
            subject_name = combo_subject.get()
            keys_found = [k for k, v in const.SUBJECTS.items() if v == subject_name]
            if not keys_found:
                return
            subject_key = keys_found[0]
            
            grades = student.grades.get(subject_key, [])
            
            try:
                target = float(entry_target.get().replace(',', '.'))
                # Умная логика: если ввели 5, цель 4.5
                if target == 5.0: target = 4.5
                elif target == 4.0: target = 3.5
                elif target == 3.0: target = 2.5
                elif target == 2.0: target = 1.5
                
                if not (1 <= target <= 5):
                    result_label.configure(text="Оценка должна быть от 1 до 5!", text_color="#ef4444")
                    return
            except ValueError:
                result_label.configure(text="Введите число (например, 4.5)", text_color="#ef4444")
                return

            if not grades:
                first_grade_needed = math.ceil(target)
                result_label.configure(text=f"У вас нет оценок. Вам нужно получить хотя бы одну {first_grade_needed}, чтобы начать.", text_color="#22c55e")
                return

            current_sum = sum(grades)
            current_count = len(grades)
            current_avg = current_sum / current_count

            if current_avg >= target:
                result_label.configure(text=f"У вас уже средний балл {current_avg:.2f}.\nВы уже достигли цели!", text_color="#22c55e")
                return

            needed_fives = 0
            test_sum = current_sum
            test_count = current_count
            
            while (test_sum / test_count) < target:
                test_sum += 5
                test_count += 1
                needed_fives += 1
                if needed_fives > 20:
                    break

            if needed_fives > 20:
                result_label.configure(text="⚠️ Цель труднодостижима.\nПотребуется слишком много пятерок подряд. Начните с малого!", text_color="#ef4444")
                return

            result_label.configure(
                text=f"Текущий средний балл: {current_avg:.2f}\n"
                     f"Чтобы выйти на {target:.2f} (окр. до {math.ceil(target)}), вам нужно получить\n"
                     f"ещё {needed_fives} оценок '5' подряд!",
                text_color="#eab308"
            )

        ctk.CTkButton(window, text="Рассчитать", font=("Segoe UI", 15, "bold"), height=45,
                      fg_color="#3b82f6", hover_color="#2563eb", command=calculate).pack(pady=10, fill="x", padx=40)

    def open_add_student_window(self):
        if self.active_window is not None and self.active_window.winfo_exists():
            self.active_window.focus()
            return

        window = ctk.CTkToplevel(self)
        self.active_window = window
        window.title("Добавить ученика")
        self.center_window(window, 420, 580) 
        window.configure(fg_color="#1e293b")
        window.attributes("-topmost", True)
        window.protocol("WM_DELETE_WINDOW", lambda: self.close_active_window(window))

        ctk.CTkLabel(window, text="Новый ученик", font=("Segoe UI", 20, "bold"), text_color="#f8fafc").pack(pady=(25, 15))

        def create_field(parent, label_text):
            ctk.CTkLabel(parent, text=label_text, font=("Segoe UI", 13), text_color="#cbd5e1").pack(anchor="w", padx=40, pady=(8, 2))
            entry = ctk.CTkEntry(parent, height=38, fg_color="#0f172a", border_color="#334155", border_width=1, corner_radius=8)
            entry.pack(fill="x", padx=40)
            return entry

        entry_full_name = create_field(window, "Фамилия:")
        entry_name = create_field(window, "Имя:")
        entry_age = create_field(window, "Возраст (16-120):")
        entry_course = create_field(window, "Курс (1-5):")

        # МЕСТО ДЛЯ ВЫВОДА ОШИБКИ
        error_label = ctk.CTkLabel(window, text="", font=("Segoe UI", 12, "bold"), text_color="#ef4444", wraplength=340)
        error_label.pack(pady=(10, 0))

        def save_student(event=None):
            error_label.configure(text="") # Очищаем ошибку
            
            f_name = entry_full_name.get().strip().capitalize()
            name = entry_name.get().strip().capitalize()
            
            if not f_name or not name:
                error_label.configure(text="Имя и фамилия не могут быть пустыми!")
                return
            if any(ch.isdigit() for ch in f_name) or any(ch.isdigit() for ch in name):
                error_label.configure(text="Имя и фамилия не должны содержать цифры!")
                return
            try:
                age = int(entry_age.get())
                course = int(entry_course.get())
            except ValueError:
                error_label.configure(text="Возраст и курс должны быть числами!")
                return
            if not (const.MIN_AGE <= age <= const.MAX_AGE) or not (const.MIN_COURSE <= course <= const.MAX_COURSE):
                error_label.configure(text="Недопустимый возраст или курс!")
                return

            same_course_students = [s for s in self.group.list_students if s.course == course]
            group_num = 1
            while True:
                members = [s for s in same_course_students if getattr(s, 'group_num', 1) == group_num]
                if len(members) < const.MAX_STUDENTS_IN_GROUP:
                    break
                group_num += 1

            new_student = Student(name, f_name, age, course, group_num)
            if new_student in self.group.list_students:
                error_label.configure(text="Такой студент уже есть в базе!")
                return

            self.group.list_students.append(new_student)
            self.group.save_to_file()
            messagebox.showinfo("Успех", f"Студент добавлен в группу {course}-{group_num}!", parent=window)
            self.close_active_window(window)
            self.show_teacher_menu()

        entry_full_name.focus_set() # Ставим курсор на первое поле при открытии

        entry_full_name.bind("<Return>", lambda e: entry_name.focus_set())
        entry_name.bind("<Return>", lambda e: entry_age.focus_set())
        entry_age.bind("<Return>", lambda e: entry_course.focus_set())
        # На последнем поле Enter вызывает сохранение
        entry_course.bind("<Return>", save_student) 

        ctk.CTkButton(window, text="Добавить", font=("Segoe UI", 15, "bold"), height=45,
                      fg_color="#22c55e", hover_color="#16a34a", command=save_student).pack(pady=15, fill="x", padx=40)
        
    def open_delete_student_window(self):
        if not self.group.list_students:
            messagebox.showinfo("Внимание", "Список учеников пуст.")
            return
        if self.active_window is not None and self.active_window.winfo_exists():
            self.active_window.focus()
            return

        window = ctk.CTkToplevel(self)
        self.active_window = window
        window.title("Удалить ученика")
        self.center_window(window, 400, 250)
        window.configure(fg_color="#1e293b")
        window.attributes("-topmost", True)
        window.protocol("WM_DELETE_WINDOW", lambda: self.close_active_window(window))

        ctk.CTkLabel(window, text="Выберите ученика", font=("Segoe UI", 18, "bold"), text_color="#f8fafc").pack(pady=(20, 10))

        student_strings = [f"{s.full_name} {s.name} (гр. {getattr(s, 'group_num', 1)})" for s in self.group.list_students]
        
        # ДОБАВЛЕН state="readonly"
        combo_student = ctk.CTkComboBox(window, values=student_strings, width=300, height=40, 
                                        fg_color="#0f172a", border_color="#334155", state="readonly")
        combo_student.pack(pady=10)
        combo_student.set(student_strings[0])

        def delete_student():
            selected_text = combo_student.get()
            for student in self.group.list_students:
                student_str = f"{student.full_name} {student.name} (гр. {getattr(student, 'group_num', 1)})"
                if student_str == selected_text:
                    confirm = messagebox.askyesno("Подтверждение", f"Удалить {student.full_name} {student.name}?")
                    if confirm:
                        self.group.list_students.remove(student)
                        self.group.save_to_file()
                        messagebox.showinfo("Успех", "Ученик удален!")
                        self.close_active_window(window)
                        self.show_teacher_menu()
                    return

        ctk.CTkButton(window, text="Удалить", font=("Segoe UI", 16, "bold"), height=40,
                      fg_color="#ef4444", hover_color="#dc2626", command=delete_student).pack(pady=20)

    def show_student_profile(self, student, is_teacher=False):
        self.clear_screen()
        self.configure(fg_color="#0f172a")
        
        self.current_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.current_frame.pack(pady=20, padx=40, fill="both", expand=True)

        header_text = f"👤 Дневник: {student.full_name} {student.name}"
        if is_teacher:
            header_text += " (режим учителя)"
        
        ctk.CTkLabel(self.current_frame, text=header_text, font=("Segoe UI", 32, "bold"), text_color="#f8fafc").pack(pady=(0, 15))

        bottom_frame = ctk.CTkFrame(self.current_frame, fg_color="transparent")
        bottom_frame.pack(side="bottom", pady=20)

        if is_teacher:
            ctk.CTkButton(bottom_frame, text="➕ Поставить оценку", font=("Segoe UI", 16, "bold"), fg_color="#3b82f6", hover_color="#2563eb", corner_radius=8, height=45, width=200, command=lambda: self.open_add_grade_window(student, is_teacher)).pack(side="left", padx=10)
            ctk.CTkButton(bottom_frame, text="🗑 Удалить оценку", font=("Segoe UI", 16, "bold"), fg_color="transparent", border_color="#ef4444", border_width=2, height=45, width=200, text_color="#ef4444", hover_color="#1e293b", corner_radius=8, command=lambda: self.open_delete_grade_window(student, is_teacher)).pack(side="left", padx=10)
            ctk.CTkButton(bottom_frame, text="↩ Назад к списку", font=("Segoe UI", 16, "bold"), fg_color="#475569", hover_color="#64748b", corner_radius=8, height=45, width=200, command=self.show_teacher_menu).pack(side="left", padx=10)
        else:
            ctk.CTkButton(bottom_frame, text="🧮 Рассчитать оценку", font=("Segoe UI", 16, "bold"), fg_color="#eab308", hover_color="#ca8a04", text_color="#0f172a", corner_radius=8, height=45, width=200, command=lambda: self.open_calculator_window(student)).pack(side="left", padx=10)
            ctk.CTkButton(bottom_frame, text="👥 Моя группа", font=("Segoe UI", 16, "bold"), fg_color="#3b82f6", hover_color="#2563eb", corner_radius=8, height=45, width=200, command=lambda: self.show_my_group_gui(student)).pack(side="left", padx=10)
            ctk.CTkButton(bottom_frame, text="↩ Назад", font=("Segoe UI", 16, "bold"), fg_color="#475569", hover_color="#64748b", corner_radius=8, height=45, width=200, command=self.show_student_menu).pack(side="left", padx=10)

        # КОНТЕЙНЕР ДЛЯ ТАБЛИЦЫ (используем ту же маскировку скроллбара)
        table_container = ctk.CTkFrame(self.current_frame, fg_color="#1e293b", corner_radius=15)
        table_container.pack(fill="both", expand=True, padx=80, pady=10)

        list_frame = ctk.CTkScrollableFrame(table_container, fg_color="#1e293b", corner_radius=0, scrollbar_fg_color="#1e293b", scrollbar_button_color="#334155")
        list_frame.pack(fill="both", expand=True, padx=2, pady=2)
        
        list_frame.grid_columnconfigure(1, weight=1) # Растягиваем колонку с оценками

        total_sum = 0
        total_count = 0

        def get_grade_color(grade):
            if grade == 5: return "#22c55e"
            if grade == 4: return "#eab308"
            if grade == 3: return "#f97316"
            return "#ef4444"

        for row_idx, (subject, title) in enumerate(const.SUBJECTS.items()):
            ctk.CTkLabel(list_frame, text=title, font=("Segoe UI", 18, "bold"), text_color="#f8fafc", width=150, anchor="w").grid(row=row_idx, column=0, padx=(30, 10), pady=15, sticky="nw")

            # ФРЕЙМ ДЛЯ ОЦЕНОК С УМНЫМ ПЕРЕНОСОМ
            grades_frame = ctk.CTkFrame(list_frame, fg_color="transparent")
            grades_frame.grid(row=row_idx, column=1, padx=10, pady=15, sticky="w")

            grades_list = student.grades.get(subject, [])
            if not grades_list:
                ctk.CTkLabel(grades_frame, text="Нет оценок", font=("Segoe UI", 16, "italic"), text_color="#64748b").pack(side="left")
            else:
                current_row_frame = ctk.CTkFrame(grades_frame, fg_color="transparent")
                current_row_frame.pack(anchor="w")
                count_in_row = 0

                for g in grades_list:
                    # Если в ряду уже 8 оценок, создаем новый ряд
                    if count_in_row >= 8:
                        current_row_frame = ctk.CTkFrame(grades_frame, fg_color="transparent")
                        current_row_frame.pack(anchor="w", pady=(5, 0))
                        count_in_row = 0

                    color = get_grade_color(g)
                    ctk.CTkLabel(current_row_frame, text=str(g), font=("Segoe UI", 16, "bold"),
                        fg_color=color, text_color="#0f172a", width=35, height=35, corner_radius=8).pack(side="left", padx=3)
                    
                    count_in_row += 1
                
                total_sum += sum(grades_list)
                total_count += len(grades_list)

            if grades_list:
                avg_sub = sum(grades_list) / len(grades_list)
                avg_str = f"Средняя: {avg_sub:.2f}"
            else:
                avg_str = ""
            
            ctk.CTkLabel(list_frame, text=avg_str, font=("Segoe UI", 16), text_color="#94a3b8", width=120, anchor="e").grid(row=row_idx, column=2, padx=(10, 30), pady=15, sticky="ne")

        if total_count > 0:
            overall_avg = total_sum / total_count
            overall_text = f"🏆 Общая средняя оценка: {overall_avg:.2f} (окр. до {correct_round(overall_avg)})"
            avg_color = "#22c55e" if overall_avg >= 4.5 else "#eab308" if overall_avg >= 3.5 else "#ef4444"
        else:
            overall_text = "🏆 Общая средняя оценка: нет оценок"
            avg_color = "#475569"

        ctk.CTkLabel(self.current_frame, text=overall_text, font=("Segoe UI", 20, "bold"), text_color="#0f172a", fg_color=avg_color, corner_radius=12).pack(pady=15, ipadx=30, ipady=10)

    def show_my_group_gui(self, student):
        self.clear_screen()
        self.current_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.current_frame.pack(pady=20, padx=40, fill="both", expand=True)

        his_group_num = getattr(student, 'group_num', 1)
        my_groupmates = [s for s in self.group.list_students 
                         if s.course == student.course and getattr(s, 'group_num', 1) == his_group_num]

        my_groupmates.sort(key=lambda s: s.cached_avg, reverse=True)

        label = ctk.CTkLabel(self.current_frame, text=f"👥 Моя группа ({student.course}-{his_group_num})", font=("Segoe UI", 32, "bold"), text_color="#f8fafc")
        label.pack(pady=(0, 15))

        ctk.CTkButton(self.current_frame, text="↩ Назад в дневник", font=("Segoe UI", 16, "bold"), fg_color="#475569", hover_color="#64748b", corner_radius=8, height=45, width=220, command=lambda: self.show_student_profile(student, is_teacher=False)).pack(side="bottom", pady=20)

        list_frame = ctk.CTkScrollableFrame(self.current_frame, fg_color="#1e293b", corner_radius=15)
        list_frame.pack(fill="both", expand=True, pady=10, padx=50)

        for index, classmate in enumerate(my_groupmates):
            is_me = (classmate == student)
            avg_score = classmate.cached_avg
            place = index + 1
            
            medal = "🥇" if place == 1 else "🥈" if place == 2 else "🥉" if place == 3 else ""

            card_color = "#1e293b" if is_me else "#0f172a" 
            
            if place == 1: border_color = "#eab308"
            elif place == 2: border_color = "#94a3b8"
            elif place == 3: border_color = "#b45309"
            else: border_color = "#3b82f6" if is_me else "#334155"
                
            border_w = 2 if (is_me or place <= 3) else 1

            card = ctk.CTkFrame(list_frame, fg_color=card_color, corner_radius=10, border_color=border_color, border_width=border_w)
            card.pack(fill="x", pady=6, padx=20)
            card.grid_columnconfigure(1, weight=1)

            name_text = f"{medal}  {classmate.full_name} {classmate.name}"
            ctk.CTkLabel(card, text=name_text, font=("Segoe UI", 18, "bold"), text_color="#ffffff" if is_me else "#cbd5e1", anchor="w").grid(row=0, column=0, padx=(20, 10), pady=15, sticky="w")

            if is_me:
                ctk.CTkLabel(card, text="ВЫ", font=("Segoe UI", 12, "bold"), text_color="#3b82f6", fg_color="#1e3a8a", corner_radius=4, width=30, height=20).grid(row=0, column=2, padx=10, pady=15, sticky="w")

            if is_me:
                score_text = f"{avg_score:.2f}" if avg_score > 0 else "Нет"
                score_bg = "#16a34a" if avg_score >= 4.5 else "#ca8a04" if avg_score >= 3.5 else "#dc2626" if avg_score > 0 else "#475569"
                score_text_color = "#ffffff" if score_bg != "#475569" else "#cbd5e1"

                ctk.CTkLabel(card, text=score_text, font=("Segoe UI", 18, "bold"), text_color=score_text_color, fg_color=score_bg, width=60, height=35, corner_radius=8).grid(row=0, column=3, padx=(10, 20), pady=15, sticky="e")
            else:
                # ФИКС БЕЗОПАСНОСТИ: Проверяем, есть ли оценки, прежде чем давать статус
                if place <= 3 and avg_score > 0:
                    status_text = "Отличник" if avg_score >= 4.5 else "Хорошист"
                    ctk.CTkLabel(card, text=status_text, font=("Segoe UI", 14, "italic"), text_color="#94a3b8").grid(row=0, column=3, padx=(10, 20), pady=15, sticky="e")
                else:
                    ctk.CTkLabel(card, text="—", font=("Segoe UI", 16, "bold"), text_color="#475569").grid(row=0, column=3, padx=(10, 20), pady=15, sticky="e")

    def open_add_grade_window(self, student, is_teacher):
        # ЖЕСТКАЯ ПРОВЕРКА ПРАВ (Защита от вызова в обход интерфейса)
        if not self.is_teacher_mode or not is_teacher:
            messagebox.showerror("Ошибка доступа", "У вас нет прав на выставление оценок!")
            return
        
        if self.active_window is not None and self.active_window.winfo_exists():
            self.active_window.focus()
            return

        window = ctk.CTkToplevel(self)
        self.active_window = window
        window.title("Добавить оценку")
        self.center_window(window, 400, 380)
        window.configure(fg_color="#1e293b")
        window.attributes("-topmost", True)
        window.protocol("WM_DELETE_WINDOW", lambda: self.close_active_window(window))

        ctk.CTkLabel(window, text=f"Ученик: {student.full_name}", font=("Segoe UI", 18, "bold"), text_color="#f8fafc").pack(pady=(20, 15))

        ctk.CTkLabel(window, text="Выберите предмет:", font=("Segoe UI", 13, "bold"), text_color="#cbd5e1").pack(anchor="w", padx=40, pady=(5, 2))
        combo_subject = ctk.CTkComboBox(window, values=list(const.SUBJECTS.values()), height=35, fg_color="#0f172a", border_color="#334155", state="readonly")
        combo_subject.pack(fill="x", padx=40)
        combo_subject.set(list(const.SUBJECTS.values())[0])

        ctk.CTkLabel(window, text="Оценка (1-5):", font=("Segoe UI", 13, "bold"), text_color="#cbd5e1").pack(anchor="w", padx=40, pady=(10, 2))
        entry_grade = ctk.CTkEntry(window, height=35, fg_color="#0f172a", border_color="#334155")
        entry_grade.pack(fill="x", padx=40)

        # МЕСТО ДЛЯ ВЫВОДА ОШИБКИ (красный текст под полем)
        error_label = ctk.CTkLabel(window, text="", font=("Segoe UI", 12, "bold"), text_color="#ef4444")
        error_label.pack(pady=(5, 0))

        def save_grade():
            error_label.configure(text="") # Очищаем старую ошибку
            
            try:
                grade = int(entry_grade.get())
                if not (const.MIN_ESTIMATION <= grade <= const.MAX_ESTIMATION):
                    error_label.configure(text=f"Оценка должна быть от {const.MIN_ESTIMATION} до {const.MAX_ESTIMATION}!")
                    return
                
                subject_name = combo_subject.get()
                keys_found = [k for k, v in const.SUBJECTS.items() if v == subject_name]
                if not keys_found:
                    error_label.configure(text="Выбран неверный предмет!")
                    return
                subject_key = keys_found[0]

                student.add_grade(subject_key, grade)
                self.group.save_to_file()
                self.close_active_window(window)
                self.show_student_profile(student, is_teacher)
                
            except ValueError:
                error_label.configure(text="Ошибка: введите целое число!")

        ctk.CTkButton(window, text="Сохранить", font=("Segoe UI", 16, "bold"), height=45,
                      fg_color="#22c55e", hover_color="#16a34a", command=save_grade).pack(pady=15, fill="x", padx=40)

    def open_delete_grade_window(self, student, is_teacher):
        # ЖЕСТКАЯ ПРОВЕРКА ПРАВ
        if not self.is_teacher_mode or not is_teacher:
            messagebox.showerror("Ошибка доступа", "У вас нет прав на удаление оценок!")
            return
        
        if self.active_window is not None and self.active_window.winfo_exists():
            self.active_window.focus()
            return

        window = ctk.CTkToplevel(self)
        self.active_window = window
        window.title("Удалить оценку")
        self.center_window(window, 400, 400)
        window.configure(fg_color="#1e293b")
        window.attributes("-topmost", True)
        window.protocol("WM_DELETE_WINDOW", lambda: self.close_active_window(window))

        ctk.CTkLabel(window, text=f"Ученик: {student.full_name}", font=("Segoe UI", 18, "bold"), text_color="#f8fafc").pack(pady=(20, 15))

        ctk.CTkLabel(window, text="Выберите предмет:", font=("Segoe UI", 13, "bold"), text_color="#cbd5e1").pack(anchor="w", padx=40, pady=(5, 2))
        
        # ДОБАВЛЕН state="readonly"
        combo_subject = ctk.CTkComboBox(window, values=list(const.SUBJECTS.values()), height=35, fg_color="#0f172a", border_color="#334155", state="readonly")
        combo_subject.pack(fill="x", padx=40)
        combo_subject.set(list(const.SUBJECTS.values())[0])

        ctk.CTkLabel(window, text="Выберите оценку для удаления:", font=("Segoe UI", 13, "bold"), text_color="#cbd5e1").pack(anchor="w", padx=40, pady=(10, 2))
        grade_var = ctk.StringVar()
        
        # ДОБАВЛЕН state="readonly"
        combo_grade = ctk.CTkComboBox(window, values=["Нет оценок"], variable=grade_var, height=35, fg_color="#0f172a", border_color="#334155", state="readonly")
        combo_grade.pack(fill="x", padx=40)

        def update_grades_list(event=None):
            subject_name = combo_subject.get()
            keys_found = [k for k, v in const.SUBJECTS.items() if v == subject_name]
            if not keys_found:
                return
            subject_key = keys_found[0]
            
            grades = student.grades.get(subject_key, [])
            if grades:
                combo_grade.configure(values=[str(g) for g in grades])
                combo_grade.set(str(grades[0]))
            else:
                combo_grade.configure(values=["Нет оценок"])
                combo_grade.set("Нет оценок")

        combo_subject.configure(command=update_grades_list)
        update_grades_list()

        def delete_grade():
            if combo_grade.get() == "Нет оценок":
                messagebox.showwarning("Внимание", "У этого ученика нет оценок по этому предмету.")
                return

            subject_name = combo_subject.get()
            keys_found = [k for k, v in const.SUBJECTS.items() if v == subject_name]
            if not keys_found:
                return
            subject_key = keys_found[0]
            
            grade_to_del = int(combo_grade.get())

            if student.del_grade(subject_key, grade_to_del):
                self.group.save_to_file()
                self.close_active_window(window)
                self.show_student_profile(student, is_teacher)
            else:
                messagebox.showerror("Ошибка", "Не удалось удалить оценку.")

        ctk.CTkButton(window, text="Удалить", font=("Segoe UI", 16, "bold"), height=45,
                      fg_color="#ef4444", hover_color="#dc2626", command=delete_grade).pack(pady=25, fill="x", padx=40)

    def show_student_menu(self):
        self.clear_screen()
        self.configure(fg_color="#0f172a")

        self.current_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.current_frame.pack(expand=True, fill="both")

        login_card = ctk.CTkFrame(self.current_frame, width=450, height=580, fg_color="#1e293b", corner_radius=20)
        login_card.place(relx=0.5, rely=0.45, anchor="center") 

        ctk.CTkLabel(login_card, text="🎓 Вход для Ученика", font=("Segoe UI", 28, "bold"), text_color="#f8fafc").pack(pady=(30, 5))
        ctk.CTkLabel(login_card, text="Введите свои данные для входа", font=("Segoe UI", 14), text_color="#94a3b8").pack(pady=(0, 20))

        form_frame = ctk.CTkFrame(login_card, fg_color="transparent")
        form_frame.pack(fill="x", padx=40)

        def create_field(parent, label_text):
            ctk.CTkLabel(parent, text=label_text, font=("Segoe UI", 13, "bold"), text_color="#cbd5e1").pack(anchor="w", pady=(10, 2))
            entry = ctk.CTkEntry(parent, height=40, fg_color="#0f172a", border_color="#334155", border_width=1, corner_radius=8)
            entry.pack(fill="x")
            return entry

        entry_full_name = create_field(form_frame, "Фамилия")
        entry_name = create_field(form_frame, "Имя")
        entry_age = create_field(form_frame, "Возраст")
        entry_course = create_field(form_frame, "Курс")

        def try_login(event=None): # Добавили event=None, чтобы функция не падала при вызове через bind
            f_name = entry_full_name.get().strip().capitalize()
            name = entry_name.get().strip().capitalize()
            
            try:
                age = int(entry_age.get())
                course = int(entry_course.get())
            except ValueError:
                messagebox.showerror("Ошибка", "Возраст и курс должны быть числами!")
                return

            for student in self.group.list_students:
                if (student.full_name == f_name and student.name == name and 
                    student.age == age and student.course == course):
                    self.show_student_profile(student, is_teacher=False)
                    return
            
            messagebox.showerror("Ошибка", "Ученик с такими данными не найден!\nПроверьте правильность ввода.")

        entry_full_name.focus_set() # Сразу ставим курсор в Фамилию

        # При нажатии Enter переводим курсор на следующее поле (используем lambda)
        entry_full_name.bind("<Return>", lambda e: entry_name.focus_set())
        entry_name.bind("<Return>", lambda e: entry_age.focus_set())
        entry_age.bind("<Return>", lambda e: entry_course.focus_set())
        
        # На последнем поле Enter вызывает функцию входа
        entry_course.bind("<Return>", lambda e: try_login())

        btn_login = ctk.CTkButton(login_card, text="Войти в дневник", font=("Segoe UI", 18, "bold"), 
                                  height=50, fg_color="#22c55e", hover_color="#16a34a", corner_radius=10, 
                                  command=try_login)
        btn_login.pack(fill="x", padx=40, pady=(30, 20))

        bottom_frame = ctk.CTkFrame(self.current_frame, fg_color="transparent")
        bottom_frame.pack(side="bottom", pady=30)

        ctk.CTkButton(bottom_frame, text="↩ Сменить роль", font=("Segoe UI", 14, "bold"), 
                      height=40, width=180, fg_color="transparent", border_color="#475569", 
                      border_width=1.5, text_color="#94a3b8", hover_color="#1e293b", corner_radius=8,
                      command=self.show_login_screen).pack(side="left", padx=15)
        
        ctk.CTkButton(bottom_frame, text="⏻ Выйти из программы", font=("Segoe UI", 14, "bold"), 
                      height=40, width=200, fg_color="transparent", border_color="#ef4444", 
                      border_width=1.5, text_color="#ef4444", hover_color="#1e293b", corner_radius=8,
                      command=self.exit_app).pack(side="left", padx=15)

# --- БЛОК ЗАПУСКА ---
if __name__ == "__main__":
    app = DiaryApp()
    app.mainloop()