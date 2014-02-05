# -*- encoding: utf-8 -*-
import abc
from abjad.tools.abctools.AbjadObject import AbjadObject


class TimeRelation(AbjadObject):
    r'''A time relation.

    Time relations are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, inequality=None):
        from abjad.tools import timespantools
        default_inequality = timespantools.CompoundInequality([
            'timespan_1.start_offset < timespan_2.start_offset',
            ])
        inequality = inequality or default_inequality
        assert isinstance(
            inequality, timespantools.CompoundInequality), repr(inequality)
        self._inequality = inequality

    ### SPECIAL METHODS ###

    @abc.abstractmethod
    def __call__(self):
        r'''Evaluates time relation.

        Returns boolean.
        '''
        pass

    @abc.abstractmethod
    def __eq__(self, expr):
        r'''Is true when `expr` is a equal-valued time relation.
        Otherwise false.

        Returns boolean.
        '''
        pass

    def __format__(self, format_specification=''):
        r'''Formats time relation.

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatManager.get_storage_format(self)
        return str(self)

    ### PUBLIC PROPERTIES ###

    @property
    def inequality(self):
        r'''Time relation inequality.

        Return ineqality.
        '''
        return self._inequality

    @abc.abstractproperty
    def is_fully_loaded(self):
        r'''Is true when both time relation terms are not none.
        Otherwise false:

        Returns boolean.
        '''
        pass

    @abc.abstractproperty
    def is_fully_unloaded(self):
        r'''Is true when both time relation terms are none.
        Otherwise false:

        Returns boolean.
        '''
        pass
