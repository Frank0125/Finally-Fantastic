import curses
import random
import time 
from typing import List, Union

seed = int(time.time()) #TODO PRINT SEED
random.seed(seed)

#* Entity
from classes.Entity.AttackStrategy import HeavyAttack, MidAttack, LightAttack
from classes.Entity.HeroCopy import Prototype, Enemy, EnemySpawner, Hero, ConcreteHero, DecoratorHero, Rogue, Mage, Tank
from classes.Entity.Stats import Stats, HeroStats

# region Stats
#! Phase 1 enemy stats
atributesEnemies1 = Stats("Goblin",40, 4, 7)
#! Phase 2 enemy stats
atributesEnemies2 = Stats("The Twins",70, 9, 12)

#! Boss (random stats)
atributesBoss = Stats("John Evil",200, 12, 40)
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
attackOptions = ["Last Option, Heavy, Mid, Light"]
party = [rogue, mage, tank]


def startEncounters(fullList : List[Union[Hero, Enemy]] ):
    for i in fullList:
        i.encounter()

def checkPartyStatus(party : List[Hero]):
    for i in party:
        i.getStatus()

def havePerished(party : List[Enemy]):
    for i in party:
        if i.stats.hp != 0:
            return True 
    return False

def createEncounterList(fullList):
    for i in fullList:
        if i.stats.hp == 0:
            fullList.remove(i)
    sortedList = sorted(fullList, key=lambda entity: entity.stats.speed, reverse=True)
    return sortedList

def attackMenu(stdscr, key_scheme, PlayerController, hero : Hero, enemies : List[Enemy]):
    while True:
        if havePerished(enemies):
            break
        stdscr.clear()
        stdscr.addstr(0, 0, f"=== {Hero.getName()}'s turn -- Attack! ===")
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
    if selected==3:
        enemies[random(0, enemies.count())].takeDamage(hero.attack())

    elif selected==2:
        stdscr.addstr(0, 0, f"Heavy Selected, now is last choice")
        hero.heroStats.attackStrategy = HeavyAttack()
        enemies[random(0, enemies.count())].takeDamage(hero.attack())

    elif selected==1:
        stdscr.addstr(0, 0, f"Mid")
        hero.heroStats.attackStrategy = MidAttack()
        enemies[random(0, enemies.count())].takeDamage(hero.attack())

    elif selected==0:
        stdscr.addstr(0, 0, f"Light")
        hero.heroStats.attackStrategy = LightAttack()
        enemies[random(0, enemies.count())].takeDamage(hero.attack())

    stdscr.refresh()
    stdscr.getch()

def story(stdscr, key_scheme, PlayerController, fullList):
    #! part 1
    turns = createEncounterList(fullList)
    stdscr.clear()
    stdscr.addstr(0, 0, "_____Defeat the evil John Evil_____")
    stdscr.getch()
    stdscr.addstr(0, 0, "Your current party is: ")
    checkPartyStatus(party)
    stdscr.getch()
    stdscr.addstr(0, 0, "Your first encounter is: ")
    startEncounters(fullList)
    for i in range(0, 100):
        attackMenu(stdscr, key_scheme, PlayerController, party[turns[i % turns.count]])

    stdscr.clear()
    stdscr.addstr(0, 0, "Sadly this game isnt't finished")
        

def game(stdscr, key_scheme, PlayerController):
    curses.curs_set(0)
    stdscr.nodelay(False)
    stdscr.keypad(True)
    stdscr.addstr(0, 0, "_____Defeat the evil John Evil_____")
    enemies = shallowGoblins + deepOrcs
    fullList = enemies + party
    while enemies in fullList:
        story(stdscr, key_scheme, PlayerController, fullList)
        stdscr.clear()

    