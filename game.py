# Description: Game class

DEBUG = True
from pathlib import Path
import sys

# Tkinter imports for GUI
import tkinter as tk
from tkinter import ttk, simpledialog
from room import Room
from player import Player
from command import Command
from actions import Actions
from item import Item
from character import Character
from item import Beamer
from quest import QuestManager, Quest
from item import Item, Beamer
from character import Character
from quest import Quest, QuestManager

class Game:
    
    # Constructor Import modules

    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
        self.direction=set()
        self.lives = 3  # Vies du joueur
    
        


    def setup(self, player_name=None):
        # Setup commands

        help = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["help"] = help
        quit = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["quit"] = quit
        go = Command("go", " <direction> : se déplacer dans une direction cardinale (N, E, S, O, U, D, U, D)", Actions.go, 1)
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
        talk = Command("talk", " <someone> : parler à quelqu'un", Actions.talk, 1)
        self.commands["talk"] = talk
        use = Command("use", " <item> [on <target>] : utiliser un objet, éventuellement sur une cible", Actions.use, -1)
        self.commands["use"] = use
        give = Command("give", " <item> to <someone> : donner un objet à quelqu'un", Actions.give, -1)
        self.commands["give"] = give
        mot_command = Command("mot", "<le_mot> : entrer le mot secret", Actions.check_secret_word, -1)
        self.commands["mot"] = mot_command
    

         # Setup rooms
        gare = Room("gare", " la gare de départ de l’Orient Express, entouré de voyageurs élégants et de valises en cuir.", image="gare.png")
        self.rooms.append(gare)
        piece1 = Room("piece1", " dans le niveau bas de première classe du premier wagon , luxueusement décoré, avec des sièges en velours, des tables basses et des lampes dorées.", image="piece1.png")
        self.rooms.append(piece1)
        restaurant= Room("restaurant", " le niveau haut du premier wagon, dans le restaurant somptueux, aux nappes blanches et lumières tamisées.", image="restaurant.png")
        self.rooms.append(restaurant)
        dortoir = Room("dortoir", " le niveau bas du deuxième wagon, dans le dortoir de luxe, où les somptueux lits forment un véritable labyrinthe.", image="dortoir.png")
        self.rooms.append(dortoir)
        bibliotheque = Room("bibliotheque", " le niveau haut du deuxième wagon dans la bibliothèque silencieuse, remplie de livres anciens.", image="bibliotheque.png")
        self.rooms.append(bibliotheque)
        espace_bagage = Room("espace_bagage", " le niveau bas du troisième wagon dans l'espace bagage, où valises et coffres s’entassent et quelques affaires traînent sur le sol.", image="espace_bagage.png")
        self.rooms.append(espace_bagage)
        bureau_du_maitre_du_Jeu = Room("bureau_du_Maitre_du_jeu", " le niveau haut du troisième wagon dans le bureau du Maitre du jeu , sombre et silencieux, où le contrôleur vous observe attentivement.", image="bureau_du_Maitre_du_jeu.png")
        self.rooms.append(bureau_du_maitre_du_Jeu)
        locomotive = Room("locomotive", " la locomotive! Félicitations vous arrivez à votre destination ! Bon voyage...", image="locomotive.png")
        self.rooms.append(locomotive)

                # Association des quetes aux pièces
        piece1.quest_title = "Quête 1"
        restaurant.quest_title = "Quête 2"
        dortoir.quest_title = "Quête 3"
        bibliotheque.quest_title = "Quête 4"
        espace_bagage.quest_title = "Quête 5"
        bureau_du_maitre_du_Jeu.quest_title = "Quête 6"        
        # Labyrinthe
        lits_entree = Room("lits_entree", "à l’entrée du niveau bas du deuxième wagon. Les lits sont empilés de manière chaotique, formant des passages étroits. Une faible lumière filtre depuis le sud.", image="lits_entree.png")
        self.rooms.append(lits_entree)
        lits_croisement = Room("lits_croisement", "au centre du labyrinthe. Vous êtes entouré de lits superposés formant un croisement. Des ronflements lointains résonnent dans l’obscurité.", image="lits_croisement.png")
        self.rooms.append(lits_croisement)
        lits_impasse = Room("lits_impasse", "dans une impasse étouffante. Un mur massif de lits bloque complètement le passage ouest. L’air est lourd et oppressant ; il faut revenir en arrière.", image="lits_impasse.png")
        self.rooms.append(lits_impasse)
        lits_boucle = Room("lits_boucle", "dans un passage qui semble tourner en rond. Vous reconnaissez un matelas déchiré que vous avez déjà vu… attention à ne pas boucler indéfiniment.", image="lits_boucle.png")
        self.rooms.append(lits_boucle)
        lits_vers_biblio = Room("lits_vers_biblio", "dans un passage qui monte légèrement. Une odeur familière de vieux papier et une lumière plus chaude proviennent du nord. C’est prometteur.", image="lits_vers_biblio.png")
        self.rooms.append(lits_vers_biblio)
        lits_sortie = Room("lits_sortie", "à la sortie du labyrinthe ! Vous apercevez une échelle menant vers le niveau supérieur. Vous avez réussi cette épreuve.", image="lits_sortie.png")
        self.rooms.append(lits_sortie)

       

        
        # === CONNEXIONS ===
        name_to_room = {r.name: r for r in self.rooms}
        r = name_to_room

         # Create exits for rooms
        gare.exits = {"N" : None, "E" : piece1, "S" : None, "O" : None,"U" : None, "D" : None}
        piece1.exits = {"N" :None , "E" : None, "S" : None, "O" : None, "U" : restaurant, "D" : None}
        restaurant.exits = {"N" : dortoir, "E" : None, "S" : None, "O" : None, "U" : None, "D" : piece1}
        dortoir.exits = {"N" : None, "E" : None, "S" : None, "O" : None, "U" : None , "D" : bibliotheque}
        bibliotheque.exits = {"N" : espace_bagage, "E" : None, "S" : None, "O" : None, "U" : None, "D" : dortoir }
        espace_bagage.exits = {"N" : None, "E" : None, "S" : None, "O" : None, "U" : bureau_du_maitre_du_Jeu, "D" : None}
        bureau_du_maitre_du_Jeu.exits = {"N" : locomotive, "E" : None, "S" : None, "O" : None, "U" : None, "D" : espace_bagage}
        locomotive.exits = {"N" : None, "E" : None, "S" : None, "O" : None,"U" : None, "D" : None}
        
        r["dortoir"].exits.update({"N": r["lits_croisement"], "S": r["restaurant"]})
        r["lits_croisement"].exits.update({"S": r["lits_entree"], "O": r["lits_impasse"], "E": r["lits_vers_biblio"], "N": r["lits_boucle"]})
        r["lits_impasse"].exits["E"] = r["lits_croisement"]
        r["lits_boucle"].exits["S"] = r["lits_croisement"]
        r["lits_vers_biblio"].exits.update({"O": r["lits_croisement"], "N": r["lits_sortie"]})
        r["lits_sortie"].exits.update({"S": r["lits_vers_biblio"], "U": r["bibliotheque"]})

        
        

        for room in self.rooms:
            self.direction.update(room.exits.keys())


        
        coffre = Item("coffre", "Un coffre ancien et verrouillé", 5)
        tapis = Item("tapis", "Un petit tapis fin et coloré", 1)
        lampe = Item("lampe", "Une lampe posée sur une table", 2)
        livre = Item("livre", "Un livre ouvert sur un siège", 1)
        clé = Item("clé", "Une clé ancienne et rouillée", 0.5)
        note = Item("note", "Une petite note mystérieuse", 0.05)
        MadameLoisel = Character("MadameLoisel", "Une femme élégante et mystérieuse.", piece1, ["Avez-vous vu mon collier perdu"])
            # Pas de clé au début
        

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
        Gouteur = Character("Gouteur", "Un personnage qui goûte les plats.", restaurant, ["Attention il ne faut pas m'empoisonner!"])

        # Ajouter des items à wagon_bibliothèque
        livre1 = Item("livre1", "spleen1", 1)
        livre2 = Item("livre2", "les misérAbles", 1)
        livre3 = Item("livre3", "madame boVary", 1)
        livre4 = Item("livre4", "le rouge et le nOir", 1)
        livre5 = Item("livre5", "l'omBre du vent", 1)
        livre6 = Item("livre6", "poweR", 1)
        beamer= Item("beamer", "Un appareil qui permet de mémoriser des lieux.", 1)
        Bibliothécaire = Character("Bibliothécaire", "Un personnage qui garde les livres.", bibliotheque, ["Chut! Ici c'est une bibliothèque."])
        
        # Ajouter des items à wagon_bagagiste
        montre = Item("montre", "descrip", 1)
        parapluie = Item("parapluie", "descrip", 1)
        lettre = Item("lettre", "descrip", 1)
        Paul = Character("Paul", "Voyageur", espace_bagage, ["Je ne pars jamais sans vérifier l’heure, surtout quand le train s’arrête."])
        Claire = Character("Claire", "Voyageuse", espace_bagage, ["J’aime que mes affaires restent sèches."])
        Henri = Character("Henri", "Voyageur", espace_bagage, ["Je n’oublie jamais mes messages, ils contiennent des secrets importants."])

        Controleur = Character("Contrôleur", "Le maître du jeu.", bureau_du_maitre_du_Jeu, ["La mémoire est quelque chose de très important dans ce train."])
        


        piece1.inventory[coffre.name] = coffre
        piece1.inventory[tapis.name] = tapis
        piece1.inventory[lampe.name] = lampe
        piece1.inventory[livre.name] = livre
        piece1.inventory[clé.name] = clé

        piece1.inventory[note.name] = note
        piece1.characters[MadameLoisel.name] = MadameLoisel

        restaurant.inventory[fourchette.name] = fourchette
        restaurant.inventory[couteau.name] = couteau
        restaurant.inventory[carafe.name] = carafe
        restaurant.inventory[serviette.name] = serviette
        restaurant.inventory[livre_recettes.name] = livre_recettes
        restaurant.inventory[sel.name] = sel
        restaurant.inventory[ragout.name] = ragout
        restaurant.inventory[salade.name] = salade
        restaurant.inventory[gratin.name] = gratin
        restaurant.characters[Gouteur.name] = Gouteur

        beamer = Beamer()
        bibliotheque.inventory[livre1.name] = livre1
        bibliotheque.inventory[livre2.name] = livre2
        bibliotheque.inventory[livre3.name] = livre3
        bibliotheque.inventory[livre4.name] = livre4
        bibliotheque.inventory[livre5.name] = livre5
        bibliotheque.inventory[livre6.name] = livre6
        bibliotheque.inventory[beamer.name] = beamer
        bibliotheque.characters[Bibliothécaire.name] = Bibliothécaire


        espace_bagage.inventory[montre.name] = montre
        espace_bagage.inventory[parapluie.name] = parapluie
        espace_bagage.inventory[lettre.name] = lettre
        espace_bagage.characters[Paul.name] = Paul
        espace_bagage.characters[Claire.name] = Claire
        espace_bagage.characters[Henri.name] = Henri

        bureau_du_maitre_du_Jeu.characters[Controleur.name] = Controleur

       

        # Renseigner toutes les directions utilisées 
        for room in self.rooms:
            self.direction.update(room.exits.keys())

        # Setup player and starting room
        if player_name and player_name.strip() != "":
            self.player = Player(player_name.strip())
        else:
            self.player = Player(input("\nEntrez votre nom: ").strip())


        self.player.current_room = gare 
        self._setup_quests()


        # Renseigner toutes les directions utilisées
        for room in self.rooms:
            self.direction.update(room.exits.keys())
            


    def _setup_quests(self):
        """Initialize all quests."""
        quete1 = Quest(
            title="Quête 1",
            description=(
                "Vous êtes dans le niveau bas du wagon de première classe.\n"
                "Madame Loisel a perdu sa parure.\n"
                "Objectif : utiliser la clé sur le coffre pour la retrouver."
            ),
            objectives=["utiliser clé sur coffre"],
            reward="Parure de Madame Loisel récupérée"
        )


        quete2 = Quest(
            title="Quête 2",
            description=(
                "Vous êtes dans le niveau haut du wagon, dans le restaurant.\n"
                "le repas est empoisonné.\n"
                "Objectif : trouver quel repas est empoisonné."
            ),
            objectives=["utiliser le sel"],
            reward="repas sain et sauf"
        )

        quete3 = Quest(
            title="Quête 3",
            description=(
                "Vous êtes dans le niveau bas du deuxieme wagon, dans le dortoir.\n"
            ),
            objectives=["Trouver la sortie du labyrinthe"],
            reward="Expert en sens de l'orientation"
        )

        quete4 = Quest(
            title="Quête 4",
            description="Vous êtes dans le niveau haut du deuxieme wagon, dans la bibliotheque.\n"
            "Trouver les lettres cachées dans les livres.",
            objectives=[
                "trouver les lettres",
                "trouver le mot secret"
            ],
            reward="Expert des livres"
      )

        quete5 = Quest(
            title="Quête 5",
            description=(
                "Vous êtes dans le niveau bas du troisième wagon, dans l'espace bagage.\n"
                "les affaires sont eparpillées.\n"
                "Objectif : trouver les affaires de chaque personnages."
            ),
            objectives=["utiliser les indices"],
            reward="Expert rangement "
        )

        quete6 = Quest(
            title="Quête 6",
            description=(
                "Vous êtes dans le niveau haut du troisième wagon, dans le bureau du maitre du jeu.\n"
                "Objectif : répondre correctement a toutes les questions."
            ),
            objectives=["utiliser votre mémoire ou le beamer"],
            reward="Arrive à destination"
        )

        

        # Add quests to player's quest manager
        self.player.quest_manager.add_quest(quete1)
        self.player.quest_manager.add_quest(quete2)
        self.player.quest_manager.add_quest(quete3)
        self.player.quest_manager.add_quest(quete4)
        self.player.quest_manager.add_quest(quete5)
        self.player.quest_manager.add_quest(quete6)
        


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
    # Remove leading/trailing spaces
        command_string = command_string.strip()

    # If the command is empty, do nothing
        if not command_string:
            return

    # Split the command string into a list of words
    # Split the command string into a list of words
        list_of_words = command_string.split(" ")

        command_word = list_of_words[0]

    # If the command is not recognized, print an error message
    # If the command is not recognized, print an error message
        if command_word not in self.commands.keys():
            print(f"\nCommande '{command_word}' non reconnue. Entrez 'help' pour voir la liste des commandes disponibles.\n")
    # If the command is recognized, execute it
    # If the command is recognized, execute it
        
        command = self.commands[command_word]
        command.action(self, list_of_words, command.number_of_parameters)
            # =========================
            # Tests de fin de partie (appelés à chaque tour)
            # =========================
        if self.win():
                print("🎉 Toutes les quêtes ont été validées ! Vous avez gagné !")
                self.finished = True

        elif self.loose():
                print("\n☠️ Vous avez perdu la partie. Game Over.Le wagon se détache, vous ne pouvvez pas arriver à destination!!!\n")
                self.finished = True




    # Print the welcome message
    def print_welcome(self):
        print(f"\nBienvenue {self.player.name} prenez place : votre aventure commence à bord de l’Orient Expres !")
        print("Entrez 'help' si vous avez besoin d'aide.")
        #
        print(self.player.current_room.get_long_description())

    
    def win(self):
    # Vérifie si la quête 6 du joueur est terminée
        if len(self.player.quest_manager.quests) >= 6:
            return self.player.quest_manager.quests[5].is_completed
        return False


    def check_win(self):
        if self.win():
            print("🎉 Toutes les quêtes ont été validées ! Vous avez gagné !")
            self.finished = True  # Termine automatiquement la boucle du jeu
            return True
        return False
    
    def loose(self):
        """
        MODIF : fonction de TEST de défaite (nom imposé par l’énoncé)
        Retourne True si les conditions de défaite sont remplies
        """
        if self.lives <= 0:
            return True

        return False


    def lose_life(self, message):
        """
        MODIF : action simple → perdre une vie
        """
        self.lives -= 1
        print(f"\n💀 {message}")
        print(f"❤️ Vies restantes : {self.lives}\n")

    
##############################
# Tkinter GUI Implementation #
##############################

class _StdoutRedirector:
    """Redirect sys.stdout writes into a Tkinter Text widget."""
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, msg):
        """Write message to the Text widget."""
        if msg:
            self.text_widget.configure(state="normal")
            self.text_widget.insert("end", msg)
            self.text_widget.see("end")
            self.text_widget.configure(state="disabled")

    def flush(self):
        """Flush method required by sys.stdout interface (no-op for Text widget)."""


class GameGUI(tk.Tk):
    """Tkinter GUI for the text-based adventure game.

    Layout layers:
    L3 (top): Split into left image area (600x400) and right buttons.
    L2 (middle): Scrolling terminal output.
    L1 (bottom): Command entry field.
    """

    IMAGE_WIDTH = 600
    IMAGE_HEIGHT = 400

    def __init__(self):
        super().__init__()
        self.title("TBA")
        self.geometry("900x700")  # Provide enough space
        self.minsize(900, 650)

        # Underlying game logic instance
        self.game = Game()

        # Ask player name via dialog (fallback to 'Joueur')
        name = simpledialog.askstring("Nom", "Entrez votre nom:", parent=self)
        if not name:
            name = "Joueur"
        self.game.setup(player_name=name)  # Pass name to avoid double prompt

        # Build UI layers
        self._build_layout()

        # Redirect stdout so game prints appear in terminal output area
        self.original_stdout = sys.stdout
        sys.stdout = _StdoutRedirector(self.text_output)

        # Print welcome text in GUI
        self.game.print_welcome()

        # Load initial room image
        self._update_room_image()

        # Handle window close
        self.protocol("WM_DELETE_WINDOW", self._on_close)


    # -------- Layout construction --------
    def _build_layout(self):
        # Configure root grid: 3 rows (L3, L2, L1)
        self.grid_rowconfigure(0, weight=0)  # Image/buttons fixed height
        self.grid_rowconfigure(1, weight=1)  # Terminal output expands
        self.grid_rowconfigure(2, weight=0)  # Entry fixed
        self.grid_columnconfigure(0, weight=1)

        # L3 Top frame
        top_frame = ttk.Frame(self)
        top_frame.grid(row=0, column=0, sticky="nsew", padx=6, pady=(6,3))
        top_frame.grid_columnconfigure(0, weight=0)
        top_frame.grid_columnconfigure(1, weight=1)

        # L3L Image area (left)
        image_frame = ttk.Frame(top_frame, width=self.IMAGE_WIDTH, height=self.IMAGE_HEIGHT)
        image_frame.grid(row=0, column=0, sticky="nw", padx=(0,6))
        image_frame.grid_propagate(False)  # Keep requested size
        self.canvas = tk.Canvas(image_frame,
                                width=self.IMAGE_WIDTH,
                                height=self.IMAGE_HEIGHT,
                                bg="#222")
        self.canvas.pack(fill="both", expand=True)

        # Initialize image reference (will be loaded by _update_room_image)
        self._image_ref = None  # Keep reference to prevent garbage collection
        # Initial image will be loaded after welcome message

        # L3R Buttons area (right)
        buttons_frame = ttk.Frame(top_frame)
        buttons_frame.grid(row=0, column=1, sticky="ne")
        for i in range(10):
            buttons_frame.grid_rowconfigure(i, weight=0)
        buttons_frame.grid_columnconfigure(0, weight=1)

        # Load button images (keep references to prevent garbage collection)
        assets_dir = Path(__file__).parent / 'assets'
        # Load pre-resized 50x50 PNG images for better quality
        self._btn_help = tk.PhotoImage(file=str(assets_dir / 'help-50.png'))
        self._btn_up = tk.PhotoImage(file=str(assets_dir / 'up-arrow-50.png'))
        self._btn_down = tk.PhotoImage(file=str(assets_dir / 'down-arrow-50.png'))
        self._btn_left = tk.PhotoImage(file=str(assets_dir / 'left-arrow-50.png'))
        self._btn_right = tk.PhotoImage(file=str(assets_dir / 'right-arrow-50.png'))
        self._btn_quit = tk.PhotoImage(file=str(assets_dir / 'quit-50.png'))

        # Command buttons
        tk.Button(buttons_frame,
                  image=self._btn_help,
                  command=lambda: self._send_command("help"),
                  bd=0).grid(row=0, column=0, sticky="ew", pady=2)
        # Movement buttons (N,E,S,O)
        move_frame = ttk.LabelFrame(buttons_frame, text="Déplacements")
        move_frame.grid(row=1, column=0, sticky="ew", pady=4)
        tk.Button(move_frame,
                  image=self._btn_up,
                  command=lambda: self._send_command("go N"),
                  bd=0).grid(row=0, column=0, columnspan=2)
        tk.Button(move_frame,
                  image=self._btn_left,
                  command=lambda: self._send_command("go O"),
                  bd=0).grid(row=1, column=0)
        tk.Button(move_frame,
                  image=self._btn_right,
                  command=lambda: self._send_command("go E"),
                  bd=0).grid(row=1, column=1)
        tk.Button(move_frame,
                  image=self._btn_down,
                  command=lambda: self._send_command("go S"),
                  bd=0).grid(row=2, column=0, columnspan=2)

        # Quit button
        tk.Button(buttons_frame,
                  image=self._btn_quit,
                  command=lambda: self._send_command("quit"),
                  bd=0).grid(row=2, column=0, sticky="ew", pady=(8,2))

        # L2 Terminal output area (Text + Scrollbar)
        output_frame = ttk.Frame(self)
        output_frame.grid(row=1, column=0, sticky="nsew", padx=6, pady=3)
        output_frame.grid_rowconfigure(0, weight=1)
        output_frame.grid_columnconfigure(0, weight=1)

        scrollbar = ttk.Scrollbar(output_frame, orient="vertical")
        self.text_output = tk.Text(output_frame,
                                   wrap="word",
                                   yscrollcommand=scrollbar.set,
                                   state="disabled",
                                   bg="#111", fg="#eee")
        scrollbar.config(command=self.text_output.yview)
        self.text_output.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # L1 Entry area
        entry_frame = ttk.Frame(self)
        entry_frame.grid(row=2, column=0, sticky="ew", padx=6, pady=(3,6))
        entry_frame.grid_columnconfigure(0, weight=1)

        self.entry_var = tk.StringVar()
        self.entry = ttk.Entry(entry_frame, textvariable=self.entry_var)
        self.entry.grid(row=0, column=0, sticky="ew")
        self.entry.bind("<Return>", self._on_enter)
        self.entry.focus_set()


    # -------- Image update --------
    def _update_room_image(self):
        """Update the canvas image based on the current room."""
        if not self.game.player or not self.game.player.current_room:
            return

        room = self.game.player.current_room
        assets_dir = Path(__file__).parent / 'assets'

        # Use room-specific image if available, otherwise fallback
        if room.image:
            image_path = assets_dir / room.image
        else:
            image_path = assets_dir / 'scene.png'

        try:
            # Load new image
            self._image_ref = tk.PhotoImage(file=str(image_path))
            # Clear canvas and redraw image
            self.canvas.delete("all")
            self.canvas.create_image(
                self.IMAGE_WIDTH/2,
                self.IMAGE_HEIGHT/2,
                image=self._image_ref
            )
        except (FileNotFoundError, tk.TclError):
            # Fallback to text if image not found or cannot be loaded
            self.canvas.delete("all")
            self.canvas.create_text(
                self.IMAGE_WIDTH/2,
                self.IMAGE_HEIGHT/2,
                text=f"Image: {room.name}",
                fill="white",
                font=("Helvetica", 18)
            )


    # -------- Event handlers --------
    def _on_enter(self, _event=None):
        """Handle Enter key press in the entry field."""
        value = self.entry_var.get().strip()
        if value:
            self._send_command(value)
        self.entry_var.set("")


    def _send_command(self, command):
        if self.game.finished:
            return
        # Echo the command in output area
        print(f"> {command}\n")
        self.game.process_command(command)
        # Update room image after command (in case player moved)
        self._update_room_image()
        if self.game.finished:
            # Disable further input and schedule close (brief delay to show farewell)
            self.entry.configure(state="disabled")
            self.after(600, self._on_close)


    def _on_close(self):
        # Restore stdout and destroy window
        sys.stdout = self.original_stdout
        self.destroy()


def main():
    """Entry point.

    If '--cli' is passed as an argument, start the classic console version.
    Otherwise launch the Tkinter GUI.
    Fallback to CLI if GUI cannot be initialized (e.g., headless environment).
    """
    args = sys.argv[1:]
    if '--cli' in args:
        Game().play()
        return
    try:
        app = GameGUI()
        app.mainloop()
    except tk.TclError as e:
        # Fallback to CLI if GUI fails (e.g., no DISPLAY, Tkinter not available)
        print(f"GUI indisponible ({e}). Passage en mode console.")
        Game().play()
    

if __name__ == "__main__":
    main()
