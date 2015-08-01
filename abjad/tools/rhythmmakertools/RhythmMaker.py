# -*- encoding: utf-8 -*-
import abc
import copy
from abjad.tools import datastructuretools
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import scoretools
from abjad.tools import selectiontools
from abjad.tools import sequencetools
from abjad.tools import spannertools
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import detach
from abjad.tools.topleveltools import inspect_
from abjad.tools.topleveltools import iterate


class RhythmMaker(AbjadValueObject):
    '''Rhythm-maker abstract base class.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Rhythm-makers'

    __slots__ = (
        '_beam_specifier',
        '_duration_spelling_specifier',
        '_output_masks',
        '_rotation',
        '_tie_specifier',
        '_tuplet_spelling_specifier',
        )

    _class_name_abbreviation = 'RM'

    _human_readable_class_name = 'rhythm-maker'

    ### INITIALIZER ###

    def __init__(
        self,
        beam_specifier=None,
        duration_spelling_specifier=None,
        output_masks=None,
        tie_specifier=None,
        tuplet_spelling_specifier=None,
        ):
        from abjad.tools import rhythmmakertools
        prototype = (rhythmmakertools.BeamSpecifier, type(None))
        assert isinstance(beam_specifier, prototype)
        self._beam_specifier = beam_specifier
        prototype = (rhythmmakertools.DurationSpellingSpecifier, type(None))
        self._duration_spelling_specifier = duration_spelling_specifier
        assert isinstance(duration_spelling_specifier, prototype)
        if output_masks is not None:
            if isinstance(output_masks, rhythmmakertools.BooleanPattern):
                output_masks = (output_masks,)
            output_masks = rhythmmakertools.BooleanPatternInventory(
                items=output_masks,
                )
        self._output_masks = output_masks
        prototype = (rhythmmakertools.TieSpecifier, type(None))
        assert isinstance(tie_specifier, prototype)
        self._tie_specifier = tie_specifier
        prototype = (rhythmmakertools.TupletSpellingSpecifier, type(None))
        assert isinstance(tuplet_spelling_specifier, prototype)
        self._tuplet_spelling_specifier = tuplet_spelling_specifier

    ### SPECIAL METHODS ###

    def __call__(self, divisions, rotation=None):
        r'''Calls rhythm-maker.

        Makes music as a list of selections.

        Applies cross-division ties (when specified by tie specifier).
        Other types of ties specified by tie specifier must be
        applied by child classes.

        Validates output type.

        Returns list of selections.
        '''
        divisions = [mathtools.NonreducedFraction(_) for _ in divisions]
        rotation = self._to_tuple(rotation)
        self._rotation = rotation
        selections = self._make_music(
            divisions,
            rotation,
            )
        self._simplify_tuplets(selections)
        selections = self._flatten_trivial_tuplets(selections)
        self._apply_tie_specifier(selections)
        self._validate_selections(selections)
        self._validate_tuplets(selections)
        return selections

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

    def __hash__(self):
        r'''Hashes rhythm-maker.

        Required to be explicitly re-defined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(RhythmMaker, self).__hash__()

    def __illustrate__(self, divisions=None):
        r'''Illustrates rhythm-maker.

        Returns LilyPond file.
        '''
        from abjad.tools import rhythmmakertools
        divisions = divisions or [
            (3, 8),
            (4, 8),
            (3, 16),
            (4, 16),
            (5, 8),
            (2, 4),
            (5, 16),
            (2, 8),
            (7, 8),
            ]
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

    def _apply_beam_specifier(self, selections):
        beam_specifier = self._get_beam_specifier()
        if beam_specifier.beam_divisions_together:
            durations = []
            for x in selections:
                if isinstance(x, selectiontools.Selection):
                    duration = x.get_duration()
                else:
                    duration = x._get_duration()
                durations.append(duration)
            beam = spannertools.DuratedComplexBeam(
                durations=durations,
                span_beam_count=1,
                )
            components = []
            for x in selections:
                if isinstance(x, selectiontools.Selection):
                    components.extend(x)
                elif isinstance(x, scoretools.Tuplet):
                    components.append(x)
                else:
                    raise TypeError(x)
            attach(beam, components)
        elif beam_specifier.beam_each_division:
            for cell in selections:
                beam = spannertools.MultipartBeam()
                attach(beam, cell)

    def _apply_output_masks(self, selections, rotation):
        from abjad.tools import rhythmmakertools
        if not self.output_masks:
            return selections
        new_selections = []
        duration_spelling_specifier = self._get_duration_spelling_specifier()
        decrease_durations_monotonically = \
            duration_spelling_specifier.decrease_durations_monotonically
        forbidden_written_duration = \
            duration_spelling_specifier.forbidden_written_duration
        tie_specifier = self._get_tie_specifier()
        length = len(selections)
        output_masks = self.output_masks
        for i, selection in enumerate(selections):
            matching_output_mask = output_masks.get_matching_pattern(
                i, length, rotation=rotation)
            if not matching_output_mask:
                new_selections.append(selection)
                continue
            duration = selection.get_duration()
            if isinstance(matching_output_mask, rhythmmakertools.SustainMask):
                new_selection = scoretools.make_leaves(
                    [0],
                    [duration],
                    decrease_durations_monotonically=\
                        decrease_durations_monotonically,
                    forbidden_written_duration=forbidden_written_duration,
                    use_messiaen_style_ties=\
                        tie_specifier.use_messiaen_style_ties,
                    )
            elif isinstance(matching_output_mask, rhythmmakertools.NullMask):
                new_selections.append(selection)
                continue
            else:
                use_multimeasure_rests = getattr(
                    matching_output_mask,
                    'use_multimeasure_rests',
                    False,
                    )
                new_selection = scoretools.make_leaves(
                    [None],
                    [duration],
                    decrease_durations_monotonically=\
                        decrease_durations_monotonically,
                    forbidden_written_duration=forbidden_written_duration,
                    use_multimeasure_rests=use_multimeasure_rests,
                    )
            for component in iterate(selection).by_class():
                detach(spannertools.Tie, component)
            new_selections.append(new_selection)
        return new_selections

    def _apply_tie_specifier(self, selections):
        tie_specifier = self._get_tie_specifier()
        tie_specifier(selections)

    def _flatten_trivial_tuplets(self, selections):
        tuplet_spelling_specifier = self._get_tuplet_spelling_specifier()
        if not tuplet_spelling_specifier.flatten_trivial_tuplets:
            return selections
        new_selections = []
        for selection in selections:
            new_selection = []
            for component in selection:
                if not (isinstance(component, scoretools.Tuplet) and 
                    component.is_trivial):
                    new_selection.append(component)
                    continue
                spanners = inspect_(component).get_spanners()
                contents = component[:]
                for spanner in spanners:
                    new_spanner = copy.copy(spanner)
                    attach(new_spanner, contents)
                new_selection.extend(contents)
                del(component[:])
            new_selection = selectiontools.Selection(new_selection)
            new_selections.append(new_selection)
        return new_selections

    def _get_beam_specifier(self):
        from abjad.tools import rhythmmakertools
        if self.beam_specifier is not None:
            return self.beam_specifier
        return rhythmmakertools.BeamSpecifier()

    def _get_duration_spelling_specifier(self):
        from abjad.tools import rhythmmakertools
        if self.duration_spelling_specifier is not None:
            return self.duration_spelling_specifier
        return rhythmmakertools.DurationSpellingSpecifier()

    @staticmethod
    def _get_rhythmic_staff(lilypond_file):
        score_block = lilypond_file.items[-1]
        score = score_block.items[0]
        rhythmic_staff = score[-1]
        return rhythmic_staff

    def _get_tie_specifier(self):
        from abjad.tools import rhythmmakertools
        if self.tie_specifier is not None:
            return self.tie_specifier
        return rhythmmakertools.TieSpecifier()

    def _get_tuplet_spelling_specifier(self):
        from abjad.tools import rhythmmakertools
        if self.tuplet_spelling_specifier is not None:
            return self.tuplet_spelling_specifier
        return rhythmmakertools.TupletSpellingSpecifier()

    @staticmethod
    def _is_leaf_selection(expr):
        if isinstance(expr, selectiontools.Selection):
            return all(isinstance(x, scoretools.Leaf) for x in expr)
        return False

    @staticmethod
    def _is_sign_tuple(expr):
        if isinstance(expr, tuple):
            prototype = (-1, 0, 1)
            return all(_ in prototype for _ in expr)
        return False

    @staticmethod
    def _make_cyclic_tuple_generator(iterable):
        cyclic_tuple = datastructuretools.CyclicTuple(iterable)
        i = 0
        while True:
            yield cyclic_tuple[i]
            i += 1

    @abc.abstractmethod
    def _make_music(self, divisions, rotation):
        raise NotImplementedError

    def _make_secondary_divisions(
        self,
        divisions,
        split_divisions_by_counts,
        ):
        if not split_divisions_by_counts:
            return divisions[:]
        numerators = [
            division.numerator
            for division in divisions
            ]
        secondary_numerators = sequencetools.split_sequence(
            numerators,
            split_divisions_by_counts,
            cyclic=True,
            overhang=True,
            )
        secondary_numerators = \
            sequencetools.flatten_sequence(secondary_numerators)
        denominator = divisions[0].denominator
        secondary_divisions = [
            (n, denominator)
            for n in secondary_numerators
            ]
        return secondary_divisions

    def _make_tuplets(self, divisions, leaf_lists):
        assert len(divisions) == len(leaf_lists)
        tuplets = []
        for division, leaf_list in zip(divisions, leaf_lists):
            tuplet = scoretools.FixedDurationTuplet(division, leaf_list)
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

    def _scale_taleas(self, divisions, talea_denominator, taleas):
        talea_denominator = talea_denominator or 1
        dummy_division = (1, talea_denominator)
        divisions.append(dummy_division)
        Duration = durationtools.Duration
        divisions = Duration.durations_to_nonreduced_fractions(divisions)
        dummy_division = divisions.pop()
        lcd = dummy_division.denominator
        multiplier = lcd / talea_denominator
        scaled_taleas = []
        for talea in taleas:
            talea = [multiplier * _ for _ in talea]
            talea = datastructuretools.CyclicTuple(talea)
            scaled_taleas.append(talea)
        result = [divisions, lcd]
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

    def _simplify_tuplets(self, selections):
        tuplet_spelling_specifier = self._get_tuplet_spelling_specifier()
        if not tuplet_spelling_specifier.simplify_tuplets:
            return
        for tuplet in iterate(selections).by_class(scoretools.Tuplet):
            if tuplet.is_trivial:
                continue
            duration = tuplet._get_duration()
            if all(isinstance(x, scoretools.Rest) for x in tuplet):
                rests = scoretools.make_rests([duration])
                tuplet[:] = rests
            elif all(isinstance(x, scoretools.Note) for x in tuplet):
                logical_ties = set([x._get_logical_tie() for x in tuplet])
                if len(logical_ties) == 1:
                    notes = scoretools.make_notes([0], [duration])
                    tuplet[:] = notes

    def _to_tuple(self, expr):
        if isinstance(expr, list):
            expr = tuple(expr)
        return expr

    def _trivial_helper(self, talea, rotation):
        if isinstance(rotation, int) and len(talea):
            return sequencetools.rotate_sequence(talea, rotation)
        return talea

    def _validate_selections(self, selections):
        assert isinstance(selections, list), repr(selections)
        assert len(selections), repr(selections)
        for selection in selections:
            assert isinstance(selection, selectiontools.Selection), selection

    def _validate_tuplets(self, selections):
        for tuplet in iterate(selections).by_class(scoretools.Tuplet):
            assert tuplet.multiplier.is_proper_tuplet_multiplier, repr(
                tuplet)
            assert len(tuplet), repr(tuplet)

    ### PUBLIC PROPERTIES ###

    @property
    def beam_specifier(self):
        r'''Gets beam specifier of rhythm-maker.

        Set to beam specifier or none.
        '''
        return self._beam_specifier

    @property
    def duration_spelling_specifier(self):
        r'''Gets duration spelling specifier of rhythm-maker.

        Set to duration spelling specifier or none.
        '''
        return self._duration_spelling_specifier

    @property
    def output_masks(self):
        r'''Gets output masks of rhythm-maker.

        Set to output masks or none.
        '''
        return self._output_masks

    @property
    def tie_specifier(self):
        r'''Gets tie specifier of rhythm-maker.

        Set to tie specifier or none.
        '''
        return self._tie_specifier

    @property
    def tuplet_spelling_specifier(self):
        r'''Gets tuplet spelling specifier of rhythm-maker.

        Set to tuplet spelling specifier or none.
        '''
        return self._tuplet_spelling_specifier