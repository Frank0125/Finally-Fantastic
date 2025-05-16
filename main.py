import keyboard
import os
import time

options = ["Start Game", "Load Game", "Options", "Exit"]
selected = 0

def print_menu():
    os.system('cls' if os.name == 'nt' else 'clear')  # Limpiar consola
    print("=== MAIN MENU ===\n")
    for i, option in enumerate(options):
        if i == selected:
            print(f"> {option}")
        else:
            print(f"  {option}")

print_menu()

while True:
    if keyboard.is_pressed("up"):
        selected = (selected - 1) % len(options)
        print_menu()
        time.sleep(0.15)  # prevent fast skipping

    elif keyboard.is_pressed("down"):
        selected = (selected + 1) % len(options)
        print_menu()
        time.sleep(0.15)

    elif keyboard.is_pressed("enter"):
        print(f"\nYou selected: {options[selected]}")
        break
