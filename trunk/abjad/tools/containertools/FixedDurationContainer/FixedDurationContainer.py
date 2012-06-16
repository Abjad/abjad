from abjad.tools import durationtools
from abjad.tools.containertools.Container import Container


class FixedDurationContainer(Container):
    r'''.. versionadded:: 2.9

    Fixed-duration container::

        >>> container = containertools.FixedDurationContainer((3, 8), "c'8 d'8 e'8")

    ::

        >>> container
        FixedDurationContainer(Duration(3, 8), [Note("c'8"), Note("d'8"), Note("e'8")])

    ::

        >>> f(container)
        {
            c'8
            d'8
            e'8
        }


    Fixed-duration containers extend container behavior with format-time
    checking against a user-specified target duration.

    Return fixed-duration container.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_target_duration', )

    ### INITIALIZER ###

    def __init__(self, target_duration, music=None, **kwargs):
        Container.__init__(self, music=music, **kwargs)
        target_duration = durationtools.Duration(target_duration)
        assert 0 < target_duration
        self._target_duration = target_duration

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '{}({!r}, {})'.format(self._class_name, self.target_duration, self[:])

    ### PRIVATE METHODS ###

    def _check_duration(self):
        from abjad.tools import contexttools
        preprolatedg_duration = self.contents_duration
        if preprolatedg_duration < self.target_duration:
            raise UnderfullContainerError
        if self.target_duration < preprolatedg_duration:
            raise OverfullContainerError

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def lilypond_format(self):
        '''Read-only LilyPond format of fixed-duration container.
        '''
        self._check_duration()
        return self._format_component()

    @property
    def is_full(self):
        '''True when preprolated duration equals target duration.
        '''
        return self.preprolated_duration == self.target_duration

    @property
    def is_misfilled(self):
        '''True when preprolated duration does not equal target duration.
        '''
        return not self.is_full

    @property
    def is_overfull(self):
        '''True when preprolated duration is greater than target duration.
        '''
        return self.target_duration < self.preprolated_duration

    @property
    def is_underfull(self):
        '''True when preprolated duration is less than target duration.
        '''
        return self.preprolated_duration < self.target_duration

    ### READ / WRITE PUBLIC PROPERTIES ###

    @apply
    def target_duration():
        def fget(self):
            '''Read / write target duration of fixed-duration container.
            '''
            return self._target_duration
        def fset(self, target_duration):
            target_duration = durationtools.Duration(target_duration)
            assert 0 < target_duration
            self._target_duration = target_duration
        return property(**locals())
