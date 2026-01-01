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
            
    def read_book(self, book, player):
        letter = book.check_for_uppercase()

        if letter is None:
            print("Aucune lettre trouvée.\n")
            return
        if letter in self.secret_letters:
            print("Lettre déjà enregistrée.\n")
            return

        self.secret_letters.append(letter)
        print(f"Lettre {letter} enregistrée.\n")

        # Vérifie si toutes les lettres ont été trouvées
        total_letters_needed = 6
        if len(self.secret_letters) >= total_letters_needed:
            print("Toutes les lettres ont été enregistrées.")
            print("Veuillez trouver le mot secret.")
            player.waiting_for_secret_word = True  # <-- utilise player passé en argument






            
    
class QuestManager:
    """
    This class manages all quests in the game.
    """
    def __init__(self, player=None):
        self.quests = []
        self.active_quests = []
        self.player = player

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



