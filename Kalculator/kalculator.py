import flet as ft
from pint import UnitRegistry

# Инициализация библиотеки pint
ureg = UnitRegistry()

# Словарь для преобразования пользовательских сокращений в единицы pint
unit_map = {
    'мм': 'millimeter',
    'см': 'centimeter',
    'м': 'meter',
    'км': 'kilometer',
    'с': 'second',
    'мин': 'minute',
    'час': 'hour',
    'сутки': 'day',
    'год': 'year',
    'кв.мм': 'square millimeter',
    'кв.см': 'square centimeter',
    'кв.м': 'square meter',
    'кв.км': 'square kilometer',
    'бит': 'bit',
    'байт': 'byte',
    'кб': 'kilobyte',
    'мб': 'megabyte',
    'гб': 'gigabyte',
    'тб': 'terabyte',
    'пб': 'petabyte',
    'т': 'tonne',
    'кг': 'kilogram',
    'мг': 'milligram',
    'мкг': 'microgram',
    'ц': 'quintal',
    'c': 'celsius',
    'f': 'fahrenheit',
    'k': 'kelvin',
    'мл': 'milliliter',
    'л': 'liter',
    'куб.м': 'cubic meter'
}

# Функция для конвертации единиц
def convert_units(value, from_unit, to_unit):
    try:
        # Преобразование пользовательских сокращений в единицы pint
        from_unit_converted = unit_map[from_unit]
        to_unit_converted = unit_map[to_unit]
        # Конвертация значений с использованием pint
        result = (value * ureg(from_unit_converted)).to(to_unit_converted)
        return result
    except Exception as e:
        return str(e)

# Функция для сложения и вычитания единиц
def add_or_subtract_units(value1, unit1, value2, unit2, operation):
    try:
        # Преобразование пользовательских сокращений в единицы pint
        unit1_converted = unit_map[unit1]
        unit2_converted = unit_map[unit2]
        quantity1 = value1 * ureg(unit1_converted)
        quantity2 = value2 * ureg(unit2_converted)
        # Выполнение операции сложения или вычитания
        if operation == "add":
            result = quantity1 + quantity2
        elif operation == "subtract":
            result = quantity1 - quantity2
        return result.to_base_units()
    except Exception as e:
        return str(e)

# Главная функция для приложения Flet
def main(page: ft.Page):
    # Определение элементов интерфейса
    value1_input = ft.TextField(label="Значение 1", width=200, border_color=ft.colors.LIME, color=ft.colors.LIME)
    unit1_input = ft.TextField(label="Единица 1", width=200, border_color=ft.colors.LIME, color=ft.colors.LIME)
    value2_input = ft.TextField(label="Значение 2", width=200, border_color=ft.colors.LIME, color=ft.colors.LIME)
    unit2_input = ft.TextField(label="Единица 2", width=200, border_color=ft.colors.LIME, color=ft.colors.LIME)
    to_unit_input = ft.TextField(label="Целевая единица", width=200, border_color=ft.colors.LIME, color=ft.colors.LIME)
    result_text = ft.Text(style="bodyText1", color=ft.colors.LIME, font_family="Roboto Condensed")

    # Обработчик события для кнопки "Конвертировать"
    def convert_click(e):
        try:
            value = float(value1_input.value)
            from_unit = unit1_input.value.strip().lower()
            to_unit = to_unit_input.value.strip().lower()
            # Проверка на правильность ввода единиц
            if from_unit not in unit_map or to_unit not in unit_map:
                result_text.value = "Неправильная единица измерения. Пожалуйста, используйте допустимые сокращения."
            else:
                result = convert_units(value, from_unit, to_unit)
                if isinstance(result, str):
                    result_text.value = f"Ошибка при конвертации: {result}"
                else:
                    result_text.value = f"{value} {from_unit} = {result:.20f} {to_unit}"
        except ValueError:
            result_text.value = "Введите корректное числовое значение"
        page.update()

    # Обработчик события для кнопки "Сложить"
    def add_click(e):
        try:
            value1 = float(value1_input.value)
            unit1 = unit1_input.value.strip().lower()
            value2 = float(value2_input.value)
            unit2 = unit2_input.value.strip().lower()
            # Проверка на правильность ввода единиц
            if unit1 not in unit_map or unit2 not in unit_map:
                result_text.value = "Неправильная единица измерения. Пожалуйста, используйте допустимые сокращения."
            else:
                result = add_or_subtract_units(value1, unit1, value2, unit2, "add")
                if isinstance(result, str):
                    result_text.value = f"Ошибка при сложении: {result}"
                else:
                    result_text.value = f"{value1} {unit1} + {value2} {unit2} = {result:.6f} ({result.units})"
        except ValueError:
            result_text.value = "Введите корректное числовое значение"
        page.update()

    # Обработчик события для кнопки "Вычесть"
    def subtract_click(e):
        try:
            value1 = float(value1_input.value)
            unit1 = unit1_input.value.strip().lower()
            value2 = float(value2_input.value)
            unit2 = unit2_input.value.strip().lower()
            # Проверка на правильность ввода единиц
            if unit1 not in unit_map or unit2 not in unit_map:
                result_text.value = "Неправильная единица измерения. Пожалуйста, используйте допустимые сокращения."
            else:
                result = add_or_subtract_units(value1, unit1, value2, unit2, "subtract")
                if isinstance(result, str):
                    result_text.value = f"Ошибка при вычитании: {result}"
                else:
                    result_text.value = f"{value1} {unit1} - {value2} {unit2} = {result:.6f} ({result.units})"
        except ValueError:
            result_text.value = "Введите корректное числовое значение"
        page.update()

    # Обработчик события для кнопки "Очистить"
    def clear_click(e):
        value1_input.value = ""
        unit1_input.value = ""
        value2_input.value = ""
        unit2_input.value = ""
        to_unit_input.value = ""
        result_text.value = ""
        page.update()

    # Заголовок страницы и добавление элементов интерфейса
    page.title = "Универсальный Калькулятор"
    page.add(
        ft.Text("Универсальный Калькулятор", style="headline4", color=ft.colors.LIME, font_family="Roboto Condensed"),
        ft.Text("Пожалуйста, используйте сокращенные обозначения единиц измерения (например, мм вместо миллиметр).", color=ft.colors.LIME, font_family="Roboto Condensed"),
        ft.Text("Доступные единицы измерения:", color=ft.colors.LIME, font_family="Roboto Condensed"),
        ft.Text("Расстояние: мм, см, м, км", color=ft.colors.LIME, font_family="Roboto Condensed"),
        ft.Text("Время: с, мин, час, сутки, год", color=ft.colors.LIME, font_family="Roboto Condensed"),
        ft.Text("Площадь: кв.мм, кв.см, кв.м, кв.км", color=ft.colors.LIME, font_family="Roboto Condensed"),
        ft.Text("Данные: бит, байт, кб, мб, гб, тб, пб", color=ft.colors.LIME, font_family="Roboto Condensed"),
        ft.Text("Масса: т, кг, мг, мкг, ц", color=ft.colors.LIME, font_family="Roboto Condensed"),
        ft.Text("Температура: C, F, K", color=ft.colors.LIME, font_family="Roboto Condensed"),
        ft.Text("Объем: мл, л, куб.м", color=ft.colors.LIME, font_family="Roboto Condensed"),
        value1_input,
        unit1_input,
        value2_input,
        unit2_input,
        to_unit_input,
        ft.Row([
            ft.ElevatedButton(text="Конвертировать", on_click=convert_click, bgcolor=ft.colors.LIME, color=ft.colors.BLACK, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))),
            ft.ElevatedButton(text="Сложить", on_click=add_click, bgcolor=ft.colors.LIME, color=ft.colors.BLACK, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))),
            ft.ElevatedButton(text="Вычесть", on_click=subtract_click, bgcolor=ft.colors.LIME, color=ft.colors.BLACK, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))),
            ft.ElevatedButton(text="Очистить", on_click=clear_click, bgcolor=ft.colors.LIME, color=ft.colors.BLACK, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))),
        ]),
        result_text
    )

    # Установка фонового цвета страницы
    page.bgcolor = ft.colors.BLACK
    page.update()

# Запуск сайта
ft.app(target=main, view=ft.AppView.WEB_BROWSER)