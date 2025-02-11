#Creating a room class.
class Room:
#Properties of the room class:name, description, exits, items and npcs.
    def __init__(self, name, description, north=None, south=None, east=None, west=None):
        self.name = name
        self.description = description
        self.north = north
        self.south = south
        self.east = east
        self.west = west
        self.items = []
        self.npcs = []
         
#This method adds items to the room.        
    def add_item(self, item):
        self.items.append(item)
    
#This method removes items from the room.
    def remove_item(self, item):
        if item in self.items:
           self.items.remove(item)
           return item
        else:
            print(f"{item} is not in this room.")
            return None
            
#This gets the exits.
    def get_exits(self):
        return self.exits
    
    
#Adding exits to the rooms.
    def add_exits(self, direction, Room):
        self.exits[direction] = Room 
        
#Adding NPCs to the rooms.
    def add_npc(self, npc):
        self.npcs.append(npc)

#Creating an item class.
class Item:
    def __init__(self, name, description, can_be_taken=True, effect=None):
        self.name = name
        self.description = description
        self.can_be_taken = can_be_taken
        self.effect = effect

#Stating the items and their descriptions.
    def __str__(self):
        return f"{self.name}: {self.description}"
    
#Stating the effects or uses of the items.
    def use(self, player):
        print(f"Attempting to use {self.name}.")
        if self.effect:
            print(f"Effect is set for {self.name}.")
            self.effect(player)
            print(f"You used the {self.name}!")
        else:
            print(f"The {self.name} has no effect;it's practically useless.")
            
#Creating an effect of an item that nourishes players.
def nourishes_player(player):
    if player.strength < 100:
        player.strength += 30
        if player.strength > 100:
            player.strength = 100
        print("You feel stronger and better. Your strength is now, {player.strength}")
    else:
        print("You are already bursting with power!")

#Creating the effect of an itrem that defends players.
def defends_player(player):
    print("With the dagger in your hand, you can defend yourself. ")

#The effect of the map.
def use_map(player):
    if "Map" in [item.name for item in player.inventory]:
        print("You look at the map and discover a hidden room behind the shelves")
        player.current_room.south = hidden_room  
        print("You can now move south to the hidden room.")
    else:
        print("You need a map to find the hidden room.")


#The effect of an item.
def find_evidence(player):
    print("You read the letter and discover that the princess wasn't kidnapped but left the castle on her own, because of danger. The letter further states that there's a key that leads to a secret exit further south.")
    princess_key = Item("Princess's Key", "A key to the castle's secret exit.")
    player.add_to_inventory(princess_key)
    print("You have obtained the Princess's keyy")
    

#Creating an NPC class.
class NPC:
    def __init__(self, name, dialogue, item=None):
        self.name = name
        self.dialogue = dialogue  
        self.item = item  # Optional item the NPC may give
    
#Interaction with the players.
    def talk(self):
        print(f"{self.name} says: {self.dialogue}")
    
    def give_item(self, player):
        if self.item:
            print(f"{self.name} gives you {self.item.name}.")
            player.add_to_inventory(self.item)
        else:
            print(f"{self.name} has nothing to give.")


#Create NPCs.
guard = NPC("Guard", "Halt! You shall not pass without permission.")
inmate = NPC("Inmate", "I have items to trade, if you have the coin.")


#Create rooms.    
cell_entrance = Room("cell entrance", "You stand at the entrance of your dungeon.")
cafeteria = Room("Cafeteria", "A spacious, messy place where prisoners take their meals, there's spilled food on a table." )
gem_room = Room("Gem room", "A place that contains the palace's treasure, so shiny!")
guard_room = Room("Guard room", "A tiny brightly lit space. You see a guard fast asleep with a bowl of broth infront of him")
hidden_room = Room("Hidden room", "A secret room behind the shelves, containing evidence that proves your innocence!!")
secret_exit = Room("Secret Exit", "A hidden exit from the dungeon. You must have the Princess's Key to escape.")


#Listing all the rooms.
all_rooms = [cell_entrance, cafeteria, gem_room, guard_room, hidden_room]


#Adding effects of items.
food = Item("Food", "Consuming food restores your health and strength", effect=nourishes_player)
gold_dagger = Item("Gold dagger", "A beautiful but deadly dagger, can be used for self-defense.", effect=defends_player)
map = Item("Map", "A map showing the layout of the dungeon with some hidden areas marked", effect=use_map)
evidence = Item("Princess's letter", "A letter that proves the princess wasn't kidnapped but left the castle on her own, to avoid danger. The letter also states that there's a key in the hidden room that leads to an exit from the dungeon.", effect=find_evidence)


#Add items.
cafeteria.add_item(food)
cafeteria.add_item(Item("Cutleries and dishes", "Sharp utensils and dirty plates"))
gem_room.add_item(Item("Diamonds", "A sparkling diamond"))
gem_room.add_item(gold_dagger)
gem_room.add_item(map)
hidden_room.add_item(evidence)


#Add NPCs to rooms.
cell_entrance.add_npc(guard)
cafeteria.add_npc(inmate)


#Examining item.
def examine_item(self, player):
        if self.effect:
            self.effect(player)
            print("You picked up {self.name} to examine it!")

    


#Linking the rooms.
cell_entrance.north = cafeteria
cell_entrance.south = gem_room
cell_entrance.east = guard_room
cafeteria.south = cell_entrance
cafeteria.east = gem_room
cafeteria.north = guard_room
gem_room.north = cell_entrance
hidden_room.north = gem_room
hidden_room.south = secret_exit


#Map grid for testing.
map_grid = {
    "cell_entrance": {"north": "cafeteria", "south": "gem_room", "east": "guard_room"},
    "cafeteria": {"south": "cell_entrance", "east": "gem_room", "north": "guard_room"},
    "gem_room": {"north": "cell_entrance"},
    "hidden_room": {"north": "gem_room", "south": "secret_exit"}
}


#Creating a player class.
class Player:
    def __init__(self, name, current_room, inventory=None):
        self.name = name
        self.current_room = current_room #current room.
        self.rooms_visited = [current_room]  #Tracks visited rooms.
        self.inventory = inventory if inventory is not None else [] #Shows inventory.
        self.time_played = 0  #Time played.
        self.strength = 100   #Strength of the player.
        
    
#Adds to inventory.
    def add_to_inventory(self, item):
         self.inventory.append(item)
         print(f"{item.name} has been added to your inventory!")

    def take_item(self, item_name):
        for item in self.current_room.items:
            if item.name.lower() == item_name.lower():
                self.inventory.append(item)
                self.current_room.remove_item(item)
                print(f"You picked up {item.name}.")
                return
        print(f"{item_name} is not in this room.")



#Shows inventory.
    def show_inventory(self):
        """Display the player's inventory."""
        if self.inventory:
            print("Your Inventory:")
            for item in self.inventory:
                print(f"- {item.name}: {item.description}")
        else:
            print("Your inventory is empty. Get some items,oh brave one.")

#Win condition.
    def check_win(self):
        if "Princess's Key" in [item.name for item in self.inventory]:
            print("You have the key! You can now escape the dungeon!")
            quit()
        return False

    
#Lose condition.
    def check_lose(self):
        print(f"Checking if lost. Current room: {self.current_room.name}")
        if self.current_room.name == "Guard room":  
            print("You've been caught! You lose!")
            quit()
        

    
#Move method.
    def move(self, direction):
        next_room = getattr(self.current_room, direction, None)
        if next_room:
            print(f"Moving {direction} from {self.current_room.name} to {next_room.name}")
            if next_room == secret_exit and "Princess's Key" not in [item.name for item in self.inventory]:
                print("You cannot escape without the Princess's Key.")
            else:
                self.current_room = next_room
                if next_room.name not in [room.name for room in self.rooms_visited]:
                    self.rooms_visited.append(next_room)
                print(f"You moved {direction} to {self.current_room.name}.")
                
                
#Displays rooms visited.
                print("Rooms visited: ")
                for room in self.rooms_visited:
                    print(f"- {room.name}")
                
#Displays the map layout.
                print("\nMap of Rooms:")
                for room, directions in map_grid.items():
                    print(f"{room}: {', '.join(directions.keys())}")

    
        
            if self.check_lose():  #Checks lose condition after moving.
                print("Game over! Try again.")
                return
            # Ends the game if lose condition is met.
            
            if self.check_win():  #Checks win condition after moving.
                print("Congratulations, you've escaped the dungeon!")
                return  # Ends the game if win condition is met.
        else:
            print("You can't go that way.")
            
        
#Displays the current rooms,visited rooms.
    def display_map(self):
        print(f"Current room: {self.current_room.name}")
        print("Rooms visited: ")
        for room in self.visited_rooms:
            print(f"- {room}")

#Display the overall map layout.
        print("\nMap of Rooms:")
        for room, exits in map_grid.items():
            exit_directions = ', '.join(exits.keys())
            print(f"{room}: {exit_directions}")
        

#Welcoming the player.            
player_name = input("Enter your name! ")
player = Player(player_name, cell_entrance)  #Starting point.
#Prints a welcome message.
print(f"Greetings {player_name}, Welcome to Escape from the King's Dungeon!")
print("You've been wrongfully imprisoned for kidnapping the princess")
print("You have to escape soon as your sentence is Death by stoning!")
print(f"The game begins in {player.current_room.name}.")



#Importing JSON to save and load the game state such as progress and inventory.
import json

def save_game(player):
    game_state = {
        "current_room": player.current_room.name,
        "inventory": [item.name for item in player.inventory],
        }
    
    with open("game_save.json", "w") as save_file:
        json.dump(game_state, save_file)
    print("Game saved!")


def load_game(player, cell_entrance, cafeteria, gem_room, guard_room, hidden_room):
    try:
        with open("game_save.json", "r") as save_file:
            game_state = json.load(save_file)
            
        # Load player data
        current_room_name = game_state["current_room"]
        player.inventory.clear()  # Clear the inventory to avoid adding duplicate items
        for item_name in game_state["inventory"]:
            item = next((item for item in all_rooms if item.name == item_name), None)
            if item:
                player.inventory.append(item)
        
        # Set current room
        player.current_room = next(room for room in all_rooms if room.name == current_room_name)
        
        print(f"Game loaded! You are in {player.current_room.name}.")
    
    except FileNotFoundError:
        print("No saved game found.")



response = ""  #Initialise the response variable to an empty string.
while response != "quit":  #Keeps the game running until the player types quit.
    print(f"You are in {player.current_room.name}.") #Displays the player"s current room.
    response = input("What would you like to do?")  #Asks the player for their next action.
    if response in ["north", "south", "east", "west"]:

#Check if the player wants to move in any of the four directions.        
        player.move(response)  #Moves the player in the chosen direction.

#Checks if the player has won or lost after moving.        
        if player.check_win() or player.check_lose():
            break  #Ends the game if the player has won or lost.  
  
#If the player wants to save their game progress.
    elif response == "save":
        save_game(player)  #Saves the current game state.
    
#If the player wants to load a previously saved game.
    elif response == "load":  
        load_game(player, cell_entrance, cafeteria, gem_room, guard_room, hidden_room)  #Loads the saved game state.
        

#If the player wants to examine an item in the room.    
    elif response.startswith("examine"):
        success = False  #Checks if it was successful.
#Goes through all items in the current room.
        for item in player.current_room.items:
#If the player specified what item to examine.
            if response.endswith(item.name.lower()):
                print(f"You examine the {item.name}: {item.description}")  #Shows the items description.
             
#Special action if the item is Princess's letter.                
                if item.name == "Princess's Letter":
                    find_evidence(player)  #Activates the fnction after finding the letter.
                success = True  #Checks if it was successful.
                break  #Exits the loop.
            
#If the player wants to examine an item not in the room.
        if not success:
                print("There is no item like that here.")
            
#Taking an item from the current room.
    elif response.startswith("take "):
        success = False
        item_name = response[5:].strip().lower()
        for item in player.current_room.items:
            if item.name.lower() == item_name:
                player.current_room.remove_item(item)  #Removes the item from the room.
                player.add_to_inventory(item)  #Adds the item to the player's inventory.
                success = True  #Checks if it was successful.
                print(f"Picked up {item.name}.")  #Notifies the player if it was.
                break  #Exit the loop.
        else:
            print("Couln't carry out that action.")  #If the item wasn't in thr room.

#Interacting with an npc.
    elif response.startswith("talk"):
        npc_name = response[5:].strip().lower()  #Extract the NPC's name from the input.
        found_npc = None  #Store NPC.
#Go through all the NPCs to look for the required one.
        for npc in player.current_room.npcs:
            if npc.name.lower() == npc_name:
                found_npc = npc  #Set found NPC.
                break  #Exit the loop if the NPC is found.
#If npc is found,talk to the NPC.        
        if found_npc:
            found_npc.talk()  #The NPC should also talk back.
            found_npc.give_item(player)  #Give the item if available.
        else:
            print(f"There is no NPC named {npc_name} in this room.")

#Using an item from the inventory.
    elif response.startswith("use"):
        success = False
        for item in player.inventory:  #Checks if item is in the inventory.
            if response.endswith(item.name.lower()):
                item.use(player)  #Player uses the item.
                success = True  #Checks if it was successful.
                break  #Exit the loop if affirmative.
        if not success:
            print("You don't have that item in your inventory.")  #If the player lacks that item.

  
 #Displays the inventory.
    elif response == "inventory":
        if player.inventory:
            print("You are carrying:")  #Notifies the player of the items they currently possess.
            for item in player.inventory:
                print(f"- {item.name}")  #Prints the items name.
        else:
            print("Your inventory is empty.")  #The inventory has nothing. 

#Looks around the current room.    
    elif response == "look":
        print(player.current_room.description)  #Displays current room's description.
        if player.current_room.items:
            print("You see:")  #Notifies the player of the items in the room.
            for item in player.current_room.items:
                print(f"- {item.name}")  #Prints the items names.

#If the response is quit.
    elif response == "quit":
        print("Thanks for playing, adventurer!")
    else:
        print("Invalid command. Try 'north', 'take <item>', or 'look'.")
             
