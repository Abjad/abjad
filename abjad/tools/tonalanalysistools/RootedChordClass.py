# -*- coding: utf-8 -*-
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.pitchtools import PitchClassSet


class RootedChordClass(PitchClassSet):
    '''A rooted chord class.

    ..  container:: example

        G major triad in root position:

        ::

            >>> tonalanalysistools.RootedChordClass('g', 'major')
            GMajorTriadInRootPosition

    ..  container:: example

        G dominant seventh in root position:

        ::

            >>> chord_class = tonalanalysistools.RootedChordClass('g', 'dominant', 7)

    Note that notions like a G dominant seventh represent an entire class of
    chords because there are many different spacings and registrations of a G
    dominant seventh.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_bass',
        '_chord_quality',
        '_root',
        )

    _cardinality_to_extent = {
        3: 5,
        4: 7,
        5: 9,
        6: 11,
        7: 13,
        }

    _extent_to_cardinality = {
        5: 3,
        7: 4,
        9: 5,
        11: 6,
        13: 7,
        }

    _extent_to_extent_name = {
        5: 'triad',
        7: 'seventh',
        9: 'ninth',
        11: 'eleventh',
        13: 'thirteenth',
        }

    ### INITIALIZER ###

    def __init__(self, root=None, *args):
        from abjad.tools import tonalanalysistools
        root = root or 'c'
        root = pitchtools.NamedPitchClass(root)
        chord_quality = tonalanalysistools.RootlessChordClass(*args)
        npcs = []
        for hdi in chord_quality:
            mdi = pitchtools.NamedInterval(hdi)
            npc = root + mdi
            npcs.append(npc)
        bass = npcs[0]
        PitchClassSet.__init__(
            self,
            items=npcs,
            item_class=pitchtools.NamedPitchClass,
            )
        self._root = root
        self._chord_quality = chord_quality
        self._bass = bass

    ### SPECIAL METHODS ###

    def __eq__(self, arg):
        r'''Is true when `arg` is a rooted chord-class with root, chord quality
        and inversion equal to those of this rooted chord-class. Otherwise
        false.

        Returns true or false.
        '''
        if isinstance(arg, type(self)):
            if self.root == arg.root:
                if self.chord_quality == arg.chord_quality:
                    if self.inversion == arg.inversion:
                        return True
        return False

    def __hash__(self):
        r'''Hashes rooted chord-class.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(RootedChordClass, self).__hash__()

    def __ne__(self, arg):
        r'''Is true when rooted chord-class does not equal `arg`. Otherwise
        false.

        Returns true or false.
        '''
        return not self == arg

    def __repr__(self):
        r'''Gets interpreter representation of rooted chord-class.

        Returns string.
        '''
        root = str(self.root).title()
        quality = self.chord_quality._title_case_name
        return root + quality

    ### PUBLIC METHODS ###

    @staticmethod
    def cardinality_to_extent(cardinality):
        r'''Change `cardinality` to extent.

        ..  container:: example

            Tertian chord with four pitch classes qualifies as a seventh chord:

            ::

                >>> tonalanalysistools.RootedChordClass.cardinality_to_extent(4)
                7

        Returns integer.
        '''
        return RootedChordClass._cardinality_to_extent[cardinality]

    @staticmethod
    def extent_to_cardinality(extent):
        r'''Change `extent` to cardinality.

        ..  container:: example

            Tertian chord with extent of seven
            comprises four pitch-clases:

            ::

                >>> tonalanalysistools.RootedChordClass.extent_to_cardinality(7)
                4

        Returns integer.
        '''
        return RootedChordClass._extent_to_cardinality[extent]

    @staticmethod
    def extent_to_extent_name(extent):
        r'''Change `extent` to extent name.

        ..  container:: example

            Extent of seven is a seventh:

            ::

                >>> tonalanalysistools.RootedChordClass.extent_to_extent_name(7)
                'seventh'

        Returns string.
        '''
        return RootedChordClass._extent_to_extent_name[extent]

    def transpose(self):
        r'''Transpose rooted chord-class.

        Not yet implemented.

        Will return new rooted chord-class.
        '''
        raise NotImplementedError

    ### PRIVATE PROPERTIES ###

    @property
    def _markup_root(self):
        if self.chord_quality._quality_string in (
            'major', 'augmented', 'dominant'):
            root = str(self.root).upper()
        else:
            root = str(self.root).lower()
        if len(root) == 2:
            adjustment = r'\hspace #-0.5 \raise #1 \fontsize #-3'
            if root[-1].lower() == 's':
                root = root[0] + r'{} \sharp'.format(adjustment)
            elif root[-1].lower() == 'f':
                root = root[0] + r'{} \flat'.format(adjustment)
            else:
                message = 'unknown note name: {}'
                message = message.format(root)
                raise ValueError(message)
        return root

    @property
    def _markup_symbol(self):
        circle = r'\draw-circle #0.35 #0 ##f'
        if self.chord_quality._quality_string == 'augmented':
            return '+'
        elif self.chord_quality._quality_string == 'diminished':
            return circle
        elif self.chord_quality._quality_string == 'half diminished':
            line = r"\draw-line #'(1 . 1)"
            markup = r'\concat {{ {} \hspace #-0.85 \raise #-0.5 {} }}'.format(
                circle, line)
            return markup
        elif self.chord_quality._quality_string == 'major' and \
            5 < self.extent.number:
            return 'M'
        elif self.chord_quality._quality_string == 'minor' and \
            5 < self.extent.number:
            return 'm'
        else:
            return ''

    ### PUBLIC PROPERTIES ###

    @property
    def bass(self):
        r'''Bass of rooted chord-class.

        ::

            >>> chord_class.bass
            NamedPitchClass('g')

        Returns named pitch-class.
        '''
        return self._bass

    @property
    def cardinality(self):
        r'''Cardinality of rooted chord-class.

        ::

            >>> chord_class.cardinality
            4

        Returns nonnegative integer.
        '''
        return len(self)

    @property
    def chord_quality(self):
        r'''Chord quality of rooted chord-class.

        ::

            >>> chord_class.chord_quality
            DominantSeventhInRootPosition('P1', '+M3', '+P5', '+m7')

        Returns chord quality.
        '''
        return self._chord_quality

    @property
    def extent(self):
        r'''Extent of rooted chord-class.

        ::

            >>> chord_class.extent
            ChordExtent(number=7)

        Returns chord extent.
        '''
        from abjad.tools import tonalanalysistools
        extent = self.cardinality_to_extent(self.cardinality)
        return tonalanalysistools.ChordExtent(extent)

    @property
    def figured_bass(self):
        r'''Figured bass of rooted chord-class.

        ::

            >>> chord_class.figured_bass
            '7'

        Returns string.
        '''
        extent, inversion = self.extent, self.inversion
        if extent.number == 5:
            if inversion == 0:
                return ''
            elif inversion == 1:
                return '6/3'
            elif inversion == 2:
                return '6/4'
        elif extent.number == 7:
            if inversion == 0:
                return '7'
            elif inversion == 1:
                return '6/5'
            elif inversion == 2:
                return '4/3'
            elif inversion == 3:
                return '4/2'
        elif extent.number == 9:
            if inversion == 0:
                return ''
            elif inversion == 1:
                raise NotImplementedError
            elif inversion == 2:
                raise NotImplementedError
            elif inversion == 3:
                raise NotImplementedError
            elif inversion == 4:
                raise NotImplementedError

    @property
    def inversion(self):
        r'''Inversion of rooted chord-class.

        ::

            >>> chord_class.inversion
            0

        Returns nonnegative integer.
        '''
        return self._chord_quality.inversion

    @property
    def markup(self):
        r'''Markup of rooted chord-class.

        ::

            >>> show(chord_class.markup) # doctest: +SKIP

        Returns markup.
        '''
        markup = [self._markup_root, self._markup_symbol, self.figured_bass]
        markup = ''.join(markup)
        markup = r'\fontsize #1 {} \hspace #-0.5'.format(self._markup_root)
        symbol = self._markup_symbol
        if symbol:
            markup += r' \hspace #0.5 \raise #1 \fontsize #-3 {}'.format(
                symbol)
            if 'circle' in symbol:
                if 'sharp' in self._markup_root:
                    markup += r' \hspace #0'
                else:
                    markup += r' \hspace #-1.2'
        inversion = self.figured_bass
        if inversion:
            inv = r" \raise #1 \fontsize #-3 \override #'(baseline-skip . 1.5)"
            inv += r' \column {{ {} }}'.format(' '.join(inversion.split('/')))
            markup += inv
        return markuptools.Markup(markup, Down)

    @property
    def quality_pair(self):
        r'''Quality pair of rooted chord-class.

        ::

            >>> chord_class.quality_pair
            ('dominant', 'seventh')

        Returns pair.
        '''
        chord_quality = self.chord_quality
        return chord_quality.quality_string, chord_quality.extent_name

    @property
    def root(self):
        r'''Root of rooted chord-class.

        ::

            >>> chord_class.root
            NamedPitchClass('g')

        Returns
        '''
        return self._root

    @property
    def root_string(self):
        r'''Root string of rooted chord-class.

        ::

            >>> chord_class.root_string
            'G'

        Returns string.
        '''
        capitalized_qualities = ('major', 'dominant', 'augmented')
        symbolic_name = self.root.pitch_class_label
        letter, accidental = symbolic_name[0], symbolic_name[1:]
        if self.chord_quality.quality_string in capitalized_qualities:
            letter = letter.upper()
        else:
            letter = letter.lower()
        return letter + accidental
