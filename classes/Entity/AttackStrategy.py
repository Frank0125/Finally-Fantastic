from abc import ABC, abstractmethod

#! Strategy interface
class AttackStrategy(ABC):
    def __init__(self, manaCost : int):
        self.manaCost = manaCost

    @abstractmethod
    def attack(self, baseStrength : int) -> int:
        pass
    
    def getManaCost(self):
        return self.manaCost
        
#* Concrete strategies (H, M, L)
class HeavyAttack(AttackStrategy):
    def __init__(self):
        self.manaCost = 7

    def attack(self, baseStrength : int):
        return round(baseStrength * 2.5)
    
class MidAttack(AttackStrategy):
    def __init__(self):
        self.manaCost = 3

    def attack(self, baseStrength : int):
        return round(baseStrength * 1.5)

class LightAttack(AttackStrategy):
    def __init__(self):
        self.manaCost = 1

    def attack(self, baseStrength : int):
        return round(baseStrength * 0.7)

__all__ = ['AttackStrategy', 'HeavyAttack', 'MidAttack', 'LightAttack']