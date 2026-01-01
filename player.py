# Define the Player class.
from quest import QuestManager

class Player():
    """
    This class represents a player in a adventure game
    Attributes:
        name (str) =  le nom du joueur 
        current_room (Room) =   le lieu dans lequel se trouve le joueur 

    Methods:
        __init__(self, name) : The constructor.

    Examples:

    >>> p = Player("Julie")
    >>> p.name
    'Julie'
    >>> player.current_room
    none
 
    """

    # Define the constructor.
    def __init__(self, name, max_weight=6):
        self.name = name
        self.current_room = None
        self.history = []
        self.inventory = {}
        self.max_weight = max_weight
        self.quest_manager = QuestManager(self)  
        self.rewards = []
        self.move_count = 0
        self.poisoned_plate = None 
        self.found_letters = []
        self.waiting_for_secret_word = False






        
    # Define the move method.
    def move(self, direction):
        # Get the next room from the exits dictionary of the current room.
        next_room = self.current_room.exits[direction]
        # If the next room is None, print an error message and return False.
        if next_room is None:
            print("\nAucune porte dans cette direction !\n")
            print(self.get_history())
            return False
        # Ajoute la salle actuelle à l'historique
        self.history.append(self.current_room)

        # Set the current room to the next room.
        self.current_room = next_room
        print(self.current_room.get_long_description())
        print(self.get_history())
        # Compteur de mouvements
        self.move_count += 1
        self.quest_manager.check_action_objectives("Se déplacer", self.move_count)

         # Détecter la pièce spéciale pour lancer la quête
        if self.current_room.name == "piece1":
            # Activer la quête si elle n'est pas déjà active
            self.quest_manager.activate_quest("Trouver la parure de Madame Loisel")
            print("🔔 Quête 'Trouver la parure de Madame Loisel' activée !")
        if self.current_room.name == "restaurant":
            # Activer la quête si elle n'est pas déjà active
            self.quest_manager.activate_quest("Le repas empoisonné")
            print("🔔 Quête 'Le repas empoisonné' activée !")

            self.poisoned_plate = "salade"
        if self.current_room.name == "bibliotheque":
            # Activer la quête si elle n'est pas déjà active
            self.quest_manager.activate_quest("Mot secret")
            print("🔔 Quête 'Mot secret' activée !")


        return True

    def get_history(self):
        """
        Liste les pièces visitées.
        """
        
        result = "Vous avez déja visité les pièces suivantes:\n"
        for room in self.history:
            result += f"    - {room.description}\n"
        return result

   
    def back(self):
        """
        Revient à la pièce précédente si possible.
        """
        if len(self.history) == 0:
            print("\nVous ne pouvez pas revenir en arrière : aucun déplacement précédent.\n")
            return False  # l'utilisateur est au départ

        # Retirer la dernière pièce visitée
        previous_room = self.history.pop()

        # Revenir dans cette pièce
        self.current_room = previous_room

        # Afficher tout comme un déplacement normal
        print(self.current_room.get_long_description())
        print(self.get_history())

        return True
    
    def get_inventory(self):
        """
        Affiche le contenu de l'inventaire du joueur.
        """
        if len(self.inventory) == 0:
            return "Vous n'avez rien dans votre inventaire."

        result = "Vous disposez des items suivants:\n"
        for name, item in self.inventory.items():
            result += f"    - {name} : {item.description} ({item.weight} kg)\n"
        return result
    
    def current_weight(self):
        return sum(item.weight for item in self.inventory.values())
    


    def add_reward(self, reward):
        """
        Add a reward to the player's rewards list.
        
        Args:
            reward (str): The reward to add.
            
        Examples:
        
        >>> player = Player("Bob")
        >>> player.add_reward("Épée magique") # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Vous avez obtenu: Épée magique
        <BLANKLINE>
        >>> "Épée magique" in player.rewards
        True
        >>> player.add_reward("Épée magique") # Adding same reward again
        >>> len(player.rewards)
        1
        """
        if reward and reward not in self.rewards:
            self.rewards.append(reward)
            print(f"\n🎁 Vous avez obtenu: {reward}\n")


    def show_rewards(self):
        """
        Display all rewards earned by the player.
        
        Examples:
        
        >>> player = Player("Charlie")
        >>> player.show_rewards() # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Aucune récompense obtenue pour le moment.
        <BLANKLINE>
        >>> player.add_reward("Bouclier d'or") # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Vous avez obtenu: Bouclier d'or
        <BLANKLINE>
        >>> player.show_rewards() # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Vos récompenses:
        • Bouclier d'or
        <BLANKLINE>
        """
        if not self.rewards:
            print("\n🎁 Aucune récompense obtenue pour le moment.\n")
        else:
            print("\n🎁 Vos récompenses:")
            for reward in self.rewards:
                print(f"  • {reward}")
            print()