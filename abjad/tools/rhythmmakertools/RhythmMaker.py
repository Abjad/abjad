# -*- encoding: utf-8 -*-
import abc
import copy
from abjad.tools import datastructuretools
from abjad.tools import durationtools
from abjad.tools import indicatortools
from abjad.tools import lilypondfiletools
from abjad.tools import markuptools
from abjad.tools import mathtools
from abjad.tools import schemetools
from abjad.tools import scoretools
from abjad.tools import selectiontools
from abjad.tools import sequencetools
from abjad.tools import stringtools
from abjad.tools.abctools.AbjadObject import AbjadObject
from abjad.tools.topleveltools import new


class RhythmMaker(AbjadObject):
    '''Rhythm-maker abstract base class.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_beam_specifier',
        '_duration_spelling_specifier',
        '_tie_specifier',
        )

    _class_name_abbreviation = 'RM'

    _human_readable_class_name = 'rhythm-maker'

    ### INITIALIZER ###

    def __init__(
        self,
        beam_specifier=None,
        duration_spelling_specifier=None,
        tie_specifier=None,
        ):
        from abjad.tools import rhythmmakertools
        prototype = (rhythmmakertools.BeamSpecifier, type(None))
        assert isinstance(beam_specifier, prototype)
        prototype = (rhythmmakertools.DurationSpellingSpecifier, type(None))
        assert isinstance(duration_spelling_specifier, prototype)
        prototype = (rhythmmakertools.TieSpecifier, type(None))
        assert isinstance(tie_specifier, prototype)
        self._beam_specifier = beam_specifier
        self._duration_spelling_specifier = duration_spelling_specifier
        self._tie_specifier = tie_specifier

    ### SPECIAL METHODS ###

    def __call__(self, divisions, seeds=None):
        r'''Calls rhythm-maker.

        Makes music.

        Applies ties specified by tie specifier.

        Checks output type.

        Returns list of selections.
        '''
        from abjad.tools import rhythmmakertools
        duration_pairs = [
            mathtools.NonreducedFraction(x).pair
            for x in divisions
            ]
        seeds = self._to_tuple(seeds)
        music = self._make_music(duration_pairs, seeds)
        tie_specifier = self.tie_specifier
        if tie_specifier is None:
            tie_specifier = rhythmmakertools.TieSpecifier()
        tie_specifier._make_ties(music)
        assert isinstance(music, list), repr(music)
        assert len(music), repr(music)
        prototype = selectiontools.Selection
        assert all(isinstance(x, prototype) for x in music), repr(music)
        return music

    def __eq__(self, expr):
        r'''Is true when `expr` is a rhythm-maker with type and public
        properties equal to those of this rhythm-maker. Otherwise false.

        Returns boolean.
        '''
        from abjad.tools import systemtools
        return systemtools.StorageFormatManager.compare(self, expr)

    def __format__(self, format_specification=''):
        r'''Formats rhythm-maker.

        Set `format_specification` to `''` or `'storage'`.

        Defaults `format_specification=None` to
        `format_specification='storage'`.

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatManager.get_storage_format(self)
        return str(self)

    def __getstate__(self):
        r'''Gets state of rhythm-maker.

        Returns dictionary.
        '''
        if hasattr(self, '__dict__'):
            return vars(self)
        state = {}
        for class_ in type(self).__mro__:
            for slot in getattr(class_, '__slots__', ()):
                state[slot] = getattr(self, slot, None)
        return state

    def __illustrate__(self, divisions=None):
        r'''Illustrates rhythm-maker.

        Defaults `divisions` to ``3/8``, ``4/8``, ``3/16``, ``4/16``.

        Returns LilyPond file.
        '''
        from abjad.tools import rhythmmakertools
        divisions = divisions or [(3, 8), (4, 8), (3, 16), (4, 16)]
        selections = self(divisions)
        lilypond_file = rhythmmakertools.make_lilypond_file(
            selections,
            divisions,
            )
        return lilypond_file
        
    ### PRIVATE METHODS ###

    @staticmethod
    def _all_are_tuplets_or_all_are_leaf_selections(expr):
        if all(isinstance(x, scoretools.Tuplet) for x in expr):
            return True
        elif all(RhythmMaker._is_leaf_selection(x) for x in expr):
            return True
        else:
            return False

    @staticmethod
    def _get_rhythmic_staff(lilypond_file):
        score_block = lilypond_file.items[-1]
        score = score_block.items[0]
        rhythmic_staff = score[-1]
        return rhythmic_staff

    @staticmethod
    def _is_leaf_selection(expr):
        if isinstance(expr, selectiontools.Selection):
            return all(isinstance(x, scoretools.Leaf) for x in expr)
        return False

    @abc.abstractmethod
    def _make_music(self, duration_pairs, seeds):
        pass

    def _make_secondary_duration_pairs(
        self,
        duration_pairs,
        split_divisions_by_counts,
        ):
        if not split_divisions_by_counts:
            return duration_pairs[:]
        numerators = [
            duration_pair.numerator
            for duration_pair in duration_pairs
            ]
        secondary_numerators = sequencetools.split_sequence(
            numerators,
            split_divisions_by_counts,
            cyclic=True,
            overhang=True,
            )
        secondary_numerators = \
            sequencetools.flatten_sequence(secondary_numerators)
        denominator = duration_pairs[0].denominator
        secondary_duration_pairs = [
            (n, denominator)
            for n in secondary_numerators
            ]
        return secondary_duration_pairs

    def _make_tuplets(self, duration_pairs, leaf_lists):
        assert len(duration_pairs) == len(leaf_lists)
        tuplets = []
        for duration_pair, leaf_list in zip(duration_pairs, leaf_lists):
            tuplet = scoretools.FixedDurationTuplet(duration_pair, leaf_list)
            tuplets.append(tuplet)
        return tuplets

    def _none_to_trivial_helper(self, expr):
        if expr is None:
            expr = self._trivial_helper
        assert callable(expr)
        return expr

    def _none_to_tuple(self, expr):
        if expr is None:
            expr = ()
        assert isinstance(expr, tuple), expr
        return expr

    @staticmethod
    def _reverse_tuple(expr):
        if expr is not None:
            return tuple(reversed(expr))

    @staticmethod
    def _rotate_tuple(expr, n):
        if expr is not None:
            return tuple(sequencetools.rotate_sequence(expr, n))

    def _scale_taleas(self, duration_pairs, talea_denominator, taleas):
        dummy_duration_pair = (1, talea_denominator)
        duration_pairs.append(dummy_duration_pair)
        Duration = durationtools.Duration
        duration_pairs = Duration.durations_to_nonreduced_fractions(
            duration_pairs)
        dummy_duration_pair = duration_pairs.pop()
        lcd = dummy_duration_pair.denominator
        multiplier = lcd / talea_denominator
        scaled_taleas = []
        for talea in taleas:
            talea = datastructuretools.CyclicTuple(
                [multiplier * x for x in talea],
                )
            scaled_taleas.append(talea)
        result = [duration_pairs, lcd]
        result.extend(scaled_taleas)
        return tuple(result)

    def _sequence_to_ellipsized_string(self, sequence):
        if not sequence:
            return '[]'
        if len(sequence) <= 4:
            result = ', '.join([str(x) for x in sequence])
        else:
            result = ', '.join([str(x) for x in sequence[:4]])
            result += ', ...'
        result = '[${}$]'.format(result)
        return result

    def _to_tuple(self, expr):
        if isinstance(expr, list):
            expr = tuple(expr)
        return expr

    def _trivial_helper(self, talea, seeds):
        if isinstance(seeds, int) and len(talea):
            return sequencetools.rotate_sequence(talea, seeds)
        return talea

    ### PUBLIC PROPERTIES ###

    @property
    def beam_specifier(self):
        r'''Gets beam specifier of rhythm-maker.

        Returns beam specifier or none.
        '''
        return self._beam_specifier

    @property
    def duration_spelling_specifier(self):
        r'''Gets duration spelling specifier of rhythm-maker.

        Returns duration spelling specifier or none.
        '''
        return self._duration_spelling_specifier

    @property
    def tie_specifier(self):
        r'''Gets tie specifier of rhythm-maker.

        Return tie specifier or none.
        '''
        return self._tie_specifier

    ### PUBLIC METHODS ###

    def reverse(self):
        r'''Reverses rhythm-maker.

        Concrete rhythm-makers should override this method.

        Returns new rhythm-maker.
        '''
        from abjad.tools import rhythmmakertools
        specifier = self.duration_spelling_specifier
        if specifier is None:
            specifier = rhythmmakertools.DurationSpellingSpecifier()
        specifier = specifier.reverse()
        maker = new(
            self,
            duration_spelling_specifier=specifier,
            )
        return maker
