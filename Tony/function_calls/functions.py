from random import randint
import json


def roll_dice(prof):
    a = randint(1,20)
    a += prof
    return a


def get_skill_mod(skill: str) -> str:
    skills = {
        'stealth': 3,
        'medicine': 2
    }
    ability = skills[skill]
    roll = randint(1,20)
    roll += ability
    return f'(you make a {skill} roll: {roll})'



def no_function():
    return f'no fitting function to call'

all_functions = {
    
    'get_skill_mod':get_skill_mod,
    'roll_dice':roll_dice,
    'no_function':no_function
}



