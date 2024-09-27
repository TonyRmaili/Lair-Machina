from random import randint
import json
# def addition(a,b):
#     return a+b

# def subtraction(a,b):
#     return a-b


def rolldice(prof):

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


all_functions = {
    
    'get_skill_mod':get_skill_mod

}


# all_functions = {
#     'addition' :addition,
#     'subtraction' :subtraction
# }


