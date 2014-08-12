# -*- encoding: utf-8 -*-
import abc
from abjad.tools import abctools
from abjad.tools import scoretools


class Handler(abctools.AbjadValueObject):
    r'''Handler.
    '''

    ### CLASS VARIABLES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        r'''Copies handler.

        Returns new handler.
        '''
        return type(self)(*self.__getnewargs__())

    def __deepcopy__(self, *args):
        r'''Deecopies handler.

        Returns new handler.
        '''
        return type(self)(*self.__getnewargs__())

    def __eq__(self, expr):
        r'''Is true when `expr` is a handler with the same type and
        initializer parameter values as this one.

        Returns boolean.
        '''
        from abjad.tools import systemtools
        return systemtools.StorageFormatManager.compare(self, expr)

    def __format__(self, format_specification=''):
        r'''Formats handler.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatManager.get_storage_format(self)
        return str(self)

    def __getnewargs__(self):
        r'''Gets new arguments of handler.

        Returns tuple.
        '''
        from abjad.tools import systemtools
        return systemtools.StorageFormatManager.get_input_argument_values(
            self)

    ### PRIVATE METHODS ###

    @staticmethod
    def _remove_outer_rests_from_sequence(sequence):
        first_keep_index = None
        for i, element in enumerate(sequence):
            if not isinstance(element, scoretools.Rest):
                first_keep_index = i
                break
        last_keep_index = None
        for i, element in enumerate(reversed(sequence)):
            if not isinstance(element, scoretools.Rest):
                last_keep_index = len(sequence) - i
                break
        return sequence[first_keep_index:last_keep_index]