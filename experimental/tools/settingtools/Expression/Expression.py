import abc
from abjad.tools.abctools import AbjadObject


class Expression(AbjadObject):
    '''Expression base class.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if not isinstance(expr, type(self)):
            return False
        if not self._positional_argument_values == expr._positional_argument_values:
            return False
        if not self._keyword_argument_values == expr._keyword_argument_values:
            return False
        return True

    ### PRIVATE METHODS ###

    @abc.abstractmethod
    def _evaluate(self):
        pass

    ### PUBLIC METHODS ###

    def new(self, **kwargs):
        positional_argument_dictionary = self._positional_argument_dictionary
        keyword_argument_dictionary = self._keyword_argument_dictionary
        for key, value in kwargs.iteritems():
            if key in positional_argument_dictionary:
                positional_argument_dictionary[key] = value
            elif key in keyword_argument_dictionary:
                keyword_argument_dictionary[key] = value
            else:
                raise KeyError(key)
        positional_argument_values = []
        for positional_argument_name in self._positional_argument_names:
            positional_argument_value = positional_argument_dictionary[positional_argument_name]
            positional_argument_values.append(positional_argument_value)
        result = type(self)(*positional_argument_values, **keyword_argument_dictionary)
        return result
