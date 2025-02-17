import flet as ft

def main(page: ft.Page):

    # Функция для обработки нажатия кнопки
    def redirect_to_dogs(button):
        page.go("/dogs")

    # Создание кнопки с текстом "Перейти к собакам" и привязкой функции
    button = ft.Button()
    button.text = "Перейти к собакам"
    button.on_click = redirect_to_dogs

    # Добавление кнопки на страницу
    page.add(button)

ft.app(target=main)
