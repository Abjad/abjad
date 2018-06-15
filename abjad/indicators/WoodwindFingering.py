import collections
import typing
from abjad.system.AbjadObject import AbjadObject
from abjad.markups import MarkupCommand
from abjad.scheme import Scheme
from abjad.scheme import SchemePair
from abjad.system.StorageFormatManager import StorageFormatManager


class WoodwindFingering(AbjadObject):
    r"""
    Woodwind fingering.

    ..  container:: example

        Initializes from a valid instrument name and up to three keyword lists
        or tuples:

        >>> center_column = ('one', 'two', 'three', 'five')
        >>> left_hand = ('R', 'thumb')
        >>> right_hand = ('e',)
        >>> woodwind_fingering = abjad.WoodwindFingering(
        ...     name='clarinet',
        ...     center_column=center_column,
        ...     left_hand=left_hand,
        ...     right_hand=right_hand,
        ...     )

        >>> print(format(woodwind_fingering, 'storage'))
        abjad.WoodwindFingering(
            name='clarinet',
            center_column=('one', 'two', 'three', 'five'),
            left_hand=('R', 'thumb'),
            right_hand=('e',),
            )

    ..  container:: example

        Initializes a WoodwindFingering from another WoodwindFingering:

        >>> woodwind_fingering_2 = abjad.WoodwindFingering(
        ...     woodwind_fingering)
        >>> print(format(woodwind_fingering_2))
        abjad.WoodwindFingering(
            name='clarinet',
            center_column=('one', 'two', 'three', 'five'),
            left_hand=('R', 'thumb'),
            right_hand=('e',),
            )

    ..  container:: exmaple

        Calls Woodwind fingering to create woodwind diagram markup command:

        >>> fingering_command = woodwind_fingering()
        >>> print(format(fingering_command, 'storage'))
        abjad.MarkupCommand(
            'woodwind-diagram',
            abjad.Scheme(
                'clarinet',
                quoting="'",
                ),
            abjad.Scheme(
                [
                    abjad.SchemePair(('cc', ('one', 'two', 'three', 'five'))),
                    abjad.SchemePair(('lh', ('R', 'thumb'))),
                    abjad.SchemePair(('rh', ('e',))),
                    ],
                quoting="'",
                )
            )

    ..  container:: example

        Attaches the MarkupCommand to score components, such as a chord
        representing a multiphonic sound:

        >>> markup = abjad.Markup(contents=fingering_command, direction=abjad.Down)
        >>> chord = abjad.Chord("<ds' fs''>4")
        >>> abjad.attach(markup, chord)
        >>> abjad.show(chord) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(chord)
            <ds' fs''>4
            _ \markup {
                \woodwind-diagram
                    #'clarinet
                    #'((cc . (one two three five)) (lh . (R thumb)) (rh . (e)))
                }

    ..  container:: example

        Initializes fingerings for eight different woodwind instruments:

        >>> names = [
        ...     'piccolo', 'flute', 'oboe', 'clarinet', 'bass-clarinet',
        ...     'saxophone', 'bassoon', 'contrabassoon',
        ...     ]
        >>> for name in names:
        ...    abjad.WoodwindFingering(name)
        ...
        WoodwindFingering(name='piccolo', center_column=(), left_hand=(), right_hand=())
        WoodwindFingering(name='flute', center_column=(), left_hand=(), right_hand=())
        WoodwindFingering(name='oboe', center_column=(), left_hand=(), right_hand=())
        WoodwindFingering(name='clarinet', center_column=(), left_hand=(), right_hand=())
        WoodwindFingering(name='bass-clarinet', center_column=(), left_hand=(), right_hand=())
        WoodwindFingering(name='saxophone', center_column=(), left_hand=(), right_hand=())
        WoodwindFingering(name='bassoon', center_column=(), left_hand=(), right_hand=())
        WoodwindFingering(name='contrabassoon', center_column=(), left_hand=(), right_hand=())

    ..  container:: example

        An override displays diagrams symbolically instead of graphically:

        >>> chord = abjad.Chord("<e' as' gqf''>1")
        >>> fingering = abjad.WoodwindFingering(
        ...     'clarinet',
        ...     center_column=['one', 'two', 'three', 'four'],
        ...     left_hand=['R','cis'],
        ...     right_hand=['fis'])
        >>> diagram = fingering()
        >>> not_graphical = abjad.MarkupCommand(
        ...     'override',
        ...     abjad.SchemePair(('graphical', False)),
        ...     )
        >>> markup = abjad.Markup(contents=
        ...     [not_graphical, diagram], direction=abjad.Down)
        >>> abjad.attach(markup, chord)
        >>> abjad.show(chord) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(chord)
            <e' as' gqf''>1
            _ \markup {
                \override
                    #'(graphical . #f)
                \woodwind-diagram
                    #'clarinet
                    #'((cc . (one two three four)) (lh . (R cis)) (rh . (fis)))
                }

    ..  container:: example

        The thickness and size of diagrams can also be changed with overrides:

        >>> chord = abjad.Chord("<e' as' gqf''>1")
        >>> fingering = abjad.WoodwindFingering(
        ...     'clarinet',
        ...     center_column=('one', 'two', 'three', 'four'),
        ...     left_hand=('R', 'cis'),
        ...     right_hand=('fis',),
        ...     )
        >>> diagram = fingering()
        >>> not_graphical = abjad.MarkupCommand(
        ...     'override',
        ...     abjad.SchemePair(('graphical', False)),
        ...     )
        >>> size = abjad.MarkupCommand(
        ...     'override',
        ...     abjad.SchemePair(('size', .5)),
        ...     )
        >>> thickness = abjad.MarkupCommand(
        ...     'override',
        ...     abjad.SchemePair(('thickness', .4)),
        ...     )
        >>> markup = abjad.Markup(
        ...     contents=[not_graphical, size, thickness, diagram],
        ...     direction=abjad.Down,
        ...     )
        >>> abjad.attach(markup, chord)
        >>> abjad.show(chord) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(chord)
            <e' as' gqf''>1
            _ \markup {
                \override
                    #'(graphical . #f)
                \override
                    #'(size . 0.5)
                \override
                    #'(thickness . 0.4)
                \woodwind-diagram
                    #'clarinet
                    #'((cc . (one two three four)) (lh . (R cis)) (rh . (fis)))
                }

    Inspired by Mike Solomon's LilyPond woodwind diagrams.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_center_column',
        '_name',
        '_left_hand',
        '_right_hand',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        name: typing.Union[str, 'WoodwindFingering'] = 'flute',
        *,
        center_column: typing.Iterable = None,
        left_hand: typing.Iterable = None,
        right_hand: typing.Iterable = None,
        ) -> None:
        assert isinstance(center_column, (type(None), collections.Iterable))
        assert isinstance(left_hand, (type(None), collections.Iterable))
        assert isinstance(right_hand, (type(None), collections.Iterable))
        # initialize from a string and up to three lists
        if isinstance(name, str):
            assert name in self._valid_names
            self._name = name
            if center_column is None:
                self._center_column: typing.Tuple[str, ...] = ()
            else:
                self._center_column = tuple(center_column)
            if left_hand is None:
                self._left_hand: typing.Tuple[str, ...] = ()
            else:
                self._left_hand = tuple(left_hand)
            if right_hand is None:
                self._right_hand: typing.Tuple[str, ...] = ()
            else:
                self._right_hand = tuple(right_hand)
        # initialize from WoodwindDiagram with up to three overriding lists
        elif isinstance(name, type(self)):
            self._name = name.name
            self._center_column = name.center_column
            self._left_hand = name.left_hand
            self._right_hand = name.right_hand
            if center_column is not None:
                self._center_column = tuple(center_column)
            if left_hand is not None:
                self._left_hand = tuple(left_hand)
            if right_hand is not None:
                self._right_hand = tuple(right_hand)

    ### SPECIAL METHODS ###

    def __call__(self) -> MarkupCommand:
        """
        Calls woodwind fingering.
        """
        key_groups_as_scheme = []
        cc_scheme_pair = SchemePair(('cc', self._center_column))
        key_groups_as_scheme.append(cc_scheme_pair)
        lh_scheme_pair = SchemePair(('lh', self._left_hand))
        key_groups_as_scheme.append(lh_scheme_pair)
        rh_scheme_pair = SchemePair(('rh', self._right_hand))
        key_groups_as_scheme.append(rh_scheme_pair)
        key_groups_as_scheme_ = Scheme(
            key_groups_as_scheme,
            quoting="'",
            )
        instrument_as_scheme = Scheme(self._name, quoting="'")
        return MarkupCommand(
            'woodwind-diagram',
            instrument_as_scheme,
            key_groups_as_scheme_,
            )

    def __format__(self, format_specification='') -> str:
        """
        Formats woodwind fingering.

        Set ``format_specification`` to `''` or `'storage'`.
        """
        if format_specification in ('', 'storage'):
            return StorageFormatManager(self).get_storage_format()
        raise ValueError(format_specification)

    ### PRIVATE PROPERTIES ###

    @property
    def _valid_names(self):
        return (
            'piccolo',
            'flute',
            'oboe',
            'clarinet',
            'bass-clarinet',
            'saxophone',
            'bassoon',
            'contrabassoon',
            )

    ### PUBLIC METHODS ###

    def print_guide(self) -> None:
        """
        Print read-only string containing instrument's valid key strings,
        instrument diagram, and syntax explanation.

        ..  container:: example

            >>> center_column = ('one', 'two', 'three', 'five')
            >>> left_hand = ('R', 'thumb')
            >>> right_hand = ('e',)
            >>> woodwind_fingering = abjad.WoodwindFingering(
            ...     name='clarinet',
            ...     center_column=center_column,
            ...     left_hand=left_hand,
            ...     right_hand=right_hand,
            ...     )

            >>> woodwind_fingering.print_guide()
            list of valid key strings for clarinet:
            <BLANKLINE>
            cc
            possibilities for one:
            (one oneT one1qT oneT1q one1q one1qT1h one1hT1q one1qT3q one3qT1q one1qTF oneFT1q one1hT oneT1h one1h one1hT3q one3qT1h one1hTF oneFT1h one3qT oneT3q one3q one3qTF oneFT3q oneFT oneF)
            possibilities for two:
            (two twoT two1qT twoT1q two1q two1qT1h two1hT1q two1qT3q two3qT1q two1qTF twoFT1q two1hT twoT1h two1h two1hT3q two3qT1h two1hTF twoFT1h two3qT twoT3q two3q two3qTF twoFT3q twoFT twoF)
            possibilities for three:
            (three threeT three1qT threeT1q three1q three1qT1h three1hT1q three1qT3q three3qT1q three1qTF threeFT1q three1hT threeT1h three1h three1hT3q three3qT1h three1hTF threeFT1h three3qT threeT3q three3q three3qTF threeFT3q threeFT threeF)
            possibilities for four:
            (four fourT four1qT fourT1q four1q four1qT1h four1hT1q four1qT3q four3qT1q four1qTF fourFT1q four1hT fourT1h four1h four1hT3q four3qT1h four1hTF fourFT1h four3qT fourT3q four3q four3qTF fourFT3q fourFT fourF)
            possibilities for five:
            (five fiveT five1qT fiveT1q five1q five1qT1h five1hT1q five1qT3q five3qT1q five1qTF fiveFT1q five1hT fiveT1h five1h five1hT3q five3qT1h five1hTF fiveFT1h five3qT fiveT3q five3q five3qTF fiveFT3q fiveFT fiveF)
            possibilities for six:
            (six sixT six1qT sixT1q six1q six1qT1h six1hT1q six1qT3q six3qT1q six1qTF sixFT1q six1hT sixT1h six1h six1hT3q six3qT1h six1hTF sixFT1h six3qT sixT3q six3q six3qTF sixFT3q sixFT sixF)
            possibilities for h:
            (h hT h1qT hT1q h1q h1qT1h h1hT1q h1qT3q h3qT1q h1qTF hFT1q h1hT hT1h h1h h1hT3q h3qT1h h1hTF hFT1h h3qT hT3q h3q h3qTF hFT3q hFT hF)
            <BLANKLINE>
            lh
            possibilities for thumb:
            (thumb thumbT)
            possibilities for R:
            (R RT)
            possibilities for a:
            (a aT)
            possibilities for gis:
            (gis gisT)
            possibilities for ees:
            (ees eesT)
            possibilities for cis:
            (cis cisT)
            possibilities for f:
            (f fT)
            possibilities for e:
            (e eT)
            possibilities for fis:
            (fis fisT)
            <BLANKLINE>
            rh
            possibilities for one:
            (one oneT)
            possibilities for two:
            (two twoT)
            possibilities for three:
            (three threeT)
            possibilities for four:
            (four fourT)
            possibilities for b:
            (b bT)
            possibilities for fis:
            (fis fisT)
            possibilities for gis:
            (gis gisT)
            possibilities for e:
            (e eT)
            possibilities for f:
            (f fT)
            <BLANKLINE>
            diagram syntax
            <BLANKLINE>
            Lilypond woodwind diagram syntax divides an instrument into keyholes and keys.
            Keyholes belong to the central column (cc) group.
            Keys belong to either left-hand (lh) or right-hand (rh) groups.
            In Abjad's diagrams, central column (cc) keyholes appear along a central dotted line.
            Keys are grouped relative to the presence or absence of a dividing horizontal line:
            If a horizontal line divides a side of the diagram,
            keys above the line are left-hand keys (lh),
            and those below are right-hand keys (rh).
            If no horizontal line appears, all keys on that side of the diagram are left-hand keys (lh).
            A key located along the central dotted line will be grouped
            according to the playing hand of the nearest keyhole fingers.
            <BLANKLINE>
            To draw half- or quarter-covered keys, and to draw trills,
            refer to the comprehensive list of possible key strings that precedes this explanation.
            <BLANKLINE>
            <BLANKLINE>
                        a  gis
                R        |
                        one
                thumb    h
                        two
                        |  ees
            --------- three
                        |
                    one | cis
                    two |    f
                three | e
                    four |    fis
                        |
                        four
                        |
                        five
                    b |
                        six
                fis    |
                    gis |
                e      |
                    f  |
            <BLANKLINE>
            clarinet
            as modeled in LilyPond by Mike Solomon
            diagram explanation and key string index above
            <BLANKLINE>

        """
        if self._name == 'clarinet':
            lines = [
                'list of valid key strings for clarinet:',
                '',
                'cc',
                'possibilities for one:',
                '(one oneT one1qT oneT1q one1q one1qT1h one1hT1q one1qT3q one3qT1q one1qTF oneFT1q one1hT oneT1h one1h one1hT3q one3qT1h one1hTF oneFT1h one3qT oneT3q one3q one3qTF oneFT3q oneFT oneF)',
                'possibilities for two:',
                '(two twoT two1qT twoT1q two1q two1qT1h two1hT1q two1qT3q two3qT1q two1qTF twoFT1q two1hT twoT1h two1h two1hT3q two3qT1h two1hTF twoFT1h two3qT twoT3q two3q two3qTF twoFT3q twoFT twoF)',
                'possibilities for three:',
                '(three threeT three1qT threeT1q three1q three1qT1h three1hT1q three1qT3q three3qT1q three1qTF threeFT1q three1hT threeT1h three1h three1hT3q three3qT1h three1hTF threeFT1h three3qT threeT3q three3q three3qTF threeFT3q threeFT threeF)',
                'possibilities for four:',
                '(four fourT four1qT fourT1q four1q four1qT1h four1hT1q four1qT3q four3qT1q four1qTF fourFT1q four1hT fourT1h four1h four1hT3q four3qT1h four1hTF fourFT1h four3qT fourT3q four3q four3qTF fourFT3q fourFT fourF)',
                'possibilities for five:',
                '(five fiveT five1qT fiveT1q five1q five1qT1h five1hT1q five1qT3q five3qT1q five1qTF fiveFT1q five1hT fiveT1h five1h five1hT3q five3qT1h five1hTF fiveFT1h five3qT fiveT3q five3q five3qTF fiveFT3q fiveFT fiveF)',
                'possibilities for six:',
                '(six sixT six1qT sixT1q six1q six1qT1h six1hT1q six1qT3q six3qT1q six1qTF sixFT1q six1hT sixT1h six1h six1hT3q six3qT1h six1hTF sixFT1h six3qT sixT3q six3q six3qTF sixFT3q sixFT sixF)',
                'possibilities for h:',
                '(h hT h1qT hT1q h1q h1qT1h h1hT1q h1qT3q h3qT1q h1qTF hFT1q h1hT hT1h h1h h1hT3q h3qT1h h1hTF hFT1h h3qT hT3q h3q h3qTF hFT3q hFT hF)',
                '',
                'lh',
                'possibilities for thumb:',
                '(thumb thumbT)',
                'possibilities for R:',
                '(R RT)',
                'possibilities for a:',
                '(a aT)',
                'possibilities for gis:',
                '(gis gisT)',
                'possibilities for ees:',
                '(ees eesT)',
                'possibilities for cis:',
                '(cis cisT)',
                'possibilities for f:',
                '(f fT)',
                'possibilities for e:',
                '(e eT)',
                'possibilities for fis:',
                '(fis fisT)',
                '',
                'rh',
                'possibilities for one:',
                '(one oneT)',
                'possibilities for two:',
                '(two twoT)',
                'possibilities for three:',
                '(three threeT)',
                'possibilities for four:',
                '(four fourT)',
                'possibilities for b:',
                '(b bT)',
                'possibilities for fis:',
                '(fis fisT)',
                'possibilities for gis:',
                '(gis gisT)',
                'possibilities for e:',
                '(e eT)',
                'possibilities for f:',
                '(f fT)',
                '',
                'diagram syntax',
                '',
                '   Lilypond woodwind diagram syntax divides an instrument into keyholes and keys.',
                '   Keyholes belong to the central column (cc) group.',
                '   Keys belong to either left-hand (lh) or right-hand (rh) groups.',
                "   In Abjad's diagrams, central column (cc) keyholes appear along a central dotted line.",
                '   Keys are grouped relative to the presence or absence of a dividing horizontal line:',
                '   If a horizontal line divides a side of the diagram,',
                '   keys above the line are left-hand keys (lh),',
                '   and those below are right-hand keys (rh).',
                '   If no horizontal line appears, all keys on that side of the diagram are left-hand keys (lh).',
                '   A key located along the central dotted line will be grouped',
                '   according to the playing hand of the nearest keyhole fingers.',
                '',
                '   To draw half- or quarter-covered keys, and to draw trills,',
                '   refer to the comprehensive list of possible key strings that precedes this explanation.',
                '',
                '',
                '             a  gis',
                '    R        |',
                '            one',
                '    thumb    h',
                '            two',
                '             |  ees',
                ' --------- three',
                '             |',
                '         one | cis',
                '         two |    f',
                '       three | e',
                '        four |    fis',
                '             |',
                '            four',
                '             |',
                '            five',
                '           b |',
                '            six',
                '      fis    |',
                '         gis |',
                '      e      |',
                '          f  |',
                '',
                '   clarinet',
                '   as modeled in LilyPond by Mike Solomon',
                '   diagram explanation and key string index above',
                ''
                ]
            for line in lines:
                print(line)
        return None

    ### PUBLIC PROPERTIES ###

    @property
    def center_column(self) -> typing.Tuple[str, ...]:
        """
        Gets tuple of contents of key strings in center column key group.

        ..  container:: example

            >>> center_column = ('one', 'two', 'three', 'five')
            >>> left_hand = ('R', 'thumb')
            >>> right_hand = ('e',)
            >>> woodwind_fingering = abjad.WoodwindFingering(
            ...     name='clarinet',
            ...     center_column=center_column,
            ...     left_hand=left_hand,
            ...     right_hand=right_hand,
            ...     )

            >>> woodwind_fingering.center_column
            ('one', 'two', 'three', 'five')

        """
        return self._center_column

    @property
    def left_hand(self) -> typing.Tuple[str, ...]:
        """
        Gets tuple of contents of key strings in left hand key group.

        ..  container:: example

            >>> center_column = ('one', 'two', 'three', 'five')
            >>> left_hand = ('R', 'thumb')
            >>> right_hand = ('e',)
            >>> woodwind_fingering = abjad.WoodwindFingering(
            ...     name='clarinet',
            ...     center_column=center_column,
            ...     left_hand=left_hand,
            ...     right_hand=right_hand,
            ...     )

            >>> woodwind_fingering.left_hand
            ('R', 'thumb')

        """
        return self._left_hand

    @property
    def name(self) -> str:
        """
        Gets woodwind name.

        ..  container:: example

            >>> center_column = ('one', 'two', 'three', 'five')
            >>> left_hand = ('R', 'thumb')
            >>> right_hand = ('e',)
            >>> woodwind_fingering = abjad.WoodwindFingering(
            ...     name='clarinet',
            ...     center_column=center_column,
            ...     left_hand=left_hand,
            ...     right_hand=right_hand,
            ...     )

            >>> woodwind_fingering.name
            'clarinet'

        """
        return self._name

    @property
    def right_hand(self) -> typing.Tuple[str, ...]:
        """
        Gets tuple of contents of key strings in right hand key group.

        ..  container:: example

            >>> center_column = ('one', 'two', 'three', 'five')
            >>> left_hand = ('R', 'thumb')
            >>> right_hand = ('e',)
            >>> woodwind_fingering = abjad.WoodwindFingering(
            ...     name='clarinet',
            ...     center_column=center_column,
            ...     left_hand=left_hand,
            ...     right_hand=right_hand,
            ...     )

            >>> woodwind_fingering.right_hand
            ('e',)

        """
        return self._right_hand

    @property
    def tweaks(self) -> None:
        """
        Are not implemented on woodwind fingering.

        Enclose woodwind fingering in markup and tweak markup instead.
        """
        pass
