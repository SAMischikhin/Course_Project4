from dataclasses import dataclass
from typing import TypeVar

from classes import UnitClass
from equipment import Weapon, Armor

SelfClass = TypeVar("SelfClass", bound="BaseUnit")


@dataclass()
class BaseUnit:
    name: str
    unit_class: UnitClass
    health_points: float
    stamina_points: float
    weapon: Weapon
    armor: Armor
    skill_used: bool = False

    def equip_with_weapons(self, weapon: Weapon):
        self.weapon = weapon

    def equip_with_armors(self, armor: Armor):
        self.armor = armor

    def check_health(self) -> bool:
        if self.health_points <= 0:
            return False
        else:
            return True

    def _real_damage(self, target: SelfClass) -> str:
        attack_damage = round(self.weapon.real_damage() * self.unit_class.attack, 1)
        armor_block = round(target.armor.defence * target.unit_class.armor, 1)
        final_damage = round(attack_damage - armor_block, 1)

        if attack_damage > armor_block:
            target.take_hit(final_damage)
            return f'{self.name}, используя {self.weapon.name}, пробивает {target.armor.name}\
                 соперника и наносит {final_damage} урона'
        else:
            return f'{self.name}, используя {self.weapon.name}, наносит удар,\
                 но {target.armor.name} соперника его останавливает.'

    def take_hit(self, damage: float):
        self.health_points = max(round(self.health_points - damage, 1), 0)

    def use_skill(self, target: SelfClass) -> str:
        if not self.skill_used:
            self.skill_used = True
            return self.unit_class.skill.use(self, target)
        else:
            return f'Навык уже использован'

    def get_hit(self, target: SelfClass) -> str:
        if self.stamina_points <= self.weapon.stamina_per_hit:
            return f'{self.name} попытался использовать {self.weapon.name},\
             но у него не хватило выносливости'
        else:
            self.stamina_points = round((self.stamina_points - self.unit_class.stamina * self.weapon.stamina_per_hit), 1)
            target.stamina_points = round((target.stamina_points - target.unit_class.stamina * self.armor.stamina_per_turn), 1)
            return self._real_damage(target)
