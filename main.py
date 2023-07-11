import copy
from config import spawn_player, level_steps, mark_player, mark_enemy, spawn_enemy
from graphics import game_start_art, game_end_art

is_game_on = True

class ShootBehavior:
    def shoot(self, directory):
        pass

class CatchBehavior:
    def is_catch(self, character):
        if self.location[0] == character.location[0] and self.location[1] == character.location[1]:
            return False
        else:
            return True


class MoveFollowBehavior:
    def move_follow(self, object_to_follow):
        if self.location[0] > object_to_follow.location[0]:
            self.location[0] -= 1
            return
        if self.location[0] < object_to_follow.location[0]:
            self.location[0] += 1
            return
        if self.location[1] > object_to_follow.location[1]:
            self.location[1] -= 1
            return
        if self.location[1] < object_to_follow.location[1]:
            self.location[1] += 1
            return
        
class PhysicalObject:
    def __init__(self, name, location):
        self.name = name
        self.location = location
    
    @property
    def get_location():
        pass


class Character(PhysicalObject):
    def __init__(self, name, location, hp):
        super().__init__(name, location)
        self.hp = hp

    
    def move(self, direction):
        if direction=="s":
            self.location[1] += 1
        elif direction=="w":
            self.location[1] -= 1
        elif direction=="a":
            self.location[0] -= 1
        elif direction=="d":
            self.location[0] += 1


class Player(Character):
    def __init__(self, name, location, hp=100, exp=0):
        super().__init__(name, location, hp)
        self.exp = exp
    
    @property
    def get_level(self):
        level = 1
        for level_step in level_steps:
            if self.exp < level_step:
                self.level = level
                return self.level
            level += 1
    
    @property
    def get_when_text_level(self):
        return level_steps[(self.get_level - 1)]
    
    def get_introduce(self):
        return f"""
{self.name} {self.get_level}lv | {self.exp}/{self.get_when_text_level}exp
{self.hp}hp
        """    


class Enemy(Character, MoveFollowBehavior, CatchBehavior):
    def __init__(self, name, location, hp):
        super().__init__(name, location, hp)


class Map:
    def __init__(self, x=10, y=10):
        full_map = []
        for y_field in range(y):
            y_field = []
            for x_field in range(x):
                y_field.append("* ")
            full_map.append(y_field)
        self.full_map = full_map
        
        
    def display_map(self, character, enemy):
        self.map_state = copy.deepcopy(self.full_map)
        self.map_state[character.location[1]][character.location[0]] = mark_player
        self.map_state[enemy.location[1]][enemy.location[0]] = mark_enemy


        for map_row in self.map_state:
            row_to_print = ""
            for map_field in map_row:
                row_to_print += map_field
            print(row_to_print)

    




print(game_start_art)
print("")
print("Witaj w grze, stwórz swojego bohatera")
name = input("Podaj imię bohatera: ")
player_01 = Player(name=name, location=spawn_player, hp=50)
map_01 = Map()
spider_01 = Enemy(name="Spider", location=spawn_enemy, hp=10)
map_01.display_map(player_01, spider_01)
print(player_01.get_introduce())


while is_game_on == True:

   # player_input = input("1 aby iść, 2 aby strzelać: ")
   # if player_input == "1":
    player_input = input("Podaj kierunek ruchu: ")
    player_01.move(player_input)
    # elif player_input == "2":
        #player_input = input("Podaj kierunek strzału: ")
        #player_01.shoot(player_input)

    
    spider_01.move_follow(player_01)
    is_game_on = spider_01.is_catch(player_01)
    print(player_01.get_introduce())
    map_01.display_map(player_01, spider_01)
    print(f"P{player_01.location} E{spider_01.location}")
print(game_end_art)
print(f"P{player_01.location} E{spider_01.location}")



