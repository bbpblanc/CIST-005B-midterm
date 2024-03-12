"""
Special package deferring most of the printing from the code to this package.
Basic and default printing mechanism are still available as part of the code,
likely targeting point-usage or debugging purposes.
This package focuses on the various ways the information is displayed to the
end-users. It is possible to modify the printing mechanism by changing the
"skins" via this package, without having to edit the rest of the code, hence
decreasing the risks to create bugs.
"""

__author__ = "Bertrand Blanc (Alan Turing)"
__all__ = ["Receipt", "PrettyPrint", "PrintOnGoingOrder"]
"""Not all Objects are exposed to the public, only a tiny set used as generics"""

import pandas as pd
from datetime import datetime
import pytz

class Printer():
    """ Basic printer defining basic printing capabilities.
    Let's note that this object is good enough to have a working system.
    """
    def __init__(self, order):
        self.order = order

    def issue(self):
        """rough display leveraging the serialization of the calling object"""
        print(self.order)

    def store(self):
        """basic storing on file"""
        filename = 'receipt_' + str(self.order.id) + '.txt'
        with open(filename, 'w') as fd:
            fd.write(str(self.order) + '\n')
    

class Receipt(Printer):
    """The receipt is is what is exposed to to access printing capabilities
    to issue a printed receipt.
    No code is needed, all methods are inherited from the parent.
    It still leaves the door open for future look-n-feel enhancements.
    """
    pass


    
class PrettyPrint(Receipt):
    """Printer for a receipt"""
    def __init__(self,order):
        super().__init__(order)

    def issue(self):
        transactions = str(self.order.transactions)
        max_length = max([len(transaction) for transaction in transactions.split('\n')])
        LENGTH = max_length + 5

        buf = "{0:^{1}}\n".format("RECEIPT", LENGTH)
        buf += datetime.now(pytz.timezone('US/Pacific')).strftime("%A %B %d,%Y %I:%M%p") + '\n'
        buf += "order: {}\n".format(str(self.order.id))
        buf += "="*LENGTH + '\n'
        buf += str(self.order.transactions)
        buf += "="*LENGTH + '\n'
        buf += "{:>15s}: ${:>6.2f}\n".format("pre tax amount", self.order.pre_tax)
        buf += "{:>15s}: ${:>6.2f}\n".format("taxes " + str(round(self.order.tax_rate*100,2)) + "%", self.order.taxes)
        buf += "{:>15s}: ${:>6.2f}\n".format("grand total", self.order.post_tax)
        buf += "="*LENGTH + '\n'
        
        return buf


class _PrintOnGoingOrderBasic(Printer):
    """Internal skin to print the content of an order while the end-user is still working on it.
    The formatting is basic and good enough"""
    def issue(self):
        buf = ""
        buf += f"*** ORDER {self.order.id} ***\n"
        buf += str(self.order.transactions)
        print(buf)

class _PrintOnGoingOrderPandas(Printer):
    """Using Pandas for a standardized display. The look-n-feel doesn't look that great."""
    def issue(self):
        df = pd.DataFrame(columns=['key', 'name', 'unit price', 'quantity'])
        df.set_index('key', inplace=True)
        for v in self.order.transactions:
            df.loc[v.id] = [v.item.name, v.item.price, v.quantity]
        print(df)


class PrintOnGoingOrder(_PrintOnGoingOrderBasic):
    """Interface explosed outside. The look-n-feel can be be changed here by changing the skin defined as a superclass"""
    pass


if __name__ == "__main__":
    df = pd.DataFrame(columns=['key', 'name', 'unit price', 'quantity'])
    print(df)