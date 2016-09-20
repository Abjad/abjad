# -*- coding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools.scoretools.Container import Container


class FixedDurationContainer(Container):
    r'''A fixed-duration container.

    ::

        >>> container = scoretools.FixedDurationContainer(
        ...     (3, 8), "c'8 d'8 e'8")
        >>> show(container) # doctest: +SKIP

    ..  doctest::

        >>> print(format(container))
        {
            c'8
            d'8
            e'8
        }


    Fixed-duration containers extend container behavior with format-time
    checking against a user-specified target duration.

    Returns fixed-duration container.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Containers'

    __slots__ = (
        '_target_duration',
        )

    ### INITIALIZER ###

    def __init__(self, target_duration=None, music=None, **kwargs):
        Container.__init__(self, music=music, **kwargs)
        target_duration = target_duration or durationtools.Duration(1, 4)
        target_duration = durationtools.Duration(target_duration)
        assert 0 < target_duration
        self._target_duration = target_duration

    ### SPECIAL METHODS ###

    def __repr__(self):
        r'''Gets interpreter representation of fixed-duration container.

        Returns string.
        '''
        result = '{}({!r}, {})'
        result = result.format(
            type(self).__name__,
            self.target_duration,
            list(self[:]),
            )
        return result

    ### PRIVATE METHODS ###

    def _check_duration(self):
        from abjad.tools import indicatortools
        preprolated_duration = self._contents_duration
        if preprolated_duration < self.target_duration:
            raise UnderfullContainerError
        if self.target_duration < preprolated_duration:
            raise OverfullContainerError

    ### PRIVATE PROPERTIES ###

    @property
    def _lilypond_format(self):
        self._check_duration()
        return self._format_component()

    ### PUBLIC PROPERTIES ###

    @property
    def is_full(self):
        r'''Is true when preprolated duration equals target duration. Otherwise
        false.

        Returns true or false.
        '''
        return self._preprolated_duration == self.target_duration

    @property
    def is_misfilled(self):
        r'''Is true when preprolated duration does not equal target duration.
        Otherwise false.

        Returns true or false.
        '''
        return not self.is_full

    @property
    def is_overfull(self):
        r'''Is true when preprolated duration is greater than target duration.
        Otherwise false.

        Returns true or false.
        '''
        return self.target_duration < self._preprolated_duration

    @property
    def is_underfull(self):
        r'''Is true when preprolated duration is less than target duration.
        Otherwise false.

        Returns true or false.
        '''
        return self._preprolated_duration < self.target_duration

    @property
    def target_duration(self):
        r'''Gets and sets target duration of fixed-duration container.

        Returns duration.
        '''
        return self._target_duration

    @target_duration.setter
    def target_duration(self, target_duration):
        target_duration = durationtools.Duration(target_duration)
        assert 0 < target_duration
        self._target_duration = target_duration
