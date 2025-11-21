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
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
    
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
