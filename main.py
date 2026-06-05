import flet as ft
import requests

# Твой рабочий URL сервера на Render
RENDER_URL = "https://ai-telegram-bot-9vt3.onrender.com" 
USER_ID = "my_mobile_user_1" 

def main(page: ft.Page):
    try:
        page.title = "Gemini AI Multi-Bot"
        page.theme_mode = "dark"
        page.padding = 10  # Уменьшили отступы, чтобы на вертикальном экране было больше места
        
        # История чата с автоскроллом
        chat_history = ft.Column(scroll="auto", expand=True)
        
        # Поле ввода сообщения
        query_input = ft.TextField(
            hint_text="Напишите сообщение...",
            expand=True,
            shift_enter=True,
        )
        
        # Индикатор загрузки (появится, пока нейронка думает)
        loader = ft.ProgressBar(visible=False, color="blue")
        
        def send_message(e):
            user_text = query_input.value.strip()
            if not user_text:
                return
                
            # Блокируем ввод и показываем загрузку
            query_input.disabled = True
            send_button.disabled = True
            loader.visible = True
            
            # Отображаем сообщение пользователя
            chat_history.controls.append(
                ft.Container(
                    content=ft.Text(f"Вы: {user_text}", color="white"),
                    padding=10,
                    bgcolor="#455A64",
                    border_radius=10,
                )
            )
            query_input.value = ""
            page.update()
            
            # Отправка запроса к Gemini
            try:
                response = requests.post(
                    f"{RENDER_URL}/api/chat",
                    json={"user_id": USER_ID, "message": user_text},
                    timeout=30
                )
                if response.status_code == 200:
                    bot_reply = response.json().get("reply", "Ошибка: пустой ответ.")
                else:
                    bot_reply = f"Ошибка сервера: {response.status_code}"
            except Exception as req_err:
                bot_reply = f"Ошибка сети: {req_err}"
                
            # Отображаем ответ нейронки
            chat_history.controls.append(
                ft.Container(
                    content=ft.Text(f"Gemini: {bot_reply}", color="white"),
                    padding=10,
                    bgcolor="#1E3A8A",
                    border_radius=10,
                )
            )
            
            # Возвращаем интерфейс в рабочее состояние
            query_input.disabled = False
            send_button.disabled = False
            loader.visible = False
            page.update()

        # Кнопка отправки (Заменили IconButton на 100% рабочий ElevatedButton с текстом)
        send_button = ft.ElevatedButton(
            text="ОТПРАВИТЬ",
            bgcolor="#1E3A8A",
            color="white",
            on_click=send_message
        )
        
        # Панель ввода (внутри строки элементы красиво сожмутся по ширине экрана)
        input_panel = ft.Container(
            content=ft.Row(
                controls=[query_input, send_button],
                alignment="center"
            ),
            padding=5,
        )
        
        # Главный контейнер
        page.add(
            ft.Column(
                controls=[
                    ft.Text("Gemini AI Multi-Bot", size=20, weight="bold"),
                    ft.Divider(),
                    loader,
                    chat_history,
                    input_panel
                ],
                expand=True
            )
        )
        
    except Exception as crash_error:
        page.controls.clear()
        page.add(
            ft.Container(
                content=ft.Text(f"Вылет при запуске:\n\n{crash_error}", color="red", size=16),
                padding=20
            )
        )
        page.update()

ft.app(target=main)
