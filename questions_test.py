"""Test the package questions"""

__author__ = "Bertrand Blanc (Alan Turing)"


import unittest
from unittest.mock import patch
from questions import *


class TestQuestions(unittest.TestCase):
    @patch('builtins.input', create=True)
    def test_integerquestion_basic(self, mocked_input):
        range_ = range(2,10)

        for i in range_:
            mocked_input.side_effect = ["12", "10", "-2", str(i)]
            q = IntegerQuestion("give a number", range_).ask()
            self.assertEqual(q,i)
        
        for i in ["3.2", "a"]:
            mocked_input.side_effect = [i, "4"]
            q = IntegerQuestion("give a number", range_).ask()
            self.assertEqual(q,4)

        mocked_input.side_effect = ["5"]
        q = IntegerQuestion("give a number", range_)
        self.assertIsNone(q.result)
        self.assertEqual(q.ask(),5)
        self.assertEqual(q.result,5)


    @patch('builtins.input', create=True)
    def test_integerquestion_null(self, mocked_input):
        range_ = range(2,10)

        for i in ["", "    "]:
            with self.assertRaises(SkipInput):
                mocked_input.side_effect = [i]
                IntegerQuestion("give a number", range_).ask()
        
    @patch('builtins.input', create=True)
    def test_integerquestion_range(self, mocked_input):
        range_ = [3,16]

        for x in range_:
            mocked_input.side_effect = ["19", "-2", str(x), "9"]
            q = IntegerQuestion("give a number", range_).ask()
            self.assertEqual(q,x)


    @patch('builtins.input', create=True)
    def test_enumquestion_basic(self, mocked_input):
        enum = [(2,"choice 1", 3), (3,"choice 2", [2,3])]
        q = EnumQuestion(enum)
        mocked_input.side_effect = ["1", "4", "2"]
        self.assertIsNone(q.result)
        q.ask()
        self.assertIsNotNone(q.result)
        self.assertEqual(q.result,3)

        mocked_input.side_effect = ["1", "4", "3"]
        q.ask()
        self.assertIsInstance(q.result,list)


    @patch('builtins.input', create=True)
    def test_enumquestion_null(self, mocked_input):
        enum = [(2,"choice 1", 3), (3,"choice 2", [2,3])]
        q = EnumQuestion(enum)

        for i in ["", "    "]:
            with self.assertRaises(SkipInput):
                mocked_input.side_effect = [i]
                q.ask()


if __name__ == "__main__":
    unittest.main(argv=['ignore'], exit=False, verbosity=2)