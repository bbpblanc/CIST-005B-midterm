"""
The questions asked to the end-users to interact with them are wrapped
into dedicated Question objects. The nature of the question involves 
different checking mechanism. Two styles of question are currently available.
"""

__author__ = "Bertrand Blanc (Alan Turing)"
__all__ = ["IntegerQuestion", "EnumQuestion", "SkipInput"]

from abc import ABC, abstractmethod


class IllegalChoice(Exception):
    pass

class SkipInput(Exception):
    pass

class Question(ABC):
    """Generic abstract superclass to inforce an interface requirement"""
    def __init__(self, question, default_error_message):
        self._question = question
        self._result = None
        self._error_message = default_error_message

    @abstractmethod
    def ask(self):
        """Abstract method to be implemented by all children"""
        pass
    
    @property
    def result(self):
        """The answer to the question is kept and remains accessible"""
        return self._result
    

class IntegerQuestion(Question):
    """The answer to this question is expected to be an Integer value within a 
    specific range
    """
    def __init__(self, question, val_range, *, error_message=None):
        if not error_message:
            error_message = f"please select a valid item in {val_range}. Thank you."

        super().__init__(question, error_message)
        self._range = val_range

    def ask(self):
        """The question is asked to the end-user until s/he provides a valid answer:
        An integer within the specific range is a correct answer
        Other erroneous answers like outside the range of allowed values, or any other types
        are dealt inside this class.
        An empty answer is also correct, raising an error, allowing the flow to continue.
        """
        while True:
            try:
                choice = input(self._question + ": ")
                if len(choice.strip()) == 0:
                    raise SkipInput()
                choice = int(choice)
                if choice not in self._range:
                    raise IllegalChoice()
            except TypeError:
                print(self._error_message)
            except IllegalChoice:
                print(self._error_message)
            except ValueError as e:
                print(self._error_message)
            except SkipInput as e:
                raise e
            else:
                self._result = choice
                return self.result
            
        assert False, "unreachable location"
    
class EnumQuestion(Question):
    """The answer to this question is expected to be based on an enumeration.
    The format is a list of candidates represented as tuples.
    tuple(value to be keyed, short description in plain english, object to return upon selection)
    """
    def __init__(self, enum):
        # enum format = List[(value,description,object)]
        question = "Select [" + ", ".join(str(x[0])+'-'+x[1] for x in enum) + ']'
        error_message = f"please select an numeric choice from [{', '.join(str(x[0])+'-'+x[1] for x in enum)}]. Thank you."
        super().__init__(question, error_message)
        self._enum = enum

    def ask(self):
        """
        The user can answer with the boundaries of the expected keys from the enumeration.
        """
        while True:
            try:
                choice = input(self._question + ": ")
                if len(choice.strip()) == 0:
                    raise SkipInput
                choice = int(choice)
                for e in self._enum:
                    if choice == e[0]:
                        self._result = e[2]
                        return self.result
                raise IllegalChoice()
            except TypeError:
                print(self._error_message)
            except IllegalChoice:
                print(self._error_message)
            except ValueError as e:
                print(self._error_message)
            except SkipInput as e:
                raise e

        assert False, "unreachable location"

"""
test_enumquestion_basic (__main__.TestQuestions.test_enumquestion_basic) ... please select an numeric choice from [2-choice 1, 3-choice 2]. Thank you.
please select an numeric choice from [2-choice 1, 3-choice 2]. Thank you.
please select an numeric choice from [2-choice 1, 3-choice 2]. Thank you.
please select an numeric choice from [2-choice 1, 3-choice 2]. Thank you.
ok
test_enumquestion_null (__main__.TestQuestions.test_enumquestion_null) ... ok
test_integerquestion_basic (__main__.TestQuestions.test_integerquestion_basic) ... please select a valid item in range(2, 10). Thank you.
please select a valid item in range(2, 10). Thank you.
please select a valid item in range(2, 10). Thank you.
please select a valid item in range(2, 10). Thank you.
please select a valid item in range(2, 10). Thank you.
please select a valid item in range(2, 10). Thank you.
please select a valid item in range(2, 10). Thank you.
please select a valid item in range(2, 10). Thank you.
please select a valid item in range(2, 10). Thank you.
please select a valid item in range(2, 10). Thank you.
please select a valid item in range(2, 10). Thank you.
please select a valid item in range(2, 10). Thank you.
please select a valid item in range(2, 10). Thank you.
please select a valid item in range(2, 10). Thank you.
please select a valid item in range(2, 10). Thank you.
please select a valid item in range(2, 10). Thank you.
please select a valid item in range(2, 10). Thank you.
please select a valid item in range(2, 10). Thank you.
please select a valid item in range(2, 10). Thank you.
please select a valid item in range(2, 10). Thank you.
please select a valid item in range(2, 10). Thank you.
please select a valid item in range(2, 10). Thank you.
please select a valid item in range(2, 10). Thank you.
please select a valid item in range(2, 10). Thank you.
please select a valid item in range(2, 10). Thank you.
please select a valid item in range(2, 10). Thank you.
ok
test_integerquestion_null (__main__.TestQuestions.test_integerquestion_null) ... ok
test_integerquestion_range (__main__.TestQuestions.test_integerquestion_range) ... please select a valid item in [3, 16]. Thank you.
please select a valid item in [3, 16]. Thank you.
please select a valid item in [3, 16]. Thank you.
please select a valid item in [3, 16]. Thank you.
ok

----------------------------------------------------------------------
Ran 5 tests in 0.012s

OK
"""