import flet as ft


def main(page):
    # Создаем references для текстовых полей и колонок
    first_name = ft.Ref[ft.TextField]()
    last_name = ft.Ref[ft.TextField]()
    password = ft.Ref[ft.TextField]()
    confirmpassword = ft.Ref[ft.TextField]()
    greetings = ft.Ref[ft.Column]()

    selected_products = []  # Список для выбранных продуктов
    total_price = 0  # Общая стоимость выбранных продуктов

    products = [
        {"name": "Pizza", "price": 8.99},
        {"name": "Burger", "price": 5.49},
        {"name": "Sushi", "price": 12.99}
    ]

    def show_product_selection(e):
        # Обновляем вид на страницу выбора продукта
        product_buttons = [
            ft.ElevatedButton(f"{product['name']} - ${product['price']}", on_click=lambda e, p=product: add_product(p))
            for product in products
        ]
        product_buttons.append(ft.ElevatedButton("Go back", on_click=lambda _: page.go("/")))
        page.views.append(
            ft.View(
                "/products",
                [
                    ft.AppBar(title=ft.Text("Product Selection")),
                    *product_buttons,
                    ft.ElevatedButton("Checkout", on_click=show_receipt)
                ]
            )
        )
        page.update()

    def add_product(product):
        nonlocal total_price
        selected_products.append(product)
        total_price += product['price']
        page.snack_bar = ft.SnackBar(ft.Text(f"Added {product['name']} to cart. Total: ${total_price:.2f}"))
        page.snack_bar.open = True
        page.update()

    def remove_product(index):
        nonlocal total_price
        product = selected_products.pop(index)
        total_price -= product['price']
        show_receipt(None)

    def show_receipt(e):
        receipt_controls = [
            ft.Row([
                ft.Text(f"{product['name']} - ${product['price']}"),
                ft.IconButton(ft.icons.DELETE, on_click=lambda e, i=i: remove_product(i))
            ])
            for i, product in enumerate(selected_products)
        ]
        receipt_controls.append(ft.Text(f"Total: ${total_price:.2f}"))
        receipt_controls.append(ft.ElevatedButton("Go back", on_click=lambda _: page.go("/products")))
        page.views.append(
            ft.View(
                "/receipt",
                [
                    ft.AppBar(title=ft.Text("Receipt")),
                    *receipt_controls
                ]
            )
        )
        page.update()

    def btn_click(e):
        if password.current.value != confirmpassword.current.value:
            greetings.current.controls.append(
                ft.Text("Passwords do not match!", color=ft.colors.RED)
            )
            page.update()
            return

        # Добавляем сообщение о регистрации
        greetings.current.controls.append(
            ft.Text(
                f"User {first_name.current.value} {last_name.current.value} registered! Your password is {password.current.value}")
        )
        first_name.current.value = ""
        last_name.current.value = ""
        password.current.value = ""
        confirmpassword.current.value = ""
        page.update()
        first_name.current.focus()

    # Главная страница регистрации
    page.add(
        ft.TextField(ref=first_name, label="First name", autofocus=True),
        ft.TextField(ref=last_name, label="Last name"),
        ft.TextField(ref=password, label="Enter password", password=True, can_reveal_password=True),
        ft.TextField(ref=confirmpassword, label="Confirm the password", password=True, can_reveal_password=True),
        ft.ElevatedButton("Register me!", on_click=btn_click),
        ft.ElevatedButton("Go to product selection", on_click=show_product_selection),
        ft.Column(ref=greetings),
    )

    # Обрабатываем переходы между страницами
    def route_change(route):
        page.views.clear()
        if page.route == "/":
            page.views.append(
                ft.View(
                    "/",
                    [
                        ft.TextField(ref=first_name, label="First name", autofocus=True),
                        ft.TextField(ref=last_name, label="Last name"),
                        ft.TextField(ref=password, label="Enter password", password=True, can_reveal_password=True),
                        ft.TextField(ref=confirmpassword, label="Confirm the password", password=True,
                                     can_reveal_password=True),
                        ft.ElevatedButton("Register me!", on_click=btn_click),
                        ft.ElevatedButton("Go to product selection", on_click=show_product_selection),
                        ft.Column(ref=greetings),
                    ]
                )
            )
        elif page.route == "/products":
            product_buttons = [
                ft.ElevatedButton(f"{product['name']} - ${product['price']}",
                                  on_click=lambda e, p=product: add_product(p))
                for product in products
            ]
            product_buttons.append(ft.ElevatedButton("Go back", on_click=lambda _: page.go("/")))
            page.views.append(
                ft.View(
                    "/products",
                    [
                        ft.AppBar(title=ft.Text("Product Selection")),
                        *product_buttons,
                        ft.ElevatedButton("Checkout", on_click=show_receipt)
                    ]
                )
            )
        elif page.route == "/receipt":
            receipt_controls = [
                ft.Row([
                    ft.Text(f"{product['name']} - ${product['price']}"),
                    ft.IconButton(ft.icons.DELETE, on_click=lambda e, i=i: remove_product(i))
                ])
                for i, product in enumerate(selected_products)
            ]
            receipt_controls.append(ft.Text(f"Total: ${total_price:.2f}"))
            receipt_controls.append(ft.ElevatedButton("Go back", on_click=lambda _: page.go("/products")))
            page.views.append(
                ft.View(
                    "/receipt",
                    [
                        ft.AppBar(title=ft.Text("Receipt")),
                        *receipt_controls
                    ]
                )
            )
        page.update()

    page.on_route_change = route_change


ft.app(target=main, view=ft.AppView.WEB_BROWSER)
