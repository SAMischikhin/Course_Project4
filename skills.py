from dataclasses import dataclass
from typing import TypeVar

UnitClass = TypeVar("UnitClass", bound="unit.BaseUnit")


@dataclass()
class Skill:
    name: str
    damage: float
    req_stamina: float

    def skill_effect(self, target: UnitClass):
        pass

    def use(self, user: UnitClass, target: UnitClass) -> str:
        if user.stamina_points >= self.req_stamina:
            self.skill_effect(target)
            return f'{user.name} использует {self.name} и наносит {self.damage} урона сопернику.'
        else:
            return f'{user.name} попытался использовать {self.name}, но у него не хватило выносливости.'


class ConcreteSkill(Skill):
    def __init__(self, name: str, damage: float, req_stamina: float):
        self.name = name
        self.damage = damage
        self.req_stamina = req_stamina

    def skill_effect(self, target: UnitClass):
        target.health_points = round(target.health_points-self.damage, 1)


fury_kick = ConcreteSkill(name="Свирепый пинок", damage=12, req_stamina=6)
power_hit = ConcreteSkill(name="Мощный укол", damage=15, req_stamina=5)
