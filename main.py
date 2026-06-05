import flet as ft
import requests

# Твой рабочий URL сервера на Render
RENDER_URL = "https://ai-telegram-bot-9vt3.onrender.com" 
USER_ID = "my_mobile_user_1" 

def main(page: ft.Page):
    # Капкан для ошибок: если код споткнется, мы увидим причину на экране телефона
    try:
        page.title = "Gemini AI Multi-Bot"
        page.theme_mode = "dark"  # Строка вместо ft.ThemeMode
        page.padding = 15
        
        # История чата с автоскроллом (строка вместо ft.ScrollMode)
        chat_history = ft.Column(scroll="auto", expand=True)
        
        query_input = ft.TextField(
            hint_text="Напишите сообщение...",
            expand=True,
            shift_enter=True,
        )
        
        def send_message(e):
            user_text = query_input.value.strip()
            if not user_text:
                return
                
            # Выводим сообщение пользователя
            chat_history.controls.append(
                ft.Container(
                    content=ft.Text(f"Вы: {user_text}", color="white"),
                    padding=10,
                    bgcolor="#455A64",  # HEX-код вместо ft.colors
                    border_radius=10,
                )
            )
            query_input.value = ""
            page.update()
            
            # Отправка запроса на твой Render сервер
            try:
                response = requests.post(
                    f"{RENDER_URL}/api/chat",
                    json={"user_id": USER_ID, "message": user_text},
                    timeout=30
                )
                if response.status_code == 200:
                    bot_reply = response.json().get("reply", "Ошибка получения ответа.")
                else:
                    bot_reply = f"Ошибка сервера: {response.status_code}"
            except Exception as req_err:
                bot_reply = f"Ошибка сети/сервера: {req_err}"
                
            # Выводим ответ от Gemini
            chat_history.controls.append(
                ft.Container(
                    content=ft.Text(f"Gemini: {bot_reply}", color="white"),
                    padding=10,
                    bgcolor="#1E3A8A",  # HEX-код вместо ft.colors
                    border_radius=10,
                )
            )
            page.update()

        # Кнопка отправки (иконка и цвет заданы чистыми строками)
        send_button = ft.IconButton(
            icon="send",
            icon_color="blue",
            on_click=send_message
        )
        
        input_panel = ft.Container(
            content=ft.Row(controls=[query_input, send_button]),
            padding=5,
        )
        
        # Главный контейнер экрана
        page.add(
            ft.Column(
                controls=[
                    ft.Text("Gemini AI Multi-Bot", size=22, weight="bold"), # Строка вместо ft.FontWeight
                    ft.Divider(),
                    chat_history,
                    input_panel
                ],
                expand=True
            )
        )
        
    except Exception as crash_error:
        # Если интерфейс упадет при инициализации, этот блок выведет ошибку на экран
        page.controls.clear()
        page.add(
            ft.Container(
                content=ft.Text(f"Критический вылет приложения:\n\n{crash_error}", color="red", size=16),
                padding=20
            )
        )
        page.update()

# Запуск программы
ft.app(target=main)
