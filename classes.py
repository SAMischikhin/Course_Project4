from dataclasses import dataclass, field
from skills import ConcreteSkill, fury_kick, power_hit


@dataclass()
class UnitClass:
    name: str
    max_health: float
    max_stamina: float
    attack: float
    stamina: float
    armor: float
    skill: ConcreteSkill


@dataclass()
class Warrior(UnitClass):
    name: str = 'Воин'
    max_health: float = 60.0
    max_stamina: float = 30.0
    skill: ConcreteSkill = fury_kick
    attack: float = 0.8  # модификатор атаки
    stamina: float = 0.9  # модификатор выносливости
    armor: float = 1.2  # модификатор брони


@dataclass()
class Thief(UnitClass):
    name: str = 'Вор'
    max_health: float = 50.0
    max_stamina: float = 25.0
    skill: ConcreteSkill = power_hit
    attack: float = 1.5  # модификатор атаки
    stamina: float = 1.2  # модификатор выносливости
    armor: float = 1.0  # модификатор брони


@dataclass()
class UnitClasses:
    unit_classes: dict = field(default_factory=dict)

    def __init__(self):
        self.unit_classes = {Warrior.name: Warrior, Thief.name: Thief}


unitclasses = UnitClasses()
