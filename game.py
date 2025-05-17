import curses
import random
import time 
from typing import List, Union

seed = int(time.time()) #TODO PRINT SEED
random.seed(seed)

#* Entity
from classes.Entity.AttackStrategy import HeavyAttack, MidAttack, LightAttack
from classes.Entity.Hero import Prototype, Enemy, EnemySpawner, Hero, ConcreteHero, DecoratorHero, Rogue, Mage, Tank
from classes.Entity.Stats import Stats, HeroStats

# region Stats
#! Phase 1 enemy stats
atributesEnemies1 = Stats("Goblin", 40, 4, 7)
#! Phase 2 enemy stats
atributesEnemies2 = Stats("The Twins", 70, 9, 12)

#! Boss (random stats)
atributesBoss = Stats("John Evil", 200, 12, 40)
atributesBossRandom = Stats("Rosephith",random.randint(1, 1000), random.randint(0, 100), random.randint(0, 100))

#! Random player stats 0_0
regularStats = Stats("", 160 + random.randint(0, 100), 30 + random.randint(-50, 50), 10 + random.randint(0, 40))
heroStats = HeroStats(100, LightAttack())

# region Enemy Spawner
goblinPrototype = Enemy(atributesEnemies1)
orcPrototype = Enemy(atributesEnemies2)

goblinSpawner = EnemySpawner(goblinPrototype)
orcSpawner = EnemySpawner(orcPrototype)

#* copies
shallowGoblins = [goblinSpawner.spawn_enemy(deep=False) for _ in range(3)]

deepOrcs = [orcSpawner.spawn_enemy(deep=True) for _ in range(2)]

boss = Enemy(atributesBoss)
johnEvil = Enemy(atributesBossRandom)

bosses = [boss, johnEvil]

#region Heroes

templateHero = ConcreteHero(stats=regularStats, heroStats=heroStats)

rogue = Rogue(templateHero)
mage = Mage(templateHero)
tank = Mage(templateHero)

#! not finished, was supoosed to pick names
rogue.hero.stats.name = "Kei"
mage.hero.stats.name = "Nitro"
tank.hero.stats.name = "America"

# region Main
selected = 0
attackOptions = ["Last Option", "Heavy", "Mid", "Light"]
party : List[DecoratorHero] = [rogue, mage, tank]


def startEncountersHeroes(stdscr, party : DecoratorHero):
    for i in party:
        i.hero.encounter(stdscr)

def startEncountersEnemies(stdscr, enemies : List[Enemy]):
    for i in enemies:
        i.encounter(stdscr)

def checkPartyStatus(stdscr, party : List[DecoratorHero]):
    for i in party:
        i.hero.getStatus(stdscr)

def removePerished(enemies : List[Enemy]):
    for i in enemies:
        if i.stats.hp == 0:
            enemies.remove(i)
            
    return enemies

def createEncounterList(fullList):
    filteredList = [
        i for i in fullList 
        if not (isinstance(i, Enemy) and i.stats.hp == 0) 
        and not (isinstance(i, DecoratorHero) and i.hero.stats.hp == 0)
    ]

    print(filteredList)

    # not enough time to make sense of this or make it pretty
    sortedList = sorted(filteredList, key=lambda entity: entity.stats.speed if hasattr(entity, 'stats') and hasattr(entity.stats, 'speed') else entity.hero.stats.speed, reverse=True)
    return sortedList

def attackMenu(stdscr, key_scheme, PlayerController, enemies : List[Enemy]):
    global selected

    this_enemies = enemies
    
    while True:
        randomHero = party[random.randint(0, 2)]
        this_enemies = removePerished(this_enemies)
        if len(this_enemies) == 0:
            break
        stdscr.clear()
        stdscr.addstr(0, 0, f"=== {randomHero.hero.getName()}'s turn -- Attack! ===")
        for i, option in enumerate(attackOptions):
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
            PlayerController.pressButton("enter")
            break

    stdscr.clear()
    if selected == 3:
        this_enemies[random.randint(0, len(this_enemies) - 1)].takeDamage(randomHero.attack(stdscr))

    elif selected == 2:
        stdscr.addstr(0, 0, f"Heavy Selected, now is last choice")
        randomHero.hero.heroStats.attackStrategy = HeavyAttack()
        this_enemies[random.randint(0, len(this_enemies) - 1)].takeDamage(randomHero.attack(stdscr), stdscr
                                                                )

    elif selected == 1:
        stdscr.addstr(0, 0, f"Mid")
        randomHero.hero.heroStats.attackStrategy = MidAttack()
        this_enemies[random.randint(0, len(this_enemies) - 1)].takeDamage(randomHero.attack(stdscr), stdscr)

    elif selected == 0:
        stdscr.addstr(0, 0, f"Light")
        randomHero.hero.heroStats.attackStrategy = LightAttack()
        this_enemies[random.randint(0, len(this_enemies) - 1)].takeDamage(randomHero.attack(stdscr), stdscr)

    randomHero.takeDamage(this_enemies[random.randint(0, len(this_enemies) - 1)].attack(stdscr), stdscr)
    stdscr.refresh()
    stdscr.getch()


def story(stdscr, key_scheme, PlayerController, party, enemies):
    #! part 1
    stdscr.clear()
    stdscr.addstr(0, 0, "_____Defeat the evil John Evil_____")
    stdscr.getch()
    stdscr.refresh()
    stdscr.clear()
    stdscr.addstr(0, 0, "Your current party is: ")
    stdscr.getch()
    checkPartyStatus(stdscr, party)
    stdscr.getch()
    stdscr.addstr(0, 0, "Your first encounter is: ")
    startEncountersHeroes(stdscr, party)
    for i in range(0, 100):
        attackMenu(stdscr, key_scheme, PlayerController, enemies)
        

    stdscr.clear()
    stdscr.addstr(0, 0, "Sadly this game isnt't finished")


def game(stdscr, key_scheme, PlayerController):
    curses.curs_set(0)
    stdscr.nodelay(False)
    stdscr.keypad(True)
    enemies = shallowGoblins
    global party
    while any(e.stats.hp > 0 for e in enemies): #! its reading hp as tuple???
        story(stdscr, key_scheme, PlayerController, party, enemies)
        stdscr.clear()
