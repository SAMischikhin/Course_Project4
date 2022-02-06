import random
from typing import Tuple

from singleton_decorator import singleton

from unit import BaseUnit


@singleton
class Arena:
    def play_start(self, player: BaseUnit, enemy: BaseUnit, stamina_recover: float):
        self.player = player
        self.enemy = enemy
        self.stamina_recover = stamina_recover
        self.play = True

    def recovery(self, target: BaseUnit):
        target.stamina_points += self.stamina_recover * target.unit_class.stamina
        target.stamina_points = min(round(target.stamina_points, 1), target.unit_class.max_stamina)

    def next_turn(self) -> Tuple[str, str]:
        if not self.enemy.check_health():
            return '', self.game_over(self.enemy.name)
        else:
            self.recovery(self.enemy)
            enemy_turn_res = self.enemy_turn()
            if not self.player.check_health():
                return enemy_turn_res, self.game_over(self.player.name)
            else:
                return enemy_turn_res, 'Бой продолжается...'

    def enemy_turn(self) -> str:
        skill_use_agreed = random.choices([False, True], weights=[9, 1])[0]
        if not self.enemy.skill_used and skill_use_agreed:
            return self.enemy.use_skill(self.player)
        else:
            return self.enemy.get_hit(self.player)

    def player_hit(self) -> Tuple[str, str]:
        self.recovery(self.player)
        player_turn = self.player.get_hit(self.enemy)
        enemy_turn, battle_result = self.next_turn()
        return f'{player_turn}\n {enemy_turn}', battle_result

    def player_wait(self) -> Tuple[str, str]:
        self.recovery(self.player)
        enemy_turn, battle_result = self.next_turn()
        return f'{self.player.name} выжидает удобного момента... \n {enemy_turn}', battle_result

    def player_skill_use(self):
        self.recovery(self.player)
        player_turn = self.player.use_skill(self.enemy)
        enemy_turn, battle_result = self.next_turn()
        return f'{player_turn}\n {enemy_turn}', battle_result

    def game_over(self, loser: str) -> str:
        self.play = False
        return f'Битва закончена! {loser} проиграл!'
