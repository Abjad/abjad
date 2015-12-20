# -*- coding: utf-8 -*-
from abjad.tools import abctools
from abjad.tools import durationtools
from abjad.tools import pitchtools
from abjad.tools import schemetools
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

    _pc_number_to_color = {
        0: schemetools.SchemeColor('red'),
        1: schemetools.SchemeColor('MediumBlue'),
        2: schemetools.SchemeColor('orange'),
        3: schemetools.SchemeColor('LightSlateBlue'),
        4: schemetools.SchemeColor('ForestGreen'),
        5: schemetools.SchemeColor('MediumOrchid'),
        6: schemetools.SchemeColor('firebrick'),
        7: schemetools.SchemeColor('DeepPink'),
        8: schemetools.SchemeColor('DarkOrange'),
        9: schemetools.SchemeColor('IndianRed'),
        10: schemetools.SchemeColor('CadetBlue'),
        11: schemetools.SchemeColor('SeaGreen'),
        12: schemetools.SchemeColor('LimeGreen'),
        }

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

    def color_container(self, color):
        r'''Colors contents of `container`.

        ..  container:: example

            **Example 1.** Colors measure:

            ::

                >>> measure = Measure((2, 8), "c'8 d'8")
                >>> label(measure).color_container('red')
                >>> show(measure) # doctest: +SKIP

            ..  doctest::

                >>> print(format(measure))
                {
                    \override Accidental #'color = #red
                    \override Beam #'color = #red
                    \override Dots #'color = #red
                    \override NoteHead #'color = #red
                    \override Rest #'color = #red
                    \override Stem #'color = #red
                    \override TupletBracket #'color = #red
                    \override TupletNumber #'color = #red
                    \time 2/8
                    c'8
                    d'8
                    \revert Accidental #'color
                    \revert Beam #'color
                    \revert Dots #'color
                    \revert NoteHead #'color
                    \revert Rest #'color
                    \revert Stem #'color
                    \revert TupletBracket #'color
                    \revert TupletNumber #'color
                }

        Returns none.
        '''
        override(self.client).accidental.color = color
        override(self.client).beam.color = color
        override(self.client).dots.color = color
        override(self.client).note_head.color = color
        override(self.client).rest.color = color
        override(self.client).stem.color = color
        override(self.client).tuplet_bracket.color = color
        override(self.client).tuplet_number.color = color

    def color_note_heads(self, color_map=None):
        r'''Colors note heads by `color_map`.

        ..  container:: example

            **Example 1.** Colors chord note heads:

            ::

                >>> chord = Chord([12, 14, 18, 21, 23], (1, 4))
                >>> pitches = [[-12, -10, 4], [-2, 8, 11, 17], [19, 27, 30, 33, 37]]
                >>> colors = ['red', 'blue', 'green']
                >>> color_map = pitchtools.NumberedPitchClassColorMap(pitches, colors)
                >>> label(chord).color_note_heads(color_map)
                >>> show(chord) # doctest: +SKIP

            ..  doctest::

                >>> print(format(chord))
                <
                    \tweak #'color #red
                    c''
                    \tweak #'color #red
                    d''
                    \tweak #'color #green
                    fs''
                    \tweak #'color #green
                    a''
                    \tweak #'color #blue
                    b''
                >4

        ..  container:: example

            **Example 2.** Colors note note head:

            ::

                >>> note = Note("c'4")
                >>> label(note).color_note_heads(color_map)
                >>> show(note) # doctest: +SKIP

            ..  doctest::

                >>> print(format(note))
                \once \override NoteHead #'color = #red
                c'4

        ..  container:: example

            **Example 3.** Colors nothing:

            ::

                >>> staff = Staff([])
                >>> label(staff).color_note_heads(color_map)

        ..  container:: example

            **Example 4.** Colors note heads:

            ::

                >>> staff = Staff("c'8 cs'8 d'8 ds'8 e'8 f'8 fs'8 g'8 gs'8 a'8 as'8 b'8 c''8")
                >>> label(staff).color_note_heads()
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    \once \override NoteHead #'color = #(x11-color 'red)
                    c'8
                    \once \override NoteHead #'color = #(x11-color 'MediumBlue)
                    cs'8
                    \once \override NoteHead #'color = #(x11-color 'orange)
                    d'8
                    \once \override NoteHead #'color = #(x11-color 'LightSlateBlue)
                    ds'8
                    \once \override NoteHead #'color = #(x11-color 'ForestGreen)
                    e'8
                    \once \override NoteHead #'color = #(x11-color 'MediumOrchid)
                    f'8
                    \once \override NoteHead #'color = #(x11-color 'firebrick)
                    fs'8
                    \once \override NoteHead #'color = #(x11-color 'DeepPink)
                    g'8
                    \once \override NoteHead #'color = #(x11-color 'DarkOrange)
                    gs'8
                    \once \override NoteHead #'color = #(x11-color 'IndianRed)
                    a'8
                    \once \override NoteHead #'color = #(x11-color 'CadetBlue)
                    as'8
                    \once \override NoteHead #'color = #(x11-color 'SeaGreen)
                    b'8
                    \once \override NoteHead #'color = #(x11-color 'red)
                    c''8
                }

        Returns none.
        '''
        color_map = color_map or self._pc_number_to_color
        for leaf in iterate(self.client).by_class(scoretools.Leaf):
            if isinstance(leaf, scoretools.Chord):
                for note_head in leaf.note_heads:
                    pc = note_head.written_pitch.numbered_pitch_class
                    color = color_map.get(pc, None)
                    if color is not None:
                        note_head.tweak.color = color
            elif isinstance(leaf, scoretools.Note):
                note_head = leaf.note_head
                pc = note_head.written_pitch.numbered_pitch_class
                color = color_map[pc.pitch_class_number]
                if color is not None:
                    override(leaf).note_head.color = color

    def color_leaves(self, color):
        r"""Colors leaves.

        ..  container:: example

            **Example 1.** Colors leaves red:

            ::

                >>> staff = Staff("cs'8. [ r8. s8. <c' cs' a'>8. ]")
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    cs'8. [
                    r8.
                    s8.
                    <c' cs' a'>8. ]
                }

            ::

                >>> label(staff).color_leaves('red')
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