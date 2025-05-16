import copy
import random
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

    def getName(self):
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

    def getName(self):
        return self.stats.name
    
class EnemySpawner:
    def __init__(self, prototype: Enemy):
        self.prototype = prototype

    def spawn_enemy(self, deep: bool = True):
        return self.prototype.clone(deep=deep)
    
# endregion

# region Hero
class Hero(Prototype):
    # * El heroe usa Decorator por lo que no tiene constructor en su base
    def __init__(self, stats : Stats, heroStats : HeroStats):
        self.stats = stats
        self.heroStats = heroStats

    def clone(self, deep: bool = True):
        pass

    def encounter(self):
        pass

    def perish(self):
       pass

    def takeDamage(self, hit : int):    
        pass

    def getName(self):
        return self.stats.name
    
    def getStatus(self):
        print(f"{self.getName} \n --------------------\nHP: {self.stats.hp} MANA: {self.heroStats.mana}")
    
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
        print(f"{self.getName()}: I trusted you. X_X")

    def takeDamage(self, hit : int):

        print(f"{self.getName()} gets hit for {hit} damage \n")    
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

# region Decorators

class DecoratorHero(Hero):
    def __init__(self, hero : Hero):
        self.hero = hero
    
    def clone(self, deep: bool = True):
        pass

    def encounter(self):
        pass

    def takeDamage(self, hit : int):    
        pass

    def attack(self):
        pass

    def getStatus(self):
        pass

class Rogue(DecoratorHero):
    def clone(self, deep: bool = True):
        return copy.deepcopy(self) if deep else copy.copy(self)

    def encounter(self):
        print("CLASS: Swordsman \n")
        self.hero.encounter()


    def takeDamage(self, hit : int):
        if (random.randint(1,5) == 5):
            print(f"{self.hero.getName()} dodged the attack!")

        multiplier = 1.3
        newHit = round(multiplier * hit)
        print(newHit)
        self.hero.takeDamage(newHit) 

    def attack(self):
        chance = random.randint(1,5)
        if chance == 3:
            print(f"{self.hero.getName()} hits a CRIT, X2 Damage")
            return self.attack() * 2
        
        elif chance == 5:
            print(f"{self.hero.getName()} whiffs thier attack dealing 0 damage!")
            return 0
        
        return self.hero.attack()
    
    def getStatus(self):
        self.hero.getStatus()

class Mage(DecoratorHero):
    def clone(self, deep: bool = True):
        return copy.deepcopy(self) if deep else copy.copy(self)

    def encounter(self):
        print("CLASS: Mage \n")
        self.hero.encounter()

    def takeDamage(self, hit : int):
        multiplier = 1.7
        newHit = round(multiplier * hit)
        if (random.randint(1, 10) == 10):
            print(f"{self.hero.getName()} tripped! Gets hit with a CRIT X2 damage")
            self.hero.takeDamage()

        self.hero.takeDamage(newHit) 
        self.heroStats.mana =+ hit/2

        print(f"{self.getName} recovers {hit/2} mana")

    def attack(self):
        chance = random.randint(1, 5)
        damage = self.attack()
        if chance == 5:
            print(f"{self.hero.getName()} life steals the enemy, damage dealt also healed")
            self.hero.stats =+ damage
            return damage

        elif chance == 3:
            print(f"{self.hero.getName()} overstepped! Gets braced by their own attack!")
            self.hero.takeDamage(damage)
            return damage
        
        return self.hero.attack()
    
    def getStatus(self):
        self.hero.getStatus()

class Tank(DecoratorHero):
    def clone(self, deep: bool = True):
        return copy.deepcopy(self) if deep else copy.copy(self)

    def encounter(self):
        print("CLASS: Tank \n")
        self.hero.encounter()

    def takeDamage(self, hit : int):
        multiplier = 0.5
        newHit = round(multiplier * hit)
        if (random.randint(1, 100) == 100):
            print(f"{self.hero.getName()} got a heart attack, they die")
            self.hero.perish()

        self.hero.takeDamage(newHit)

    def attack(self):
        return round(self.hero.attack() * 0.7)
    
    def getStatus(self):
        self.hero.getStatus()
# endregion
