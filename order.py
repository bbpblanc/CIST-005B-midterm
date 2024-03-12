"""
Main class to run the system: the Order.
The basic flow is:
. Menu data are loaded creating the Menu data structure aka available burgers.
. The burgers are displayed inviting the customer/end-user to select the burger,
. Additional commands are displayed after the menu
.. command to update the current order
.. command to delete an item from the order
.. display the menu again
.. display the current content of the order
.. finalizing the order to get the receipt
.. quitting (and loosing the tramsactions)
"""

__all__ = ["Order", "IllegalChoice", "OrderTermination"]
__author__ = "Bertrand Blanc (Alan Turing)"

from menu4order import MenuDecoratorForOrder
from menu import Menu
from linkedbag import LinkedBag
from person import *
from transaction import *
from questions import *
from functools import reduce
from random import randint
import printer

class IllegalChoice(Exception):
    pass

class OrderTermination(Exception):
    pass

class Order():
    MAX_ITEM = 50

    commands = [
        ('update', lambda obj:obj.update()),
        ('delete', lambda obj:obj.delete()),
        ("display the menu", lambda obj:obj.print_commands()),
        ("display the order", lambda obj:obj.display_order()),
        ("finalize the order and pay", lambda obj:obj.commit()),
        ("quit", lambda obj:obj.shutdown()),
    ]



    def __init__(self):
        self._menu = MenuDecoratorForOrder(Menu(auto_load=True))
        self._transactions = Transactions() # composed of (MenuItem, quantity)

        self._commands = LinkedBag()
        for i,command in enumerate(Order.commands,1):
            self._commands.add((len(self._menu)+i,command))

        self._total = {'pre_tax': 0.0, 'tax_rate': 0.0, 'taxes': 0.0, 'grand_total': 0.0}
        self._len = len(self._commands)+len(self._menu)+1
        self._id = randint(10_000, 100_000)

    @property
    def transactions(self):
        return self._transactions
    @transactions.setter
    def transactions(self, value):
        raise IllegalChoice('modifying transactions is prohibited')
    

    @property
    def menu(self):
        return self._menu
    @menu.setter
    def menu(self, value):
        raise IllegalChoice('modifying menu is prohibited')
    
    @property
    def pre_tax(self):
        return self._total['pre_tax']
    @pre_tax.setter
    def pre_tax(self, amount):
        raise IllegalChoice('modifying the pre tax amount is prohibited')

    @property
    def tax_rate(self):
        return self._total['tax_rate']
    @tax_rate.setter
    def tax_rate(self, amount):
        self._total['tax_rate'] = amount

    @property
    def post_tax(self):
        return self._total['grand_total']
    @post_tax.setter
    def post_tax(self, amount):
        raise IllegalChoice('modifying the post tax amount is prohibited')
    
    @property
    def taxes(self):
        return self._total['taxes']
    @taxes.setter
    def taxes(self, amount):
        raise IllegalChoice('modifying the tax amount is prohibited')

    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, amount):
        raise IllegalChoice('modifying the order ID is prohibited')


    def fill(self):
        """Main method called by the system to start the flow"""
        self.add()

    def add(self):
        """
        Add an item aka a transaction in the order:
        . the menu items are displayed
        . the user selects the burger 
        . the user selects the quantity (bounded to 50 max) for that burger
        . If the quantity is 0, the customer probably doesn't want that burger anymore
        . If no data is entered the menu is re-displayed
        """

        self.print_commands()
        while True:
            try:
                question = "Select from the menu"
                question = IntegerQuestion(question, range(1,self._len), error_message='please select a valid item from the menu options. Thank you.')
                choice = question.ask()
            except SkipInput: 
                # the user entered an empty string
                self.print_commands()
                continue

            # the user entered a menu item
            if 1 <= choice <= len(self.menu):
                try:
                    question = f'Select the quantity for {self.menu[choice].name}'
                    question = IntegerQuestion(question, range(0,self.MAX_ITEM+1), error_message=f"up to {self.MAX_ITEM} please...")
                    quantity = question.ask()
                except SkipInput:
                    quantity = 0

                if quantity == 0:
                    print(f'{self.menu[choice].name} choice has been cancelled')
                    continue

                self._transactions.add(Transaction(self.menu[choice],quantity))
                continue

            # the user entered a sub-menu command e.g. update, pay, quit...
            for command in self._commands:
                if choice == command[0]:
                    command[1][1](self)


    def update(self):
        """Update a trasaction, entering in a "sub-menu".
        . the items compising the current order are displayed
        . the user selects an existing item from their order
        . the user changes the number of items.
        . if the entered value is null, the transaction for that item is removed
        """
        self.display_order()
        while True:
            try:
                question = "Select a transaction from the order to update a quantity"
                choice = IntegerQuestion(question, self._transactions.keys()).ask()
            except SkipInput: 
                # the user enters nothing
                print(f'update cancelled, back to main menu.')
                break

            if choice > len(self.menu):
                for command in self._commands:
                    if choice == command[0]:
                        command[1][1](self)
                continue

            existing_transaction = self._transactions[choice]

            """ maybe redundant
            try:
                existing_transaction = self._transactions[choice]
            except KeyError:
                print(f'please select an item from your order. Thank you.')
                continue
            """
            try:
                question = f'Select the new quantity for {existing_transaction.item.name}'
                question = IntegerQuestion(question, range(0,self.MAX_ITEM+1), error_message=f'please up to {self.MAX_ITEM} items. Thanks.')
                quantity = question.ask()
            except SkipInput:
                # empty input
                print(f'update cancelled, back to main menu.')
                break

            self._transactions.update(Transaction(existing_transaction.item,quantity))


            if quantity == 0:
                print(f'{existing_transaction.item.name} has been deleted')
            break
            
        self.add()

    def delete(self):
        """Delete a transaction from the order:
        . display the content of the current order
        . the user selects a transaction ID
        . the transaction is removed
        """
        self.display_order()
        while True:
            try:
                question = "Select from the order to delete an item"
                choice = IntegerQuestion(question, self._transactions.keys()).ask()
            except SkipInput: 
                # the user enters nothing
                print(f'deletion cancelled, back to main menu.')
                break

            if choice > len(self.menu):
                for command in self._commands:
                    if choice == command[0]:
                        command[1][1](self)
                continue

            existing_transaction = self._transactions[choice]
            """
            try:
                existing_transaction = self._transactions[choice]
            except SkipInput:
                # empty input
                print(f'deletion cancelled, back to main menu.')
                break
            """

            self._transactions.delete(Transaction(existing_transaction.item,0))
            print(f'{existing_transaction.item.name} has been deleted')
            break

        self.add()


    def print_commands(self):
        """Print the list of commands:
        . the menu items
        . the different additional commands
        """
        print(self.menu)
        for i,c in self._commands:
            print(f'{i:<3} - {c[0]}')


    def commit(self):
        """Finalize the order
        . collects the status of the customer student/staff
        . computes the pre-tax, tax and grand total amounts
        . prints the receipt
        . stores the receipt on file
        """
        if len(self.transactions.keys()) == 0:
            print('Empty order. Order aborted.')
            self.shutdown()

        enum = [(1,"student",Student),(2,"staff",Staff)]
        flag = True
        while flag:
            try:
                choice = EnumQuestion(enum).ask()
            except ValueError:
                continue
            else:
                flag = False
        
        choice().compute(self)

        receipt = printer.Receipt(self)
        receipt.issue()
        receipt.store()
        self.shutdown()
        
    def compute(self):
        """Compute the pre-tax, taxes and grand-total amounts"""
        self._total['pre_tax'] = round(reduce(lambda total,transaction: total+transaction.item.price*transaction.quantity, self.transactions,0),2)
        self._total['taxes'] = round(self.pre_tax*self.tax_rate,2)
        self._total['grand_total'] = round(self.pre_tax+self.taxes,2)

    def shutdown(self):
        """Close the order for the current customer"""
        print('Thank you for your visit. See you soon!!')
        raise OrderTermination()

    def __str__(self):
        return printer.PrettyPrint(self).issue()

    def display_order(self):
        """Display the order, deferring the look-n-feel to the printer package"""
        printer.PrintOnGoingOrder(self).issue()


if __name__ == "__main__":
    order = Order()
    try:
        order.fill()
    except OrderTermination:
        exit(0)


"""
*************************
*** TRACE #1:
*************************

=======================================
================ MENU =================
=======================================
1     de Anza Burger: $5.25
2       Bacon Cheese: $5.75
3     Mushroom Swiss: $5.95
4     Western Burger: $5.95
5    Don Cali Burger: $5.95
=======================================
6   - update
7   - delete
8   - display the menu
9   - display the order
10  - finalize the order and pay
11  - quit
Select from the menu: 4
Select the quantity for Western Burger: 15
Select from the menu: 2
Select the quantity for Bacon Cheese: 3
Select from the menu: 9
*** ORDER 26500 ***
  1     Western Burger: 5.95 x 15
  2       Bacon Cheese: 5.75 x 3

Select from the menu: 7
*** ORDER 26500 ***
  1     Western Burger: 5.95 x 15
  2       Bacon Cheese: 5.75 x 3

Select from the order to delete an item: 
deletion cancelled, back to main menu.
=======================================
================ MENU =================
=======================================
1     de Anza Burger: $5.25
2       Bacon Cheese: $5.75
3     Mushroom Swiss: $5.95
4     Western Burger: $5.95
5    Don Cali Burger: $5.95
=======================================
6   - update
7   - delete
8   - display the menu
9   - display the order
10  - finalize the order and pay
11  - quit
Select from the menu: 7
*** ORDER 26500 ***
  1     Western Burger: 5.95 x 15
  2       Bacon Cheese: 5.75 x 3

Select from the order to delete an item: 4
please select a valid item in [1, 2]. Thank you.
Select from the order to delete an item: 1
Western Burger has been deleted
=======================================
================ MENU =================
=======================================
1     de Anza Burger: $5.25
2       Bacon Cheese: $5.75
3     Mushroom Swiss: $5.95
4     Western Burger: $5.95
5    Don Cali Burger: $5.95
=======================================
6   - update
7   - delete
8   - display the menu
9   - display the order
10  - finalize the order and pay
11  - quit
Select from the menu: 9
*** ORDER 26500 ***
  1     Bacon Cheese: 5.75 x 3

Select from the menu: 10
Select [1-student, 2-staff]: 1
              RECEIPT
Friday March 08,2024 05:23PM
order: 26500
===================================
  1     Bacon Cheese: 5.75 x 3
===================================
 pre tax amount: $ 17.25
     taxes 0.0%: $  0.00
    grand total: $ 17.25
===================================

Thank you for your visit. See you soon!!

*******************************
*** receipt_26500.txt generated
*******************************



*************************
*** TRACE #2:
*************************

=======================================
================ MENU =================
=======================================
1     de Anza Burger: $5.25
2       Bacon Cheese: $5.75
3     Mushroom Swiss: $5.95
4     Western Burger: $5.95
5    Don Cali Burger: $5.95
=======================================
6   - update
7   - delete
8   - display the menu
9   - display the order
10  - finalize the order and pay
11  - quit
Select from the menu: 2
Select the quantity for Bacon Cheese: 5
Select from the menu: 1
Select the quantity for de Anza Burger: 56
up to 50 please...
Select the quantity for de Anza Burger: 0
de Anza Burger choice has been cancelled
Select from the menu: 4
Select the quantity for Western Burger:
Western Burger choice has been cancelled
Select from the menu: 5
Select the quantity for Don Cali Burger: 1
Select from the menu: 9
*** ORDER 56374 ***
  1        Bacon Cheese: 5.75 x 5
  2     Don Cali Burger: 5.95 x 1

Select from the menu: 6
*** ORDER 56374 ***
  1        Bacon Cheese: 5.75 x 5
  2     Don Cali Burger: 5.95 x 1

Select a transaction from the order to update a quantity: 0
please select a valid item in [1, 2]. Thank you.
Select a transaction from the order to update a quantity:
update cancelled, back to main menu.
=======================================
================ MENU =================
=======================================
1     de Anza Burger: $5.25
2       Bacon Cheese: $5.75
3     Mushroom Swiss: $5.95
4     Western Burger: $5.95
5    Don Cali Burger: $5.95
=======================================
6   - update
7   - delete
8   - display the menu
9   - display the order
10  - finalize the order and pay
11  - quit
Select from the menu: 6
*** ORDER 56374 ***
  1        Bacon Cheese: 5.75 x 5
  2     Don Cali Burger: 5.95 x 1

Select a transaction from the order to update a quantity: 6
please select a valid item in [1, 2]. Thank you.
Select a transaction from the order to update a quantity: 1
Select the new quantity for Bacon Cheese: 4
=======================================
================ MENU =================
=======================================
1     de Anza Burger: $5.25
2       Bacon Cheese: $5.75
3     Mushroom Swiss: $5.95
4     Western Burger: $5.95
5    Don Cali Burger: $5.95
=======================================
6   - update
7   - delete
8   - display the menu
9   - display the order
10  - finalize the order and pay
11  - quit
Select from the menu: 9
*** ORDER 56374 ***
  1        Bacon Cheese: 5.75 x 4
  2     Don Cali Burger: 5.95 x 1

Select from the menu: 10
Select [1-student, 2-staff]: 2
               RECEIPT
Friday March 08,2024 05:20PM
order: 56374
======================================
  1        Bacon Cheese: 5.75 x 4
  2     Don Cali Burger: 5.95 x 1
======================================
 pre tax amount: $ 28.95
     taxes 9.0%: $  2.61
    grand total: $ 31.56
======================================

Thank you for your visit. See you soon!!

*******************************
*** receipt_56374.txt generated
*******************************
"""