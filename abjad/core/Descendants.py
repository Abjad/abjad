import collections
from abjad.system.StorageFormatManager import StorageFormatManager


class Descendants(collections.abc.Sequence):
    r'''
    Descendants of a component.

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

        >>> for component in abjad.inspect(score).descendants():
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
        >>> agent = abjad.inspect(bass_voice)
        >>> for component in agent.descendants():
        ...     component
        ...
        Voice('b,4', name='Bass_Voice')
        Note('b,4')

    Descendants is treated as the component's improper descendants.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = "Selections"

    __slots__ = ("_component", "_components")

    ### INITIALIZER ###

    def __init__(self, component=None, cross_offset=None):
        import abjad

        assert isinstance(component, (abjad.Component, type(None)))
        self._component = component
        if component is None:
            components = ()
        else:
            components = list(abjad.select(component).components())
        result = []
        if cross_offset is None:
            result = components
        else:
            for component in components:
                append_x = True
                if not (
                    abjad.inspect(component).timespan().start_offset
                    < cross_offset
                    and cross_offset
                    < abjad.inspect(component).timespan().stop_offset
                ):
                    append_x = False
                if append_x:
                    result.append(component)
        self._components = tuple(result)

    ### SPECIAL METHODS ###

    def __getitem__(self, argument):
        """
        Gets ``argument``.

        Returns component or tuple of components.
        """
        return self.components.__getitem__(argument)

    def __len__(self):
        """
        Gets length of descendants.

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
        The component from which descendants were derived.
        """
        return self._component

    @property
    def components(self):
        """
        Gets components.

        Returns tuple.
        """
        return self._components
