from .Selection import Selection


class Descendants(Selection):
    r'''Descendants of a component.

    ..  container:: example

        ::

            >>> score = abjad.Score()
            >>> staff = abjad.Staff(
            ...     r"""\new Voice = "Treble Voice" { c'4 }""",
            ...     name='Treble Staff',
            ...     )
            >>> score.append(staff)
            >>> bass = abjad.Staff(
            ...     r"""\new Voice = "Bass Voice" { b,4 }""",
            ...     name='Bass Staff',
            ...     )
            >>> score.append(bass)

        ..  docs::

            >>> f(score)
            \new Score <<
                \context Staff = "Treble Staff" {
                    \context Voice = "Treble Voice" {
                        c'4
                    }
                }
                \context Staff = "Bass Staff" {
                    \context Voice = "Bass Voice" {
                        b,4
                    }
                }
            >>

        ::

            >>> for component in abjad.inspect(score).get_descendants():
            ...     component
            ...
            <Score<<2>>>
            <Staff-"Treble Staff"{1}>
            Voice("c'4", name='Treble Voice')
            Note("c'4")
            <Staff-"Bass Staff"{1}>
            Voice('b,4', name='Bass Voice')
            Note('b,4')

        ::

            >>> bass_voice = score['Bass Voice']
            >>> agent = abjad.inspect(bass_voice)
            >>> for component in agent.get_descendants():
            ...     component
            ...
            Voice('b,4', name='Bass Voice')
            Note('b,4')

    Descendants is treated as the selection of the component's improper
    descendants.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_component',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        component=None,
        cross_offset=None,
        include_self=True,
        ):
        import abjad
        assert isinstance(component, (abjad.Component, type(None)))
        if component is None:
            components = ()
        else:
            components = list(abjad.select(component).by_class())
            if not include_self:
                components.remove(component)
        result = []
        if cross_offset is None:
            result = components
        else:
            for component in components:
                append_x = True
                if not (component._get_timespan().start_offset < cross_offset and
                    cross_offset < component._get_timespan().stop_offset):
                    append_x = False
                if append_x:
                    result.append(component)
        Selection.__init__(self, result)
        self._component = component

    ### SPECIAL METHODS ###

    def __getitem__(self, argument):
        r'''Gets `argument`.

        Returns component or vanilla selection (not descendants).
        '''
        result = self.items.__getitem__(argument)
        if isinstance(result, tuple):
            result = Selection(result)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def component(self):
        r'''The component from which the selection was derived.
        '''
        return self._component
