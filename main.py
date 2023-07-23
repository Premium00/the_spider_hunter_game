import copy
import random
from config import spawn_player, level_steps, mark_player, mark_enemy, spawn_enemy, mark_win_area
from graphics import game_start_art, game_dead_art, game_win_art 
from serializer import ElementSaveManagerMixin
is_game_on = True
win_state = False

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

    def get_introduce(self):
        pass

class Character(PhysicalObject):
    def __init__(self, name, location, hp):
        super().__init__(name, location)
        self.hp = hp

    
    def move(self, direction, map):
        if direction=="s":
            if not self.location[1] >= len(map.full_map)-1: 
                self.location[1] += 1
        elif direction=="w":
            if not self.location[1] <= 0: 
                self.location[1] -= 1
        elif direction=="a":
            if not self.location[0] <= 0: 
                self.location[0] -= 1
        elif direction=="d":
            if not self.location[0] >= len(map.full_map[0])-1: 
                self.location[0] += 1


class Player(Character, ElementSaveManagerMixin):
    def __init__(self, name, location, hp=100, exp=0, moves=0, is_winner=False, level=1, **kwargs):
        super().__init__(name, location, hp)
        self.exp = exp
        self.moves = moves
        self.is_winner = is_winner
        self.level = level
        for key, value in kwargs.items():
            setattr(self, key, value)
    
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
    
    def count_moves(self):
        self.moves += 1
    
    def set_winner(self):
        self.is_winner = True
    
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
        self.map_state[self.win_area[1]][self.win_area[0]] = mark_win_area
        for map_row in self.map_state:
            row_to_print = ""
            for map_field in map_row:
                row_to_print += map_field
            print(row_to_print)

    def create_win_area(self):
        win_area_x = random.randint(1,len(self.full_map)-1)
        win_area_y = random.randint(1,len(self.full_map[0])-1)
        self.win_area =  [win_area_x, win_area_y]

    def is_player_win(self, character):
        if self.win_area[0] == character.location[0] and self.win_area[1] == character.location[1]:
            return True
        else:
            return False
        


#TODO in the future, create a "Game" class to handle the gameplay and interface
print(game_start_art)
print("")
print("Lista top graczy:")
for row in Player.get_loaded_elements_atr("name", "moves"):
    print(row)
print("")
print("Witaj w grze, stwórz swojego bohatera")
name = input("Podaj imię bohatera: ")
is_name_exist = Player.check_if_element_exist(name)
while is_name_exist:
    name = input(f"Gracz o nazwie {name} już istnieje. Podaj inne imię bohatera: ")
    is_name_exist = Player.check_if_element_exist(name)
player_01 = Player(name=name, location=spawn_player, hp=50)
map_01 = Map()
map_01.create_win_area()
spider_01 = Enemy(name="Spider", location=spawn_enemy, hp=10)
map_01.display_map(player_01, spider_01)
print(player_01.get_introduce())

while is_game_on == True and win_state == False:
    player_input = input("Podaj kierunek ruchu: ")
    player_01.move(player_input, map_01)
    player_01.count_moves()
    spider_01.move_follow(player_01)
    is_game_on = spider_01.is_catch(player_01)
    win_state = map_01.is_player_win(player_01)
    print(player_01.get_introduce())
    map_01.display_map(player_01, spider_01)
    print(f"P{player_01.location} E{spider_01.location} win{map_01.win_area}")
if win_state:
    player_01.set_winner()
    player_01.save_element()
    print(game_win_art)
else:
    print(game_dead_art)

print(f"Gratulacje {player_01.name}, udało ci się ukończyć grę w {player_01.moves} ruchach!")
#print(f"P{player_01.location} M{player_01.moves} E{spider_01.location} win{map_01.win_area}")



