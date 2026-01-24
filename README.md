# Orient Express – Projet TBA

**Jeu d'aventure textuel** inspiré de l'Orient Express  
**Auteurs** :** Tidar Ouakrim & Aminata Dabo
**Année** : 2025-2026

## Contexte général du projet

Le joueur arrive à la **gare de départ** de l’Orient Express et doit traverser un train luxueux pour arriver à sa **destination finale** (la locomotive).  
Le train est composé de plusieurs lieux successifs. Chaque lieu contient un défi à réussir.  
**En cas d'échec **, le train se détache et le joueur perd la partie (mécanique des 3 vies).

## L'univers du jeu

Le joueur traverse **7 lieux** dans cet ordre précis :

1. **Gare de départ**
2. **Première Classe**
3. **Restaurant**
4. **Lits** (labyrinthe)
5. **Bibliothèque**
6. **Espace Bagagiste**
7. **Bureau du Contrôleur** → **Locomotive** (fin)

## Description détaillée des lieux

### 1. Gare de départ
Le joueur commence ici, entouré de voyageurs élégants et de valises en cuir.  
Il monte dans le train vers la Première Classe.

### 2. Première Classe
Le joueur entre dans le niveau bas de première classe, luxueusement décoré avec des sièges en velours, des tables basses et des lampes dorées.  
**Objectif** : retrouver la parure de Madame Loisel, cachée dans un coffre verrouillé.

Objets présents :
- Un coffre fermé
- Un petit tapis
- Une lampe posée sur une table
- Un livre ouvert sur un siège
- **Une clé en cuivre** 
- Une petite note mystérieuse

**Indice** : Madame Loisel est présente et dit :
> "Quelque chose d’important se cache sous ce qui est doux et moelleux."

**Solution** : `use clé coffre`

### 3. Restaurant
Le joueur entre dans le restaurant somptueux du niveau haut, nappes blanches et lumières tamisées.  
**Défi** : identifier quel repas est empoisonné.

Le goûteur du train est chargé de vérifier la sécurité des plats.  
Trois plats sont servis :
1. Le ragoût de bœuf
2. La salade forestière
3. Le gratin de légumes

**Un seul est empoisonné.**  
Objets utiles autour :
- Fourchette, couteau, assiette vide
- Carafe d’eau
- Serviette
- Livre de recettes
- **Sel** (seul objet utile)

**Indice** : le sel réagit spécial au contact de certains champignons toxiques.  
En saupoudrant le sel sur les plats, un seul change légèrement de couleur.

**Solution** : `use sel [plat]` → identifier le poison → `give [plat sûr]` au goûteur.

### 4. Lits (labyrinthe)
Le joueur entre dans le niveau bas du wagon-lits. Les lits sont empilés de manière chaotique, formant un labyrinthe.  
**Objectif** : trouver la sortie pour avancer à l’épreuve suivante.

Le labyrinthe est moyennement compliqué avec :
- Une impasse
- Une petite boucle
- Indices subtils dans les descriptions (ronflements, matelas déchiré, odeur de vieux papier, lumière chaude…)

**Solution** : explorer en suivant les indices  (ex : odeur de vieux papier = direction bibliothèque).

### 5. Bibliothèque
Le joueur entre dans la bibliothèque calme et silencieuse du niveau haut.  
Rangées de livres anciens, petites lampes tamisées, un bibliothécaire supervise.

**Objectif** : trouver le mot secret en utilisant les lettres majuscules cachées dans certains titres de livres.

Quand le joueur touche un livre avec une majuscule dans le titre :
> "Lettre [X] enregistrée"

Quand toutes les lettres sont trouvées :
> "Toutes les lettres sont enregistrées. Veuillez former le mot secret."

**Indice du bibliothécaire** :
> "Vous remarquez qu’une lettre est plus prononcée ou inhabituelle dans certains titres."

**Solution** : `use livreX` → mot secret = "BRAVO" → `mot bravo`

### 6. Espace Bagagiste
Le joueur entre dans l’espace bagage rempli de valises, sacs et coffres.  
**Objectif** : restituer trois objets perdus à leurs propriétaires légitimes.

Objets à restituer :
- Montre → Paul
- Parapluie → Claire
- Lettre → Henri

**Indices subtils** via `talk` :
- Paul : "Je ne pars jamais sans vérifier l’heure..."
- Claire : "J’aime que mes affaires restent sèches."
- Henri : "Je n’oublie jamais mes messages, ils contiennent des secrets importants."

**Solution** : `give montre Paul`, `give parapluie Claire`, `give lettre Henri`

### 7. Bureau du Contrôleur → Locomotive (fin)
**Défi final** : le contrôleur interroge le joueur sur tout ce qu’il a fait dans les lieux précédents.

Questions :
- Où était la clé ?
- Quel plat était empoisonné ?
- Quel objet appartient à Claire ?
- Quel est le mot secret ?

**Solution** : répondre aux questions (commande adaptée selon votre implémentation).

En cas de réussite : arrivée à la locomotive → victoire !

## Mécaniques spéciales
- **3 vies** : en cas d’échec majeur (plat empoisonné, mauvais give, trop de mauvaises réponses, etc.) → perte d’une vie
- **0 vie** → défaite immédiate : "Le train s’est détaché... Vous n’arrivez pas à destination."
- **Victoire** : quand la quête 6 est réussie → "Toutes les quêtes validées ! Vous avez gagné !"

## Commandes principales (version actuelle)
- `help` → liste des commandes
- `quit` → quitter
- `go <direction>` (N/S/E/O/U/D)
- `look` → description + objets
- `take <objet>`
- `use <objet> <cible>` (ex : `use clé coffre`)
- `give <objet> <personnage>` (ex : `give montre Paul`)
- `talk <personnage>`
- `mot <mot_secret>`
- `quests` → liste des quêtes
- `quest <titre>` → détails d’une quête
- `activate <titre>` → activer une quête

Bon jeu et bon voyage dans l’Orient Express ! 
## Diagramme de Classes

```mermaid
classDiagram
    Game --> Player
    Game --> Room
    Game --> Command
    Player --> QuestManager
    Player --> Room
    Room --> Item
    Room --> Character
    QuestManager --> Quest
    Item --> Beamer
    
    class Game {
        bool finished
        list rooms
        dict commands
        Player player
        set direction
        int lives
        setup(player_name)
        play()
        process_command(command_string)
        win()
        loose()
    }
    
    class GameGUI {
        Game game
        int IMAGE_WIDTH
        int IMAGE_HEIGHT
        _build_layout()
        _update_room_image()
        _send_command(command)
    }
    
    class Player {
        str name
        Room current_room
        list history
        dict inventory
        float max_weight
        int move_count
        list found_letters
        int lives
        move(direction)
        back()
        get_history()
        get_inventory()
        current_weight()
    }
    
    class Room {
        str name
        str description
        str image
        dict exits
        dict inventory
        dict characters
        get_exit(direction)
        get_exit_string()
        get_long_description()
        get_inventory()
    }
    
    class Item {
        str name
        str description
        float weight
    }
    
    class Beamer {
        Room charged_room
    }
    
    class Character {
        str name
        str description
        Room current_room
        list msgs
        move()
        get_msg()
    }
    
    class Command {
        str command_word
        str help_string
        action
        int number_of_parameters
    }
    
    class Quest {
        str title
        str description
        list objectives
        list completed_objectives
        bool is_completed
        bool is_active
        str reward
        activate()
        complete_objective(objective, player)
        complete_quest(player)
        get_status()
    }
    
    class QuestManager {
        list quests
        list active_quests
        Player player
        add_quest(quest)
        activate_quest(title)
        complete_objective(objective)
        check_action_objectives(action, target)
    }