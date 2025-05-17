import copy
import random
from .Stats import Stats, HeroStats
from .AttackStrategy import AttackStrategy
from abc import ABC, abstractmethod

#! In this file both Hero and Enemy are declared and defined 

# region Prototype 
class Prototype(ABC):
    @abstractmethod
    def clone(self, deep: bool = True):
        pass

    @abstractmethod
    def encounter(self, stdscr):
        pass

    @abstractmethod
    def perish(self, stdscr):
        pass

    @abstractmethod
    def takeDamage(self, hit: int, stdscr):
        pass

    @abstractmethod
    def attack(self, stdscr):
        pass

    def getName(self):
        pass

# region Enemy 
class Enemy(Prototype):
    def __init__(self, stats: Stats):
        self.stats = stats

    def clone(self, deep: bool = True):
        return copy.deepcopy(self) if deep else copy.copy(self)

    def encounter(self, stdscr):
        stdscr.clear()
        stdscr.addstr("An enemy has started a battle with your party.\n")
        stdscr.addstr(f"NAME: {self.stats.name} HP: {self.stats.hp}\n")
        stdscr.refresh()


    def perish(self, stdscr):
        self.stats.hp = 0
        stdscr.clear()
        stdscr.addstr(f"{self.stats.name} has been defeated. \n")
        stdscr.refresh()

    def takeDamage(self, hit: int, stdscr):
        self.stats.hp -= hit
        if self.stats.hp <= 0:
            self.perish(stdscr)

    def attack(self, stdscr):
        return 1 * self.stats.strength

    def getName(self) -> str:
        return self.stats.name

# Clase para crear enemigos a partir de un prototipo base
class EnemySpawner:
    def __init__(self, prototype: Enemy):
        self.prototype = prototype

    def spawn_enemy(self, deep: bool = True):
        return self.prototype.clone(deep=deep)

# region Hero
class Hero(Prototype):
    def __init__(self, stats: Stats, heroStats: HeroStats):
        self.stats = stats
        self.heroStats = heroStats

    def clone(self, deep: bool = True):
        pass

    def encounter(self, stdscr):
        pass

    def perish(self, stdscr):
        pass

    def takeDamage(self, hit: int, stdscr):
        pass

    def getName(self) -> str:
        return self.stats.name

    def getStatus(self, stdscr):
        stdscr.clear()
        stdscr.addstr(f"{self.getName()} \n--------------------\nHP: {self.stats.hp} MANA: {self.heroStats.mana}\n")
        stdscr.refresh()

    def setAttackStrategy(self, attackStrategy : AttackStrategy):
        self.heroStats.attackStrategy = attackStrategy

#* Este sería el heroe más basico que hay
class ConcreteHero(Hero):
    def __init__(self, stats: Stats, heroStats: HeroStats):
        self.stats = stats
        self.heroStats = heroStats

    def clone(self, deep: bool = True):
        return copy.deepcopy(self) if deep else copy.copy(self)

    def encounter(self, stdscr):
        stdscr.clear()
        stdscr.addstr(f"NAME: {self.stats.name} HP: {self.stats.hp} STR: {self.stats.strength} \n")
        stdscr.refresh()

    def perish(self, stdscr):
        self.stats.hp = 0
        stdscr.clear()
        stdscr.addstr(f"{self.stats.name} has perished. One party member less... \n")
        stdscr.refresh()
        stdscr.getch() # dramatic pause
        stdscr.addstr(f"{self.getName()}: I trusted you. X_X\n")
        stdscr.refresh()
        stdscr.clear()

    def takeDamage(self, hit: int, stdscr):
        stdscr.clear()
        stdscr.addstr(f"{self.getName()} gets hit for {hit} damage \n")
        stdscr.refresh()
        self.stats.hp -= hit
        if self.stats.hp <= 0:
            self.perish(stdscr)

    #* A Hero uses an attack strategy to eihter use a Heavy, Mid, or Light attack
    def attack(self, stdscr):
        if self.heroStats.mana < self.heroStats.attackStrategy.getManaCost():
            stdscr.clear()
            stdscr.addstr("Not enough mana to attack with chosen attack\n")
            stdscr.refresh()
            return 0
        return self.heroStats.attackStrategy.attack(self.stats.strength)
    
# region Decorators
class DecoratorHero(Hero):
    def __init__(self, hero: Hero):
        self.hero = hero

    def clone(self, deep: bool = True):
        pass

    def encounter(self, stdscr):
        pass

    def takeDamage(self, hit: int, stdscr):
        pass

    def attack(self, stdscr):
        pass

    def getStatus(self, stdscr):
        pass

# Clase para los Rogue
class Rogue(DecoratorHero):
    def clone(self, deep: bool = True):
        return copy.deepcopy(self) if deep else copy.copy(self)

    def encounter(self, stdscr):
        stdscr.clear()
        stdscr.addstr("CLASS: Swordsman \n")
        stdscr.refresh()
        self.hero.encounter(stdscr)

    def takeDamage(self, hit: int, stdscr):
        stdscr.clear()
        if random.randint(1, 5) == 5:
            stdscr.addstr(f"{self.hero.getName()} dodged the attack!\n")
            stdscr.refresh()
            return
        multiplier = 1.3
        newHit = round(multiplier * hit)
        stdscr.addstr(f"{newHit}\n")
        stdscr.refresh()
        self.hero.takeDamage(newHit, stdscr)

    def attack(self, stdscr):
        stdscr.clear()
        chance = random.randint(1, 5)
        if chance == 3:
            stdscr.addstr(f"{self.hero.getName()} hits a CRIT, X2 Damage\n")
            stdscr.refresh()
            return self.hero.attack(stdscr) * self.hero.stats.speed / 2
        elif chance == 5:
            stdscr.addstr(f"{self.hero.getName()} whiffs their attack dealing 0 damage!\n")
            stdscr.refresh()
            return 0
        return self.hero.attack(stdscr) * 1.3

    def getStatus(self, stdscr):
        self.hero.getStatus(stdscr)

# Clase para los Magos
class Mage(DecoratorHero):
    def clone(self, deep: bool = True):
        return copy.deepcopy(self) if deep else copy.copy(self)

    def encounter(self, stdscr):
        stdscr.clear()
        stdscr.addstr("CLASS: Mage \n")
        stdscr.refresh()
        self.hero.encounter(stdscr)

    def takeDamage(self, hit: int, stdscr):
        stdscr.clear()
        multiplier = 1.7
        newHit = round(multiplier * hit)
        if random.randint(1, 10) == 10:
            stdscr.addstr(f"{self.hero.getName()} tripped! Gets hit with a CRIT X2 damage\n")
            stdscr.refresh()
            self.hero.takeDamage(hit * 2, stdscr)
        stdscr.addstr(f"{self.hero.getName()} recovers {hit / 2} mana\n")
        self.hero.takeDamage(newHit, stdscr)
        self.hero.heroStats.mana += hit / 4
        stdscr.refresh()

    def attack(self, stdscr):
        stdscr.clear()
        chance = random.randint(1, 5)
        damage = self.hero.attack(stdscr)
        if chance == 5:
            stdscr.addstr(f"{self.hero.getName()} life steals the enemy, damage dealt also healed")
            self.hero.takeDamage(damage, stdscr)
            return damage

        elif chance == 3:
            stdscr.addstr(f"{self.hero.getName()} overstepped! Gets braced by their own attack!")
            self.hero.takeDamage(damage, stdscr)
            return damage
        
        return damage

class Tank(DecoratorHero):
    def clone(self, deep: bool = True):
        return copy.deepcopy(self) if deep else copy.copy(self)

    def encounter(self, stdscr):
        stdscr.clear()
        stdscr.addstr("CLASS: Tank \n")
        stdscr.refresh()
        self.hero.encounter(stdscr)

    def takeDamage(self, hit: int, stdscr):
        stdscr.clear()
        multiplier = 0.5
        newHit = round(multiplier * hit)
        if (random.randint(1, 100) == 100):
            stdscr.addstr(f"{self.hero.getName()} got a heart attack, they die")
            stdscr.refresh()
            self.hero.perish(stdscr)

        self.hero.takeDamage(newHit, stdscr)

    def attack(self, stdscr):
        return round(self.hero.attack(stdscr) * 0.7)
    
    def getStatus(self):
        self.hero.getStatus()