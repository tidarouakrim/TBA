class Item:

    def __init__(self, name, description, weight):
        """
        Crée un nouvel objet.

        name: str, nom de l'objet
        description: str, description de l'objet
        weight: float ou int, poids de l'objet en kg
        """
        self.name = name
        self.description = description
        self.weight = weight
        self.letter = None  # Cette lettre va contenir la lettre majuscule trouvée

    def check_for_uppercase(self):
        for c in self.description:
            if c.isupper():
                return c
        return None

    def __str__(self):
        """
        Retourne une représentation de l'objet.
        Exemple : sword : une épée au fil tranchant comme un rasoir (2 kg)
        """
        return f"{self.name} : {self.description} ({self.weight} kg)"
    
class Beamer(Item):
    def __init__(self, name="beamer", description="Un appareil qui permet de mémoriser des lieux.", weight=1):
        super().__init__(name, description, weight)
        self.charged_room = None