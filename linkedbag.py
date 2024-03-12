"""
Implement the LinkedBag for the BagInterface, using a Node internal data structure.

The BagInterface is provided as the contract: I tweaked it to make it abstract, helping
to enforce the implementation of the abstract methods.
"""

__author__ = "Bertrand Blanc (Alan Turing)"

import unittest
from node import Node
from baginterface import BagInterface


class LinkedBag(BagInterface):
    """Implement the LinkedBag for the BagInterface, using a Node internal data structure."""


    def __init__(self, source = None):
        self._head = None
        self._tail = None
        self._len  = 0

        if source:
            if isinstance(source, list):
                pass
            elif isinstance(source, LinkedBag):
                pass
            else:
                raise NotImplementedError(f'creating an ArrayBag from a {type(source).__name__} is not implemented')

            for v in source:
                self.add(v)
        

    # Accessor methods
    def __len__(self):
        """Returns the number of items in self."""
        return self._len

    def __str__(self):
        """Returns the string representation of self."""
        if self.isEmpty():
            return "[]"
        lst = []
        ptr = self._head
        while ptr:
            lst.append(ptr.data)
            ptr = ptr.next
        return "[" + ", ".join([str(x) for x in lst]) + "]"

    def __iter__(self):
        """Supports iteration over a view of self."""
        ptr = self._head
        while ptr:
            yield ptr.data
            ptr = ptr.next

    def __add__(self, other):
        """Returns a new bag containing the contents
        of self and other."""
        ll = LinkedBag(self)
        for v in other:
            ll.add(v)
        return ll


    def __eq__(self, other):
        """Returns True if self equals other,
        or False otherwise."""
        if len(self) != len(other):
            return False
        for x, y in zip(self, other):
            if x != y:
                return False
            return True

    def count(self, item):
        """Returns the number of instances of item in self."""
        cpt = 0
        ptr = self._head
        while ptr:
            cpt += 1 if ptr.data == item else 0
            ptr = ptr.next
        return cpt

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._head = None
        self._tail = None
        self._len  = 0

    def add(self, item):
        """Adds item to self."""
        if self._head:
            self._tail.next = Node(item)
            self._tail = self._tail.next
            self._len += 1
            return
        self._head = Node(item)
        self._tail = self._head
        self._len += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item in not in self.
        Postcondition: item is removed from self."""
        if item not in self:
            raise KeyError(f'{item} not in the list')
        
        # lst.remove removes only 1 instance of the item
        # I followed this behavior
        if self._head.data == item:
            self._head = self._head.next
            self._len -= 1
            return True
        
        ptr = self._head
        previous = None
        while ptr:
            if ptr.data != item:
                previous = ptr
                ptr = ptr.next
                continue
            previous.next = ptr.next
            self._len -= 1
            return True

        assert False, "reaching this location should be impossible"        
        return False 


class TestArrayBag(unittest.TestCase):
    def test_creation(self):
        lb = LinkedBag()
        self.assertEqual(lb._len, 0)
        self.assertIsNone(lb._head)
        self.assertIsNone(lb._tail)

    def test_creation_copy_list(self):
        lst = [x for x in range(5)]
        lb = LinkedBag(lst)
        self.assertEqual(lb._len, len(lst))

        self.assertTrue(isinstance(lb._head, Node))
        self.assertTrue(isinstance(lb._tail, Node))
        self.assertFalse(lb._tail is lb._head)
        self.assertEqual(lb._head.data, 0)
        for x in lst:
            self.assertTrue(x in lb)
 
    def test_creation_copy_bag(self):
        lst = [x for x in range(5)]
        lb1 = LinkedBag()
        for x in lst:
            lb1.add(x)
        lb2 = LinkedBag(lb1)
        self.assertEqual(lb2._len, len(lst))
        self.assertTrue(isinstance(lb2._head, Node))
        self.assertTrue(isinstance(lb2._tail, Node))
        self.assertFalse(lb2._tail is lb2._head)
        self.assertEqual(len(lb1), len(lb2))
        for x in lst:
            self.assertTrue(x in lb2)

    def test_creation_from_random(self):
        for x in [list(), LinkedBag()]:
            ab = LinkedBag(x)
            self.assertEqual(len(ab), 0)

        with self.assertRaises(NotImplementedError):
            d = {'a':1}
            ab = LinkedBag(d)

    def test_len(self):
        lst = [x for x in range(5)]
        lb = LinkedBag(lst)
        self.assertEqual(len(lb), len(lst))


    def test_str(self):
        lb = LinkedBag([x for x in range(5)])
        self.assertEqual(str(lb), "[0, 1, 2, 3, 4]")

        lb = LinkedBag()
        self.assertEqual(str(lb), "[]")


    def test_eq(self):
        lb1 = LinkedBag([x for x in range(5)])
        lb2 = LinkedBag()
        self.assertFalse(lb1 == lb2)
        for x in range(4):
            lb2.add(x)
            self.assertFalse(lb1 == lb2)
        lb2.add(4)
        self.assertTrue(lb1 == lb2)
        for x in range(2):
            lb2.add(x)
            self.assertFalse(lb1 == lb2)


    def test_count(self):
        lst = [x for x in range(5)]
        lb = LinkedBag(lst)
        for i in lst:
            self.assertEqual(lb.count(i), 1)
        lb.add(2)
        self.assertEqual(lb.count(2), 2)
        self.assertEqual(lb.count(23), 0)


    def test_clear(self):
        lb = LinkedBag([x for x in range(5)])
        self.assertEqual(len(lb), 5)
        lb.clear()
        self.assertEqual(len(lb), 0)
        self.assertIsNone(lb._head)
        self.assertIsNone(lb._tail)


    def test_is_empty(self):
        lb = LinkedBag()
        self.assertTrue(lb.isEmpty())
        lb.add(3)
        self.assertFalse(lb.isEmpty())
        lb.clear()
        self.assertTrue(lb.isEmpty())


    def test_add(self):
        lb = LinkedBag()
        self.assertTrue(lb.isEmpty())
        lb.add(3)
        self.assertFalse(lb.isEmpty())
        self.assertTrue(3 in lb)
        self.assertFalse(4 in lb)
        self.assertEqual(len(lb), 1)
        
        self.assertFalse(lb._head is None)
        self.assertFalse(lb._tail is None)
        self.assertTrue(lb._head is lb._tail)
        self.assertTrue(lb._tail.next is None)

        for x in range(10, 15):
            self.assertFalse(x in lb)

        for x in range(10, 15):
            lb.add(x)
            self.assertFalse(lb.isEmpty())
            self.assertFalse(lb._head is lb._tail)
            self.assertTrue(lb._tail.next is None)
            self.assertFalse(lb._head is None)

        for x in range(10, 15):
            self.assertTrue(x in lb)
        
        self.assertFalse(20 in lb)
        self.assertEqual(len(lb), 6)


    def test_remove(self):
        lst = [x for x in range(5)]
        lb = LinkedBag(lst)
        self.assertTrue(3 in lb)
        lb.remove(3)
        lst.remove(3)
        self.assertEqual(len(lb), len(lst))
        self.assertFalse(3 in lb)
        for v in lst:
            self.assertTrue(v in lb)

        with self.assertRaises(KeyError):
            lb.remove(34)

        self.assertTrue(lb.remove(2))


def main():
    ab = LinkedBag()
    print(len(ab), ab)
    ab.add(5)
    ab.add(4)
    print(len(ab), ab)
    ab.remove(4)
    print(len(ab), ab)
    ab.add(8)
    c = ab + ab + ab
    print(len(c), c)

    d = {'a':1, 'b':4}
    #ab = ArrayBag(d)
    #print(ab)


def exercise_flow():
    print('='*79)
    lb = LinkedBag([6,-1,8,5,85, -12])
    print("LinkedBag filled with [6,-1,8,5,85, -12].")
    print("Check if the LinkedBag is empty:", "it is empty" if lb.isEmpty() else "it's not empty")
    lb.remove(5)
    print("Number 5 removed from the LinkedBag.")
    print("Content of the ArrayBag: ", lb)
    lb.clear()
    print("LinkedBag has been emptied.")
    print("Check if the LinkedBag is empty:", "it is empty" if lb.isEmpty() else "it's not empty")
    print('='*79)


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
    exercise_flow()
    #main()
    exit(0)


"""
test_add (__main__.TestArrayBag.test_add) ... ok
test_clear (__main__.TestArrayBag.test_clear) ... ok
test_count (__main__.TestArrayBag.test_count) ... ok
test_creation (__main__.TestArrayBag.test_creation) ... ok
test_creation_copy_bag (__main__.TestArrayBag.test_creation_copy_bag) ... ok
test_creation_copy_list (__main__.TestArrayBag.test_creation_copy_list) ... ok
test_creation_from_random (__main__.TestArrayBag.test_creation_from_random) ... ok
test_eq (__main__.TestArrayBag.test_eq) ... ok
test_is_empty (__main__.TestArrayBag.test_is_empty) ... ok
test_len (__main__.TestArrayBag.test_len) ... ok
test_remove (__main__.TestArrayBag.test_remove) ... ok
test_str (__main__.TestArrayBag.test_str) ... ok

----------------------------------------------------------------------
Ran 12 tests in 0.003s

OK
===============================================================================
LinkedBag filled with [6,-1,8,5,85, -12].
Check if the LinkedBag is empty: it's not empty
Number 5 removed from the LinkedBag.
Content of the ArrayBag:  [6, -1, 8, 85, -12]
LinkedBag has been emptied.
Check if the LinkedBag is empty: it is empty
===============================================================================
"""
