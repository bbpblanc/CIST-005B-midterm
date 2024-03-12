
"""
Attempt to implement a Decorator Design Pattern "by the book".
A mere Menu was not enough, an extension was needed, especially
to add a key to the menu items to be referenced by the end-users.
"""

__author__ = "Bertrand Blanc (Alan Turing)"
__all__ = ["MenuDecoratorForOrder"]

from menu import Menu
from menuitem import ItemDisplay
from linkedbag import LinkedBag


class MenuDecoratorForOrder(Menu):
    def __init__(self, menu):
        self._menu = menu
        # this DP does encapsulate a Menu
        # while extending the Menu super class
        # Then adds its custom layer
        self._keyed_bag = LinkedBag()
        if not menu.bag.isEmpty():
            for i,item in enumerate(menu.bag,1):
                self._keyed_bag.add((i,item))
        

    @property
    def bag(self):
        return self._keyed_bag
    
    def __len__(self):
        return len(self._keyed_bag)

    def load(self, file):
        """load override"""
        # Override by forwarding the method to the object
        # it wraps, then adding its custom layer if needed
        self._menu.load(file)
        for i,item in enumerate(menu.bag,1):
            self._keyed_bag.add((i,item))

    def __getitem__(self, idx):
        found = False
        item = None
        for v in self._keyed_bag:
            if v[0] == idx:
                found = True
                item = v[1]
                break
        if not found:
            raise IndexError(f'index {idx} not found')
        return item


    def dump(self, file):
        """export override"""
        self._menu.dump(file)

    def __str__(self):
        if len(self.bag) > 0:
            column_size = max([len(item.name) for _,item in self.bag])+4
        else:
            column_size = 20
        
        line_size = column_size + 20

        line = '='*line_size
        buf = line + '\n'
        buf += f'{" MENU ":=^{line_size}}' '\n'
        buf += line + '\n'

        for record in self.bag:
            buf += format(str(record[0]), "2>")
            item_to_display = ItemDisplay(record[1], column_size=column_size)
            buf += str(item_to_display) + "\n"
        buf += line
        return buf
    