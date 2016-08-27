# -*- coding: utf-8 -*-
import copy
from abjad.tools import datastructuretools
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import patterntools
from abjad.tools import scoretools
from abjad.tools import selectiontools
from abjad.tools import sequencetools
from abjad.tools import spannertools
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import detach
from abjad.tools.topleveltools import inspect_
from abjad.tools.topleveltools import iterate
from abjad.tools.topleveltools import mutate


class RhythmMaker(AbjadValueObject):
    '''Rhythm-maker.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Rhythm-makers'

    __slots__ = (
        '_beam_specifier',
        '_logical_tie_masks',
        '_division_masks',
        '_duration_spelling_specifier',
        '_rotation',
        '_tie_specifier',
        '_tuplet_spelling_specifier',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        beam_specifier=None,
        logical_tie_masks=None,
        division_masks=None,
        duration_spelling_specifier=None,
        tie_specifier=None,
        tuplet_spelling_specifier=None,
        ):
        from abjad.tools import rhythmmakertools
        prototype = (rhythmmakertools.BeamSpecifier, type(None))
        assert isinstance(beam_specifier, prototype)
        self._beam_specifier = beam_specifier
        logical_tie_masks = self._prepare_masks(logical_tie_masks)
        self._logical_tie_masks = logical_tie_masks
        prototype = (rhythmmakertools.DurationSpellingSpecifier, type(None))
        self._duration_spelling_specifier = duration_spelling_specifier
        assert isinstance(duration_spelling_specifier, prototype)
        division_masks = self._prepare_masks(division_masks)
        self._division_masks = division_masks
        prototype = (rhythmmakertools.TieSpecifier, type(None))
        assert isinstance(tie_specifier, prototype)
        self._tie_specifier = tie_specifier
        prototype = (rhythmmakertools.TupletSpellingSpecifier, type(None))
        assert isinstance(tuplet_spelling_specifier, prototype)
        self._tuplet_spelling_specifier = tuplet_spelling_specifier

    ### SPECIAL METHODS ###

    def __call__(self, divisions, rotation=None):
        r'''Calls rhythm-maker.

        Returns selections.
        '''
        self._rotation = rotation
        divisions = self._coerce_divisions(divisions)
        selections = self._make_music(divisions, rotation)
        selections = self._apply_specifiers(selections, divisions)
        self._check_well_formedness(selections)
        return selections

    def __illustrate__(self, divisions=((3, 8), (4, 8), (3, 16), (4, 16))):
        r'''Illustrates rhythm-maker.

        Returns LilyPond file.
        '''
        from abjad.tools import rhythmmakertools
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

    def _apply_division_masks(self, selections, rotation=None):
        from abjad.tools import rhythmmakertools
        if not self.division_masks:
            return selections
        new_selections = []
        duration_spelling_specifier = self._get_duration_spelling_specifier()
        decrease_durations_monotonically = \
            duration_spelling_specifier.decrease_durations_monotonically
        forbidden_written_duration = \
            duration_spelling_specifier.forbidden_written_duration
        tie_specifier = self._get_tie_specifier()
        length = len(selections)
        division_masks = self.division_masks
        for i, selection in enumerate(selections):
            matching_division_mask = division_masks.get_matching_pattern(
                i,
                length,
                rotation=rotation,
                )
            if not matching_division_mask:
                new_selections.append(selection)
                continue
            duration = selection.get_duration()
            if isinstance(
                matching_division_mask,
                rhythmmakertools.SustainMask,
                ):
                new_selection = scoretools.make_leaves(
                    [0],
                    [duration],
                    decrease_durations_monotonically=\
                        decrease_durations_monotonically,
                    forbidden_written_duration=forbidden_written_duration,
                    use_messiaen_style_ties=\
                        tie_specifier.use_messiaen_style_ties,
                    )
            else:
                use_multimeasure_rests = getattr(
                    matching_division_mask,
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

    def _apply_logical_tie_masks(self, selections):
        from abjad.tools import rhythmmakertools
        if self.logical_tie_masks is None:
            return selections
        # wrap every selection in a temporary container;
        # this allows the call to mutate().replace() to work
        containers = []
        for selection in selections:
            container = scoretools.Container(selection)
            attach('temporary container', container)
            containers.append(container)
        logical_ties = iterate(selections).by_logical_tie()
        logical_ties = list(logical_ties)
        total_logical_ties = len(logical_ties)
        for index, logical_tie in enumerate(logical_ties[:]):
            matching_mask = self.logical_tie_masks.get_matching_pattern(
                index,
                total_logical_ties,
                )
            if not isinstance(matching_mask, rhythmmakertools.SilenceMask):
                continue
            if isinstance(logical_tie.head, scoretools.Rest):
                continue
            for leaf in logical_tie:
                rest = scoretools.Rest(leaf.written_duration)
                inspector = inspect_(leaf)
                if inspector.has_indicator(durationtools.Multiplier):
                    multiplier = inspector.get_indicator(
                        durationtools.Multiplier,
                        )
                    multiplier = durationtools.Multiplier(multiplier)
                    attach(multiplier, rest)
                mutate(leaf).replace([rest])
                detach(spannertools.Tie, rest)
        # remove every temporary container and recreate selections
        new_selections = []
        for container in containers:
            inspector = inspect_(container)
            assert inspector.get_indicator(str) == 'temporary container'
            new_selection = mutate(container).eject_contents()
            new_selections.append(new_selection)
        return new_selections

    def _apply_specifiers(self, selections, divisions=None):
        selections = self._apply_tuplet_spelling_specifier(
            selections,
            divisions,
            )
        self._apply_tie_specifier(selections)
        selections = self._apply_logical_tie_masks(selections)
        self._validate_selections(selections)
        self._validate_tuplets(selections)
        return selections

    def _apply_tie_specifier(self, selections):
        tie_specifier = self._get_tie_specifier()
        tie_specifier(selections)


    def _apply_tuplet_spelling_specifier(self, selections, divisions):
        # TODO: migrate functionality to TupletSpellingSpecifier.__call__()
        tuplet_spelling_specifier = self._get_tuplet_spelling_specifier()
        tuplet_spelling_specifier._do_simplify_redundant_tuplets(selections)
        selections = self._rewrite_rest_filled_tuplets(selections)
        selections = self._flatten_trivial_tuplets(selections)
        tuplet_spelling_specifier._apply_preferred_denominator(
            selections,
            divisions,
            )
        return selections

    def _check_well_formedness(self, selections):
        for component in iterate(selections).by_class():
            inspector = inspect_(component)
            if not inspector.is_well_formed():
                report = inspector.tabulate_well_formedness_violations()
                report = repr(component) + '\n' + report
                raise Exception(report)

    @staticmethod
    def _coerce_divisions(divisions):
        divisions_ = []
        for division in divisions:
            if isinstance(division, mathtools.NonreducedFraction):
                divisions_.append(division)
            elif isinstance(division, durationtools.Division):
                division = mathtools.NonreducedFraction(division.duration)
                divisions_.append(division)
            else:
                division = mathtools.NonreducedFraction(division)
                divisions_.append(division)
        divisions = divisions_
        prototype = mathtools.NonreducedFraction
        assert all( isinstance(_, prototype) for _ in divisions)
        return divisions

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
    def _get_staff(lilypond_file):
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

    @staticmethod
    def _prepare_masks(masks):
        from abjad.tools import rhythmmakertools
        prototype = (
            rhythmmakertools.SilenceMask,
            rhythmmakertools.SustainMask,
            )
        if masks is None:
            return
        if isinstance(masks, patterntools.Pattern):
            masks = (masks,)
        if isinstance(masks, prototype):
            masks = (masks,)
        masks = patterntools.PatternInventory(
            items=masks,
            )
        return masks

    @staticmethod
    def _reverse_tuple(expr):
        if expr is not None:
            return tuple(reversed(expr))

    def _rewrite_rest_filled_tuplets(self, selections):
        tuplet_spelling_specifier = self._get_tuplet_spelling_specifier()
        if not tuplet_spelling_specifier.rewrite_rest_filled_tuplets:
            return selections
        new_selections = []
        for selection in selections:
            new_selection = []
            for component in selection:
                if not (isinstance(component, scoretools.Tuplet) and
                    component._is_rest_filled):
                    new_selection.append(component)
                    continue
                duration = inspect_(component).get_duration()
                new_rests = scoretools.make_rests([duration])
                mutate(component[:]).replace(new_rests)
                new_selection.append(component)
            new_selection = selectiontools.Selection(new_selection)
            new_selections.append(new_selection)
        return new_selections

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
        assert mathtools.is_integer_equivalent_expr(multiplier), repr(multiplier)
        multiplier = int(multiplier)
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

    def _trivial_helper(self, sequence_, rotation):
        if isinstance(rotation, int) and len(sequence_):
            return sequencetools.rotate_sequence(sequence_, rotation)
        return sequence_

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
        r'''Gets beam specifier.

        Set to beam specifier or none.
        '''
        return self._beam_specifier

    @property
    def division_masks(self):
        r'''Gets division masks.

        Set to division masks or none.
        '''
        return self._division_masks

    @property
    def duration_spelling_specifier(self):
        r'''Gets duration spelling specifier.

        Set to duration spelling specifier or none.
        '''
        return self._duration_spelling_specifier

    @property
    def logical_tie_masks(self):
        r'''Gets logical tie masks.

        Set to patterns or none.

        Defaults to none.

        Returns patterns or none.
        '''
        return self._logical_tie_masks

    @property
    def tie_specifier(self):
        r'''Gets tie specifier.

        Set to tie specifier or none.
        '''
        return self._tie_specifier

    @property
    def tuplet_spelling_specifier(self):
        r'''Gets tuplet spelling specifier.

        Set to tuplet spelling specifier or none.
        '''
        return self._tuplet_spelling_specifier
