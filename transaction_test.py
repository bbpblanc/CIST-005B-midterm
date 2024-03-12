
"""Test the classes Transaction and Transactions"""
__author__ = "Bertrand Blanc"

from transaction import *
from linkedbag import LinkedBag
from menu4order import MenuDecoratorForOrder
from menu import Menu
import unittest

class TestTransactions(unittest.TestCase):
    menu = MenuDecoratorForOrder(Menu(auto_load=True))

    def test_transaction_creation(self):
        l = [3,4]
        t = Transaction(l,3)
        self.assertIs(t.item, l)
        self.assertEqual(t.quantity,3)
        self.assertIsNone(t.id)
        l[1]=3
        self.assertIs(t.item, l)
        self.assertEqual(t.item[1],3)

        with self.assertRaises(TypeError):
            t = Transaction(l,3,2)

        t = Transaction(l,3,id=2)
        self.assertEqual(t.id,2)

        

    def test_transactions_creation(self):
        ts = Transactions()
        self.assertIsInstance(ts._bag,LinkedBag)
        self.assertEqual(ts._id,1)

        ts._inc()
        self.assertEqual(ts._id,2)

    def test_transactions_add(self):
        ts = Transactions()

        with self.assertRaises(IndexError):
            t = Transaction(self.menu[0],0)

        t = Transaction(self.menu[1],3)
        ts.add(t)
        self.assertEqual(ts._id,2)
        self.assertEqual(len(ts._bag),1)
        self.assertEqual(ts._bag._head.data.quantity,3)
        ts.add(t)
        self.assertEqual(ts._id,2)
        self.assertEqual(len(ts._bag),1)
        self.assertEqual(ts._bag._head.data.quantity,6)

    def test_delete(self):
        ts = Transactions()
        t1 = Transaction(self.menu[1],3)
        t2 = Transaction(self.menu[2],5)
        t3 = Transaction(self.menu[3],7)
        ts.add(t1)
        ts.add(t2)
        self.assertFalse(ts.delete(t3))

        self.assertEqual(len(ts._bag),2)
        self.assertTrue(ts.delete(t1))
        self.assertEqual(len(ts._bag),1)
        self.assertFalse(ts.delete(t1))

    def test_getitem_by_id(self):
        ts = Transactions()
        t1 = Transaction(self.menu[1],3)
        t2 = Transaction(self.menu[2],5)
        t3 = Transaction(self.menu[3],7)
        id_t1 = ts._id
        ts.add(t1)
        id_t2 = ts._id
        ts.add(t2)

        self.assertEqual(ts[id_t1].item,t1.item)
        self.assertEqual(ts[id_t1].quantity,t1.quantity)
        self.assertEqual(ts[id_t2].item,t2.item)
        self.assertEqual(ts[id_t2].quantity,t2.quantity)
        with self.assertRaises(KeyError):
            ts[14]

        
    def test_getitem_by_menuitem(self):
        ts = Transactions()
        t1 = Transaction(self.menu[1],3)
        t2 = Transaction(self.menu[2],5)
        t3 = Transaction(self.menu[3],7)
        ts.add(t1)
        ts.add(t2)

        self.assertIs(ts[t1.item].item,t1.item)
        self.assertEqual(ts[t1.item].quantity,t1.quantity)
        self.assertIs(ts[t2.item].item,t2.item)
        self.assertEqual(ts[t2.item].quantity,t2.quantity)
        with self.assertRaises(KeyError):
            ts[t3.item]

    def test_update_positive(self):
        ts = Transactions()
        t1 = Transaction(self.menu[1],3)
        t2 = Transaction(self.menu[2],5)
        ts.add(t1)
        ts.add(t2)

        t3 = Transaction(self.menu[1],7)
        ts.update(t3)
        self.assertEqual(ts[t3.item].quantity,7)
        t3 = Transaction(self.menu[1],11)
        ts.update(t3)
        self.assertEqual(ts[t3.item].quantity,11)
        self.assertEqual(ts[t2.item].quantity,5)

    def test_update_null(self):
        ts = Transactions()
        t1 = Transaction(self.menu[1],3)
        t2 = Transaction(self.menu[2],5)
        ts.add(t1)
        ts.add(t2)

        t3 = Transaction(self.menu[1],0)
        self.assertEqual(ts[t3.item].quantity,3)
        self.assertEqual(len(ts._bag),2)
        ts.update(t3)
        with self.assertRaises(KeyError):
            ts[t3.item]
        self.assertEqual(len(ts._bag),1)
        

    def test_delete(self):
        ts = Transactions()
        t1 = Transaction(self.menu[1],3)
        t2 = Transaction(self.menu[2],5)
        t3 = Transaction(self.menu[1],0)
        ts.add(t1)

        self.assertFalse(ts._bag.isEmpty())
        self.assertTrue(ts.delete(t3))
        self.assertTrue(ts._bag.isEmpty())
        self.assertFalse(ts.delete(t2))

    def test_str(self):
        ts = Transactions()
        t1 = Transaction(self.menu[1],3)
        ts.add(t1)
        self.assertRegex(str(ts), r'\s*\d+\s*[\s|\w]+:\s*\d*.\d{2}\s++x\s+\d+')

    def test_reset_IDs(self):
        ts = Transactions()
        t1 = Transaction(self.menu[1],3)
        t2 = Transaction(self.menu[2],5)
        t3 = Transaction(self.menu[3],5)
        ts.add(t1)
        ts.add(t2)
        ts.add(t3)
        ids = []
        for v in ts:
            ids.append(v.id)
        self.assertEqual(ids,[1,2,3])

        ts.delete(t1)
        ts.add(t1)
        ids = [v.id for v in ts]
        self.assertEqual(ids,[1,2,3])
        self.assertEqual(ts._id,4)

        ts.reset_IDs()
        ids = [v.id for v in ts]
        self.assertEqual(ids,[1,2,3])
        self.assertEqual(ts._id,4)


    def test_iter(self):
        ts = Transactions()
        t1 = Transaction(self.menu[1],3)
        t2 = Transaction(self.menu[2],5)
        t3 = Transaction(self.menu[3],5)
        ts.add(t1)
        ts.add(t2)
        ts.add(t3)
        reference = [t1,t2,t3]
        transactions = []
        [transactions.append(v) for v in ts]
        transactions.sort(key=lambda x:x.id)
        for i,t in enumerate(reference):
            self.assertIs(t.item,reference[i].item)
            self.assertEqual(t.quantity, reference[i].quantity)

    def test_keys(self):
        ts = Transactions()
        t1 = Transaction(self.menu[1],3)
        t2 = Transaction(self.menu[2],5)
        t3 = Transaction(self.menu[3],5)
        ts.add(t1)
        ts.add(t2)
        ts.add(t3)
        self.assertEqual(ts.keys(),[1,2,3])

        ts.delete(t1)
        ts.add(t1)
        self.assertEqual(ts.keys(),[1,2,3])



if __name__ == "__main__":
    unittest.main(argv=['ignore'], exit=False, verbosity=2)
