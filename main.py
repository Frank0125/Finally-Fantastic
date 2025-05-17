import curses

from game import game

#! Classes implemented Command
#* Command
from classes.Command.Command import Command as ClassCommand, Controller

class GoUp(ClassCommand):
    def execute():
        global selected
        selected = (selected - 1) % len(options)

class GoDown(ClassCommand):

    def execute():
        global selected
        selected = (selected + 1) % len(options)

class Confirm(ClassCommand):
    def execute():
        print("Thank You")


# region Main
#! MAIN

# region Controllers
PlayerController = Controller()

PlayerController.asignCommand("up", GoUp)
PlayerController.asignCommand("down", GoDown)
PlayerController.asignCommand("enter", Confirm)

selected = 0
options = ["Start Game", "Exit"]

# Setup key mappings# Setup key mappings using curses
def getInputScheme(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "=== Controller Scheme Menu ===\n")
        stdscr.addstr(1, 0, "Press 1 to use ARROW keys\n")
        stdscr.addstr(2, 0, "Press 2 to use W/S keys\n")
        stdscr.addstr(3, 0, "Enter key is confirm\n")
        stdscr.refresh()

        key = stdscr.getch()

        if key == ord("1"):
            return ["ARROW"]
        elif key == ord("2"):
            return ["w", "s"]
        else:
            stdscr.addstr(5, 0, "Invalid option, press 1 or 2")
            stdscr.refresh()
            curses.napms(1000)
        

# Main menu loop with curses
def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(False)
    stdscr.keypad(True)

    key_scheme = getInputScheme(stdscr)
    global selected, options
    selected = 0
    options = ["Start Game", "Exit"]

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "=== MAIN MENU ===")
        for i, option in enumerate(options):
            prefix = "> " if i == selected else "  "
            stdscr.addstr(i + 1, 0, f"{prefix}{option}")
        stdscr.refresh()

        key = stdscr.getch()

        if key_scheme == ["ARROW"]:
            if key == curses.KEY_UP:
                PlayerController.pressButton("up")
            elif key == curses.KEY_DOWN:
                PlayerController.pressButton("down")
        else:
            if key in [ord("w"), ord("W")]:
                PlayerController.pressButton("up")
            elif key in [ord("s"), ord("S")]:
                PlayerController.pressButton("down")

        if key == ord("\n"):
            # PlayerController.pressButton("enter")
            break

    if selected==1:
        stdscr.addstr(0, 0, f"Exiting...")

    stdscr.addstr(0, 0, f"Exiting...")

    if selected==0:
        stdscr.addstr(0, 0, f"Starting Game...")
        game(stdscr, key_scheme, PlayerController)

# Start 
curses.wrapper(main)