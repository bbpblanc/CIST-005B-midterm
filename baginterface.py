from abc import ABC, abstractmethod

class BagInterface(ABC):
    """Interface for all bag types."""

    # Constructor
    def __init__(self, sourceCollection = None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        pass

    # Accessor methods
    def isEmpty(self):
        """Returns True if len(self) == 0, or False otherwise."""
        return len(self) == 0
    
    @abstractmethod
    def __len__(self):
        """-Returns the number of items in self."""
        pass

    @abstractmethod
    def __str__(self):
        """Returns the string representation of self."""
        pass

    @abstractmethod
    def __iter__(self):
        """Supports iteration over a view of self."""
        pass

    @abstractmethod
    def __add__(self, other):
        """Returns a new bag containing the contents
        of self and other."""
        pass

    @abstractmethod
    def __eq__(self, other):
        """Returns True if self equals other,
        or False otherwise."""
        pass

    @abstractmethod
    def count(self, item):
        """Returns the number of instances of item in self."""
        pass

    # Mutator methods
    @abstractmethod
    def clear(self):
        """Makes self become empty."""
        pass

    @abstractmethod
    def add(self, item):
        """Adds item to self."""
        pass

    @abstractmethod
    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item in not in self.
        Postcondition: item is removed from self."""
        pass

