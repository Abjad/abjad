# -*- coding: utf-8 -*-
from abjad.tools.topleveltools import select
from abjad.tools.selectiontools.Selection import Selection


class Descendants(Selection):
    r'''A selection of components that descend from a component.

    ::

        >>> score = Score()
        >>> score.append(Staff(r"""\new Voice = "Treble Voice" { c'4 }""",
        ...     name='Treble Staff'))
        >>> score.append(Staff(r"""\new Voice = "Bass Voice" { b,4 }""",
        ...     name='Bass Staff'))

    ..  doctest::

        >>> print(format(score))
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

        >>> for x in selectiontools.Descendants(score): x
        ...
        <Score<<2>>>
        <Staff-"Treble Staff"{1}>
        Voice("c'4")
        Note("c'4")
        <Staff-"Bass Staff"{1}>
        Voice('b,4')
        Note('b,4')

    ::

        >>> for x in selectiontools.Descendants(score['Bass Voice']): x
        ...
        Voice('b,4')
        Note('b,4')

    Descendants is treated as the selection of the component's
    improper descendants.

    Returns descendants.
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
