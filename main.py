from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


class BusinessApp(App):

    def build(self):
        layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=10
        )

        title = Label(
            text="Business Assistant",
            font_size=28
        )

        layout.add_widget(title)

        dashboard = Button(text="📊 Dashboard")
        sale = Button(text="💰 Sale")
        stock = Button(text="📦 Stock")
        expense = Button(text="💸 Expense")
        customer = Button(text="👤 Customer")

        layout.add_widget(dashboard)
        layout.add_widget(sale)
        layout.add_widget(stock)
        layout.add_widget(expense)
        layout.add_widget(customer)

        return layout


BusinessApp().run()
