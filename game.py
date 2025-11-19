# Description: Game class

#
from room import Room
from player import Player
from command import Command
from actions import Actions

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
        
        # Setup rooms
        gare = Room("Gare", " une gare élégante où l’Orient Express attend, luxueux et mystérieux, prêt à traverser l’Europe.")
        self.rooms.append(gare)
        wagon_1_classe = Room("wagon_1_classe", " le wagon de première classe, luxueusement décoré, avec des sièges en velours, des tables basses et des lampes dorées.")
        self.rooms.append(wagon_1_classe)
        wagon_restaurant= Room("wagon_restaurant", " le wagon restaurant somptueux, aux nappes blanches et lumières tamisées.")
        self.rooms.append(wagon_restaurant)
        wagon_lits = Room("wagon_lits", " le wagon lit de luxe, où les somptueux lits forment un véritable labyrinthe.")
        self.rooms.append(wagon_lits)
        wagon_bibliotheque = Room("wagon_bibliothèque", " le wagon bibliothèque silencieux, rempli de livres anciens.")
        self.rooms.append(wagon_bibliotheque)
        wagon_bagagiste = Room("wagon_bagagiste", " le wagon bagages, où valises et coffres s’entassent et quelques affaires traînent sur le sol.")
        self.rooms.append(wagon_bagagiste)
        wagon_memoire = Room("wagon_memoire", " Vous êtes dans le Wagon Mémoire, sombre et silencieux, où le contrôleur vous observe attentivement.")
        self.rooms.append(wagon_memoire)
        locomotive = Room("locomotive", " Félicitations vous arrivez à votre destination ! Bon voyage...")
        self.rooms.append(locomotive)
        # Create exits for rooms
        gare.exits = {"N" : None, "E" : wagon_1_classe, "S" : None, "O" : None,"U" : None, "D" : None}
        wagon_1_classe.exits = {"N" :None , "E" : None, "S" : None, "O" : None, "U" : wagon_restaurant, "D" : None}
        wagon_restaurant.exits = {"N" : wagon_lits, "E" : None, "S" : None, "O" : None, "U" : None, "D" : wagon_1_classe}
        wagon_lits.exits = {"N" : None, "E" : None, "S" : None, "O" : None, "U" : None , "D" : wagon_bibliotheque}
        wagon_bibliotheque.exits = {"N" : wagon_bagagiste, "E" : None, "S" : None, "O" : None, "U" : None, "D" : wagon_lits}
        wagon_bagagiste.exits = {"N" : None, "E" : None, "S" : None, "O" : None, "U" : wagon_memoire, "D" : None}
        wagon_memoire.exits = {"N" : locomotive, "E" : None, "S" : None, "O" : None, "U" : None, "D" : wagon_bagagiste}
        locomotive.exits = {"N" : None, "E" : None, "S" : None, "O" : None,"U" : None, "D" : None}
        
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
