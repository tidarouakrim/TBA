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

    def __str__(self):
        """
        Retourne une représentation de l'objet.
        Exemple : sword : une épée au fil tranchant comme un rasoir (2 kg)
        """
        return f"{self.name} : {self.description} ({self.weight} kg)"