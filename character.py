class Character:
    """
    This class represents a non-player character (NPC) in the game.
    """

    def __init__(self, name, description, current_room, messages):
        self.name = name                    # nom du PNJ
        self.description = description      # description du PNJ
        self.current_room = current_room    # pièce où il se trouve
        self.messages = messages             # messages qu'il dit

    def __str__(self):
        """
        retrourne une représentation textuelle du PNJ
        """
        return f"{self.name} : {self.description}"