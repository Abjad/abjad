import abc
from abjad.tools.abctools import AbjadObject


class Expression(AbjadObject):
    '''Expression.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        '''True expression and `expr` are of the same type
        and when positional and keyword argument values equal.
        Otherwise false.

        Return boolean.
        '''
        if not isinstance(expr, type(self)):
            return False
        if not self._positional_argument_values == expr._positional_argument_values:
            return False
        if not self._keyword_argument_values == expr._keyword_argument_values:
            return False
        return True

    def __hash__(self):
        '''Expression hash.
        
        Return hash of expression repr.
        '''
        return hash(repr(self))

    ### PRIVATE METHODS ###

    def _get_tools_package_qualified_keyword_argument_repr_pieces(self, is_indented=True):
        filtered_result = []
        result = AbjadObject._get_tools_package_qualified_keyword_argument_repr_pieces(
            self, is_indented=is_indented)
        for string in result:
            if not 'callbacks=specificationtools.CallbackInventory([])' in string:
                filtered_result.append(string)
        return filtered_result

    @property
    def _keyword_argument_name_value_strings(self):
        result = AbjadObject._keyword_argument_name_value_strings.fget(self)
        if 'callbacks=CallbackInventory([])' in result:
            result = list(result)
            result.remove('callbacks=CallbackInventory([])')
        return tuple(result)

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def evaluate(self):
        '''Evaluate expression.

        Return new expression when evaluable.

        Return none when nonevaluable.
        '''
        pass

    def new(self, **kwargs):
        '''Initialize new expression with `kwargs`.
        '''
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
