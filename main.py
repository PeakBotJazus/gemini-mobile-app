import flet as ft
import requests

def main(page: ft.Page):
    page.title = "Gemini AI Multi-Bot"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    
    # История чата с автоматическим скроллом
    chat_history = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    
    # Поле ввода сообщения
    query_input = ft.TextField(
        hint_text="Напишите сообщение...",
        expand=True,
        shift_enter=True,
    )
    
    # Функция обработки отправки
    def send_message(e):
        if not query_input.value.strip():
            return
            
        user_text = query_input.value.strip()
        
        # Добавляем сообщение пользователя в чат
        chat_history.controls.append(
            ft.Container(
                content=ft.Text(f"Вы: {user_text}", color=ft.colors.WHITE),
                padding=10,
                bgcolor=ft.colors.BLUE_GREY_800,
                border_radius=10,
            )
        )
        query_input.value = ""
        page.update()
        
        # Заглушка ответа (сюда потом встанет твой реальный запрос к Gemini API)
        chat_history.controls.append(
            ft.Container(
                content=ft.Text("Gemini: Привет! Интерфейс работает идеально, ошибок нет.", color=ft.colors.WHITE),
                padding=10,
                bgcolor=ft.colors.GREEN_800,
                border_radius=10,
            )
        )
        page.update()

    # Кнопка отправки (исправлено: берем иконку напрямую из ft.icons)
    send_button = ft.IconButton(
        icon=ft.icons.SEND,
        icon_color=ft.colors.BLUE,
        on_click=send_message
    )
    
    # Нижняя панель ввода (исправлено: padding перенесен в Container)
    input_panel = ft.Container(
        content=ft.Row(
            controls=[query_input, send_button],
        ),
        padding=10,
    )
    
    # Собираем главный экран приложения
    page.add(
        ft.Column(
            controls=[
                ft.Text("Gemini AI Multi-Bot", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                chat_history,
                input_panel
            ],
            expand=True
        )
    )

# Запуск приложения
ft.app(target=main)
