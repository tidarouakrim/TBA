# Description: The actions module.

# The actions module contains the functions that are called when a command is executed.
# Each function takes 3 parameters:
# - game: the game object
# - list_of_words: the list of words in the command
# - number_of_parameters: the number of parameters expected by the command
# The functions return True if the command was executed successfully, False otherwise.
# The functions print an error message if the number of parameters is incorrect.
# The error message is different depending on the number of parameters expected by the command.


# The error message is stored in the MSG0 and MSG1 variables and formatted with the command_word variable, the first word in the command.
# The MSG0 variable is used when the command does not take any parameter.
MSG0 = "\nLa commande '{command_word}' ne prend pas de paramètre.\n"
# The MSG1 variable is used when the command takes 1 parameter.
MSG1 = "\nLa commande '{command_word}' prend 1 seul paramètre.\n"

class Actions:

    def go(game, list_of_words, number_of_parameters):
        """
        Move the player in the direction specified by the parameter.
        The parameter must be a cardinal direction (N, E, S, O).

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:
        
        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> go(game, ["go", "N"], 1)
        True
        >>> go(game, ["go", "N", "E"], 1)
        False
        >>> go(game, ["go"], 1)
        False

        """
        direction_map = {
        "N": "N", "NORD": "N",
        "S": "S", "SUD": "S",
        "E": "E", "EST": "E",
        "O": "O", "OUEST": "O",
        "U": "U", "UP": "U",
        "D": "D", "DOWN": "D"
        }

        player = game.player
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            print(player.current_room.get_long_description())
            return False
        # Get the direction from the list of words.
        input_direction = list_of_words[1].strip().upper()  #supprime les espaces ...

        # Vérifier que l'entrée est dans le dictionnaire 
        if input_direction not in direction_map:
             print(f"Direction '{list_of_words[1]}' non reconnue")
             print(player.current_room.get_long_description())
             return False

        
        direction = direction_map[input_direction]

        # Vérifier que c'est une direction valide
        if direction not in game.direction:
            print(f"Direction '{direction}' non reconnue")
            print(player.current_room.get_long_description())
            return False

        moved = game.player.move(direction)

        if moved:
            
            all_characters = set()
            for room in game.rooms:
                all_characters.update(room.characters.values())

            for character in list(all_characters):
                character.move()
        return moved


    def quit(game, list_of_words, number_of_parameters):
        """
        Quit the game.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> quit(game, ["quit"], 0)
        True
        >>> quit(game, ["quit", "N"], 0)
        False
        >>> quit(game, ["quit", "N", "E"], 0)
        False

        """
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        # Set the finished attribute of the game object to True.
        player = game.player
        msg = f"\nMerci {player.name} d'avoir joué. Au revoir.\n"
        print(msg)
        game.finished = True
        return True

    def help(game, list_of_words, number_of_parameters):
        """
        Print the list of available commands.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> help(game, ["help"], 0)
        True
        >>> help(game, ["help", "N"], 0)
        False
        >>> help(game, ["help", "N", "E"], 0)
        False

        """

        # If the number of parameters is incorrect, print an error message and return False.
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        # Print the list of available commands.
        print("\nVoici les commandes disponibles:")
        for command in game.commands.values():
            print("\t- " + str(command))
        print()
        return True
    
   
    def history(game, list_of_words, number_of_parameters):
        print(game.player.get_history())

    def back(game, list_of_words, number_of_parameters):
        if len(list_of_words) != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        moved = game.player.back()

        if moved:
            all_characters = set()
            for room in game.rooms:
                all_characters.update(room.characters.values())

            for character in list(all_characters):
                character.move()
        return moved
    
    def look(game, list_of_words, number_of_parameters):
        if len(list_of_words) != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        # Récupérer la pièce actuelle
        room = game.player.current_room

        # Afficher description de la pièce
        print(room.get_long_description())

        # Afficher les items via get_inventory()
        print(room.get_inventory())

        return True
    
    def take(game, list_of_words, number_of_parameters):
         
        item_name = list_of_words[1]

        room = game.player.current_room  # pièce actuelle

        # Vérifier si l'objet est présent dans la pièce
        if item_name not in room.inventory:
            print(f"L'objet '{item_name}' n'est pas dans la pièce.")
            return False

        # Récupérer l’objet
        item = room.inventory[item_name]

        # Vérifier le poids total
        if game.player.current_weight() + item.weight > game.player.max_weight:
            print(f"Vous ne pouvez pas prendre '{item_name}', trop lourd !")
            return False


        # Ajouter à l’inventaire du joueur
        game.player.inventory[item_name] = item

        # Retirer de la pièce
        del room.inventory[item_name]
        print(f"Vous avez pris l'objet '{item_name}'.")
        return True
    

    def drop(game, list_of_words, number_of_parameters):
        if len(list_of_words) != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # item à déposer
        item_name = list_of_words[1]

        # Pièce actuelle du joueur
        room = game.player.current_room

        # Vérifier si l'objet est dans l'inventaire du joueur
        if item_name not in game.player.inventory:
            print(f"L'objet '{item_name}' n'est pas dans l'inventaire.")
            return False
        
         # Récupérer l’item
        item = game.player.inventory[item_name]

         # Ajouter à l'inventaire de la pièce
        room.inventory[item_name] = item

        # Retirer de l’inventaire du joueur
        del game.player.inventory[item_name]
        print(f"Vous avez déposé l'objet '{item_name}'.")

        return True
    
    def check(game, list_of_words, number_of_parameters):
        # Afficher l'inventaire du joueur
        print(game.player.get_inventory())

        return True
    
    def beamer_charge(game, list_of_words, number_of_parameters):

    # vérifie si joueur possède le beamer
        if "beamer" not in game.player.inventory:
            print("Vous n'avez pas de beamer sur vous.")
            return False

        beamer = game.player.inventory["beamer"]

    # enregistrer la room actuelle
        beamer.charged_room = game.player.current_room
        print(f" Le beamer a mémorisé : {beamer.charged_room.name}")
        return True
    
    def beamer_teleportation(game, list_of_words, number_of_parameters):
        # vérifie si joueur possède le beamer
        if "beamer" not in game.player.inventory:
            print("Vous n'avez pas le beamer sur vous.")
            return False

        beamer = game.player.inventory["beamer"]

        # vérifier si le beamer est chargé
        if beamer.charged_room is None:
            print("Le beamer n'est pas chargé.")
            return False

        # téléporter le joueur
        game.player.current_room = beamer.charged_room
        print(f" Téléportation vers : {beamer.charged_room.name}")
        return True
    

    def talk(game, list_of_words, number_of_parameters):

        if len(list_of_words) != number_of_parameters + 1:
            print(f"Usage : talk <someone>")
            return False

        pnj_name = list_of_words[1]
        room = game.player.current_room

        # Vérifie si le PNJ est dans la pièce
        if pnj_name not in room.characters:
            print(f"{pnj_name} n'est pas ici.")
            return False

        # Fait parler le PNJ
        pnj_name = room.characters[pnj_name]
        pnj_name.get_msg()
        return True
