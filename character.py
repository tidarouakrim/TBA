import random


class Character:
    """
    This class represents a non-player character (NPC) in the game.
    """

    def __init__(self, name, description, current_room, msgs):
        self.name = name                    # nom du PNJ
        self.description = description      # description du PNJ
        self.current_room = current_room    # pièce où il se trouve
        self.msgs = msgs                    # messages qu'il dit

        self.current_room.characters[self.name] = self


    def __str__(self):
        """
        retrourne une représentation textuelle du PNJ
        """
        return f"{self.name} : {self.description}"

    def move(self):
        from game import DEBUG

        if self.name in ["Gouteur", "Contrôleur", "Paul", "Claire", "Henri"]:
            if DEBUG:
                print(f"DEBUG: {self.name} reste dans {self.current_room.name}.")
            return False
            
        # 1 chance sur 2 de ne pas bouger
        if random.choice([True, False]) is False:
            if DEBUG:
                print(f"DEBUG: {self.name} reste dans {self.current_room.name}")
            return False

        # Liste des pièces adjacentes valides
        exits = [room for room in self.current_room.exits.values() if room is not None]

        if not exits:
            if DEBUG:
                print(f"DEBUG: {self.name} n'a aucune sortie depuis {self.current_room.name}")
            return False

        # Choix d'une pièce au hasard
        new_room = random.choice(exits)

        if DEBUG:
            print(
                f"DEBUG: {self.name} se déplace de "
                f"{self.current_room.name} vers {new_room.name}")
            
        # Déplacement réel
        del self.current_room.characters[self.name]
        new_room.characters[self.name] = self
        self.current_room = new_room

        return True
    
    def get_msg(self):
        """
        Affiche les messages du PNJ de manière cyclique.
        """
        if not self.msgs:
            print("Le PNJ n'a rien à dire.")
            return

        # Prend le premier message
        msg = self.msgs.pop(0)
        print(msg)

        # Remet le message à la fin pour continuer le cycle
        self.msgs.append(msg)