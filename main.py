class Student:
    _base = []

    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}
        Student._base.append(self)

    def add_courses(self, course_name):
        self.finished_courses.append(course_name)
        if course_name in self.courses_in_progress:
            self.courses_in_progress.remove(course_name)

    def rate_hw(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and course in \
                lecturer.courses_attached and course in \
                self.courses_in_progress:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def _rating(self):
        res = 0
        lens = 0
        for key in self.grades:
            lens += len(self.grades.get(key))
            for value in self.grades.get(key):
                res += value
        if lens != 0:
            return round(res / lens, 1)
        else:
            return 'Оценки еще не выставлялись'

    def __str__(self):
        return f'Имя: {self.name} \nФамилия: {self.surname}'\
               f'\nСредняя оценка за домашние задания: {self._rating()}' \
               f'\nКурсы в процессе изучения: ' \
               f'{", ".join(self.courses_in_progress)}'\
               f'\nЗавершенные курсы: {", ".join(self.finished_courses)}'


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    _base = []

    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}
        Lecturer._base.append(self)

    def __str__(self):
        return f'Имя: {self.name} \nФамилия: {self.surname}' \
               f'\nСредняя оценка за лекции: {self._rating()}'

    def _rating(self):
        res = 0
        lens = 0
        for key in self.grades:
            lens += len(self.grades.get(key))
            for value in self.grades.get(key):
                res += value
        if lens != 0:
            return round(res / lens, 1)
        else:
            return 'Оценки еще не выставлялись'

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return 'Нет такого лектора!'
        if self._rating() < other._rating():
            return f'{self.name} {self.surname} хуже преподает чем ' \
                   f'{other.name + " " + other.surname}'
        elif self._rating() > other._rating():
            return f'{self.name} {self.surname} лучше преподает чем ' \
                   f'{other.name + " " + other.surname}'
        else:
            return 'Равны'


class Reviewer(Mentor):
    def __str__(self):
        return f'Имя: {self.name} \nФамилия: {self.surname}'

    def rate_hw(self, student, lecturer, course, grade):
        if isinstance(student, Student) and course in \
                lecturer.courses_attached and course in \
                student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'


def rating_all(who, course):
    res = 0
    count_value = 0
    for student in who._base:
        if course in student.grades.keys():
            for value in student.grades.get(course):
                res += value
                count_value += 1
    if count_value != 0:
        return f'{course}: {round(res / count_value, 1)}'
    else:
        return 'Оценки еще не выставлялись по данному предмету'


student_1 = Student('Иван', 'Иванов', 'муж')
student_1.courses_in_progress += ['Python', 'C++', 'HTML']
student_1.finished_courses += ['Maths']
student_1.add_courses('HTML')
student_2 = Student('Сергей', 'Петров', 'муж')
student_2.courses_in_progress += ['C++', 'HTML', 'Maths']
student_2.add_courses('Python')
lecturer_1 = Lecturer('Мария', 'Коновалова')
lecturer_1.courses_attached += ['Python', 'C++', 'Maths']
lecturer_2 = Lecturer('Илья', 'Мещеряков')
lecturer_2.courses_attached += ['C++', 'HTML']
reviewer_1 = Reviewer('Артур', 'Мальцев')
reviewer_1.courses_attached += ['Python', 'C++', 'Maths']
reviewer_2 = Reviewer('Арина', 'Новикова')
reviewer_2.courses_attached += ['C++', 'HTML']

student_1.rate_hw(lecturer_1, 'Python', 10)
student_1.rate_hw(lecturer_1, 'C++', 11)
student_1.rate_hw(lecturer_1, 'C++', 8)
student_2.rate_hw(lecturer_2, 'HTML', 7)
reviewer_1.rate_hw(student_2, lecturer_1, 'C++', 8)
reviewer_2.rate_hw(student_2, lecturer_2, 'HTML', 10)

print(f'\nСтуденты: \n{student_1} \n\n{student_2}')
print(f'\nЛекторы: \n{lecturer_1} \n\n{lecturer_2}')
print(f'\nСравнение лекторов:', '\n    ', lecturer_1 < lecturer_2)
print(f'\nЭксперты: \n{reviewer_1} \n\n{reviewer_2}')
print(f'\nСредняя оценка за ДЗ по всем студентам по курсу'
      f' {rating_all(Student, "C++")}')
print(f'\nСредняя оценка за лекции всех лекторов в рамках курса'
      f' {rating_all(Lecturer, "Python")}')
