import ollama


class OllamaDmg:
    def __init__(self):
        self.model = 'llama3.1'


    def will_the_player_take_damage(self, prompt):
        system = 'does text describes feeling pain? ONLY ANSWER yes OR no'
        prompt = prompt

        resp = ollama.generate(
            model=self.model,
            prompt=prompt,
            system=system

        )
        
        return resp['response']


    def player_takes_damage(self, prompt):
        system = 'You must evaluate how much damage the character takes from the desciption. ANSWER ONLY with a number 1-20'
        prompt = prompt

        resp = ollama.generate(
            model=self.model,
            prompt=prompt,
            system=system

        )
        return int(resp['response'])


    def damage_check_and_resolve(self, prompt):
        # prompt= 'the music box explodes upon pickup! sending sparks and flame everywere'
        resp = self.will_the_player_take_damage(prompt=prompt)

        if resp.lower() == 'yes':
            damage_nmbr = self.player_takes_damage(prompt)
            print(damage_nmbr)
            return damage_nmbr
        else:
            print('no damage')
            return 0