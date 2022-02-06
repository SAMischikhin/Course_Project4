from flask import Flask, render_template, request, redirect, url_for

from arena import Arena
from equipment import equip
from classes import unitclasses

from unit import BaseUnit


app = Flask(__name__)

heroes = {}
arena = Arena()


def set_page(name: str, templ_name: str):
    result = {
        "header": f'{name}',  # для названия страниц
        "classes": list(unitclasses.unit_classes.keys()),  # для названия классов
        "weapons": equip.get_weapon_names(),  # для названия оружия
        "armors": equip.get_armor_names()  # для названия брони
    }
    return render_template(templ_name, result=result)


def get_form(name: str):
    if request.method == "POST":
        unit = BaseUnit(name=request.form['name'],
                        unit_class=unitclasses.unit_classes[request.form['unit_class']],
                        health_points=unitclasses.unit_classes[request.form['unit_class']].max_health,
                        stamina_points=unitclasses.unit_classes[request.form['unit_class']].max_stamina,
                        weapon=equip.get_weapon(request.form['weapon']),
                        armor=equip.get_armour(request.form['armor'])
                        )
        heroes[name] = unit
        return heroes


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/choose-hero/', methods=['GET', 'POST'])
def choose_hero():
    if request.method == "GET":
        return set_page('Player', 'hero_choosing.html')
    if request.method == "POST":
        get_form('player')
        return redirect(url_for('choose_enemy'), code=302)


@app.route('/choose-enemy/', methods=['GET', 'POST'])
def choose_enemy():
    if request.method == "GET":
        return set_page('Enemy', 'hero_choosing.html')
    if request.method == "POST":
        print(get_form('enemy'))
    return redirect(url_for('fight'), code=302)


@app.route('/fight/')
def fight():
    arena.play_start(player=heroes['player'], enemy=heroes['enemy'], stamina_recover=2)
    return render_template('fight.html', heroes=heroes)


@app.route('/fight/hit/')
def hit():
    result, battle_result = arena.player_hit()
    return render_template('fight.html', heroes=heroes, result=result, battle_result=battle_result)


@app.route('/fight/use-skill/')
def use_skill():
    result, battle_result = arena.player_skill_use()
    return render_template('fight.html', heroes=heroes, result=result, battle_result=battle_result)


@app.route('/fight/pass-turn/')
def pass_turn():
    result, battle_result = arena.player_wait()
    return render_template('fight.html', heroes=heroes, result=result, battle_result=battle_result)


@app.route('/fight/end-fight/')
def end_fight():
    arena.game_running = False
    return render_template('fight.html', heroes=heroes, result='', battle_result=arena.game_over(arena.player.name))


if __name__ == '__main__':
    app.run()
