<<<<<<< HEAD
class Quest:
    def __init__(self, title, description, objectives=None, reward=None):
        self.title = title
        self.description = description
        self.objectives = objectives or []
=======
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
>>>>>>> origin/main
        self.completed_objectives = []
        self.is_completed = False
        self.is_active = False
        self.reward = reward
<<<<<<< HEAD

    def activate(self):
        self.is_active = True
        print(f"\nNouvelle quête activée : {self.title}\n{self.description}\n")
=======
        
    def activate(self):
        self.is_active = True
        print(f"\nNouvelle quête activée: {self.title}")
        print(f"{self.description}\n")
>>>>>>> origin/main

    def complete_objective(self, objective, player=None):
        if objective in self.objectives and objective not in self.completed_objectives:
            self.completed_objectives.append(objective)
<<<<<<< HEAD
            print(f"Objectif accompli : {objective}")
=======
            print(f"Objectif accompli: {objective}")
>>>>>>> origin/main
            if len(self.completed_objectives) == len(self.objectives):
                self.complete_quest(player)
            return True
        return False

    def complete_quest(self, player=None):
        if not self.is_completed:
            self.is_completed = True
<<<<<<< HEAD
            print(f"\nQuête terminée : {self.title} !")
            if self.reward and player:
                player.add_reward(self.reward)

class QuestManager:
=======
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


class QuestManager:
    """
    This class manages all quests in the game.
    """
>>>>>>> origin/main
    def __init__(self, player=None):
        self.quests = []
        self.active_quests = []
        self.player = player

    def add_quest(self, quest):
        self.quests.append(quest)

<<<<<<< HEAD
    def activate_quest(self, title):
        for q in self.quests:
            if q.title == title and not q.is_active:
                q.activate()
                self.active_quests.append(q)
                return True
        return False

    def complete_objective(self, objective):
        for q in self.active_quests[:]:
            if q.complete_objective(objective):
                if q.is_completed:
                    self.active_quests.remove(q)
=======
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
>>>>>>> origin/main
                return True
        return False

    def check_action_objectives(self, action, target=None):
<<<<<<< HEAD
        for q in self.active_quests[:]:
            variations = [action]
            if target:
                variations += [f"{action} {target}", f"{action} sur {target}"]
            for var in variations:
                if q.complete_objective(var):
                    if q.is_completed:
                        self.active_quests.remove(q)
                    break
=======
        for quest in self.active_quests[:]:
            quest.check_action_objective(action, target, self.player)
            if quest.is_completed:
                self.active_quests.remove(quest)


# --- Création de la première quête ---
def create_first_quest():
    title = "Quête 1"
    description = (
        "Vous êtes dans le niveau bas du wagon de première classe.\n"
        "Madame Loisel a perdu sa parure.\n"
        "Objectif : utiliser la clé sur le coffre pour la retrouver."
    )
    objectives = [
        "utiliser clé sur coffre"
    ]
    reward = "Parure de Madame Loisel récupérée"

    return Quest(title, description, objectives, reward)
>>>>>>> origin/main
