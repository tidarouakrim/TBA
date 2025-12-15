# Description: Game class

#
from room import Room
from player import Player
from command import Command
from actions import Actions
from item import Item
from item import Beamer

class Game:

    # Constructor Import modules

    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
        self.direction=set()
    
    # Setup the game
    def setup(self):

        # Setup commands

        help = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["help"] = help
        quit = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["quit"] = quit
        go = Command("go", " <direction> : se déplacer dans une direction cardinale (N, E, S, O, U, D)", Actions.go, 1)
        self.commands["go"] = go
        history = Command("history", " : afficher l'historique des pièces visitées", Actions.history, 0)
        self.commands["history"] = history
        back = Command("back", " : retourner en arrière", Actions.back, 0)
        self.commands["back"] = back
        look = Command("look", " : observer la pièce actuelle", Actions.look, 0)
        self.commands["look"] = look
        take = Command("take", " <item> : prendre un objet", Actions.take, 1)
        self.commands["take"] = take
        drop = Command("drop", " <item> : deposer un objet", Actions.drop, 1)
        self.commands["drop"] = drop
        check = Command("check", " <item> : vérifier son inventaire", Actions.check, 1)
        self.commands["check"] = check
        beamer_charge = Command("beamer_charge", " : charger le beamer", Actions.beamer_charge, 0)
        self.commands["beamer_charge"] = beamer_charge
        beamer_teleportation = Command("beamer_teleportation", " : utiliser le beamer pour retourner à l'endroit chargé", Actions.beamer_teleportation, 0)
        self.commands["beamer_teleportation"] = beamer_teleportation
        
        # Setup rooms
        gare = Room("gare", " la gare de départ de l’Orient Express, entouré de voyageurs élégants et de valises en cuir.")
        self.rooms.append(gare)
        piece1 = Room("piece1", " dans le niveau bas de première classe du premier wagon , luxueusement décoré, avec des sièges en velours, des tables basses et des lampes dorées.")
        self.rooms.append(piece1)
        restaurant= Room("restaurant", " le niveau haut du premier wagon, dans le restaurant somptueux, aux nappes blanches et lumières tamisées.")
        self.rooms.append(restaurant)
        dortoir = Room("dortoir", " le niveau bas du deuxième wagon, dans le dortoir de luxe, où les somptueux lits forment un véritable labyrinthe.")
        self.rooms.append(dortoir)
        bibliotheque = Room("bibliothèque", " le niveau haut du deuxième wagon dans la bibliothèque silencieuse, remplie de livres anciens.")
        self.rooms.append(bibliotheque)
        espace_bagage = Room("espace_bagage", " le niveau bas du troisième wagon dans l'espace bagage, où valises et coffres s’entassent et quelques affaires traînent sur le sol.")
        self.rooms.append(espace_bagage)
        bureau_du_maitre_du_Jeu = Room("bureau_du_Maitre_du_jeu", " le niveau haut du troisième wagon dans le bureau du Maitre du jeu , sombre et silencieux, où le contrôleur vous observe attentivement.")
        self.rooms.append(bureau_du_maitre_du_Jeu)
        locomotive = Room("locomotive", " la locomotive! Félicitations vous arrivez à votre destination ! Bon voyage...")
        self.rooms.append(locomotive)
        # Create exits for rooms
        gare.exits = {"N" : None, "E" : piece1, "S" : None, "O" : None,"U" : None, "D" : None}
        piece1.exits = {"N" :None , "E" : None, "S" : None, "O" : None, "U" : restaurant, "D" : None}
        restaurant.exits = {"N" : dortoir, "E" : None, "S" : None, "O" : None, "U" : None, "D" : piece1}
        dortoir.exits = {"N" : None, "E" : None, "S" : None, "O" : None, "U" : None , "D" : bibliotheque}
        bibliotheque.exits = {"N" : espace_bagage, "E" : None, "S" : None, "O" : None, "U" : None, "D" : dortoir }
        espace_bagage.exits = {"N" : None, "E" : None, "S" : None, "O" : None, "U" : bureau_du_maitre_du_Jeu, "D" : None}
        bureau_du_maitre_du_Jeu.exits = {"N" : locomotive, "E" : None, "S" : None, "O" : None, "U" : None, "D" : espace_bagage}
        locomotive.exits = {"N" : None, "E" : None, "S" : None, "O" : None,"U" : None, "D" : None}
        
        # Ajouter des items à wagon_1_classe
        coffre = Item("coffre", "Un coffre ancien et verrouillé", 5)
        tapis = Item("tapis", "Un tapis fin et coloré", 1)
        lampe = Item("lampe", "Une lampe posée sur une table", 2)
        livre = Item("livre", "Un livre ouvert sur un siège", 1)
        cle = Item("clé", "Une clé cachée sous un coussin", 0.1)
        note = Item("note", "Une petite note mystérieuse", 0.05)
    
        # Ajouter des items à wagon_restaurant
        ragout= Item("ragoût", "Un ragoût de bœuf fumant et appétissant", 1.2)
        salade = Item("salade", "Une salade fraîche aux champignons et herbes", 0.5)
        gratin = Item("gratin", "Un gratin doré de légumes variés", 0.8)
        fourchette = Item("fourchette", "Une fourchette en argent pour déguster le repas", 0.1)
        couteau = Item("couteau", "Un petit couteau de table", 0.2)
        carafe = Item("carafe", "Une carafe remplie d’eau fraîche", 1.0)
        serviette = Item("serviette", "Une serviette en tissu blanc", 0.1)
        livre_recettes = Item("livre", "Un livre détaillant diverses recettes", 0.7)
        sel = Item("sel", "Un sel de table", 0.2)  # objet crucial
      

        # Ajouter des items à wagon_bibliothèque
        livre1 = Item("livre1", "titre", 1)
        livre2 = Item("livre2", "titre", 1)
        livre3 = Item("livre3", "titre", 1)
        livre4 = Item("livre4", "titre", 1)
        livre5 = Item("livre5", "titre", 1)
        livre6 = Item("livre6", "titre", 1)
        
        # Ajouter des items à wagon_bagagiste
        montre = Item("montre", "descrip", 1)
        parapluie = Item("parapluie", "descrip", 1)
        lettre = Item("lettre", "descrip", 1)
        


        piece1.inventory[coffre.name] = coffre
        piece1.inventory[tapis.name] = tapis
        piece1.inventory[lampe.name] = lampe
        piece1.inventory[livre.name] = livre
        piece1.inventory[cle.name] = cle
        piece1.inventory[note.name] = note

        restaurant.inventory[fourchette.name] = fourchette
        restaurant.inventory[couteau.name] = couteau
        restaurant.inventory[carafe.name] = carafe
        restaurant.inventory[serviette.name] = serviette
        restaurant.inventory[livre_recettes.name] = livre_recettes
        restaurant.inventory[sel.name] = sel
        restaurant.inventory[ragout.name] = ragout
        restaurant.inventory[salade.name] = salade
        restaurant.inventory[gratin.name] = gratin

        beamer = Beamer()
        bibliotheque.inventory[livre1.name] = livre1
        bibliotheque.inventory[livre2.name] = livre2
        bibliotheque.inventory[livre3.name] = livre3
        bibliotheque.inventory[livre4.name] = livre4
        bibliotheque.inventory[livre5.name] = livre5
        bibliotheque.inventory[livre6.name] = livre6
        bibliotheque.inventory[beamer.name] = beamer


        espace_bagage.inventory[montre.name] = montre
        espace_bagage.inventory[parapluie.name] = parapluie
        espace_bagage.inventory[lettre.name] = lettre

        # Renseigner toutes les directions utilisées 
        for room in self.rooms:
            self.direction.update(room.exits.keys())

        # Setup player and starting room

        self.player = Player(input("\nEntrez votre nom: "))
        self.player.current_room = gare

    # Play the game
    def play(self):
        self.setup()
        self.print_welcome()
        # Loop until the game is finished
        while not self.finished:
            # Get the command from the player
            self.process_command(input("> "))
        return None

    # Process the command entered by the player
    def process_command(self, command_string) -> None:
        # Remove leading/trailing spaces
        command_string = command_string.strip()

        # If the command is empty, do nothing
        if not command_string:
            return
    
        # Split the command string into a list of words
        list_of_words = command_string.split(" ")

        command_word = list_of_words[0]

        # If the command is not recognized, print an error message
        if command_word not in self.commands.keys():
            print(f"\nCommande '{command_word}' non reconnue. Entrez 'help' pour voir la liste des commandes disponibles.\n")
        # If the command is recognized, execute it
        else:
            command = self.commands[command_word]
            command.action(self, list_of_words, command.number_of_parameters)

    # Print the welcome message
    def print_welcome(self):
        print(f"\nBienvenue {self.player.name} prenez place : votre aventure commence à bord de l’Orient Expres !")
        print("Entrez 'help' si vous avez besoin d'aide.")
        #
        print(self.player.current_room.get_long_description())
    

def main():
    # Create a game object and play the game
    Game().play()
    

if __name__ == "__main__":
    main()
