from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class Controller:
    def __init__(self):
        self.buttons = {}

    def asignCommand(self, buttonName, command):
        self.buttons[buttonName] = command

    def pressButton(self, buttonName):
        command = self.buttons.get(buttonName)
        if command:
            command.execute()
        else:
            print(f"No command when pressing {buttonName}")

__all__ = ['Command', 'Controller']