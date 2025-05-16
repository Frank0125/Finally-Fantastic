import copy
from .Stats import Stats, HeroStats
from abc import ABC, abstractmethod

#! In this file both Hero and Enemy are declared and defined 

# region Prototype 
class Prototype(ABC):
    @abstractmethod
    def clone(self, deep: bool = True):
        pass

    @abstractmethod
    def encounter(self):
        pass

    @abstractmethod
    def perish(self):
        pass

    @abstractmethod
    def takeDamage(self, hit : int):
        pass

    @abstractmethod
    def attack(self):
        pass
         
# region Enemy 
class Enemy(Prototype):
    def __init__(self, stats : Stats):
        self.stats = stats

    def clone(self, deep: bool = True):
        return copy.deepcopy(self) if deep else copy.copy(self)

    def encounter(self):
        print(f"An enemy has a started a battle with your party.\n NAME: {self.stats.name} HP: {self.stats.hp} \n")

    def perish(self):
        self.stats.hp = 0
        print(f"{self.stats.name} has been defeated. \n")

    def takeDamage(self, hit : int):    
        self.stats.hp =- hit

        if self.stats.hp <= 0:
            self.perish()

    #* An enemy deals its raw strength atribute as damage
    def attack(self):
        return 1 * self.stats.strength

class EnemySpawner:
    def __init__(self, prototype: Enemy):
        self.prototype = prototype

    def spawn_enemy(self, deep: bool = True):
        return self.prototype.clone(deep=deep)
    
# endregion

# region Hero
class Hero(Prototype):
    # * El heroe usa Decorator por lo que no tiene constructor en su base

    def clone(self, deep: bool = True):
        pass

    def encounter(self):
        pass

    def perish(self):
       pass

    def takeDamage(self, hit : int):    
        pass
    
    #* Este sería el heroe más basico que hay
class ConcreteHero(Hero):
    def __init__(self, stats : Stats, heroStats : HeroStats):
        self.stats = stats
        self.heroStats = heroStats

    def clone(self, deep: bool = True):
        return copy.deepcopy(self) if deep else copy.copy(self)

    def encounter(self):
        print(f"NAME: {self.stats.name} HP: {self.stats.hp} STR: {self.stats.strength} \n")

    def perish(self):
        self.stats.hp = 0
        print(f"{self.stats.name} has perished. One party member less... \n")
        input() #! dramatic pause
        print(f"{self.stats.name}: I trusted you. X_X")

    def takeDamage(self, hit : int):    
        self.stats.hp =- hit

        if self.stats.hp <= 0:
            self.perish()

    #* A Hero uses an attack strategy to eihter use a Heavy, Mid, or Light attack
    def attack(self):
        if (self.heroStats.mana < self.heroStats.attackStrategy.getManaCost()):
            print("Not enough mana to attack with chosen attack")
            return 0
        
        return self.heroStats.attackStrategy()
    
# endregion
