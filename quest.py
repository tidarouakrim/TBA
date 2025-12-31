from item import Item
""" Define the Quest class"""

class Quest:
    """
    This class represents a quest in the game. A quest has a title, description,
    objectives, completion status, and optional rewards.
    """
    def __init__(self, title, description, objectives=None, reward=None):
        self.title = title
        self.description = description
        self.objectives = objectives if objectives is not None else []
        self.completed_objectives = []
        self.is_completed = False
        self.is_active = False
        self.reward = reward
        self.secret_word = ""
        self.secret_letters = []
        
    def activate(self):
        self.is_active = True
        print(f"\nNouvelle quête activée: {self.title}")
        print(f"{self.description}\n")

    def complete_objective(self, objective, player=None):
        if objective in self.objectives and objective not in self.completed_objectives:
            self.completed_objectives.append(objective)
            print(f"Objectif accompli: {objective}")
            if len(self.completed_objectives) == len(self.objectives):
                self.complete_quest(player)
            return True
        return False

    def complete_quest(self, player=None):
        if not self.is_completed:
            self.is_completed = True
            print(f"\nQuête terminée: {self.title}")
            if self.reward:
                print(f"Récompense: {self.reward}")
                if player:
                    player.add_reward(self.reward)
            print()

    def get_status(self):
        if not self.is_active:
            return f"{self.title} (Non activée)"
        if self.is_completed:
            return f"{self.title} (Terminée)"
        completed_count = len(self.completed_objectives)
        total_count = len(self.objectives)
        return f"{self.title} ({completed_count}/{total_count} objectifs)"

    def check_action_objective(self, action, target=None, player=None):
        if target:
            objective_variations = [
                f"{action} {target}",
                f"{action} avec {target}",
                f"{action} le {target}",
                f"{action} la {target}"
            ]
        else:
            objective_variations = [action]

        for objective in objective_variations:
            if self.complete_objective(objective, player):
                return True
            
            
    def find_letters_in_books(self, player):
        """Cherche les lettres majuscules dans les livres et forme le mot secret"""
        for item_name, item in player.current_room.inventory.items():
            letter = item.check_for_uppercase()
            if letter and letter not in self.secret_letters:
                self.secret_letters.append(letter)
                print(f"Lettre {letter} enregistrée")

        if len(self.secret_letters) == len(self.objectives):
            print("Toutes les lettres ont été enregistrées. Veuillez former le mot final.")
            self.complete_objective("Trouver le mot secret")
            print("Mot secret collecté: " + "".join(self.secret_letters))

    
    def check_final_word(self, guessed_word):
        """Vérifie si le mot secret proposé est correct"""
        if ''.join(self.secret_letters) == guessed_word:
            print("Félicitations, vous avez trouvé le mot secret!")
            return True
        else:
            print("Ce n'est pas le bon mot secret. Essayez encore.")
            return False



class QuestManager:
    """
    This class manages all quests in the game.
    """
    def __init__(self, player=None):
        self.quests = []
        self.active_quests = []
        self.player = player
        self.secret_word = ""

    def add_quest(self, quest):
        self.quests.append(quest)

    def activate_quest(self, quest_title):
        for quest in self.quests:
            if quest.title == quest_title and not quest.is_active:
                quest.activate()
                self.active_quests.append(quest)
                return True
        return False

    def complete_objective(self, objective_text):
        for quest in self.active_quests:
            if quest.complete_objective(objective_text):
                if quest.is_completed:
                    self.active_quests.remove(quest)
                return True
        return False

    def check_action_objectives(self, action, target=None):
        for quest in self.active_quests[:]:
            quest.check_action_objective(action, target, self.player)
            if quest.is_completed:
                self.active_quests.remove(quest)


    def find_letters_in_books(self, player):
        """Cherche les lettres majuscules dans tous les livres et forme le mot secret"""
        for item_name, item in player.current_room.inventory.items():
                letter = item.check_for_uppercase()  # Vérifie si une majuscule est présente
                if letter:
                    print(f"Lettre {letter} enregistrée.")
                    self.secret_word += letter  # Ajout de la lettre au mot secret

        # Une fois que toutes les lettres sont enregistrées, afficher le message
        if len(self.secret_word) == 5:  # Par exemple, 5 lettres doivent être collectées
            print("Toutes les lettres ont été enregistrées. Veuillez former le mot final.")
            self.complete_objective("Trouver le mot secret")

    def check_final_word(self, guessed_word):
        """Vérifie si le mot secret proposé est correct"""
        if guessed_word.lower() == "BRAVO":
            print("✅ Félicitations ! Vous avez trouvé le mot secret !")
            return True
        else:
            print("❌ Le mot secret est incorrect. Essayez à nouveau.")
            return False
        
    def guess_word(game, args, num_params):
        """Permet au joueur de deviner le mot secret."""
        if len(args) != 2:
            print("❌ Syntaxe incorrecte : utilisez 'guess <mot>'")
            return False

        guessed_word = args[1].upper()
        game.player.quest_manager.check_final_word(guessed_word)
        return True

