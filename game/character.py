import json
class Character:
    """
    Character class - holds character data - each character is a instance of this class - if we want to make saves persistent we can save the data in a json file
    """
    def __init__(self,name=None,klass=None,race=None,description=None):

        self.name = name,
        self.klass = klass
        self.race = race
        self.description = description

        self.image = None
        self.inventory = []
        
        # paths
        self.profile_path = None
        self.dungeon_path = None
        self.sound_path = None



    def save_profile(self):  
        filename=self.profile_path+"save_file.json"
        with open(filename, 'w') as json_file:
            json.dump(self.__dict__, json_file, indent=4)