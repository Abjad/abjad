# -*- coding: utf-8 -*-
from abjad.tools.topleveltools import select
from abjad.tools.selectiontools.Selection import Selection


class Descendants(Selection):
    r'''Descendants of a component.

    ::

        >>> import abjad

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
        from abjad.tools import scoretools
        assert isinstance(component, (scoretools.Component, type(None)))
        if component is None:
            music = ()
        else:
            music = list(select(component).by_class())
            if not include_self:
                music.remove(component)
        result = []
        if cross_offset is None:
            result = music
        else:
            for x in music:
                append_x = True
                if not (x._get_timespan().start_offset < cross_offset and
                    cross_offset < x._get_timespan().stop_offset):
                    append_x = False
                if append_x:
                    result.append(x)
        Selection.__init__(self, result)
        self._component = component

    ### PUBLIC PROPERTIES ###

    @property
    def component(self):
        r'''The component from which the selection was derived.
        '''
        return self._component
