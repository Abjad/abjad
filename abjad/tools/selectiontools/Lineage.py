# -*- coding: utf-8 -*-
from abjad.tools.selectiontools.Selection import Selection


class Lineage(Selection):
    r'''A selection of components in the lineage of a component.

    ::

        >>> score = Score()
        >>> score.append(Staff(r"""\new Voice = "Treble Voice" { c'4 }""",
        ... name='Treble Staff'))
        >>> score.append(Staff(r"""\new Voice = "Bass Voice" { b,4 }""",
        ... name='Bass Staff'))

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

        >>> for x in selectiontools.Lineage(score): x
        ...
        <Score<<2>>>
        <Staff-"Treble Staff"{1}>
        Voice("c'4")
        Note("c'4")
        <Staff-"Bass Staff"{1}>
        Voice('b,4')
        Note('b,4')

    ::

        >>> for x in selectiontools.Lineage(score['Bass Voice']): x
        ...
        <Score<<2>>>
        <Staff-"Bass Staff"{1}>
        Voice('b,4')
        Note('b,4')

    Returns lineage.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_component',
        )

    ### INITIALIZER ###

    def __init__(self, component=None):
        from abjad.tools import scoretools
        assert isinstance(component, (scoretools.Component, type(None)))
        music = []
        if component is not None:
            music.extend(reversed(component._get_parentage(include_self=False)))
            music.append(component)
            music.extend(component._get_descendants(include_self=False))
        Selection.__init__(self, music)
        self._component = component

    ### PUBLIC PROPERTIES ###

    @property
    def component(self):
        r'''The component from which the selection was derived.
        '''
        return self._component
