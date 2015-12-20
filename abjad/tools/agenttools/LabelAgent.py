# -*- coding: utf-8 -*-
from abjad.tools import abctools
from abjad.tools import durationtools
from abjad.tools import scoretools
from abjad.tools.topleveltools import override
from abjad.tools.topleveltools import iterate


class LabelAgent(abctools.AbjadObject):
    r'''A wrapper around the Abjad label methods.

    ..  container:: example

        ::

            >>> staff = Staff("c'4 e'4 d'4 f'4")
            >>> show(staff) # doctest: +SKIP

        ::

            >>> label(staff)
            LabelAgent(client=Staff("c'4 e'4 d'4 f'4"))

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_client',
        )

    ### INITIALIZER ###

    def __init__(self, client=None):
        from abjad.tools import scoretools
        from abjad.tools import selectiontools
        from abjad.tools import spannertools
        prototype = (
            scoretools.Component, 
            selectiontools.Selection,
            spannertools.Spanner, 
            type(None),
            )
        assert isinstance(client, prototype), repr(client)
        self._client = client

    ### PUBLIC PROPERTIES ###

    @property
    def client(self):
        r'''Gets client of inspection agent.

        Returns component, selection, spanner or none.
        '''
        return self._client

    ### PRIVATE METHODS ###

    def _color_leaf(self, leaf, color):
        if isinstance(leaf, (scoretools.Note, scoretools.Chord)):
            override(leaf).accidental.color = color
            override(leaf).beam.color = color
            override(leaf).dots.color = color
            override(leaf).note_head.color = color
            override(leaf).stem.color = color
        elif isinstance(leaf, scoretools.Rest):
            override(leaf).dots.color = color
            override(leaf).rest.color = color
        return leaf

    ### PUBLIC METHODS ###

    def color_leaves(self, color):
        r"""Colors leaves.

        ..  container:: example

            **Example 1.** Colors leaves red:

            ::

                >>> staff = Staff("cs'8. [ r8. s8. <c' cs' a'>8. ]")

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    cs'8. [
                    r8.
                    s8.
                    <c' cs' a'>8. ]
                }

            ::

                >>> show(staff) # doctest: +SKIP

            ::

                >>> label(staff).color_leaves('red')

            ::

                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    \once \override Accidental #'color = #red
                    \once \override Beam #'color = #red
                    \once \override Dots #'color = #red
                    \once \override NoteHead #'color = #red
                    \once \override Stem #'color = #red
                    cs'8. [
                    \once \override Dots #'color = #red
                    \once \override Rest #'color = #red
                    r8.
                    s8.
                    \once \override Accidental #'color = #red
                    \once \override Beam #'color = #red
                    \once \override Dots #'color = #red
                    \once \override NoteHead #'color = #red
                    \once \override Stem #'color = #red
                    <c' cs' a'>8. ]
                }

        Returns none.
        """
        for leaf in iterate(self.client).by_class(scoretools.Leaf):
            self._color_leaf(leaf, color)