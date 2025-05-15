import flet as ft
import requests
import threading
import time

def main(page: ft.Page):
    # Page setup with improved styling
    page.title = "Smart Home Controller"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 30
    page.bgcolor = "#f5f5f5"
    page.fonts = {
        "Roboto": "https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap"
    }
    page.theme = ft.Theme(font_family="Roboto")

    SERVER_URL = "http://192.168.151.144:5000"

    # Create controls with improved styling
    brightness_slider = ft.Slider(
        min=0, 
        max=255, 
        value=0, 
        label="{value}%",
        active_color="#4caf50",
        inactive_color="#e0e0e0",
        thumb_color="#4caf50"
    )
    
    led_switch = ft.Switch(
        label="LED", 
        value=False,
        thumb_color={"": "#ffffff"},
        track_color={"false": "#cccccc", "true": "#4caf50"},
        label_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD)
    )
    
    fan_switch = ft.Switch(
        label="Fan", 
        value=False,
        thumb_color={"": "#ffffff"},
        track_color={"false": "#cccccc", "true": "#2196f3"},
        label_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD)
    )
    
    fan_speed = ft.Slider(
        min=0, 
        max=255, 
        value=0, 
        label="Speed: {value}",
        active_color="#2196f3",
        inactive_color="#e0e0e0",
        thumb_color="#2196f3"
    )

    def send_controls(e):
        data = {
            "led_enabled": led_switch.value,
            "brightness": int(brightness_slider.value),
            "fan_enabled": fan_switch.value,
            "fan_speed": int(fan_speed.value)
        }
        try:
            requests.post(f"{SERVER_URL}/flet/update", json=data, timeout=2)
        except Exception as e:
            print("Control update failed:", e)

    # Improved layout with better spacing and styling
    controls = ft.Column([
        ft.Text("💡 LED Control", size=20, weight=ft.FontWeight.BOLD, color="#4caf50"),
        ft.Container(led_switch, padding=ft.padding.only(bottom=10)),
        ft.Text("🔆 Brightness Control", size=16),
        brightness_slider,
        ft.Divider(height=20, color="#e0e0e0"),
        ft.Text("🌀 Fan Control", size=20, weight=ft.FontWeight.BOLD, color="#2196f3"),
        ft.Container(fan_switch, padding=ft.padding.only(bottom=10)),
        ft.Text("🎚️ Fan Speed Control", size=16),
        fan_speed,
    ], spacing=10)

    page.add(
        ft.Row([
            ft.Card(
                content=ft.Container(controls, padding=20),
                elevation=8,
                color=ft.Colors.WHITE,
                width=400
            )
        ], spacing=30, alignment=ft.MainAxisAlignment.CENTER)
    )

    # Set up event handlers
    for control in [led_switch, brightness_slider, fan_switch, fan_speed]:
        control.on_change = send_controls

ft.app(target=main)
