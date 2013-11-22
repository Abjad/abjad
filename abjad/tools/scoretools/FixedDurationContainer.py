# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools.scoretools.Container import Container


class FixedDurationContainer(Container):
    r'''A fixed-duration container.

    ::

        >>> container = scoretools.FixedDurationContainer(
        ...     (3, 8), "c'8 d'8 e'8")

    ::

        >>> container
        FixedDurationContainer(Duration(3, 8), [Note("c'8"), Note("d'8"), Note("e'8")])

    ..  doctest::

        >>> print format(container)
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

    __slots__ = (
        '_target_duration',
        )

    ### INITIALIZER ###

    def __init__(self, target_duration, music=None, **kwargs):
        Container.__init__(self, music=music, **kwargs)
        target_duration = durationtools.Duration(target_duration)
        assert 0 < target_duration
        self._target_duration = target_duration

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '{}({!r}, {})'.format(
            type(self).__name__, self.target_duration, list(self[:]))

    ### PRIVATE METHODS ###

    def _check_duration(self):
        from abjad.tools import indicatortools
        preprolated_duration = self._contents_duration
        if preprolated_duration < self.target_duration:
            raise UnderfullContainerError
        if self.target_duration < preprolated_duration:
            raise OverfullContainerError

    @property
    def _lilypond_format(self):
        self._check_duration()
        return self._format_component()

    ### PUBLIC PROPERTIES ###

    @property
    def is_full(self):
        r'''True when preprolated duration equals target duration.
        '''
        return self._preprolated_duration == self.target_duration

    @property
    def is_misfilled(self):
        r'''True when preprolated duration does not equal target duration.
        '''
        return not self.is_full

    @property
    def is_overfull(self):
        r'''True when preprolated duration is greater than target duration.
        '''
        return self.target_duration < self._preprolated_duration

    @property
    def is_underfull(self):
        r'''True when preprolated duration is less than target duration.
        '''
        return self._preprolated_duration < self.target_duration

    @property
    def target_duration(self):
        r'''Read / write target duration of fixed-duration container.
        '''
        return self._target_duration

    @target_duration.setter
    def target_duration(self, target_duration):
        target_duration = durationtools.Duration(target_duration)
        assert 0 < target_duration
        self._target_duration = target_duration
