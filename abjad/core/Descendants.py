import collections
import typing

from abjad.system.StorageFormatManager import StorageFormatManager
from abjad.top.inspect import inspect
from abjad.top.select import select

from .Component import Component


class Descendants(collections.abc.Sequence):
    r'''
    Descendants of a component.

    ..  container:: example

        >>> score = abjad.Score()
        >>> staff = abjad.Staff(
        ...     r"""\new Voice = "Treble_Voice" { c'4 }""",
        ...     name="Treble_Staff",
        ...     )
        >>> score.append(staff)
        >>> bass = abjad.Staff(
        ...     r"""\new Voice = "Bass_Voice" { b,4 }""",
        ...     name="Bass_Staff",
        ...     )
        >>> score.append(bass)
        >>> abjad.show(score) # doctest: +SKIP

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

        >>> bass_voice = score["Bass_Voice"]
        >>> agent = abjad.inspect(bass_voice)
        >>> for component in agent.descendants():
        ...     component
        ...
        Voice('b,4', name='Bass_Voice')
        Note('b,4')

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = "Selections"

    __slots__ = ("_component", "_components")

    ### INITIALIZER ###

    def __init__(self, component=None, cross_offset=None):
        assert isinstance(component, (Component, type(None)))
        self._component = component
        if component is None:
            components = ()
        else:
            components = list(select(component).components())
        result = []
        if cross_offset is None:
            result = components
        else:
            for component in components:
                append_x = True
                if not (
                    inspect(component).timespan().start_offset < cross_offset
                    and cross_offset < inspect(component).timespan().stop_offset
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

    def __len__(self) -> int:
        """
        Gets length of descendants.
        """
        return len(self._components)

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PUBLIC PROPERTIES ###

    @property
    def component(self) -> Component:
        """
        Gets component.
        """
        return self._component

    @property
    def components(self) -> typing.Tuple[Component]:
        """
        Gets components.
        """
        return self._components

    def count(self, prototype=None) -> int:
        r"""
        Gets number of ``prototype`` in descendants.

        ..  container:: example

            Gets tuplet count:

            >>> staff = abjad.Staff(
            ...     r"\times 2/3 { c'2 \times 2/3 { d'8 e' f' } } \times 2/3 { c'4 d' e' }"
            ... )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \times 2/3 {
                        c'2
                        \times 2/3 {
                            d'8
                            e'8
                            f'8
                        }
                    }
                    \times 2/3 {
                        c'4
                        d'4
                        e'4
                    }
                }

            >>> for component in abjad.select(staff).components():
            ...     parentage = abjad.inspect(component).descendants()
            ...     count = parentage.count(abjad.Tuplet)
            ...     print(f"{repr(component):55} {repr(count)}")
            <Staff{2}>                                              3
            Tuplet(Multiplier(2, 3), "c'2 { 2/3 d'8 e'8 f'8 }")     2
            Note("c'2")                                             0
            Tuplet(Multiplier(2, 3), "d'8 e'8 f'8")                 1
            Note("d'8")                                             0
            Note("e'8")                                             0
            Note("f'8")                                             0
            Tuplet(Multiplier(2, 3), "c'4 d'4 e'4")                 1
            Note("c'4")                                             0
            Note("d'4")                                             0
            Note("e'4")                                             0

        """
        n = 0
        if prototype is None:
            prototype = Component
        for component in self:
            if isinstance(component, prototype):
                n += 1
        return n
