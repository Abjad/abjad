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
