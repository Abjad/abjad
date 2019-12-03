import collections

from abjad.system.StorageFormatManager import StorageFormatManager


class Lineage(collections.abc.Sequence):
    r'''
    Lineage of a component.

    ..  container:: example

        >>> score = abjad.Score()
        >>> staff = abjad.Staff(
        ...     r"""\new Voice = "Treble_Voice" { c'4 }""",
        ...     name='Treble_Staff',
        ...     )
        >>> score.append(staff)
        >>> bass = abjad.Staff(
        ...     r"""\new Voice = "Bass_Voice" { b,4 }""",
        ...     name='Bass_Staff',
        ...     )
        >>> score.append(bass)

        ..  docs::

            >>> abjad.f(score)
            \new Score
            <<
                \context Staff = "Treble_Staff"
                {
                    \context Voice = "Treble_Voice"
                    {
                        c'4
                    }
                }
                \context Staff = "Bass_Staff"
                {
                    \context Voice = "Bass_Voice"
                    {
                        b,4
                    }
                }
            >>

        >>> for component in abjad.inspect(score).lineage():
        ...     component
        ...
        <Score<<2>>>
        <Staff-"Treble_Staff"{1}>
        Voice("c'4", name='Treble_Voice')
        Note("c'4")
        <Staff-"Bass_Staff"{1}>
        Voice('b,4', name='Bass_Voice')
        Note('b,4')

        >>> bass_voice = score['Bass_Voice']
        >>> for component in abjad.inspect(bass_voice).lineage():
        ...     component
        ...
        <Score<<2>>>
        <Staff-"Bass_Staff"{1}>
        Voice('b,4', name='Bass_Voice')
        Note('b,4')

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = "Selections"

    __slots__ = ("_component", "_components")

    ### INITIALIZER ###

    def __init__(self, component=None):
        import abjad

        assert isinstance(component, (abjad.Component, type(None)))
        self._component = component
        components = []
        if component is not None:
            components.extend(reversed(abjad.inspect(component).parentage()[1:]))
            components.append(component)
            components.extend(abjad.inspect(component).descendants()[1:])
        self._components = components

    ### SPECIAL METHODS ###

    def __getitem__(self, argument):
        """
        Gets ``argument``.

        Returns component or tuple.
        """
        return self.components.__getitem__(argument)

    def __len__(self):
        """
        Gets length of lineage.

        Returns int.
        """
        return len(self._components)

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PUBLIC PROPERTIES ###

    @property
    def component(self):
        """
        The component from which the lineage was derived.
        """
        return self._component

    @property
    def components(self):
        """
        Gets components.

        Returns tuple.
        """
        return self._components
