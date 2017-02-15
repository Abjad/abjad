# -*- coding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import scoretools
from abjad.tools import selectiontools
from abjad.tools.topleveltools import inspect_
from abjad.tools.selectortools.Inequality import Inequality


class DurationInequality(Inequality):
    r'''Duration inequality.

    ::

        >>> inequality = selectortools.DurationInequality('<', (3, 4))
        >>> f(inequality)
        selectortools.DurationInequality(
            operator_string='<',
            duration=durationtools.Duration(3, 4),
            )

    ::

        >>> inequality(Duration(1, 2))
        True

    ::

        >>> inequality(Note("c'4"))
        True

    ::

        >>> inequality(Container("c'1 d'1"))
        False

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Inequalities'

    __slots__ = (
        '_duration',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        operator_string='<',
        duration=mathtools.Infinity(),
        ):
        Inequality.__init__(
            self,
            operator_string=operator_string,
            )
        infinities = (
            mathtools.Infinity(),
            mathtools.NegativeInfinity(),
            )
        if duration not in infinities:
            duration = durationtools.Duration(duration)
            assert 0 <= duration
        self._duration = duration

    ### SPECIAL METHODS ###

    def __call__(self, argument):
        r'''Calls duration inequality on `argument`.

        Returns true or false.
        '''
        if isinstance(argument, scoretools.Component):
            duration = inspect_(argument).get_duration()
        elif isinstance(argument, selectiontools.Selection):
            duration = argument.get_duration()
        else:
            duration = durationtools.Duration(argument)
        result = self._operator_function(duration, self._duration)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def duration(self):
        r'''Gets duration.

        Returns duration.
        '''
        return self._duration
