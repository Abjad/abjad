# -*- encoding: utf-8 -*-
import abc
from abjad.tools import abctools
from abjad.tools import scoretools


class Handler(abctools.AbjadObject):

    ### CLASS VARIABLES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        from abjad.tools import systemtools
        return systemtools.StorageFormatManager.compare(self, expr)

    def __format__(self, format_specification=''):
        r'''Formats handler.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        Returns string.
        '''
        if format_specification in ('', 'storage'):
            return self._tools_package_qualified_indented_repr
        return str(self)

    ### PRIVATE PROPERTIES ###

    @abc.abstractproperty
    def _tools_package_name(self):
        pass

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

    ### PUBLIC METHODS ###

    def new(self, *args, **kwargs):
        new = type(self)(*args, **kwargs)
        return new
