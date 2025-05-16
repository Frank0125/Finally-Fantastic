# Finally Fantastic - Python RPG

### To run this project you should do the following commands
```shell
python -m venv venv
```
```shell
venv/Scripts/activate
```
```shell
pip install -r requirements.txt
```
```shell
python main.py
```

## This project uses the following Design Patterns:

- Creational Pattern: **Prototype**
- Structural Pattern: **Decorator**
- Behavioral Pattern: **Strategy**
- Extra Pattern (Behavioral): **Command**

## UML created in mermaid:

```mermaid
classDiagram
    class Command {
        + execute()
    }

    class UpCommand {
        + execute()
    }

    class DownCommand {
        + execute()
    }
    
    class SelectCommand {
        + execute()
    }

    class Prototype {
	    + Prototype clone()
        + void perish()
        + void takeDamage()
        + int attack()
    }

    class Hero {
        + void encounter()
        + void perish()
        + void takeDamage()
        + void setAttackStrategy(AttackStrategy)
        + int attack()
    }

    class AttackStrategy {
        - int manaCost
	    + attack()
       + getManaCost()
    }

    class LightStrategy {
	    + attack()
    }

    class MidStrategy {
	    + attack()
    }

    class HeavyStrategy {
	    + attack()
    }

    class ConcreteHero {
        - HeroStats herosStats
        - Stats stats
        + void encounter()
        + void perish()
        + void takeDamage()
        + void setAttackStrategy(AttackStrategy)
        + int attack()
	    + Hero clone()
    }

    class HeroDecorator {
	    - Hero hero
	    - attackStrategy
    }

    class ConcreteHeroDecorator {
	    - attackStrategy
    }

    class Enemy {
	    - Stats raw_stats
	    + regularAttack()
        + void encounter()
        + void perish()
        + void takeDamage()
	    + Enemy clone()
    }

    class Spawner {
	    - Prototype entity_blueprint
	    - spawnEntity()
    }

    class EnemySpawner {
	    + Enemy spawnEntity()
    }

    class HeroSpawner {
	    +Hero spawnEntity()
    }

    class Stats {
	    -string name
	    -int hp
	    -int speed
    }

    class HeroStats {
        - int mana 
        - AttackStrategy attackstrategy
    }

    %% Composición
    HeroDecorator --> Hero
    
    Enemy --> Stats
    Spawner --> Prototype
    ConcreteHero --> HeroStats
    ConcreteHero --> Stats

    %% Herencia
    UpCommand ..|> Command
    DownCommand ..|> Command
    SelectCommand ..|> Command
    LightStrategy ..|> AttackStrategy
    MidStrategy ..|> AttackStrategy
    HeavyStrategy ..|> AttackStrategy
    ConcreteHero ..|> Hero
    HeroDecorator ..|> Hero
    Hero ..|> Prototype
    ConcreteHeroDecorator ..|> HeroDecorator
    Enemy ..|> Prototype
    EnemySpawner ..|> Spawner
    HeroSpawner ..|> Spawner
```