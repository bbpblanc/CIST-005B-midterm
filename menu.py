
"""
That class represents a menu, the first interface between the system
and an eventual database. The retrieval of data from an hypothetical
database is emulated via a JSON file stored in the current folder.

A dump functionality allows the system to dump its menu in a JSON file,
leaving the doors open to future enhancements like CRUD on the menu itself. 
"""


__author__ = "Bertrand Blanc (Alan Turing)"

from linkedbag import LinkedBag
from menuitem import *
import json


class Menu():
    """The menu is composed of burgers. That class loads the burger from an ad-hoc JSON file"""
    def __init__(self, *, auto_load=False):
        self._bag = LinkedBag()
        if auto_load:
            # Emulating the dynamic retrieval of the data from the diner's database
            self.load("./burger.json.txt")

    @property
    def bag(self):
        """Access to the collection of menu items"""
        return self._bag
    
    def __len__(self):
        return len(self._bag)

    def load(self, file):
        """Load the burgers from a JSON file into the menu data structure"""
        try:
            with open(file, "r") as fd:
                data = json.loads(fd.read())
        except FileNotFoundError as e:
            print(f'file {file} not accessible. Make sure the file is located in the current folder to emulate the retrieval from a DB')
            exit(-1)
        except json.JSONDecodeError as e:
            print(f'file {file} has been corrupted. Make sure the file is properly JSON-formated to emulate the data integrity from a REST API call')
            exit(-1)

        for record in data["burgers"]:
            self._bag.add(Burger(record['name'], record['price']))

    
    def dump(self, file):
        """Export the menu data structure into a JSON file"""
        data = []
        for v in self._bag:
            data.append({'name':v.name, 'price':v.price})
        data = {"burgers": data}
        try:
            with open(file, "w") as fd:
                fd.write(json.dumps(data))
        except Exception as e:
            print(f'unexpected exception. Make sure {file} is in a writable directory to emulate the update of a DB')
            raise e
    
    def __str__(self):
        line = '='*40 
        buf = line + '\n'
        buf += '='*17 + ' MENU ' + '='*17 + '\n'
        buf += line + '\n'
        for record in self.bag:
            item_to_display = ItemDisplay(record)
            buf += str(item_to_display) + "\n"
        buf += line
        return buf




if __name__ == "__main__":
    # The JSON file is expected to come from a well-maintained DataBase
    # no expectation to have the JSON file filled with garbage
    menu = Menu()
    try:
        menu.load("./burger.json.txt")
    except Exception as e:
        print(e)
        print('shutdown...')
        exit(-1)

    print(menu)
    menu.dump('menu.json')

