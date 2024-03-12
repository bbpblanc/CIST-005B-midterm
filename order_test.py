""" Test the package order """

__author__ = "Bertrand Blanc (Alan Turing)"


from order import *
from transaction import *
from menu4order import *
from menu import Menu
import unittest
from unittest.mock import patch, call

import sys
import os
import re

class TestOrder(unittest.TestCase):
    
    def test_order_creation(self):
        order = Order()

        self.assertEqual(len(order.transactions.keys()), 0)
        with self.assertRaises(IllegalChoice):
            order.transactions = Transactions()

        self.assertNotEqual(len(order.menu),0)
        with self.assertRaises(IllegalChoice):
            order.menu = MenuDecoratorForOrder(Menu(auto_load=True))

        self.assertNotEqual(len(order._commands),0)
        self.assertEqual(len(order._commands),6)
        for v in order._commands:
            self.assertTrue(v[1] in Order.commands)
            self.assertRegex(str(v[0]), r'\d+')


        self.assertAlmostEqual(order.pre_tax,0.0)
        with self.assertRaises(IllegalChoice):
            order.pre_tax = 2.0

        self.assertAlmostEqual(order.tax_rate,0.0)
        order.tax_rate = 2.33
        self.assertAlmostEqual(order.tax_rate,2.33)

        self.assertAlmostEqual(order.post_tax,0.0)
        with self.assertRaises(IllegalChoice):
            order.post_tax = 2.0

        self.assertAlmostEqual(order.taxes,0.0)
        with self.assertRaises(IllegalChoice):
            order.taxes = 2.0

        self.assertRegex(str(order.id), r'\d+')
        with self.assertRaises(IllegalChoice):
            order.id = 2.0


    @patch('builtins.input', create=True)
    def test_menu_and_commands(self, mocked_input):
        test_file = "_test_commands.txt"
        order = Order()
        mocked_input.side_effect = ["", "11"]
        """
        empty: display the menu again
        11: quit
        """

        with open(test_file, "w") as fd:
            sys.stdout = fd
            try:
                order.fill()
            except OrderTermination:
                pass

        with open(test_file, "r") as fd:
            data = fd.read()
            attempts = len(re.findall('MENU', data))
            self.assertEqual(attempts,2)
            self.assertRegex(data, '6\s+-\s+update')
            self.assertRegex(data, '7\s+-\s+delete')
            self.assertRegex(data, '8\s+-\s+display the menu')
            self.assertRegex(data, '9\s+-\s+display the order')
            self.assertRegex(data, '10\s+-\s+finalize the order and pay')
            self.assertRegex(data, '11\s+-\s+quit')

            burgers = [{'id': idx, 'name': order.menu[idx].name, 'price': round(order.menu[idx].price,2)} for idx in range(1,len(order.menu)+1)]
            for burger in burgers:
                self.assertRegex(data, '{id}\s+{name}:\s+\$\s*{price}'.format(**burger))

            self.assertRegex(data, 'Thank you for your visit. See you soon!!')

        os.remove(test_file)


    @patch('builtins.print')
    @patch('builtins.input', create=True)
    def test_trial_mocked_IOs(self, mocked_input, mocked_print):
        # learned how to manipulate IOs in unittest instead of
        # redirecting system stdin/stdout manually
        # Note: that's not a __docstring__, hence won't end-up in documentation
        seq = ["12", "10", "-2", "4"]
        mocked_input.side_effect = seq
        for v in mocked_input.side_effect:
            print(v)
        self.assertEqual(mocked_print.mock_calls, [call(v) for v in seq])


    @patch('builtins.input', create=True)
    def test_add_burger(self, mocked_input):
        test_file = "_test_add.txt"
        order = Order()
        mocked_input.side_effect = ["0", "2", "3", "1", "10", "9", "11"]
        """
        0: wrong choice
        2: select burger #2
        3: 3 burgers #2
        1: select burget #1
        10: add 10 burgers #1
        9: display the order
        11: quit
        """
        # add 3 Bacon Cheese burgers and 10 de Anza Burger
        burger1 = {'name': order.menu[2].name, 'price': str(round(order.menu[2].price,2)), 'quantity': str(3)}
        burger2 = {'name': order.menu[1].name, 'price': str(round(order.menu[1].price,2)), 'quantity': str(10)}
        burger3 = {'name': order.menu[3].name, 'price': str(round(order.menu[3].price,2)), 'quantity': str(0)}

        with open(test_file, "w") as fd:
            sys.stdout = fd
            try:
                order.fill()
            except OrderTermination:
                pass

        with open(test_file, "r") as fd:
            data = fd.read()
            self.assertRegex(data, r'ORDER\s+\d+')
            self.assertRegex(data, '{name}:\s+{price}\s+x\s+{quantity}'.format(**burger1))
            self.assertRegex(data, '{name}:\s+{price}\s+x\s+{quantity}'.format(**burger2))
            self.assertNotRegex(data, '{}:\.*?x'.format(burger3['name']))

        os.remove(test_file)

    @patch('builtins.input', create=True)
    def test_add_burger_too_many(self, mocked_input):
        test_file = "_test_too_many.txt"
        order = Order()
        mocked_input.side_effect = ["0", "2", "100", "51", "3", "1", "10", "9", "11"]
        """
        0: wrong choice
        2: select burger #2
        100: too many, illegal choice
        51: still too many, illegal choice
        3: add 3 burger #2
        1: select burger #1
        10: add 10 burgers #1
        9: display the order
        11: quit
        """
        # add 100 Bacon Cheese burgers which is too many, back to 3, and 10 de Anza Burger
        burger1 = {'name': order.menu[2].name, 'price': str(round(order.menu[2].price,2)), 'quantity': str(3)}
        burger2 = {'name': order.menu[1].name, 'price': str(round(order.menu[1].price,2)), 'quantity': str(10)}

        with open(test_file, "w") as fd:
            sys.stdout = fd
            try:
                order.fill()
            except OrderTermination:
                pass

        with open(test_file, "r") as fd:
            data = fd.read()
            self.assertRegex(data, '{name}:\s+{price}\s+x\s+{quantity}'.format(**burger1))
            self.assertRegex(data, '{name}:\s+{price}\s+x\s+{quantity}'.format(**burger2))

        os.remove(test_file)


    @patch('builtins.input', create=True)
    def test_add_burger_zero(self, mocked_input):
        test_file = "_test_zero.txt"
        order = Order()
        mocked_input.side_effect = ["2", "", "2", "4", "1", "0", "9", "11"]
        """
        2: select burger #2
        0: cancel the selection of burger #2
        2: select burger #2
        4: add 4 burgers #2
        1: select burger #1
        0: cancel the selection of burger #1
        9: display the order
        11: quit
        """
        # add 4 Bacon Cheese burgers and 0 de Anza Burger
        burger1 = {'name': order.menu[1].name, 'price': str(round(order.menu[1].price,2)), 'quantity': str(0)}
        burger2 = {'name': order.menu[2].name, 'price': str(round(order.menu[2].price,2)), 'quantity': str(4)}

        with open(test_file, "w") as fd:
            sys.stdout = fd
            try:
                order.fill()
            except OrderTermination:
                pass

        with open(test_file, "r") as fd:
            data = fd.read()
            self.assertRegex(data, '{name}:\s+{price}\s+x\s+{quantity}'.format(**burger2))
            self.assertNotRegex(data, '{name}:\s+{price}\s+x\s+\d+'.format(**burger1))
            self.assertRegex(data, '{} choice has been cancelled'.format(burger2['name']))
            self.assertRegex(data, '{} choice has been cancelled'.format(burger1['name']))

        os.remove(test_file)


    @patch('builtins.input', create=True)
    def test_add_increase_quantity(self, mocked_input):
        test_file = "_test_inc.txt"
        order = Order()
        mocked_input.side_effect = ["2", "4", "1", "1", "2", "3", "9", "11"]
        """
        2: select burger #2
        4: add 4 burger #2
        1: select burger #1
        1: add 1 burger #1
        2: select burger #2 again
        3: add 3 more burgers #2 for a total of 7
        9: display the order
        11: quit
        """
        # add 4 Bacon Cheese burgers and 0 de Anza Burger
        burger1 = {'name': order.menu[1].name, 'price': str(round(order.menu[1].price,2)), 'quantity': str(1)}
        burger2 = {'name': order.menu[2].name, 'price': str(round(order.menu[2].price,2)), 'quantity': str(7)}

        with open(test_file, "w") as fd:
            sys.stdout = fd
            try:
                order.fill()
            except OrderTermination:
                pass

        with open(test_file, "r") as fd:
            data = fd.read()
            self.assertRegex(data, '{name}:\s+{price}\s+x\s+{quantity}'.format(**burger1))
            self.assertRegex(data, '{name}:\s+{price}\s+x'.format(**burger1))

        os.remove(test_file)


    @patch('builtins.input', create=True)
    def test_update_hesitation(self, mocked_input):
        test_file = "_test_hesitation.txt"
        order = Order()
        mocked_input.side_effect = ["2", "50", "6", "  ", "6", "2", "1", "", "9", "11"]
        """
        2: select burger #2
        50: add 50 burgers #2
        6: select update
        empty: exits the update sub-menu
        6: select again update
        2: select transaction #2 (which doesn't exist)
        1: select transaction #1
        empty: exits the update sub-menu
        9: display the order
        11: exit
        """
        burger2 = {'name': order.menu[2].name, 'price': str(round(order.menu[2].price,2)), 'quantity': str(50)}

        with open(test_file, "w") as fd:
            sys.stdout = fd
            try:
                order.fill()
            except OrderTermination:
                pass

        with open(test_file, "r") as fd:
            data = fd.read()
            self.assertRegex(data, '{name}:\s+{price}\s+x\s+{quantity}'.format(**burger2))
            self.assertRegex(data, r'please select a valid item in \[1\]. Thank you.')
            self.assertRegex(data, r'update cancelled, back to main menu.')

        os.remove(test_file)


    @patch('builtins.input', create=True)
    def test_update_quantity(self, mocked_input):
        test_file = "_test_update.txt"
        order = Order()
        mocked_input.side_effect = ["2", "50", "4", "50", "6", "1", "5", "6", "2", "4", "9", "11"]
        """
        2: select burger #2
        50: add 50 burgers #2
        4: select burger #4
        50: add 50 burgers #4
        6: select the update
        1: select transaction #1 (related to burger #2)
        5: change the quantity to 5 burgers #2
        6: select the update
        2: select transaction #1 (related to burger #4)
        4: change the quantity to 4 burgers #4
        9: display the order
        11: exit
        """
        burger2 = {'name': order.menu[2].name, 'price': str(round(order.menu[2].price,2)), 'quantity': str(5)}
        burger4 = {'name': order.menu[4].name, 'price': str(round(order.menu[4].price,2)), 'quantity': str(4)}

        with open(test_file, "w") as fd:
            sys.stdout = fd
            try:
                order.fill()
            except OrderTermination:
                pass

        with open(test_file, "r") as fd:
            data = fd.read()
            self.assertRegex(data, '{name}:\s+{price}\s+x\s+50'.format(**burger2))
            self.assertRegex(data, '{name}:\s+{price}\s+x\s+50'.format(**burger4))
            self.assertRegex(data, '{name}:\s+{price}\s+x\s+{quantity}'.format(**burger2))
            self.assertRegex(data, '{name}:\s+{price}\s+x\s+{quantity}'.format(**burger4))

        os.remove(test_file)


    @patch('builtins.input', create=True)
    def test_update_zero_quantity(self, mocked_input):
        test_file = "_test_update_zero.txt"
        order = Order()
        mocked_input.side_effect = ["2", "50", "4", "50", "6", "1", "0", "6", "1", "0", "9", "11"]
        """
        2: select burger #2
        50: add 50 burgers #2
        4: select burger #4
        50: add 50 burgers #4
        6: select the update
        1: select transaction #1 (for burger #2)
        0: set the new quantity to 0 (burger #2 should be removed)
        6: select the update
        1: select transaction #1 (for burger #4)
        0: set the new quantity to 0 (burger #4 should be removed)
        9: display the order
        11: exit
        """
        burger2 = {'name': order.menu[2].name, 'price': str(round(order.menu[2].price,2)), 'quantity': str(5)}
        burger4 = {'name': order.menu[4].name, 'price': str(round(order.menu[4].price,2)), 'quantity': str(4)}

        with open(test_file, "w") as fd:
            sys.stdout = fd
            try:
                order.fill()
            except OrderTermination:
                pass

        with open(test_file, "r") as fd:
            data = fd.read()
            self.assertRegex(data, '{name}:\s+{price}\s+x\s+\d+'.format(**burger2))
            self.assertRegex(data, '{name}:\s+{price}\s+x\s+\d+'.format(**burger4))
            self.assertRegex(data, '{name} has been deleted'.format(**burger2))
            self.assertRegex(data, '{name} has been deleted'.format(**burger4))
            self.assertRegex(data, r'ORDER.+\*\*\*[^\d]+soon!!') # empty order

        os.remove(test_file)

    @patch('builtins.input', create=True)
    def test_delete(self, mocked_input):
        test_file = "_test_delete.txt"
        order = Order()
        mocked_input.side_effect = ["2", "5", "4", "2", "7", "2", "9", "11"]
        """
        2: select burger #2
        5: add 5 burgers #2
        4: select burger #4
        2: ass 2 burgers #4
        7: select delete sub-menu
        2: select transaction #2 (related to burger #4)
        9: display the order
        11: quit
        """

        burger2 = {'name': order.menu[2].name, 'price': str(round(order.menu[2].price,2)), 'quantity': str(5)}
        burger4 = {'name': order.menu[4].name, 'price': str(round(order.menu[4].price,2)), 'quantity': str(4)}

        with open(test_file, "w") as fd:
            sys.stdout = fd
            try:
                order.fill()
            except OrderTermination:
                pass

        with open(test_file, "r") as fd:
            data = fd.read()
            self.assertRegex(data, '{name}:\s+{price}\s+x\s+\d+'.format(**burger2))
            self.assertRegex(data, '{name}:\s+{price}\s+x\s+\d+'.format(**burger4))
            self.assertRegex(data, '{name} has been deleted'.format(**burger4))
            self.assertRegex(data[data.rfind('ORDER'):], '{name}'.format(**burger2))
            self.assertNotRegex(data[data.rfind('ORDER'):], '{name}'.format(**burger4))
            
        os.remove(test_file)


    @patch('builtins.input', create=True)
    def test_delete_badkey(self, mocked_input):
        test_file = "_test_delete_badkey.txt"
        order = Order()
        mocked_input.side_effect = ["2", "5", "1", "3", "7", "4", "0", "-10", "a", "1", "9", "11"]
        """
        2: select burger #2
        5: add 5 burgers #2
        1: select burger #1
        3: add 3 burgers #1
        7: select delete sub-menu
        4: select transaction #2 (non existing transaction)
        0: select transaction #2 (illegal entry)
        -10: select transaction #2 (illegal entry)
        a: select transaction #2 (illegal entry)
        1: select transaction #1 (for burger #2)
        9: display the order
        11: quit
        """

        burger2 = {'name': order.menu[2].name, 'price': str(round(order.menu[2].price,2)), 'quantity': str(5)}  

        with open(test_file, "w") as fd:
            sys.stdout = fd
            try:
                order.fill()
            except OrderTermination:
                pass

        with open(test_file, "r") as fd:
            data = fd.read()
            self.assertRegex(data, '{name}:\s+{price}\s+x\s+\d+'.format(**burger2))
            self.assertRegex(data, '{name} has been deleted'.format(**burger2))
            self.assertRegex(data, 'please select a valid item in \[1, 2\]. Thank you.')
            attempts = len(re.findall(r'please select a valid item in \[1, 2\]', data))
            self.assertEqual(attempts,4)
            self.assertNotRegex(data[data.rfind('ORDER'):], '{name}'.format(**burger2))

        os.remove(test_file)

    @patch('builtins.input', create=True)
    def test_delete_hesitation(self, mocked_input):
        test_file = "_test_delete_hesitation.txt"
        order = Order()
        mocked_input.side_effect = ["2", "5", "7", "  ", "7", "", "9", "11"]
        """
        2: select burger #2
        5: add 5 burgers #2
        7: select delete sub-menu
        empty: go back to main menu
        7: select delete sub-menu
        empty: go back to main menu
        9: display the order
        11: exit
        """
                                    
        burger2 = {'name': order.menu[2].name, 'price': str(round(order.menu[2].price,2)), 'quantity': str(5)}  

        with open(test_file, "w") as fd:
            sys.stdout = fd
            try:
                order.fill()
            except OrderTermination:
                pass

        with open(test_file, "r") as fd:
            data = fd.read()
            attempts = len(re.findall(r'deletion cancelled', data))
            self.assertEqual(attempts, 2)
            self.assertRegex(data, '{name}:\s+{price}\s+x\s+{quantity}'.format(**burger2))
 
        os.remove(test_file)


    @patch('builtins.input', create=True)
    def test_compute_totals(self, mocked_input):
        order = Order()
        test_file = "_test_compute.txt"
        order.tax_rate = 0.1
        mocked_input.side_effect = ["2", "5", "3", "10", "9", "11"]
        """
        2: select burger #2
        5: add 5 burgers #2
        3: select burger #3
        10: select 10 burgers #3
        9: display order
        11: quit
        """
        burger2 = {'name': order.menu[2].name, 'price': order.menu[2].price, 'quantity': 5}
        burger3 = {'name': order.menu[3].name, 'price': order.menu[3].price, 'quantity': 10}

        with open(test_file, "w") as fd:
            sys.stdout = fd
            try:
                order.fill()
            except OrderTermination:
                pass
        
        order.compute()
        self.assertAlmostEqual(order.pre_tax, round(sum([b['price']*b['quantity'] for b in [burger2,burger3]]),2))
        self.assertAlmostEqual(order.tax_rate, 0.1)
        self.assertAlmostEqual(order.taxes, round(order.pre_tax*0.1,2))
        self.assertAlmostEqual(order.post_tax, round(order.pre_tax*1.1,2))

        os.remove(test_file)

    @patch('builtins.input', create=True)
    def test_compute_totals_student(self, mocked_input):
        test_file = "_test_pay.txt"
        order = Order()
        order.tax_rate = 0.1
        mocked_input.side_effect = ["2", "5", "3", "10", "10", "1", "11"]
        """
        2: select burger #2
        5: add 5 burgers #2
        3: select burger #3
        10: select 10 burgers #3
        10: validate the order
        1: select Student profile
        11: quit
        """
        burger2 = {'name': order.menu[2].name, 'price': order.menu[2].price, 'quantity': 5}
        burger3 = {'name': order.menu[3].name, 'price': order.menu[3].price, 'quantity': 10}

        order_id = order.id

        with open(test_file, "w") as fd:
            sys.stdout = fd
            try:
                order.fill()
            except OrderTermination:
                pass
        
        with open(test_file, "r") as fd:
            data = fd.read()
            self.assertRegex(data, 'RECEIPT')
            self.assertRegex(data, '{name}:\s+{price}\s+x\s+{quantity}'.format(**burger2))
            self.assertRegex(data, '{name}:\s+{price}\s+x\s+{quantity}'.format(**burger3))
            self.assertRegex(data, 'pre tax amount:\s+\$\s+{}'.format(order.pre_tax))
            self.assertRegex(data, 'taxes\s+{}%:\s+\$\s+{}'.format(round(order.tax_rate*100,2), order.taxes))
            self.assertRegex(data, 'grand total:\s+\$\s+{}'.format(order.post_tax))
            self.assertTrue(os.path.isfile(f'receipt_{order_id}.txt'))
 
        os.remove(test_file)
        os.remove(f'receipt_{order_id}.txt')


    @patch('builtins.input', create=True)
    def test_compute_totals_staff(self, mocked_input):
        test_file = "_test_pay_staff.txt"
        order = Order()
        order.tax_rate = 0.1
        mocked_input.side_effect = ["2", "5", "3", "10", "10", "3", "2", "11"]
        """
        2: select burger #2
        5: add 5 burgers #2
        3: select burger #3
        10: select 10 burgers #3
        10: validate the order
        3: invalid choice
        2: select Staff profile
        11: quit
        """
        burger2 = {'name': order.menu[2].name, 'price': order.menu[2].price, 'quantity': 5}
        burger3 = {'name': order.menu[3].name, 'price': order.menu[3].price, 'quantity': 10}

        order_id = order.id

        with open(test_file, "w") as fd:
            sys.stdout = fd
            try:
                order.fill()
            except OrderTermination:
                pass
        
        with open(test_file, "r") as fd:
            data = fd.read()
            self.assertRegex(data, 'please select an numeric choice from \[1-student, 2-staff\]. Thank you.')
            self.assertRegex(data, 'RECEIPT')
            self.assertRegex(data, '{name}:\s+{price}\s+x\s+{quantity}'.format(**burger2))
            self.assertRegex(data, '{name}:\s+{price}\s+x\s+{quantity}'.format(**burger3))
            self.assertRegex(data, 'pre tax amount:\s+\$\s+{}'.format(order.pre_tax))
            self.assertRegex(data, 'taxes\s+{}%:\s+\$\s+{}'.format(round(order.tax_rate*100,2), order.taxes))
            self.assertRegex(data, 'grand total:\s+\$\s+{}'.format(order.post_tax))
            self.assertRegex(data, 'Thank you for your visit. See you soon!!')
            self.assertTrue(os.path.isfile(f'receipt_{order_id}.txt'))
 
        os.remove(test_file)
        os.remove(f'receipt_{order_id}.txt')

if __name__ == "__main__":
    unittest.main(argv=['ignore'], verbosity=2, exit=False)

"""
test_add_burger (__main__.TestOrder.test_add_burger) ... ok
test_add_burger_too_many (__main__.TestOrder.test_add_burger_too_many) ... ok
test_add_burger_zero (__main__.TestOrder.test_add_burger_zero) ... ok
test_add_increase_quantity (__main__.TestOrder.test_add_increase_quantity) ... ok
test_compute_totals (__main__.TestOrder.test_compute_totals) ... ok
test_compute_totals_staff (__main__.TestOrder.test_compute_totals_staff) ... ok
test_compute_totals_student (__main__.TestOrder.test_compute_totals_student) ... ok
test_delete (__main__.TestOrder.test_delete) ... ok
test_delete_badkey (__main__.TestOrder.test_delete_badkey) ... ok
test_delete_hesitation (__main__.TestOrder.test_delete_hesitation) ... ok
test_menu_and_commands (__main__.TestOrder.test_menu_and_commands) ... ok
test_order_creation (__main__.TestOrder.test_order_creation) ... ok
test_trial_mocked_IOs (__main__.TestOrder.test_trial_mocked_IOs) ... ok
test_update_hesitation (__main__.TestOrder.test_update_hesitation) ... ok
test_update_quantity (__main__.TestOrder.test_update_quantity) ... ok
test_update_zero_quantity (__main__.TestOrder.test_update_zero_quantity) ... ok

----------------------------------------------------------------------
Ran 16 tests in 0.152s

OK

"""