from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.animation import Animation
from kivy.uix.popup import Popup
from kivy.metrics import dp
from kivy.core.window import Window

# Установим белый фон для всего окна
Window.clearcolor = (1, 1, 1, 1)


class GradeApp(App):
    def build(self):
        # Основной контейнер
        self.layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))

        # Заголовок
        self.label_instruction = Label(
            text="Введите оценку (2-5):",
            font_size=24,
            color=(0, 0, 0, 1)  # Черный текст
        )
        self.layout.add_widget(self.label_instruction)

        # Поле ввода
        self.grade_input = TextInput(
            hint_text='Оценка',
            font_size=20,
            multiline=False,
            size_hint=(1, 0.2),
            halign="center",
            background_color=(1, 1, 1, 1),  # Белый фон для поля
            foreground_color=(0, 0, 0, 1),  # Черный текст
            padding=[dp(10), dp(10)],
            cursor_color=(0, 0, 1, 1),  # Синий курсор
        )
        self.grade_input.bind(focus=self.on_focus)
        self.layout.add_widget(self.grade_input)

        # Кнопка для добавления оценки
        self.add_button = Button(
            text="Добавить оценку",
            size_hint=(1, 0.3),
            background_normal='',
            background_color=(0.2, 0.6, 1, 1),  # Синий фон кнопки
            color=(1, 1, 1, 1),  # Белый текст
        )
        self.add_button.bind(on_press=self.add_grade)
        self.layout.add_widget(self.add_button)

        # Кнопка для завершения недели
        self.end_button = Button(
            text="Завершить неделю",
            size_hint=(1, 0.3),
            background_normal='',
            background_color=(0, 0.4, 0.8, 1),  # Темно-синий фон кнопки
            color=(1, 1, 1, 1),  # Белый текст
        )
        self.end_button.bind(on_press=self.end_week)
        self.layout.add_widget(self.end_button)

        return self.layout

    # Голубая обводка при фокусе на поле ввода
    def on_focus(self, instance, value):
        if value:
            instance.background_color = (0.9, 0.9, 1, 1)  # Голубая обводка при фокусе
        else:
            instance.background_color = (1, 1, 1, 1)  # Белый фон при отсутствии фокуса

    # Функция для добавления оценки
    def add_grade(self, instance):
        try:
            grade = int(self.grade_input.text)
            if grade in [2, 3, 4, 5]:
                school.append(grade)
                self.grade_input.text = ''  # Очистка поля
                self.animate_button(instance, "Оценка добавлена!")
            else:
                self.show_popup("Ошибка", "Оценка должна быть 2, 3, 4 или 5")
        except ValueError:
            self.show_popup("Ошибка", "Введите число")

    # Анимация кнопки
    def animate_button(self, instance, message):
        anim = Animation(background_color=(0, 1, 0, 1), duration=0.2) + Animation(background_color=(0.2, 0.6, 1, 1),
                                                                                  duration=0.2)
        anim.start(instance)
        self.label_instruction.text = message

    # Завершение недели и подсчет результатов
    def end_week(self, instance):
        fives = school.count(5)
        fours = school.count(4)
        threes = school.count(3)
        twos = school.count(2)

        good = fives * 200 + fours * 100
        not_good = threes * 0 + twos * 0
        result = good - not_good
        tax = result / 2

        self.show_popup("Результаты", f'Итог: {result}\nНалог: {tax}\nТы получишь: {result / 2}')
        school.clear()

    # Всплывающее окно для отображения сообщений
    def show_popup(self, title, message):
        popup_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        popup_label = Label(text=message, font_size=18, color=(0, 0, 0, 1))
        popup_button = Button(text="Закрыть", size_hint=(1, 0.2), background_color=(0, 0.6, 0.8, 1), color=(1, 1, 1, 1))
        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(popup_button)

        popup = Popup(title=title, content=popup_layout, size_hint=(0.8, 0.4))
        popup_button.bind(on_press=popup.dismiss)
        popup.open()


# Запуск приложения
if __name__ == '__main__':
    school = []  # Инициализация списка оценок
    GradeApp().run()