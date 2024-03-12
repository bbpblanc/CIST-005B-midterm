
"""
Stakeholders patronizing the Diner. Their status as Student or Staff
has an impact on the design since the Taxes depends on that status.
"""

__author__ = "Bertrand Blanc (Alan Turing)"
__all__ = ["Student", "Staff"]

from abc import ABC

class Person(ABC):
    """Generic Person."""
    def __init__(self, tax_rate):
        self._tax_rate = tax_rate

    def compute(self, order):
        order.tax_rate = self._tax_rate
        order.compute()

class Student(Person):
    """Student with 0% tax rate"""
    def __init__(self):
        super().__init__(0.0)

class Staff(Person):
    """Staff member with 9% tax rate"""
    def __init__(self):
        super().__init__(0.09)

