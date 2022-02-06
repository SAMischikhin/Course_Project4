import json
import os

import marshmallow_dataclass
from dataclasses import dataclass
import random
from typing import List, Union

from werkzeug.routing import ValidationError

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

print(BASE_DIR)
print(DATA_DIR)


@dataclass()
class Weapon:
    id: int
    name: str
    min_damage: float
    max_damage: float
    stamina_per_hit: float

    def real_damage(self):
        return round(random.uniform(self.min_damage, self.max_damage), 1)


@dataclass()
class Armor:
    id: int
    name: str
    defence: float
    stamina_per_turn: float


@dataclass()
class EquipmentData:
    weapons: List[Weapon]
    armors: List[Armor]


class Equipment:
    equipment_data: EquipmentData

    def __init__(self):
        self.equipment_data = self._create_eruipment_data()

    @staticmethod
    def _get_item(name: str, items: List[Union[Weapon, Armor]]) -> Union[Weapon, Armor]:
        for item in items:
            if item.name == name:
                return item

    @staticmethod
    def _get_equipment_data(equip_json: json) -> EquipmentData:
        equipdataschema = marshmallow_dataclass.class_schema(EquipmentData)
        try:
            return equipdataschema().load(equip_json)
        except ValidationError:
            raise ValueError

    @staticmethod
    def _get_json(equip_file: str) -> json:
        with open(equip_file, "r", encoding="utf-8") as json_file:
            return json.load(json_file)

    @staticmethod
    def _get_path(file_name: str) -> Union[str, None]:
        file_path = os.path.join(DATA_DIR, file_name)
        if os.path.exists(file_path):
            return file_path
        else:
            print(f'{file_path} is not exist')
            raise ValidationError

    def _create_eruipment_data(self) -> EquipmentData:
        equip_file = self._get_path('equipment.json')
        equip_json = self._get_json(equip_file)
        return self._get_equipment_data(equip_json)

    def get_weapon(self, name: str, ) -> Weapon:
        return self._get_item(name, self.equipment_data.weapons)

    def get_armour(self, name: str, ) -> Armor:
        return self._get_item(name, self.equipment_data.armors)

    def get_weapon_names(self):
        return list([w.name for w in self.equipment_data.weapons])

    def get_armor_names(self):
        return list([a.name for a in self.equipment_data.armors])


equip = Equipment()
