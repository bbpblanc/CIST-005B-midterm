"""
Core component of the system: the transactions initiated by the end-user are
kept in this data structure and can be dynamically modified via CRUD.
"""

__author__ = "Bertrand Blanc (Alan Turing)"
__all__ = ["Transaction", "Transactions"]

from linkedbag import LinkedBag
from menuitem import MenuItem


class Transaction():
    """Atomic element representing a transaction, basically a
    tuple(item from the menu, quantity, keyed identifier).
    The items in the menu are idnetified by reference.
    """
    def __init__(self,item,quantity,*,id=None):
        self.item = item
        self.quantity = quantity
        self.id = id

class Transactions():
    """A collection of transactions based on a LinkedBag which is part of the constraints.
    """
    def __init__(self):
        self._bag = LinkedBag()
        self._id = 1

    def __iter__(self):
        return iter(self._bag)
    
    def _inc(self):
        self._id += 1

    def add(self, transaction):
        """Add a transaction in the bag.
        If a transaction for the same item was previously done, the quantity is updated
        """
        for v in self._bag:
            if transaction.item is v.item:
                v.quantity += transaction.quantity
                return True
        self._bag.add(Transaction(transaction.item,transaction.quantity, id=self._id))
        self._inc()
        return True

    def delete(self, transaction):
        """Delete an item from the list of transactions"""
        for v in self._bag:
            if transaction.item is v.item:
                self._bag.remove(v)
                self.reset_IDs()
                return True
        return False
        
    def update(self, transaction):
        """Update an existing transaction with a new positive value.
        If the value is null, the item is removed.
        """
        assert transaction.quantity >= 0, "negative values shall be prohibited by construction"
        if transaction.quantity == 0:
            return self.delete(transaction)
        
        for v in self._bag:
            if transaction.item is v.item:
                v.quantity = transaction.quantity
                return True
        return False

    def __getitem__(self, item):
        """The bag is indexed based on 2 possible keys:
        . the ID of the transaction
        . the menu item of the transaction
        """
        if isinstance(item, MenuItem):
            for v in self._bag:
                if item is v.item:
                    return v
            raise KeyError(f'the item {item.name} has never been selected')
        
        if isinstance(item, int):
            for v in self._bag:
                if item == v.id:
                    return v
            raise KeyError(f'there is no #{item} item in the list of transactions')
        
        assert False, "unreachable"
        
    def __str__(self):
        if len(self._bag) > 0:
            column_name_size = max([len(transaction.item.name) for transaction in self._bag])+4
        else:
            column_name_size = 20

        buf = ""
        for transaction in self._bag:
            buf += f'{str(transaction.id):>3s} {transaction.item.name:>{column_name_size}s}: {transaction.item.price:.2f} x {transaction.quantity}\n'
        return buf
    
    def reset_IDs(self):
        """After manipulating the transactions, all IDs may not appear that palatable for the
        end-user. Reseting these IDs restarting at 1 helps geting cleaner keys for the
        end-user to reference.
        """
        self._id = 1
        for v in self._bag:
            v.id = self._id
            self._inc()
    
    def keys(self):
        """List of IDs for the transactions"""
        seq = []
        [seq.append(transaction.id) for transaction in self._bag]
        return seq

"""
test_iter (__main__.TestTransactions.test_iter) ... ok
test_keys (__main__.TestTransactions.test_keys) ... ok
test_reset_IDs (__main__.TestTransactions.test_reset_IDs) ... ok
test_str (__main__.TestTransactions.test_str) ... ok
test_transaction_creation (__main__.TestTransactions.test_transaction_creation) ... ok
test_transactions_add (__main__.TestTransactions.test_transactions_add) ... ok
test_transactions_creation (__main__.TestTransactions.test_transactions_creation) ... ok
test_update_null (__main__.TestTransactions.test_update_null) ... ok
test_update_positive (__main__.TestTransactions.test_update_positive) ... ok

----------------------------------------------------------------------
Ran 12 tests in 0.003s

OK
"""