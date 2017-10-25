import collections
from abjad.tools import abctools


class Descendants(abctools.AbjadObject):
    r'''Descendants of a component.

    ..  container:: example

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

            >>> abjad.f(score)
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

        >>> bass_voice = score['Bass Voice']
        >>> agent = abjad.inspect(bass_voice)
        >>> for component in agent.get_descendants():
        ...     component
        ...
        Voice('b,4', name='Bass Voice')
        Note('b,4')

    Descendants is treated as the component's improper descendants.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Selections'

    __slots__ = (
        '_component',
        '_components',
        )

    ### INITIALIZER ###

    def __init__(self, component=None, cross_offset=None, include_self=True):
        import abjad
        assert isinstance(component, (abjad.Component, type(None)))
        self._component = component
        if component is None:
            components = ()
        else:
            components = list(abjad.select(component).components())
            if not include_self:
                components.remove(component)
        result = []
        if cross_offset is None:
            result = components
        else:
            for component in components:
                append_x = True
                if not (abjad.inspect(component).get_timespan().start_offset < cross_offset and
                    cross_offset < abjad.inspect(component).get_timespan().stop_offset):
                    append_x = False
                if append_x:
                    result.append(component)
        self._components = tuple(result)

    ### SPECIAL METHODS ###

    def __getitem__(self, argument):
        r'''Gets `argument`.

        Returns component or tuple of components.
        '''
        return self.components.__getitem__(argument)

    ### PUBLIC PROPERTIES ###

    @property
    def component(self):
        r'''The component from which descendants were derived.
        '''
        return self._component

    @property
    def components(self):
        r'''Gets components.

        Returns tuple.
        '''
        return self._components


collections.Sequence.register(Descendants)
