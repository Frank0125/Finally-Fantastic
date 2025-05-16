from .AttackStrategy import AttackStrategy

class Stats:
    def __init__(self, name : str, hp : int, speed : int, strength : int):
        self.name = name
        self.hp = hp,
        self.speed = speed
        self.strength = strength


class HeroStats:
    def __init__(self, mana : int, attackStrategy : AttackStrategy):
        self.mana = mana
        self.attackStrategy = attackStrategy


__all__ = ['Stats', 'HeroStats']