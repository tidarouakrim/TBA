# Define the Room class.

class Room:
    """
    This class represents a room in a adventure game
    Attributes:
        name (str) =  le nom du joueur 
        description =  description du lieu 
        exits =  sortie
    Methods:
        __init__(self, name) : The constructor.
        get_exit(self, direction): Return the room in the given direction if it exists.
        get_exit_string(self): Return a string describing the room's exits.
        get_long_description(self) : Return a long description of this room including exits.
    Examples:

    >>> 
    >>> room.name
    'gare'
    >>> room.description
    'une gare élégante où l’Orient Express attend, luxueux et mystérieux, prêt à traverser l’Europe'
    >>> room.exits
    {}
    """

    # Define the constructor.
    def __init__(self, name, description, image):
        self.name = name
        self.description = description
        self.exits = {}
        self.inventory = {}
        self.characters = {}
        self.image = image  # Path to image file (PNG/JPG) for this room

    # Define the get_exit method.
    def get_exit(self, direction):
        # Return the room in the given direction if it exists.
        if direction in self.exits.keys():
            return self.exits[direction]
        else:
            return None

    # Return a string describing the room's exits.
    def get_exit_string(self):
        exit_string = "Sorties: "
        for exit in self.exits.keys():
            if self.exits.get(exit) is not None:
                exit_string += exit + ", "
        exit_string = exit_string.strip(", ")
        return exit_string

    # Return a long description of this room including exits.
    def get_long_description(self):
        return f"\nVous êtes dans{self.description}\n\n{self.get_exit_string()}\n"

    def get_inventory(self):
        """
        Affiche le contenu de l'inventaire du joueur et les personnages présents.
        """

        if len(self.inventory) == 0 and len(self.characters) == 0:
            return "Il n'y a rien ici."

        result = "on voit:\n"

        if len(self.inventory) > 0:
            for name, item in self.inventory.items():
                result += f"    - {name} : {item.description} ({item.weight} kg)\n"
        else:
            result += "    - Aucun objet ici.\n"

        if len(self.characters) > 0:
            for name, character in self.characters.items():
                result += f"    - {character}\n"
        else:
            result += "    - Il n'y a personne ici.\n"

        return result