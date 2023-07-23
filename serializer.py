import json
import os


class Serializer:
    def serialize(self):
        pass
    
    @classmethod
    def deserialize(self, data):
        pass

    def file_type(self):
        raise NotImplementedError()


class JsonMixin(Serializer):
    def serialize(self):
        return json.dumps(self.__dict__)
    
    @classmethod
    def deserialize(cls, file):
        return json.load(file)
    
    @classmethod
    def file_type(cls):
        return "json"


class ElementSaveManagerMixin(JsonMixin):
    def save_element(self):
        folder_path = f"/home/stalkowski/projekty/projekty-git/OOP_spider_hunter/the_spider_hunter_game/elements/{self.__class__.__name__.lower()}"
        file_name = f"{self.name}.{self.file_type()}"
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, mode="w") as element_file:
            element_file.write(self.serialize())

    @classmethod
    def load_element(cls):
        loaded_objects_list = []
        folder_path = f"/home/stalkowski/projekty/projekty-git/OOP_spider_hunter/the_spider_hunter_game/elements/{cls.__name__.lower()}"
        file_list = os.listdir(folder_path)
        for element_f in file_list:
            path_to_element = os.path.join(folder_path, element_f)
            with open(path_to_element, 'r') as file:
                object_loaded = cls.deserialize(file)
                loaded_objects_list.append(cls(**object_loaded))
        return loaded_objects_list
    
    @classmethod
    def get_loaded_elements_atr(cls, *args):
        loaded_objects_list = cls.load_element()
        sorted_list = sorted(loaded_objects_list, key=lambda obj: obj.moves)
        row_list = []
        counter = 0
        for obj in sorted_list:
            counter += 1
            row = f"{counter}. "
            for argument in args:
                row += f'{argument} : {getattr(obj, argument)}  |  '
            row_list.append(row)
        return row_list

    @classmethod
    def check_if_element_exist(cls, name):
        folder_path = f"/home/stalkowski/projekty/projekty-git/OOP_spider_hunter/the_spider_hunter_game/elements/{cls.__name__.lower()}"
        file_name = f"{name}.{cls.file_type()}"
        for root, dirs, files in os.walk(folder_path):
            if file_name in files:
                return True
        else:
            return False
