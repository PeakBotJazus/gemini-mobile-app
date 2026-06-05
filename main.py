import flet as ft
import requests

# Твой рабочий URL сервера на Render
RENDER_URL = "https://ai-telegram-bot-9vt3.onrender.com" 
USER_ID = "my_mobile_user_1" 

def main(page: ft.Page):
    page.title = "Gemini AI Multi-Bot"
    page.theme_mode = "dark"
    
    # Мобильные параметры экрана
    page.padding = 0
    
    chat_history = ft.ListView(
        expand=True, 
        spacing=10, 
        padding=15,
        auto_scroll=True
    )
    
    input_field = ft.TextField(
        hint_text="Напиши что-нибудь...", 
        expand=True,
        border_radius=20,
        content_padding=12,
        on_submit=lambda e: send_message(e)
    )
    
    # Безопасное объявление иконки через обычную строку "send"
    send_btn = ft.IconButton(
        icon="send",
        icon_color="#1E3A8A",
        on_click=lambda e: send_message(e)
    )

    def send_message(e):
        user_text = input_field.value.strip()
        if not user_text:
            return
            
        input_field.disabled = True
        send_btn.disabled = True
        page.update()
        
        # Сообщение пользователя
        chat_history.controls.append(
            ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text(value=user_text, color="white"),
                        bgcolor="#455A64",
                        padding=12,
                        border_radius=10
                    )
                ],
                alignment="end"
            )
        )
        input_field.value = ""
        page.update()
        
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
        except Exception as err:
            bot_reply = f"Не удалось связаться с сервером.\n{err}"
            
        # Ответ ИИ
        chat_history.controls.append(
            ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text(value=bot_reply, color="white"),
                        bgcolor="#1E3A8A",
                        padding=12,
                        border_radius=10,
                        max_width=280
                    )
                ],
                alignment="start"
            )
        )
        
        input_field.disabled = False
        send_btn.disabled = False
        page.update()

    def change_mode(mode_key, mode_name):
        try:
            requests.post(
                f"{RENDER_URL}/api/set_mode",
                json={"user_id": USER_ID, "mode_key": mode_key}
            )
            chat_history.controls.append(
                ft.Text(
                    value=f"🤖 Режим: {mode_name}", 
                    italic=True, 
                    color="#FFC107", 
                    text_align="center"
                )
            )
            page.update()
        except:
            pass

    # Роли
    btn_bro = ft.ElevatedButton(text="😎 Бро", on_click=lambda _: change_mode("friend", "ИИ-Бро"))
    btn_psy = ft.ElevatedButton(text="🧠 Психолог", on_click=lambda _: change_mode("psychologist", "Психолог"))
    btn_code = ft.ElevatedButton(text="💻 Схемотехник", on_click=lambda _: change_mode("coder", "Схемотехник"))
    btn_train = ft.ElevatedButton(text="💪 Тренер", on_click=lambda _: change_mode("trainer", "Фитнес-Ментор"))

    roles_row = ft.Container(
        content=ft.Row(
            scroll="always",
            controls=[btn_bro, btn_psy, btn_code, btn_train]
        ),
        padding=10
    )

    bottom_row = ft.Container(
        content=ft.Row(
            controls=[input_field, send_btn]
        ),
        padding=10
    )

    page.add(
        ft.AppBar(title=ft.Text("Gemini Assistant"), bgcolor="#263238", center_title=True),
        roles_row,
        ft.Divider(height=1),
        chat_history,
        bottom_row
    )

if __name__ == "__main__":
    ft.app(target=main)