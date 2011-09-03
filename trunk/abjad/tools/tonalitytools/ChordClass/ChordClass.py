from abjad.tools import markuptools
from abjad.tools.pitchtools.MelodicDiatonicInterval import MelodicDiatonicInterval
from abjad.tools.pitchtools.NamedChromaticPitchClass import NamedChromaticPitchClass
from abjad.tools.pitchtools.NamedChromaticPitchClassSet import NamedChromaticPitchClassSet
from abjad.tools.tonalitytools.ChordQualityIndicator import ChordQualityIndicator
from abjad.tools.tonalitytools.ExtentIndicator import ExtentIndicator


class ChordClass(NamedChromaticPitchClassSet):
    '''.. versionadded:: 2.0

    Abjad model of tonal chords like G 7, G 6/5, G half-diminished 6/5, etc.

    Note that notions like G 7 represent an entire *class of* chords because
    there are many different spacings and registrations of a G 7 chord.
    '''

    __slots__ = ('_bass', '_quality_indicator', '_root', )

    def __new__(klass, root, *args):
        root = NamedChromaticPitchClass(root)
        quality_indicator = ChordQualityIndicator(*args)
        npcs = []
        for hdi in quality_indicator:
            mdi = hdi.melodic_diatonic_interval_ascending
            npc = root + mdi
            npcs.append(npc)
        bass = npcs[0]
        self = NamedChromaticPitchClassSet.__new__(klass, npcs)
        object.__setattr__(self, '_root', root)
        object.__setattr__(self, '_quality_indicator', quality_indicator)
        object.__setattr__(self, '_bass', bass)
        return self

    ### OVERLOADS ###

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            if self.root == arg.root:
                if self.quality_indicator == arg.quality_indicator:
                    if self.inversion == arg.inversion:
                        return True
        return False

    def __ne__(self, arg):
        return not self == arg

    def __repr__(self):
        root = str(self.root).title()
        quality = self.quality_indicator._title_case_name
        return root + quality

    ### PRIVATE ATTRIBUTES ###

    @property
    def _markup_root(self):
        if self.quality_indicator._quality_string in ('major', 'augmented', 'dominant'):
            root = str(self.root).upper()
        else:
            root = str(self.root).lower()
        if len(root) == 2:
            #adjustment = r'\hspace #-1 \raise #1 \fontsize #-3'
            adjustment = r'\hspace #-0.5 \raise #1 \fontsize #-3'
            if root[-1].lower() == 's':
                root = root[0] + r'%s \sharp' % adjustment
            elif root[-1].lower() == 'f':
                root = root[0] + r'%s \flat' % adjustment
            else:
                print self
                raise ValueError('unknown note name: %s' % root)
        return root

    @property
    def _markup_symbol(self):
        circle = r'\draw-circle #0.35 #0 ##f'
        if self.quality_indicator._quality_string == 'augmented':
            return '+'
        elif self.quality_indicator._quality_string == 'diminished':
            return circle
        elif self.quality_indicator._quality_string == 'half diminished':
            line = r"\draw-line #'(1 . 1)"
            markup = r'\concat { %s \hspace #-0.85 \raise #-0.5 %s }'
            markup %= (circle, line)
            return markup
        elif self.quality_indicator._quality_string == 'major' and \
            5 < self.extent.number:
            return 'M'
        elif self.quality_indicator._quality_string == 'minor' and \
            5 < self.extent.number:
            return 'm'
        else:
            return ''

    ### PUBLIC ATTRIBUTES ###

    @property
    def bass(self):
        return self._bass

    @property
    def cardinality(self):
        return len(self)

    @property
    def extent(self):
        from abjad.tools.tonalitytools.chord_class_cardinality_to_extent import chord_class_cardinality_to_extent
        extent = chord_class_cardinality_to_extent(self.cardinality)
        return ExtentIndicator(extent)

    @property
    def figured_bass(self):
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
                raise Exception(NotImplemented)
            elif inversion == 2:
                raise Exception(NotImplemented)
            elif inversion == 3:
                raise Exception(NotImplemented)
            elif inversion == 4:
                raise Exception(NotImplemented)

    @property
    def inversion(self):
        return self._quality_indicator.inversion

    @property
    def markup(self):
        markup = [self._markup_root, self._markup_symbol, self.figured_bass]
        markup = ''.join(markup)
        markup = r'\fontsize #1 %s \hspace #-0.5' % self._markup_root
        symbol = self._markup_symbol
        if symbol:
            markup += r' \hspace #0.5 \raise #1 \fontsize #-3 %s' % symbol
            if 'circle' in symbol:
                if 'sharp' in self._markup_root:
                    markup += r' \hspace #0'
                else:
                    markup += r' \hspace #-1.2'
        inversion = self.figured_bass
        if inversion:
            inv = r" \raise #1 \fontsize #-3 \override #'(baseline-skip . 1.5)"
            inv += r' \column { %s }' % ' '.join(inversion.split('/'))
            markup += inv
        return markuptools.Markup(markup, 'down')

    @property
    def quality_indicator(self):
        return self._quality_indicator

    @property
    def quality_pair(self):
        quality_indicator = self.quality_indicator
        return quality_indicator.quality_string, quality_indicator.extent_name

    @property
    def root(self):
        return self._root

    @property
    def root_string(self):
        capitalized_qualities = ('major', 'dominant', 'augmented')
        symbolic_name = self.root._symbolic_name
        letter, accidental = symbolic_name[0], symbolic_name[1:]
        if self.quality_indicator.quality_string in capitalized_qualities:
            letter = letter.upper()
        else:
            letter = letter.lower()
        return letter + accidental

    ### PUBLIC METHODS ###

    def transpose(self, mdi):
        raise Exception(NotImplemented)
