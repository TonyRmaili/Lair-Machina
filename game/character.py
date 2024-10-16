
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

        
