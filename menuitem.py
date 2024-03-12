"""
Atomic objects representing each item on the menu
"""


__author__ = "Bertrand Blanc (Alan Turing)"
__all__ = ["Burger", "ItemDisplay", "Beverage"]

from abc import ABC


class MenuItem(ABC):
    """Abstract class for the menu items defined as a tuple(name,price) """
    def __init__(self, name, price):
        self._name = name
        self._price= price

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name
    
    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, price):
        self._price = price

    def __str__(self):
        return f'({self.name},{self.price})'
    

class ItemDisplay():
    """Decorator to display a menu item in a more fancy way."""
    def __init__(self,item,column_size=20,precision=2):
        self.item = item
        self.float_precision = precision
        self.column_size = column_size

    def __str__(self):
        return f'{self.item.name:>{self.column_size}s}: ${self.item.price:.0{self.float_precision}f}'
    
class Burger(MenuItem):
    """That's a burger on the menu"""
    pass

class Beverage(MenuItem):
    """That's a beverage on the menu"""
    pass