# -*- coding: utf-8 -*-
from abjad.tools import schemetools
from abjad.tools import markuptools
from abjad.tools.abctools import AbjadObject


class WoodwindFingering(AbjadObject):
    r'''A woodwind fingering.

    Initializes from a valid instrument name and up to three keyword
    lists or tuples:

    ::

        >>> center_column = ('one', 'two', 'three', 'five')
        >>> left_hand = ('R', 'thumb')
        >>> right_hand = ('e',)
        >>> woodwind_fingering = instrumenttools.WoodwindFingering(
        ...     instrument_name='clarinet',
        ...     center_column=center_column,
        ...     left_hand=left_hand,
        ...     right_hand=right_hand,
        ...     )

    ::

        >>> print(format(woodwind_fingering, 'storage'))
        instrumenttools.WoodwindFingering(
            instrument_name='clarinet',
            center_column=('one', 'two', 'three', 'five'),
            left_hand=('R', 'thumb'),
            right_hand=('e',),
            )

    Initializes a WoodwindFingering from another WoodwindFingering:

    ::

        >>> woodwind_fingering_2 = instrumenttools.WoodwindFingering(
        ...     woodwind_fingering)
        >>> print(format(woodwind_fingering_2))
        instrumenttools.WoodwindFingering(
            instrument_name='clarinet',
            center_column=('one', 'two', 'three', 'five'),
            left_hand=('R', 'thumb'),
            right_hand=('e',),
            )

    Calls a WoodwindFingering to create a woodwind diagram MarkupCommand:

    ::

        >>> fingering_command = woodwind_fingering()
        >>> print(format(fingering_command))
        markuptools.MarkupCommand(
            'woodwind-diagram',
            schemetools.Scheme(
                'clarinet',
                quoting="'",
                ),
            schemetools.Scheme(
                schemetools.SchemePair('cc', ('one', 'two', 'three', 'five')),
                schemetools.SchemePair('lh', ('R', 'thumb')),
                schemetools.SchemePair('rh', ('e',)),
                quoting="'",
                )
            )

    Attaches the MarkupCommand to score components, such as a chord
    representing a multiphonic sound:

    ::

        >>> markup = markuptools.Markup(contents=fingering_command, direction=Down)
        >>> chord = Chord("<ds' fs''>4")
        >>> attach(markup, chord)
        >>> show(chord) # doctest: +SKIP

    ..  doctest::

        >>> print(format(chord))
        <ds' fs''>4
            _ \markup {
                \woodwind-diagram
                    #'clarinet
                    #'((cc . (one two three five)) (lh . (R thumb)) (rh . (e)))
                }

    Initializes fingerings for eight different woodwind instruments:

    ::

        >>> instrument_names = [
        ...     'piccolo', 'flute', 'oboe', 'clarinet', 'bass-clarinet',
        ...     'saxophone', 'bassoon', 'contrabassoon',
        ...     ]
        >>> for name in instrument_names:
        ...    instrumenttools.WoodwindFingering(name)
        ...
        WoodwindFingering(instrument_name='piccolo', center_column=(), left_hand=(), right_hand=())
        WoodwindFingering(instrument_name='flute', center_column=(), left_hand=(), right_hand=())
        WoodwindFingering(instrument_name='oboe', center_column=(), left_hand=(), right_hand=())
        WoodwindFingering(instrument_name='clarinet', center_column=(), left_hand=(), right_hand=())
        WoodwindFingering(instrument_name='bass-clarinet', center_column=(), left_hand=(), right_hand=())
        WoodwindFingering(instrument_name='saxophone', center_column=(), left_hand=(), right_hand=())
        WoodwindFingering(instrument_name='bassoon', center_column=(), left_hand=(), right_hand=())
        WoodwindFingering(instrument_name='contrabassoon', center_column=(), left_hand=(), right_hand=())

    An override displays diagrams symbolically instead of graphically:

    ::

        >>> chord = Chord("<e' as' gqf''>1")
        >>> fingering = instrumenttools.WoodwindFingering(
        ...     'clarinet',
        ...     center_column=['one', 'two', 'three', 'four'],
        ...     left_hand=['R','cis'],
        ...     right_hand=['fis'])
        >>> diagram = fingering()
        >>> not_graphical = markuptools.MarkupCommand(
        ...     'override',
        ...     schemetools.SchemePair('graphical', False))
        >>> markup = markuptools.Markup(contents=
        ...     [not_graphical, diagram], direction=Down)
        >>> attach(markup, chord)
        >>> show(chord) # doctest: +SKIP

    ..  doctest::

        >>> print(format(chord))
        <e' as' gqf''>1
            _ \markup {
                \override
                    #'(graphical . #f)
                \woodwind-diagram
                    #'clarinet
                    #'((cc . (one two three four)) (lh . (R cis)) (rh . (fis)))
                }

    The thickness and size of diagrams can also be changed with overrides:

    ::

        >>> chord = Chord("<e' as' gqf''>1")
        >>> fingering = instrumenttools.WoodwindFingering(
        ...     'clarinet',
        ...     center_column=('one', 'two', 'three', 'four'),
        ...     left_hand=('R','cis'),
        ...     right_hand=('fis',),
        ...     )
        >>> diagram = fingering()
        >>> not_graphical = markuptools.MarkupCommand(
        ...     'override',
        ...     schemetools.SchemePair('graphical', False))
        >>> size = markuptools.MarkupCommand(
        ...     'override', schemetools.SchemePair('size', .5))
        >>> thickness = markuptools.MarkupCommand(
        ...     'override', schemetools.SchemePair('thickness', .4))
        >>> markup = markuptools.Markup(contents=
        ...     [not_graphical, size, thickness, diagram], direction=Down)
        >>> attach(markup, chord)
        >>> show(chord) # doctest: +SKIP

    ..  doctest::

        >>> print(format(chord))
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
    '''

    ### INITIALIZER ###

    def __init__(
        self,
        instrument_name=None,
        center_column=None,
        left_hand=None,
        right_hand=None,
        ):
        assert isinstance(center_column, (type(None), list, tuple))
        assert isinstance(left_hand, (type(None), list, tuple))
        assert isinstance(right_hand, (type(None), list, tuple))
        # initialize from a string and up to three lists
        instrument_name = instrument_name or 'flute'
        if isinstance(instrument_name, str):
            assert instrument_name in self._valid_instrument_names
            self._instrument_name = instrument_name
            if center_column is None:
                self._center_column = ()
            else:
                self._center_column = tuple(center_column)
            if left_hand is None:
                self._left_hand = ()
            else:
                self._left_hand = tuple(left_hand)
            if right_hand is None:
                self._right_hand = ()
            else:
                self._right_hand = tuple(right_hand)
        # initialize from WoodwindDiagram with up to three overriding lists
        elif isinstance(instrument_name, type(self)):
            self._instrument_name = instrument_name.instrument_name
            self._center_column = instrument_name.center_column
            self._left_hand = instrument_name.left_hand
            self._right_hand = instrument_name.right_hand
            if center_column is not None:
                self._center_column = tuple(center_column)
            if left_hand is not None:
                self._left_hand = tuple(left_hand)
            if right_hand is not None:
                self._right_hand = tuple(right_hand)

    ### SPECIAL METHODS ###

    def __call__(self):
        '''Calls woodwind fingering.

        Returns markup command.
        '''
        key_groups_as_scheme = []
        cc_scheme_pair = schemetools.SchemePair('cc', self._center_column)
        key_groups_as_scheme.append(cc_scheme_pair)
        lh_scheme_pair = schemetools.SchemePair('lh', self._left_hand)
        key_groups_as_scheme.append(lh_scheme_pair)
        rh_scheme_pair = schemetools.SchemePair('rh', self._right_hand)
        key_groups_as_scheme.append(rh_scheme_pair)
        key_groups_as_scheme = schemetools.Scheme(
            key_groups_as_scheme[:], quoting="'")
        instrument_as_scheme = schemetools.Scheme(
            self._instrument_name, quoting="'")
        return markuptools.MarkupCommand(
            'woodwind-diagram',
            instrument_as_scheme,
            key_groups_as_scheme,
            )

    def __format__(self, format_specification=''):
        r'''Formats woodwind fingering.

        Set `format_specification` to `''` or `'storage'`.

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatAgent(self).get_storage_format()
        return str(self)

    ### PUBLIC METHODS ###

    def print_guide(self):
        r'''Print read-only string containing instrument's valid key strings,
        instrument diagram, and syntax explanation.

        Returns string.
        '''
        if self._instrument_name == 'clarinet':
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
                'possibilities for R:','(R RT)',
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
                'possibilities for fis:','(fis fisT)',
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

    ### PRIVATE PROPERTIES ###

    @property
    def _valid_instrument_names(self):
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

     ### PUBLIC PROPERTIES ###

    @property
    def center_column(self):
        r'''Tuple of contents of key strings in center
        column key group:

    ::

        >>> woodwind_fingering.center_column
        ('one', 'two', 'three', 'five')

    Returns tuple.
        '''
        return self._center_column

    @property
    def instrument_name(self):
        r'''String of valid woodwind instrument name:

    ::

        >>> woodwind_fingering.instrument_name
        'clarinet'

    Returns string.
        '''
        return self._instrument_name

    @property
    def left_hand(self):
        r'''Tuple of contents of key strings in left
        hand key group:

    ::

        >>> woodwind_fingering.left_hand
        ('R', 'thumb')

    Returns tuple.
        '''
        return self._left_hand

    @property
    def right_hand(self):
        r'''Tuple of contents of key strings in right
        hand key group:

    ::

        >>> woodwind_fingering.right_hand
        ('e',)

    Returns tuple.
        '''
        return self._right_hand
