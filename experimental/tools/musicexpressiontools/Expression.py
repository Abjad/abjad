# -*- encoding: utf-8 -*-
import abc
from abjad.tools.abctools import AbjadObject


class Expression(AbjadObject):
    r'''Expression.
    '''

    ### CLASS VARIABLES ###

    __metaclass__ = abc.ABCMeta

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        r'''True expression and `expr` are of the same type
        and when positional and keyword argument values equal.
        Otherwise false.

        Returns boolean.
        '''
        from abjad.tools import systemtools
        return systemtools.StorageFormatManager.compare(self, expr)

    def __format__(self, format_specification=''):
        r'''Formats expression.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatManager.get_storage_format(self)
        return str(self)

    def __hash__(self):
        r'''Expression hash.

        Returns hash of expression repr.
        '''
        return hash(repr(self))

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def evaluate(self):
        r'''Evaluate expression.

        Returns new expression when evaluable.

        Returns none when nonevaluable.
        '''
        pass

    def new(self, **kwargs):
        r'''Initialize new expression with `kwargs`.
        '''
        from abjad.tools import systemtools
        manager = systemtools.StorageFormatManager
        keyword_argument_dictionary = \
            manager.get_keyword_argument_dictionary(self)
        positional_argument_dictionary = \
            manager.get_positional_argument_dictionary(self)
        for key, value in kwargs.iteritems():
            if key in positional_argument_dictionary:
                positional_argument_dictionary[key] = value
            elif key in keyword_argument_dictionary:
                keyword_argument_dictionary[key] = value
            else:
                raise KeyError(key)
        positional_argument_values = []
        for positional_argument_name in \
            manager.get_positional_argument_names(self):
            positional_argument_value = \
                positional_argument_dictionary[positional_argument_name]
            positional_argument_values.append(positional_argument_value)
        result = type(
            self)(*positional_argument_values, **keyword_argument_dictionary)
        return result
