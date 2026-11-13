# --- ДЕЙСТВИЯ В ПРОФИЛЕ (ДЛЯ УЧИТЕЛЯ) ---
OPTION_STUDENT_ADD_ESTIMATION = 1
OPTION_STUDENT_DEL_ESTIMATION = 2
OPTION_STUDENT_SHOW_ESTIMATIONS_COMPLETELY = 3
OPTION_STUDENT_SHOW_ESTIMATIONS_BY_SUBJECT = 4
OPTION_STUDENT_SHOW_AVERAGE_SCORE_COMPLETELY = 5
OPTION_STUDENT_SHOW_AVERAGE_SCORE_BY_SUBJECT = 6
OPTION_STUDENT_EXIT_PROFILE = 7

# --- ДЕЙСТВИЯ В ПРОФИЛЕ (ДЛЯ УЧЕНИКА - только просмотр) ---
OPTION_STUDENT_VIEW_ALL_GRADES = 1
OPTION_STUDENT_VIEW_SUBJECT_GRADES = 2
OPTION_STUDENT_VIEW_ALL_AVERAGE = 3
OPTION_STUDENT_VIEW_SUBJECT_AVERAGE = 4
OPTION_STUDENT_VIEW_EXIT = 5

# --- ГЛАВНОЕ МЕНЮ (ДЛЯ УЧИТЕЛЯ) ---
OPTION_T_SHOW_ALL_STUDENTS = 1
OPTION_T_ADD_STUDENT = 2
OPTION_T_DEL_STUDENT = 3
OPTION_T_ENTER_FOR_STUDENT = 4
OPTION_T_EXIT_PROGRAM = 5

# --- ГЛАВНОЕ МЕНЮ (ДЛЯ УЧЕНИКА) ---
OPTION_S_ENTER_FOR_STUDENT = 1
OPTION_S_SHOW_MY_GROUP = 2
OPTION_S_EXIT_PROGRAM = 3

# --- ОГРАНИЧЕНИЯ ---
MAX_STUDENTS_IN_GROUP = 3  # Количество человек в одной группе
MAX_LEN_NAME = 50
MAX_LEN_FULL_NAME = 50
MIN_COURSE = 1
MAX_COURSE = 5
MIN_AGE = 16
MAX_AGE = 120
MIN_ESTIMATION = 1
MAX_ESTIMATION = 5

# --- ПРЕДМЕТЫ ---
SUBJECTS = {
    "math": "📐 Математика",
    "phys": "🧪 Физика",
    "eng": "🇬🇧 Английский",
    "inf": "💻 Информатика",
    "rus": "📖 Русский язык",
}

# --- ТЕКСТЫ МЕНЮ ---
MENU_TEACHER = """Ваш электронный дневник (Режим Учителя)

1. Список всех учеников
2. Добавить нового ученика
3. Удалить ученика из группы
4. Открыть дневник ученика
5. Завершить работу
"""

MENU_STUDENT = """Ваш электронный дневник (Режим Ученика)

1. Открыть мой дневник
2. Список учеников моей группы
3. Завершить работу
"""

THEME = {
    "main_bg": "#09090b",
    "card_bg": "#18181b",
    "text_main": "#f8fafc",
    "text_muted": "#94a3b8",
    "border": "#27272a"
}