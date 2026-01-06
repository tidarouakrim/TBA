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

    @staticmethod
    def quests(game, list_of_words, number_of_parameters):
        """
        Show all quests and their status.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.quests(game, ["quests"], 0)
        <BLANKLINE>
        📋 Liste des quêtes:
          ❓ Grand Explorateur (Non activée)
          ❓ Grand Voyageur (Non activée)
          ❓ Découvreur de Secrets (Non activée)
        <BLANKLINE>
        True
        >>> Actions.quests(game, ["quests", "param"], 0)
        <BLANKLINE>
        La commande 'quests' ne prend pas de paramètre.
        <BLANKLINE>
        False

        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Show all quests
        game.player.quest_manager.show_quests()
        return True


    @staticmethod
    def quest(game, list_of_words, number_of_parameters):
        """
        Show details about a specific quest.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.quest(game, ["quest", "Grand", "Voyageur"], 1)
        <BLANKLINE>
        📋 Quête: Grand Voyageur
        📖 Déplacez-vous 10 fois entre les lieux.
        <BLANKLINE>
        Objectifs:
          ⬜ Se déplacer 10 fois (Progression: 0/10)
        <BLANKLINE>
        🎁 Récompense: Bottes de voyageur
        <BLANKLINE>
        True
        >>> Actions.quest(game, ["quest"], 1)
        <BLANKLINE>
        La commande 'quest' prend 1 seul paramètre.
        <BLANKLINE>
        False

        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n < number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Get the quest title from the list of words (join all words after command)
        quest_title = " ".join(list_of_words[1:])

        # Prepare current counter values to show progress
        current_counts = {
            "Se déplacer": game.player.move_count
        }

        # Show quest details
        game.player.quest_manager.show_quest_details(quest_title, current_counts)
        return True


    @staticmethod
    def activate(game, list_of_words, number_of_parameters):
        """
        Activate a specific quest.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.activate(game, ["activate", "Grand", "Voyageur"], 1) # doctest: +ELLIPSIS
        <BLANKLINE>
        🗡️  Nouvelle quête activée: Grand Voyageur
        📝 Déplacez-vous 10 fois entre les lieux.
        <BLANKLINE>
        True
        >>> Actions.activate(game, ["activate"], 1)
        <BLANKLINE>
        La commande 'activate' prend 1 seul paramètre.
        <BLANKLINE>
        False

        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n < number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Get the quest title from the list of words (join all words after command)
        quest_title = " ".join(list_of_words[1:])

        # Try to activate the quest
        if game.player.quest_manager.activate_quest(quest_title):
            return True

        msg1 = f"\nImpossible d'activer la quête '{quest_title}'. "
        msg2 = "Vérifiez le nom ou si elle n'est pas déjà active.\n"
        print(msg1 + msg2)
        # print(f"\nImpossible d'activer la quête '{quest_title}'. \
        #             Vérifiez le nom ou si elle n'est pas déjà active.\n")
        return False


    @staticmethod
    def rewards(game, list_of_words, number_of_parameters):
        """
        Display all rewards earned by the player.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.rewards(game, ["rewards"], 0)
        <BLANKLINE>
        🎁 Aucune récompense obtenue pour le moment.
        <BLANKLINE>
        True
        >>> Actions.rewards(game, ["rewards", "param"], 0)
        <BLANKLINE>
        La commande 'rewards' ne prend pas de paramètre.
        <BLANKLINE>
        False
        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Show all rewards
        game.player.show_rewards()
        return True

    @staticmethod
    def repondre(game, args, num_params):
        player = game.player

        quest = None
        for q in player.quest_manager.active_quests:
            if q.title == "Quête 6":
                quest = q
                break
        if quest is None:
            print("❌ Vous n'avez pas encore commencé cette quête.")
            return False

        questions = [
            ("Quel était le plat contaminé ?", player.poisoned_plate.lower()),
            ("Quel était l’objet de Claire ?", "parapluie"),
            ("Quel est le mot secret ?", "bravo")
        ]

        if player.final_interrogation_step >= len(questions):
            print("🎉 La mission finale est déjà terminée.")
            return True

        step = player.final_interrogation_step

        if len(args) < 2:
            print(f"Le contrôleur : {questions[step][0]}")
            return True

        reponse = " ".join(args[1:]).lower()
        bonne_reponse = questions[step][1]

        if reponse == bonne_reponse:
            print("✔️ Correct.")
            player.final_interrogation_step += 1

            if player.final_interrogation_step == len(questions):
                print("🎉 Le contrôleur sourit. Mission réussie ! Vous arrivez à destination.")
                quest.complete_quest(player)
        else:
            print("❌ Mauvaise réponse.")
        if player.final_interrogation_step < len(questions):
            print(f"Le contrôleur : {questions[player.final_interrogation_step][0]}")

        return True




    @staticmethod
    def use(game, args, num_params):
        """
        Utiliser un objet sur une cible ou un plat.
        Syntaxe : use <objet> <cible/plat>
        """
        item_name = args[1].lower()
        room = game.player.current_room


        # Cas livre
        if item_name.startswith("livre"): 
            if item_name not in room.inventory: 
                print("Ce livre n'est pas ici.\n") 
                return True
            use_book(game, item_name)
            return True
        target_name = " ".join(args[2:]).lower() 
        room = game.player.current_room

        # Cas 1 : Clé sur coffre
        if item_name == "clé" and target_name == "coffre":
            if "coffre" in room.inventory:
                print("✅ Vous ouvrez le coffre et découvrez la parure de Madame Loisel !")
                game.player.quest_manager.check_action_objectives("utiliser clé sur coffre")
                return True
            else:
                print("❌ Il n'y a pas de coffre ici.")
                return False

        # Cas 2 : Sel sur plat
        if item_name == "sel":
            if target_name == game.player.poisoned_plate:
                print(f"\nLe {target_name} change légèrement de couleur ! C’est le plat empoisonné.\n")
                game.player.quest_manager.complete_objective("Saupoudrer le sel sur le plat empoisonné")
                game.player.quest_manager.complete_objective("Identifier le plat empoisonné")
            else:
                print(f"\nLe {target_name} ne réagit pas au sel.\n")
            return True
        

        # Cas général : utilisation non permise
        print(f"❌ Vous ne pouvez pas utiliser {item_name} sur {target_name}.")
        return False

        
    def give(game, list_of_words, number_of_parameters):
        """
        Donner un plat au PNJ.
        Exemple: donner ragoût
        """
        if len(list_of_words) < 2:
            print("\nLa commande 'donner' prend 1 paramètre.\n")
            return False

        plat = " ".join(list_of_words[1:]).lower()

        if plat == game.player.poisoned_plate:
            print("\nLe PNJ goûte le plat empoisonné et meurt ! La quête échoue.\n")
        else:
            print("\nLe PNJ goûte le plat sûr et vous complétez la quête !\n")
            game.player.quest_manager.complete_objective("Donner le plat sûr au PNJ")

        return True
    
   
    @staticmethod
    def check_secret_word(game, args, num_params):
        if len(args) < 2:
            print("\nVous devez entrer un mot après la commande 'mot'.\n")
            return False

        mot = args[1].strip().upper()  # récupère le mot tapé après "mot"
        if mot == "BRAVO":
            print("✅ Mot correct ! Quête terminée.")
            for quest in game.player.quest_manager.active_quests:
                if quest.title == "Mot secret":
                    quest.complete_objective("trouver le mot secret", game.player)
            game.player.waiting_for_secret_word = False
        else:
            print("❌ Mot incorrect, essayez encore.")
        return True
   
   # Dictionnaire des livres et des lettres qu'ils contiennent
books_letters = {
    "livre1": None,
    "livre2": "A",
    "livre3": "V",
    "livre4": "O",
    "livre5": "B",
    "livre6": "R",
}


def use_book(game, item_name):
    item_name = item_name.lower()
    
    if item_name not in books_letters:
        print(f"Le livre {item_name} n'existe pas.\n")
        return

    letter = books_letters[item_name]
    
    if letter is None:
        print("Aucune lettre trouvée.\n")
    else:
        if letter not in game.player.found_letters:
            game.player.found_letters.append(letter)
            print(f"Lettre {letter} enregistrée.\n")
            game.player.activate_secret_word_quest()
        else:
            print(f"Lettre {letter} déjà enregistrée.\n")
    
    # 🔔 Activer automatiquement la quête "Mot secret" si pas déjà active
    secret_quest_title = "Mot secret"
    quest_manager = game.player.quest_manager
    secret_quest = quest_manager.get_quest_by_title(secret_quest_title)
    if secret_quest.status == "not started":
        quest_manager.activate_quest(secret_quest_title)

    # Vérifier si toutes les lettres ont été trouvées
    all_letters = [l for l in books_letters.values() if l is not None]
    if set(game.player.found_letters) == set(all_letters):
        print("Toutes les lettres ont été enregistrées.")
        print("Veuillez trouver le mot secret.\n")






    