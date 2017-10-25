import collections
from abjad.tools import abctools


class Lineage(abctools.AbjadObject):
    r'''Lineage of a component.

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

        >>> for component in abjad.inspect(score).get_lineage():
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
        >>> for component in abjad.inspect(bass_voice).get_lineage():
        ...     component
        ...
        <Score<<2>>>
        <Staff-"Bass Staff"{1}>
        Voice('b,4', name='Bass Voice')
        Note('b,4')

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Selections'

    __slots__ = (
        '_component',
        '_components',
        )

    ### INITIALIZER ###

    def __init__(self, component=None):
        import abjad
        assert isinstance(component, (abjad.Component, type(None)))
        self._component = component
        components = []
        if component is not None:
            components.extend(
                reversed(
                abjad.inspect(component).get_parentage(include_self=False)))
            components.append(component)
            components.extend(
                abjad.inspect(component).get_descendants(include_self=False))
        self._components = components

    ### SPECIAL METHODS ###

    def __getitem__(self, argument):
        r'''Gets `argument`.

        Returns component or tuple.
        '''
        return self.components.__getitem__(argument)

    ### PUBLIC PROPERTIES ###

    @property
    def component(self):
        r'''The component from which the lineage was derived.
        '''
        return self._component

    @property
    def components(self):
        r'''Gets components.

        Returns tuple.
        '''
        return self._components


collections.Sequence.register(Lineage)
