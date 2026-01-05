class Quest:
    def __init__(self, title, description, objectives=None, reward=None):
        self.title = title
        self.description = description
        self.objectives = objectives or []
        self.completed_objectives = []
        self.is_completed = False
        self.is_active = False
        self.reward = reward

    def activate(self):
        self.is_active = True
        print(f"\nNouvelle quête activée : {self.title}\n{self.description}\n")

    def complete_objective(self, objective, player=None):
        if objective in self.objectives and objective not in self.completed_objectives:
            self.completed_objectives.append(objective)
            print(f"Objectif accompli : {objective}")
            if len(self.completed_objectives) == len(self.objectives):
                self.complete_quest(player)
            return True
        return False

    def complete_quest(self, player=None):
        if not self.is_completed:
            self.is_completed = True
            print(f"\nQuête terminée : {self.title} !")
            if self.reward and player:
                player.add_reward(self.reward)

class QuestManager:
    def __init__(self, player=None):
        self.quests = []
        self.active_quests = []
        self.player = player

    def add_quest(self, quest):
        self.quests.append(quest)

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
                return True
        return False

    def check_action_objectives(self, action, target=None):
        for q in self.active_quests[:]:
            variations = [action]
            if target:
                variations += [f"{action} {target}", f"{action} sur {target}"]
            for var in variations:
                if q.complete_objective(var):
                    if q.is_completed:
                        self.active_quests.remove(q)
                    break