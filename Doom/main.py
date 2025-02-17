# Задание 1: Переменные и ввод/вывод
name = input("Введите ваше имя: ")
age = input("Введите ваш возраст: ")

# Проверка, что возраст введен корректно
if age.isdigit():
    age = int(age)
    print(f"Привет, {name}! Тебе {age} лет и это прекрасный возраст! :)")
else:
    print("Ошибка: возраст должен быть числом.")

# Задание 2: Условные операторы
while True:
    user_input = input("Введите число для проверки его четности (или 'выход' для завершения): ")

    if user_input.lower() == "выход":
        break

    if user_input.isdigit():
        number = int(user_input)
        if number % 2 == 0:
            print(f"{number} - четное число.")
        else:
            print(f"{number} - нечетное число.")
    else:
        print("Ошибка: введите корректное число.")

# Задание 3: Циклы
user_input = input("Введите число минимум из 5 цифр: ")

if len(user_input) < 5 or not user_input.isdigit():
    print("Предупреждение: введите число, состоящее минимум из 5 цифр.")
else:
    total_sum = sum(int(digit) for digit in user_input)
    print(f"Сумма всех цифр введенного числа: {total_sum}")


# Задание 4: Функции
def cube(number):
    return number ** 3


def cubes_list(numbers):
    return [cube(num) for num in numbers]


user_input = input("Введите список чисел через пробел: ")
try:
    numbers = list(map(int, user_input.split()))
    cubed_numbers = cubes_list(numbers)
    print(f"Список кубов введенных чисел: {cubed_numbers}")
except ValueError:
    print("Ошибка: введите только числовые значения.")


# Задание 5: Основы ООП
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce(self):
        print(f"Меня зовут {self.name}, мне {self.age} лет.")

    def age_in_five_years(self):
        return self.age + 5

    def is_adult(self):
        return self.age >= 18

    def change_name(self, new_name):
        self.name = new_name


# Создание объектов класса Person
person1 = Person("Алексей", 25)
person2 = Person("Мария", 17)

# Использование методов
for person in [person1, person2]:
    person.introduce()
    print(f"Через 5 лет мне будет {person.age_in_five_years()} лет.")
    print(f"Совершеннолетний: {person.is_adult()}")
    print()

# Изменение имени
person1.change_name("Сергей")
person1.introduce()