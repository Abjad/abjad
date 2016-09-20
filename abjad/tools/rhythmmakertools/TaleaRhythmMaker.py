# -*- coding: utf-8 -*-
from abjad.tools import datastructuretools
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import scoretools
from abjad.tools import selectiontools
from abjad.tools import sequencetools
from abjad.tools import spannertools
from abjad.tools.rhythmmakertools.RhythmMaker import RhythmMaker
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import detach
from abjad.tools.topleveltools import inspect_
from abjad.tools.topleveltools import iterate
from abjad.tools.topleveltools import mutate
from abjad.tools.topleveltools import select


# TODO: unskip the doctest on line 1373 after making work on Python 3
class TaleaRhythmMaker(RhythmMaker):
    r'''Talea rhythm-maker.

    ..  container:: example

        **Example 1.** Repeats talea of 1/16, 2/16, 3/16, 4/16:

        ::

            >>> rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
            ...     talea=rhythmmakertools.Talea(
            ...         counts=[1, 2, 3, 4],
            ...         denominator=16,
            ...         ),
            ...     )

        ::

            >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = rhythmmakertools.make_lilypond_file(
            ...     selections,
            ...     divisions,
            ...     )
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> staff = rhythm_maker._get_staff(lilypond_file)
            >>> f(staff)
            \new RhythmicStaff {
                {
                    \time 3/8
                    c'16 [
                    c'8
                    c'8. ]
                }
                {
                    \time 4/8
                    c'4
                    c'16 [
                    c'8
                    c'16 ~ ]
                }
                {
                    \time 3/8
                    c'8
                    c'4
                }
                {
                    \time 4/8
                    c'16 [
                    c'8
                    c'8.
                    c'8 ]
                }
            }

    ..  container:: example

        **Example 2.** Formats rhythm-maker:

        ::

            >>> rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
            ...     talea=rhythmmakertools.Talea(
            ...         counts=[1, 2, 3, 4],
            ...         denominator=16,
            ...         ),
            ...     )

        ::

            >>> print(format(rhythm_maker))
            rhythmmakertools.TaleaRhythmMaker(
                talea=rhythmmakertools.Talea(
                    counts=(1, 2, 3, 4),
                    denominator=16,
                    ),
                )

    Follows the two-step configure-once / call-repeatedly pattern shown here.

    Object model of a partially evaluated function that accepts a (possibly
    empty) list of divisions as input and returns a list of selections as
    output (structured one selection per input division).
    '''

    r'''Example helpers:

    # used in a piece with four voices:
    # voice 1 starts reading talea at beginning of talea;
    # voice 2 starts reading talea at second event of talea;
    # voice 3 starts reading talea at third event of talea;
    # voice 4 starts reading talea at fourth event of talea.
    def helper(talea, rotation):
        assert len(rotation) == 2
        if not talea:
            return talea
        voice_index, measure_index = rotation
        talea = sequencetools.rotate_sequence(talea, -voice_index)
        return talea

    # used in a piece with four voices:
    # voice 1 starts reading talea at beginning of talea;
    # voice 2 starts reading talea 1/4 of way through talea;
    # voice 3 starts reading talea 2/4 of way through talea;
    # voice 4 starts reading talea 3/4 of way through talea.
    def quarter_rotation_helper(talea, rotation):
        assert len(rotation) == 2
        if not talea:
            return talea
        voice_index, measure_index = rotation
        index_of_rotation = -voice_index * (len(talea) // 4)
        index_of_rotation += -4 * measure_index
        talea = sequencetools.rotate_sequence(talea, index_of_rotation)
        return talea
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Rhythm-makers'

    __slots__ = (
        '_burnish_specifier',
        '_extra_counts_per_division',
        '_helper_functions',
        '_read_talea_once_only',
        '_rest_tied_notes',
        '_split_divisions_by_counts',
        '_talea',
        '_tie_split_notes',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        talea=None,
        beam_specifier=None,
        burnish_specifier=None,
        division_masks=None,
        duration_spelling_specifier=None,
        extra_counts_per_division=None,
        logical_tie_masks=None,
        read_talea_once_only=None,
        rest_tied_notes=None,
        split_divisions_by_counts=None,
        tie_specifier=None,
        tie_split_notes=True,
        tuplet_spelling_specifier=None,
        helper_functions=None,
        ):
        from abjad.tools import rhythmmakertools
        RhythmMaker.__init__(
            self,
            beam_specifier=beam_specifier,
            duration_spelling_specifier=duration_spelling_specifier,
            division_masks=division_masks,
            logical_tie_masks=logical_tie_masks,
            tie_specifier=tie_specifier,
            tuplet_spelling_specifier=tuplet_spelling_specifier,
            )
        prototype = (rhythmmakertools.Talea, type(None))
        assert isinstance(talea, prototype)
        assert isinstance(read_talea_once_only, (bool, type(None)))
        self._read_talea_once_only = read_talea_once_only
        self._talea = talea
        if tie_split_notes is not None:
            assert isinstance(tie_split_notes, bool), repr(tie_split_notes)
        self._tie_split_notes = tie_split_notes
        helper_functions = helper_functions or {}
        talea_helper = helper_functions.get('talea')
        extra_counts_per_division_helper = helper_functions.get(
            'extra_counts_per_division')
        lefts_helper = helper_functions.get('left_classes')
        middles_helper = helper_functions.get('middle_classes')
        rights_helper = helper_functions.get('right_classes')
        left_lengths_helper = helper_functions.get('left_counts')
        right_lengths_helper = helper_functions.get('right_counts')
        secondary_divisions_helper = \
            helper_functions.get('split_divisions_by_counts')
        if extra_counts_per_division is not None:
            extra_counts_per_division = tuple(extra_counts_per_division)
        prototype = (rhythmmakertools.BurnishSpecifier, type(None))
        assert isinstance(burnish_specifier, prototype)
        self._burnish_specifier = burnish_specifier
        if split_divisions_by_counts is not None:
            split_divisions_by_counts = tuple(split_divisions_by_counts)
        talea_helper = self._none_to_trivial_helper(talea_helper)
        extra_counts_per_division_helper = self._none_to_trivial_helper(
            extra_counts_per_division_helper)
        lefts_helper = self._none_to_trivial_helper(lefts_helper)
        middles_helper = self._none_to_trivial_helper(middles_helper)
        rights_helper = self._none_to_trivial_helper(rights_helper)
        left_lengths_helper = self._none_to_trivial_helper(
            left_lengths_helper)
        right_lengths_helper = self._none_to_trivial_helper(
            right_lengths_helper)
        secondary_divisions_helper = self._none_to_trivial_helper(
            secondary_divisions_helper)
        assert extra_counts_per_division is None or \
            mathtools.all_are_integer_equivalent_numbers(
                extra_counts_per_division)
        assert split_divisions_by_counts is None or \
            mathtools.all_are_nonnegative_integer_equivalent_numbers(
                split_divisions_by_counts)
        assert callable(talea_helper)
        assert callable(extra_counts_per_division_helper)
        assert callable(lefts_helper)
        assert callable(middles_helper)
        assert callable(rights_helper)
        assert callable(left_lengths_helper)
        assert callable(right_lengths_helper)
        self._extra_counts_per_division = extra_counts_per_division
        self._split_divisions_by_counts = split_divisions_by_counts
        assert isinstance(rest_tied_notes, (bool, type(None))), rest_tied_notes
        self._rest_tied_notes = rest_tied_notes
        if helper_functions == {}:
            helper_functions = None
        self._helper_functions = helper_functions

    ### SPECIAL METHODS ###

    def __call__(self, divisions, rotation=None):
        r'''Calls talea rhythm-maker on `divisions`.

        ..  container:: example

                >>> rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
                ...     talea=rhythmmakertools.Talea(
                ...         counts=[1, 2, 3, 4],
                ...         denominator=16,
                ...         ),
                ...     )

            ::

                >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
                >>> selections = rhythm_maker(divisions)

            ::

                >>> for selection in selections:
                ...     selection
                Selection([Note("c'16"), Note("c'8"), Note("c'8.")])
                Selection([Note("c'4"), Note("c'16"), Note("c'8"), Note("c'16")])
                Selection([Note("c'8"), Note("c'4")])
                Selection([Note("c'16"), Note("c'8"), Note("c'8."), Note("c'8")])

        ..  todo:: Add rotation examples.

        Returns list of of selections.
        '''
        return RhythmMaker.__call__(
            self,
            divisions,
            rotation=rotation,
            )

    def __format__(self, format_specification=''):
        r'''Formats talea rhythm-maker.

        Set `format_specification` to `''` or `'storage'`.

        ..  container:: example

            **Example 1.** Formats talea rhythm-maker:

                >>> rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
                ...     talea=rhythmmakertools.Talea(
                ...         counts=[1, 2, 3, 4],
                ...         denominator=16,
                ...         ),
                ...     )

            ::

                >>> print(format(rhythm_maker))
                rhythmmakertools.TaleaRhythmMaker(
                    talea=rhythmmakertools.Talea(
                        counts=(1, 2, 3, 4),
                        denominator=16,
                        ),
                    )

        ..  container:: example

            **Example 2.** Storage formats talea rhythm-maker:

                >>> rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
                ...     talea=rhythmmakertools.Talea(
                ...         counts=[1, 2, 3, 4],
                ...         denominator=16,
                ...         ),
                ...     )

            ::

                >>> print(format(rhythm_maker, 'storage'))
                rhythmmakertools.TaleaRhythmMaker(
                    talea=rhythmmakertools.Talea(
                        counts=(1, 2, 3, 4),
                        denominator=16,
                        ),
                    )

        Returns string.
        '''
        superclass = super(TaleaRhythmMaker, self)
        return superclass.__format__(format_specification=format_specification)

    def __illustrate__(self, divisions=((3, 8), (4, 8), (3, 16), (4, 16))):
        r'''Illustrates talea rhythm-maker.

        ..  container:: example

            ::

                >>> rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
                ...     talea=rhythmmakertools.Talea(
                ...         counts=[1, 2, 3, 4],
                ...         denominator=16,
                ...         ),
                ...     )
                >>> show(rhythm_maker) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = rhythm_maker.__illustrate__()
                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 3/8
                        c'16 [
                        c'8
                        c'8. ]
                    }
                    {
                        \time 4/8
                        c'4
                        c'16 [
                        c'8
                        c'16 ~ ]
                    }
                    {
                        \time 3/16
                        c'8 [
                        c'16 ~ ]
                    }
                    {
                        \time 4/16
                        c'8. [
                        c'16 ]
                    }
                }

        Defaults `divisions` to ``3/8``, ``4/8``, ``3/16``, ``4/16``.

        Returns LilyPond file.
        '''
        return RhythmMaker.__illustrate__(self, divisions=divisions)

    def __repr__(self):
        r'''Gets interpreter representation.

        ..  container:: example

            ::

                >>> rhythmmakertools.TaleaRhythmMaker(
                ...     talea=rhythmmakertools.Talea(
                ...         counts=[1, 2, 3, 4],
                ...         denominator=16,
                ...         ),
                ...     )
                TaleaRhythmMaker(talea=Talea(counts=(1, 2, 3, 4), denominator=16))

        Returns string.
        '''
        return super(TaleaRhythmMaker, self).__repr__()

    ### PRIVATE METHODS ###

    def _apply_burnish_specifier(self, divisions):
        burnish_specifier = self._get_burnish_specifier()
        return burnish_specifier(
            divisions,
            helper_functions=self.helper_functions,
            rotation=self._rotation,
            )

    def _apply_ties_to_split_notes(self, result, unscaled_talea):
        from abjad.tools import rhythmmakertools
        tie_specifier = self._get_tie_specifier()
        if not self.tie_split_notes:
            return
        leaves = select(result).by_class(scoretools.Leaf)
        written_durations = [leaf.written_duration for leaf in leaves]
        weights = []
        for numerator in unscaled_talea:
            duration = durationtools.Duration(
                numerator,
                self.talea.denominator,
                )
            weight = abs(duration)
            weights.append(weight)
        parts = sequencetools.partition_sequence_by_weights(
            written_durations,
            weights=weights,
            allow_part_weights=More,
            cyclic=True,
            overhang=True,
            )
        counts = [len(part) for part in parts]
        parts = sequencetools.partition_sequence_by_counts(leaves, counts)
        prototype = (spannertools.Tie,)
        for part in parts:
            if any(isinstance(_, scoretools.Rest) for _ in part):
                continue
            part = selectiontools.Selection(part)
            tie_spanner = spannertools.Tie()
            # voodoo to temporarily neuter the contiguity constraint
            tie_spanner._unconstrain_contiguity()
            for component in part:
                # TODO: make top-level detach() work here
                for spanner in component._get_spanners(prototype=prototype):
                    spanner._sever_all_components()
                #detach(prototype, component)
            # TODO: remove usage of Spanner._extend()
            tie_spanner._extend(part)
            tie_spanner._constrain_contiguity()

    def _get_burnish_specifier(self):
        from abjad.tools import rhythmmakertools
        if self.burnish_specifier is not None:
            return self.burnish_specifier
        return rhythmmakertools.BurnishSpecifier()

    def _get_format_specification(self):
        from abjad.tools import systemtools
        agent = systemtools.StorageFormatAgent(self)
        names = list(agent.signature_keyword_names)
        if self.tie_split_notes:
            names.remove('tie_split_notes')
        return systemtools.FormatSpecification(
            self,
            storage_format_kwargs_names=names,
            )

    def _get_talea(self):
        from abjad.tools import rhythmmakertools
        if self.talea is not None:
            return self.talea
        return rhythmmakertools.Talea()

    def _handle_rest_tied_notes(self, selections):
        if not self.rest_tied_notes:
            return selections
        # wrap every selection in a temporary container;
        # this allows the call to mutate().replace() to work
        containers = []
        for selection in selections:
            container = scoretools.Container(selection)
            attach('temporary container', container)
            containers.append(container)
        for logical_tie in iterate(selections).by_logical_tie():
            if not logical_tie.is_trivial:
                for note in logical_tie[1:]:
                    rest = scoretools.Rest(note)
                    mutate(note).replace(rest)
                detach(spannertools.Tie, logical_tie.head)
        # remove every temporary container and recreate selections
        new_selections = []
        for container in containers:
            inspector = inspect_(container)
            assert inspector.get_indicator(str) == 'temporary container'
            new_selection = mutate(container).eject_contents()
            new_selections.append(new_selection)
        return new_selections

    def _make_leaf_lists(self, numeric_map, talea_denominator):
        leaf_lists = []
        specifier = self._get_duration_spelling_specifier()
        for map_division in numeric_map:
            leaf_list = scoretools.make_leaves_from_talea(
                map_division,
                talea_denominator,
                decrease_durations_monotonically=\
                    specifier.decrease_durations_monotonically,
                forbidden_written_duration=\
                    specifier.forbidden_written_duration,
                spell_metrically=specifier.spell_metrically,
                )
            leaf_lists.append(leaf_list)
        return leaf_lists

    def _make_music(self, divisions, rotation):
        input_divisions = divisions[:]
        input_ = self._rotate_input(
            helper_functions=self.helper_functions,
            rotation=self._rotation,
            )
        talea = input_['talea']
        extra_counts_per_division = input_['extra_counts_per_division']
        unscaled_talea = tuple(talea)
        split_divisions_by_counts = input_['split_divisions_by_counts']
        taleas = (talea, extra_counts_per_division, split_divisions_by_counts)
        if self.talea is not None:
            talea_denominator = self.talea.denominator
        else:
            talea_denominator = None
        result = self._scale_taleas(divisions, talea_denominator, taleas)
        divisions = result[0]
        lcd = result[1]
        talea = result[2]
        extra_counts_per_division = result[3]
        split_divisions_by_counts = result[4]
        secondary_divisions = self._make_secondary_divisions(
            divisions,
            split_divisions_by_counts,
            )
        if talea:
            numeric_map = self._make_numeric_map(
                secondary_divisions,
                talea,
                extra_counts_per_division,
                )
            leaf_lists = self._make_leaf_lists(numeric_map, lcd)
            if not extra_counts_per_division:
                result = leaf_lists
            else:
                tuplets = self._make_tuplets(secondary_divisions, leaf_lists)
                result = tuplets
            selections = [selectiontools.Selection(x) for x in result]
        else:
            selections = []
            for division in secondary_divisions:
                selection = scoretools.make_leaves([0], [division])
                selections.append(selection)
        beam_specifier = self._get_beam_specifier()
        beam_specifier(selections)
        if talea:
            self._apply_ties_to_split_notes(selections, unscaled_talea)
        selections = self._handle_rest_tied_notes(selections)
        selections = self._apply_division_masks(selections, rotation)
        specifier = self._get_duration_spelling_specifier()
        if specifier.rewrite_meter:
            selections = specifier._rewrite_meter_(
                selections,
                input_divisions,
                )
        return selections

    def _make_numeric_map(self, divisions, talea, extra_counts_per_division):
        assert all(isinstance(_, int) for _ in talea), repr(talea)
        prolated_divisions = self._make_prolated_divisions(
            divisions,
            extra_counts_per_division,
            )
        prolated_divisions = [
            mathtools.NonreducedFraction(_) for _ in prolated_divisions
            ]
        if not talea:
            map_divisions = prolated_divisions
            return map_divisions
        prolated_numerators = [_.numerator for _ in prolated_divisions]
        map_divisions = self._split_sequence_extended_to_weights(
            talea,
            prolated_numerators,
            )
        for list_ in map_divisions:
            assert all(isinstance(_, int) for _ in list_), repr(list_)
        if self.burnish_specifier is not None:
            map_divisions = self._apply_burnish_specifier(map_divisions)
        return map_divisions

    def _make_prolated_divisions(self, divisions, extra_counts_per_division):
        prolated_divisions = []
        for i, division in enumerate(divisions):
            if not extra_counts_per_division:
                prolated_divisions.append(division)
                continue
            prolation_addendum = extra_counts_per_division[i]
            if hasattr(division, 'numerator'):
                numerator = division.numerator
            else:
                numerator = division[0]
            if 0 <= prolation_addendum:
                prolation_addendum %= numerator
            else:
                # NOTE: do not remove the following (nonfunctional) if-else;
                #       preserved for backwards compatability.
                use_old_extra_counts_logic = False
                if use_old_extra_counts_logic:
                    prolation_addendum %= numerator
                else:
                    prolation_addendum %= -numerator
            if isinstance(division, tuple):
                numerator, denominator = division
            else:
                numerator, denominator = division.pair
            prolated_division = (
                numerator + prolation_addendum,
                denominator,
                )
            prolated_divisions.append(prolated_division)
        return prolated_divisions

    def _rotate_input(self, helper_functions=None, rotation=None):
        helper_functions = helper_functions or {}
        if self.talea is not None:
            talea = self.talea.counts or ()
        else:
            talea = ()
        helper_function = helper_functions.get('talea')
        helper_function = self._none_to_trivial_helper(helper_function)
        talea = helper_function(talea, rotation)
        talea = datastructuretools.CyclicTuple(talea)
        extra_counts_per_division = self.extra_counts_per_division or ()
        helper_function = helper_functions.get('extra_counts_per_division')
        helper_function = self._none_to_trivial_helper(helper_function)
        extra_counts_per_division = helper_function(
            extra_counts_per_division,
            rotation,
            )
        extra_counts_per_division = datastructuretools.CyclicTuple(
            extra_counts_per_division)
        split_divisions_by_counts = self.split_divisions_by_counts or ()
        helper_function = helper_functions.get('split_divisions_by_counts')
        helper_function = self._none_to_trivial_helper(helper_function)
        split_divisions_by_counts = helper_function(
            split_divisions_by_counts,
            rotation,
            )
        split_divisions_by_counts = datastructuretools.CyclicTuple(
            split_divisions_by_counts)
        return {
            'extra_counts_per_division': extra_counts_per_division,
            'split_divisions_by_counts': split_divisions_by_counts,
            'talea': talea,
            }

    def _split_sequence_extended_to_weights(self, sequence, weights):
        assert mathtools.all_are_positive_integers(weights), repr(weights)
        sequence_weight = mathtools.weight(sequence)
        total_weight = mathtools.weight(weights)
        if self.read_talea_once_only:
            if sequence_weight < total_weight:
                message = 'talea is too short to read once only:'
                message += '\n{!r} in {!r}.'
                message = message.format(sequence, weights)
                raise Exception(message)
        sequence = sequencetools.repeat_sequence_to_weight(
            sequence,
            total_weight,
            )
        result = sequencetools.split_sequence(sequence, weights, cyclic=False)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def beam_specifier(self):
        r'''Gets beam specifier.

        ..  container:: example

            **Example 1.** Beams each division:

            ::

                >>> rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
                ...     talea=rhythmmakertools.Talea(
                ...         counts=[1],
                ...         denominator=16,
                ...         ),
                ...     beam_specifier=rhythmmakertools.BeamSpecifier(
                ...         beam_each_division=True,
                ...         ),
                ...     )

            ::

                >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 3/8
                        c'16 [
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16 ]
                    }
                    {
                        \time 4/8
                        c'16 [
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16 ]
                    }
                    {
                        \time 3/8
                        c'16 [
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16 ]
                    }
                    {
                        \time 4/8
                        c'16 [
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16 ]
                    }
                }

            This is default behavior.

        ..  container:: example

            **Example 2.** Beams divisions together:

            ::

                >>> rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
                ...     talea=rhythmmakertools.Talea(
                ...         counts=[1],
                ...         denominator=16,
                ...         ),
                ...     beam_specifier=rhythmmakertools.BeamSpecifier(
                ...         beam_divisions_together=True,
                ...         ),
                ...     )

            ::

                >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 3/8
                        \set stemLeftBeamCount = #0
                        \set stemRightBeamCount = #2
                        c'16 [
                        \set stemLeftBeamCount = #2
                        \set stemRightBeamCount = #2
                        c'16
                        \set stemLeftBeamCount = #2
                        \set stemRightBeamCount = #2
                        c'16
                        \set stemLeftBeamCount = #2
                        \set stemRightBeamCount = #2
                        c'16
                        \set stemLeftBeamCount = #2
                        \set stemRightBeamCount = #2
                        c'16
                        \set stemLeftBeamCount = #2
                        \set stemRightBeamCount = #1
                        c'16
                    }
                    {
                        \time 4/8
                        \set stemLeftBeamCount = #1
                        \set stemRightBeamCount = #2
                        c'16
                        \set stemLeftBeamCount = #2
                        \set stemRightBeamCount = #2
                        c'16
                        \set stemLeftBeamCount = #2
                        \set stemRightBeamCount = #2
                        c'16
                        \set stemLeftBeamCount = #2
                        \set stemRightBeamCount = #2
                        c'16
                        \set stemLeftBeamCount = #2
                        \set stemRightBeamCount = #2
                        c'16
                        \set stemLeftBeamCount = #2
                        \set stemRightBeamCount = #2
                        c'16
                        \set stemLeftBeamCount = #2
                        \set stemRightBeamCount = #2
                        c'16
                        \set stemLeftBeamCount = #2
                        \set stemRightBeamCount = #1
                        c'16
                    }
                    {
                        \time 3/8
                        \set stemLeftBeamCount = #1
                        \set stemRightBeamCount = #2
                        c'16
                        \set stemLeftBeamCount = #2
                        \set stemRightBeamCount = #2
                        c'16
                        \set stemLeftBeamCount = #2
                        \set stemRightBeamCount = #2
                        c'16
                        \set stemLeftBeamCount = #2
                        \set stemRightBeamCount = #2
                        c'16
                        \set stemLeftBeamCount = #2
                        \set stemRightBeamCount = #2
                        c'16
                        \set stemLeftBeamCount = #2
                        \set stemRightBeamCount = #1
                        c'16
                    }
                    {
                        \time 4/8
                        \set stemLeftBeamCount = #1
                        \set stemRightBeamCount = #2
                        c'16
                        \set stemLeftBeamCount = #2
                        \set stemRightBeamCount = #2
                        c'16
                        \set stemLeftBeamCount = #2
                        \set stemRightBeamCount = #2
                        c'16
                        \set stemLeftBeamCount = #2
                        \set stemRightBeamCount = #2
                        c'16
                        \set stemLeftBeamCount = #2
                        \set stemRightBeamCount = #2
                        c'16
                        \set stemLeftBeamCount = #2
                        \set stemRightBeamCount = #2
                        c'16
                        \set stemLeftBeamCount = #2
                        \set stemRightBeamCount = #2
                        c'16
                        \set stemLeftBeamCount = #2
                        \set stemRightBeamCount = #0
                        c'16 ]
                    }
                }

        ..  container:: example

            **Example 3.** Beams nothing:

            ::

                >>> rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
                ...     talea=rhythmmakertools.Talea(
                ...         counts=[1],
                ...         denominator=16,
                ...         ),
                ...     beam_specifier=rhythmmakertools.BeamSpecifier(
                ...         beam_each_division=False,
                ...         beam_divisions_together=False,
                ...         ),
                ...     )

            ::

                >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 3/8
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                    }
                    {
                        \time 4/8
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                    }
                    {
                        \time 3/8
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                    }
                    {
                        \time 4/8
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                    }
                }

        ..  container:: example

            **Example 4.** Does not beam rests:

            ::

                >>> rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
                ...     talea=rhythmmakertools.Talea(
                ...         counts=[1, 1, 1, -1],
                ...         denominator=16,
                ...         ),
                ...     beam_specifier=rhythmmakertools.BeamSpecifier(
                ...         beam_each_division=True,
                ...         ),
                ...     )

            ::

                >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 3/8
                        c'16 [
                        c'16
                        c'16 ]
                        r16
                        c'16 [
                        c'16 ]
                    }
                    {
                        \time 4/8
                        c'16
                        r16
                        c'16 [
                        c'16
                        c'16 ]
                        r16
                        c'16 [
                        c'16 ]
                    }
                    {
                        \time 3/8
                        c'16
                        r16
                        c'16 [
                        c'16
                        c'16 ]
                        r16
                    }
                    {
                        \time 4/8
                        c'16 [
                        c'16
                        c'16 ]
                        r16
                        c'16 [
                        c'16
                        c'16 ]
                        r16
                    }
                }

        ..  container:: example

            **Example 5.** Does beam rests:

            ::

                >>> rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
                ...     talea=rhythmmakertools.Talea(
                ...         counts=[1, 1, 1, -1],
                ...         denominator=16,
                ...         ),
                ...     beam_specifier=rhythmmakertools.BeamSpecifier(
                ...         beam_each_division=True,
                ...         beam_rests=True,
                ...         ),
                ...     )

            ::

                >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 3/8
                        c'16 [
                        c'16
                        c'16
                        r16
                        c'16
                        c'16 ]
                    }
                    {
                        \time 4/8
                        c'16 [
                        r16
                        c'16
                        c'16
                        c'16
                        r16
                        c'16
                        c'16 ]
                    }
                    {
                        \time 3/8
                        c'16 [
                        r16
                        c'16
                        c'16
                        c'16
                        r16 ]
                    }
                    {
                        \time 4/8
                        c'16 [
                        c'16
                        c'16
                        r16
                        c'16
                        c'16
                        c'16
                        r16 ]
                    }
                }

        ..  container:: example

            **Example 6.** Beams rests with stemlets:

            ::

                >>> rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
                ...     talea=rhythmmakertools.Talea(
                ...         counts=[1, 1, 1, -1],
                ...         denominator=16,
                ...         ),
                ...     beam_specifier=rhythmmakertools.BeamSpecifier(
                ...         beam_each_division=True,
                ...         beam_rests=True,
                ...         stemlet_length=0.75,
                ...         ),
                ...     )

            ::

                >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 3/8
                        \override Staff.Stem.stemlet-length = #0.75
                        c'16 [
                        c'16
                        c'16
                        r16
                        c'16
                        c'16 ]
                        \revert Staff.Stem.stemlet-length
                    }
                    {
                        \time 4/8
                        \override Staff.Stem.stemlet-length = #0.75
                        c'16 [
                        r16
                        c'16
                        c'16
                        c'16
                        r16
                        c'16
                        c'16 ]
                        \revert Staff.Stem.stemlet-length
                    }
                    {
                        \time 3/8
                        \override Staff.Stem.stemlet-length = #0.75
                        c'16 [
                        r16
                        c'16
                        c'16
                        c'16
                        r16 ]
                        \revert Staff.Stem.stemlet-length
                    }
                    {
                        \time 4/8
                        \override Staff.Stem.stemlet-length = #0.75
                        c'16 [
                        c'16
                        c'16
                        r16
                        c'16
                        c'16
                        c'16
                        r16 ]
                        \revert Staff.Stem.stemlet-length
                    }
                }

        Set to beam specifier or none.

        Returns beam specifier or none.
        '''
        return RhythmMaker.beam_specifier.fget(self)

    @property
    def burnish_specifier(self):
        r'''Gets burnish specifier.

        ..  container:: example

            **Example 1.** Forces the first leaf and the last two leaves to be
            rests:

            ::

                >>> rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
                ...     talea=rhythmmakertools.Talea(
                ...         counts=[1, 2, 3, 4],
                ...         denominator=16,
                ...         ),
                ...     burnish_specifier=rhythmmakertools.BurnishSpecifier(
                ...         left_classes=[Rest],
                ...         left_counts=[1],
                ...         right_classes=[Rest],
                ...         right_counts=[2],
                ...         outer_divisions_only=True,
                ...         ),
                ...     )

            ::

                >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff) # doctest: +SKIP
                \new RhythmicStaff {
                    {
                        \time 3/8
                        r16
                        c'8 [
                        c'8. ]
                    }
                    {
                        \time 4/8
                        c'4
                        c'16 [
                        c'8
                        c'16 ~ ]
                    }
                    {
                        \time 3/8
                        c'8
                        c'4
                    }
                    {
                        \time 4/8
                        c'16 [
                        c'8 ]
                        r8.
                        r8
                    }
                }

        ..  container:: example

            **Example 2.** Forces the first leaf of every division to be a
            rest:

            ::

                >>> rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
                ...     talea=rhythmmakertools.Talea(
                ...         counts=[1, 2, 3, 4],
                ...         denominator=16,
                ...         ),
                ...     burnish_specifier=rhythmmakertools.BurnishSpecifier(
                ...         left_classes=[Rest],
                ...         left_counts=[1],
                ...         ),
                ...     )

            ::

                >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 3/8
                        r16
                        c'8 [
                        c'8. ]
                    }
                    {
                        \time 4/8
                        r4
                        c'16 [
                        c'8
                        c'16 ]
                    }
                    {
                        \time 3/8
                        r8
                        c'4
                    }
                    {
                        \time 4/8
                        r16
                        c'8 [
                        c'8.
                        c'8 ]
                    }
                }

        Set to burnish specifier or none.

        Returns burnish specifier or none.
        '''
        return self._burnish_specifier

    @property
    def division_masks(self):
        r'''Gets division masks.

        ..  container:: example

            **Example 1.** No division masks:

            ::

                >>> rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
                ...     talea=rhythmmakertools.Talea(
                ...         counts=[1, 2, 3, 4],
                ...         denominator=16,
                ...         ),
                ...     )

            ::

                >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 3/8
                        c'16 [
                        c'8
                        c'8. ]
                    }
                    {
                        \time 4/8
                        c'4
                        c'16 [
                        c'8
                        c'16 ~ ]
                    }
                    {
                        \time 3/8
                        c'8
                        c'4
                    }
                    {
                        \time 4/8
                        c'16 [
                        c'8
                        c'8.
                        c'8 ]
                    }
                }

        ..  container:: example

            **Example 2.** Silences every other output division:

            ::

                >>> rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
                ...     talea=rhythmmakertools.Talea(
                ...         counts=[1, 2, 3, 4],
                ...         denominator=16,
                ...         ),
                ...     division_masks=[
                ...         rhythmmakertools.SilenceMask(
                ...             pattern=patterntools.select_every([1], period=2),
                ...             ),
                ...         ],
                ...     )

            ::

                >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 3/8
                        c'16 [
                        c'8
                        c'8. ]
                    }
                    {
                        \time 4/8
                        r2
                    }
                    {
                        \time 3/8
                        c'8
                        c'4
                    }
                    {
                        \time 4/8
                        r2
                    }
                }

        ..  container:: example

            **Example 3.** Sustains every other output division:

            ::

                >>> rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
                ...     talea=rhythmmakertools.Talea(
                ...         counts=[1, 2, 3, 4],
                ...         denominator=16,
                ...         ),
                ...     division_masks=[
                ...         rhythmmakertools.sustain_every([1], period=2),
                ...         ],
                ...     )

            ::

                >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 3/8
                        c'16 [
                        c'8
                        c'8. ]
                    }
                    {
                        \time 4/8
                        c'2
                    }
                    {
                        \time 3/8
                        c'8
                        c'4
                    }
                    {
                        \time 4/8
                        c'2
                    }
                }

        ..  container:: example

            **Example 4.** Silences every other secondary output division:

            ::

                >>> rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
                ...     talea=rhythmmakertools.Talea(
                ...         counts=[1],
                ...         denominator=16,
                ...         ),
                ...     split_divisions_by_counts=[9],
                ...     division_masks=[
                ...         rhythmmakertools.SilenceMask(
                ...             pattern=patterntools.select_every([1], period=2),
                ...             ),
                ...         ],
                ...     )

            ::

                >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 3/8
                        c'16 [
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16 ]
                    }
                    {
                        \time 4/8
                        r8.
                        c'16 [
                        c'16
                        c'16
                        c'16
                        c'16 ]
                    }
                    {
                        \time 3/8
                        r4
                        c'16 [
                        c'16 ]
                    }
                    {
                        \time 4/8
                        r4..
                        c'16
                    }
                }

        ..  container:: example

            **Example 5.** Sustains every other secondary output division:

            ::

                >>> rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
                ...     talea=rhythmmakertools.Talea(
                ...         counts=[1],
                ...         denominator=16,
                ...         ),
                ...     split_divisions_by_counts=[9],
                ...     division_masks=[
                ...         rhythmmakertools.sustain_every([1], period=2),
                ...         ],
                ...     )

            ::

                >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 3/8
                        c'16 [
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16 ]
                    }
                    {
                        \time 4/8
                        c'8.
                        c'16 [
                        c'16
                        c'16
                        c'16
                        c'16 ]
                    }
                    {
                        \time 3/8
                        c'4
                        c'16 [
                        c'16 ]
                    }
                    {
                        \time 4/8
                        c'4..
                        c'16
                    }
                }

        Set to tuple of division masks or none.

        Returns tuple of division masks or none.
        '''
        superclass = super(TaleaRhythmMaker, self)
        return superclass.division_masks

    @property
    def duration_spelling_specifier(self):
        r'''Gets duration spelling specifier.

        Several duration spelling specifier configurations are available.

        ..  container:: example

            **Example 1.** Spells nonassignable durations with monontonically
            decreasing durations:

            ::

                >>> rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
                ...     talea=rhythmmakertools.Talea(
                ...         counts=[5],
                ...         denominator=16,
                ...         ),
                ...     duration_spelling_specifier=rhythmmakertools.DurationSpellingSpecifier(
                ...         decrease_durations_monotonically=True,
                ...         ),
                ...     )

            ::

                >>> divisions = [(5, 8), (5, 8), (5, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 5/8
                        c'4 ~
                        c'16
                        c'4 ~
                        c'16
                    }
                    {
                        c'4 ~
                        c'16
                        c'4 ~
                        c'16
                    }
                    {
                        c'4 ~
                        c'16
                        c'4 ~
                        c'16
                    }
                }

            This is default behavior.

        ..  container:: example

            **Example 2.** Spells nonassignable durations with monontonically
            increasing durations:

            ::

                >>> rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
                ...     talea=rhythmmakertools.Talea(
                ...         counts=[5],
                ...         denominator=16,
                ...         ),
                ...     duration_spelling_specifier=rhythmmakertools.DurationSpellingSpecifier(
                ...         decrease_durations_monotonically=False,
                ...         ),
                ...     )

            ::

                >>> divisions = [(5, 8), (5, 8), (5, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 5/8
                        c'16 ~
                        c'4
                        c'16 ~
                        c'4
                    }
                    {
                        c'16 ~
                        c'4
                        c'16 ~
                        c'4
                    }
                    {
                        c'16 ~
                        c'4
                        c'16 ~
                        c'4
                    }
                }

        ..  container:: example

            **Example 3.** Forbids no durations:

            ::

                >>> rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
                ...     talea=rhythmmakertools.Talea(
                ...         counts=[1, 1, 1, 1, 4, 4],
                ...         denominator=16,
                ...         ),
                ...     duration_spelling_specifier=rhythmmakertools.DurationSpellingSpecifier(
                ...         forbidden_written_duration=None,
                ...         ),
                ...     )

            ::

                >>> divisions = [(3, 4), (3, 4)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 3/4
                        c'16 [
                        c'16
                        c'16
                        c'16 ]
                        c'4
                        c'4
                    }
                    {
                        c'16 [
                        c'16
                        c'16
                        c'16 ]
                        c'4
                        c'4
                    }
                }

            This is default behavior.

        ..  container:: example

            **Example 4.** Forbids durations equal to ``1/4`` or greater:

                >>> rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
                ...     talea=rhythmmakertools.Talea(
                ...         counts=[1, 1, 1, 1, 4, 4],
                ...         denominator=16,
                ...         ),
                ...     duration_spelling_specifier=rhythmmakertools.DurationSpellingSpecifier(
                ...         forbidden_written_duration=Duration(1, 4),
                ...         ),
                ...     )

            ::

                >>> divisions = [(3, 4), (3, 4)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 3/4
                        c'16 [
                        c'16
                        c'16
                        c'16
                        c'8 ~
                        c'8
                        c'8 ~
                        c'8 ]
                    }
                    {
                        c'16 [
                        c'16
                        c'16
                        c'16
                        c'8 ~
                        c'8
                        c'8 ~
                        c'8 ]
                    }
                }

            Rewrites forbidden durations with smaller durations tied together.

        ..  container:: example

            **Example 5.** Spells all durations metrically:

                >>> rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
                ...     talea=rhythmmakertools.Talea(
                ...         counts=[5, 4],
                ...         denominator=16,
                ...         ),
                ...     duration_spelling_specifier=rhythmmakertools.DurationSpellingSpecifier(
                ...         spell_metrically=True,
                ...         ),
                ...     )

            ::

                >>> divisions = [(3, 4), (3, 4), (3, 4)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 3/4
                        c'8. ~ [
                        c'8 ]
                        c'4
                        c'16 ~ [
                        c'16 ~
                        c'16 ~ ]
                    }
                    {
                        c'8
                        c'4
                        c'8. ~ [
                        c'8
                        c'16 ~ ]
                    }
                    {
                        c'16 ~ [
                        c'16 ~
                        c'16
                        c'8. ~
                        c'8 ]
                        c'4
                    }
                }

        ..  container:: example

            **Example 6.** Spells unassignable durations metrically:

                >>> rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
                ...     talea=rhythmmakertools.Talea(
                ...         counts=[5, 4],
                ...         denominator=16,
                ...         ),
                ...     duration_spelling_specifier=rhythmmakertools.DurationSpellingSpecifier(
                ...         spell_metrically='unassignable',
                ...         ),
                ...     )

            ::

                >>> divisions = [(3, 4), (3, 4), (3, 4)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 3/4
                        c'8. ~ [
                        c'8 ]
                        c'4
                        c'8. ~
                    }
                    {
                        c'8
                        c'4
                        c'8. ~ [
                        c'8
                        c'16 ~ ]
                    }
                    {
                        c'8. [
                        c'8. ~
                        c'8 ]
                        c'4
                    }
                }

        ..  container:: example

            **Example 7.** Rewrites meter:

                >>> rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
                ...     talea=rhythmmakertools.Talea(
                ...         counts=[5, 4],
                ...         denominator=16,
                ...         ),
                ...     duration_spelling_specifier=rhythmmakertools.DurationSpellingSpecifier(
                ...         rewrite_meter=True,
                ...         ),
                ...     )

            ::

                >>> divisions = [(3, 4), (3, 4), (3, 4)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 3/4
                        c'4 ~
                        c'16 [
                        c'8. ~
                        c'16
                        c'8. ~ ]
                    }
                    {
                        c'8 [
                        c'8 ~
                        c'8
                        c'8 ~
                        c'8.
                        c'16 ~ ]
                    }
                    {
                        c'8. [
                        c'16 ~ ]
                        c'4
                        c'4
                    }
                }

        Set to duration spelling specifier or none.

        Returns duration spelling specifier or none.
        '''
        return RhythmMaker.duration_spelling_specifier.fget(self)

    @property
    def extra_counts_per_division(self):
        r'''Gets extra counts per division.

        ..  container:: example

            **Example 1.** No extra counts per division:

            ::

                >>> rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
                ...     talea=rhythmmakertools.Talea(
                ...         counts=[1, 2, 3, 4],
                ...         denominator=16,
                ...         ),
                ...     )

            ::

                >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 3/8
                        c'16 [
                        c'8
                        c'8. ]
                    }
                    {
                        \time 4/8
                        c'4
                        c'16 [
                        c'8
                        c'16 ~ ]
                    }
                    {
                        \time 3/8
                        c'8
                        c'4
                    }
                    {
                        \time 4/8
                        c'16 [
                        c'8
                        c'8.
                        c'8 ]
                    }
                }

        ..  container:: example

            **Example 2.** Adds one extra count to every other division:

            ::

                >>> rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
                ...     talea=rhythmmakertools.Talea(
                ...         counts=[1, 2, 3, 4],
                ...         denominator=16,
                ...         ),
                ...     extra_counts_per_division=(0, 1,),
                ...     )

            ::

                >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 3/8
                        {
                            c'16 [
                            c'8
                            c'8. ]
                        }
                    }
                    {
                        \time 4/8
                        \times 8/9 {
                            c'4
                            c'16 [
                            c'8
                            c'8 ~ ]
                        }
                    }
                    {
                        \time 3/8
                        {
                            c'16
                            c'4
                            c'16
                        }
                    }
                    {
                        \time 4/8
                        \times 8/9 {
                            c'8 [
                            c'8. ]
                            c'4
                        }
                    }
                }

        ..  container:: example

            **Example 3.** Adds two extra counts to every other division:

            ::

                >>> rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
                ...     talea=rhythmmakertools.Talea(
                ...         counts=[1, 2, 3, 4],
                ...         denominator=16,
                ...         ),
                ...     extra_counts_per_division=(0, 2,),
                ...     )

            ::

                >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 3/8
                        {
                            c'16 [
                            c'8
                            c'8. ]
                        }
                    }
                    {
                        \time 4/8
                        \times 4/5 {
                            c'4
                            c'16 [
                            c'8
                            c'8. ]
                        }
                    }
                    {
                        \time 3/8
                        {
                            c'4
                            c'16 [
                            c'16 ~ ]
                        }
                    }
                    {
                        \time 4/8
                        \times 4/5 {
                            c'16 [
                            c'8. ]
                            c'4
                            c'16 [
                            c'16 ]
                        }
                    }
                }

            The duration of each added count equals the duration
            of each count in the rhythm-maker's input talea.

        ..  container:: example

            **Example 4.** Removes one count from every other division:

            ::

                >>> rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
                ...     talea=rhythmmakertools.Talea(
                ...         counts=[1, 2, 3, 4],
                ...         denominator=16,
                ...         ),
                ...     extra_counts_per_division=(0, -1),
                ...     )

            ::

                >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 3/8
                        {
                            c'16 [
                            c'8
                            c'8. ]
                        }
                    }
                    {
                        \time 4/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 8/7 {
                            c'4
                            c'16 [
                            c'8 ]
                        }
                    }
                    {
                        \time 3/8
                        {
                            c'8. [
                            c'8. ~ ]
                        }
                    }
                    {
                        \time 4/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 8/7 {
                            c'16 [
                            c'16
                            c'8
                            c'8. ]
                        }
                    }
                }

        Set to integer tuple or none.

        Returns integer tuple or none.
        '''
        return self._extra_counts_per_division

    @property
    def helper_functions(self):
        r'''Gets helper functions.

        Set to dictionary or none.

        Returns dictionary or none.
        '''
        return self._helper_functions

    @property
    def logical_tie_masks(self):
        r'''Gets logical tie masks.

        ..  container:: example

            **Example 1.** Silences every third logical tie:

            ::

                >>> rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
                ...     logical_tie_masks=[
                ...         rhythmmakertools.silence_every([2], period=3),
                ...         ],
                ...     talea=rhythmmakertools.Talea(
                ...         counts=[1, 2, 3, 4],
                ...         denominator=16,
                ...         ),
                ...     )

            ::

                >>> divisions = [(3, 8), (3, 8), (3, 8), (3, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 3/8
                        c'16 [
                        c'8 ]
                        r8.
                    }
                    {
                        c'4
                        c'16
                        r16
                    }
                    {
                        r16
                        c'8. [
                        c'8 ~ ]
                    }
                    {
                        c'8
                        r16
                        c'8 [
                        c'16 ]
                    }
                }

        ..  container:: example

            **Example 2.** Silences the first and last logical ties:

            ::

                >>> rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
                ...     logical_tie_masks=[
                ...         rhythmmakertools.silence_first(),
                ...         rhythmmakertools.silence_last(),
                ...         ],
                ...     talea=rhythmmakertools.Talea(
                ...         counts=[1, 2, 3, 4],
                ...         denominator=16,
                ...         ),
                ...     )

            ::

                >>> divisions = [(3, 8), (3, 8), (3, 8), (3, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 3/8
                        r16
                        c'8 [
                        c'8. ]
                    }
                    {
                        c'4
                        c'16 [
                        c'16 ~ ]
                    }
                    {
                        c'16 [
                        c'8.
                        c'8 ~ ]
                    }
                    {
                        c'8 [
                        c'16
                        c'8 ]
                        r16
                    }
                }

        Returns patterns or none.
        '''
        superclass = super(TaleaRhythmMaker, self)
        return superclass.logical_tie_masks

    @property
    def read_talea_once_only(self):
        r'''Is true when rhythm-maker should read talea once only.

        ..  container:: example

            **Example 1.** Reads talea cyclically:

            ::

                >>> rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
                ...     talea=rhythmmakertools.Talea(
                ...         counts=[1, 2, 3, 4],
                ...         denominator=16,
                ...         ),
                ...     )

            ::

                >>> divisions = [(3, 8), (3, 8), (3, 8), (3, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 3/8
                        c'16 [
                        c'8
                        c'8. ]
                    }
                    {
                        c'4
                        c'16 [
                        c'16 ~ ]
                    }
                    {
                        c'16 [
                        c'8.
                        c'8 ~ ]
                    }
                    {
                        c'8 [
                        c'16
                        c'8
                        c'16 ]
                    }
                }

        ..  container:: example

            **Example 2.** Reads talea once only:

            ::

                >>> rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
                ...     read_talea_once_only=True,
                ...     talea=rhythmmakertools.Talea(
                ...         counts=[1, 2, 3, 4],
                ...         denominator=16,
                ...         ),
                ...     )

            Calling rhythm_maker on these divisions raises an exception because talea
            is too short to read once only:

            ::

                >>> divisions = [(3, 8), (3, 8), (3, 8), (3, 8)]
                >>> rhythm_maker(divisions)
                Traceback (most recent call last):
                ...
                Exception: talea is too short to read once only:
                CyclicTuple([1, 2, 3, 4]) in [6, 6, 6, 6].

        Set to true to ensure talea is long enough to cover all divisions
        without repeating.

        Provides way of using talea noncyclically when, for example,
        interpolating from short durations to long durations.

        Set to true, false or none.

        Defaults to none.

        Returns true, false or none.
        '''
        return self._read_talea_once_only

    @property
    def rest_tied_notes(self):
        r'''Is true when rhythm-maker should leave the head of each logical
        tie but change tied notes to rests and remove ties.

        ..  container:: example

            **Example 1.** Does not rest tied notes:

            ::

                >>> rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
                ...     talea=rhythmmakertools.Talea(
                ...         counts=[1, 2, 3, 4],
                ...         denominator=16,
                ...         ),
                ...     )

            ::

                >>> divisions = [(3, 8), (3, 8), (3, 8), (3, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 3/8
                        c'16 [
                        c'8
                        c'8. ]
                    }
                    {
                        c'4
                        c'16 [
                        c'16 ~ ]
                    }
                    {
                        c'16 [
                        c'8.
                        c'8 ~ ]
                    }
                    {
                        c'8 [
                        c'16
                        c'8
                        c'16 ]
                    }
                }

        ..  container:: example

            **Example 2.** Rests tied notes:

            ::

                >>> rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
                ...     rest_tied_notes=True,
                ...     talea=rhythmmakertools.Talea(
                ...         counts=[1, 2, 3, 4],
                ...         denominator=16,
                ...         ),
                ...     )

            ::

                >>> divisions = [(3, 8), (3, 8), (3, 8), (3, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 3/8
                        c'16 [
                        c'8
                        c'8. ]
                    }
                    {
                        c'4
                        c'16 [
                        c'16 ]
                    }
                    {
                        r16
                        c'8. [
                        c'8 ]
                    }
                    {
                        r8
                        c'16 [
                        c'8
                        c'16 ]
                    }
                }

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._rest_tied_notes

    @property
    def split_divisions_by_counts(self):
        r'''Gets secondary divisions.

        Secondary divisions impose a cyclic split operation on divisions.

        ..  container:: example

            **Example 1.** Here's a talea equal to two thirty-second notes
            repeating indefinitely. Output equals four divisions of 12
            thirty-second notes each:

            ::

                >>> rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
                ...     talea=rhythmmakertools.Talea(
                ...         counts=[2],
                ...         denominator=32,
                ...         ),
                ...     )

            ::

                >>> divisions = [(3, 8), (3, 8), (3, 8), (3, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 3/8
                        c'16 [
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16 ]
                    }
                    {
                        c'16 [
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16 ]
                    }
                    {
                        c'16 [
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16 ]
                    }
                    {
                        c'16 [
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16 ]
                    }
                }

        ..  container:: example

            **Example 2.** Here's the same talea with secondary divisions set
            to split the divisions every 17 thirty-second notes. The rhythm_maker
            makes six divisions with durations equal, respectively, to 12, 5,
            7, 10, 2 and 12 thirty-second notes.

            Note that ``12 + 5 = 17`` and ``7 + 10 = 17``:

            ::

                >>> rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
                ...     talea=rhythmmakertools.Talea(
                ...         counts=[2],
                ...         denominator=32,
                ...         ),
                ...     split_divisions_by_counts=[17],
                ...     )

            ::

                >>> divisions = [(3, 8), (3, 8), (3, 8), (3, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 3/8
                        c'16 [
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16 ]
                    }
                    {
                        c'16 [
                        c'16
                        c'32 ~ ]
                        c'32 [
                        c'16
                        c'16
                        c'16 ]
                    }
                    {
                        c'16 [
                        c'16
                        c'16
                        c'16
                        c'16 ]
                        c'16
                    }
                    {
                        c'16 [
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16 ]
                    }
                }

            Additional divisions created when using `split_divisions_by_counts`
            are subject to `extra_counts_per_division` just like other
            divisions.

        ..  container:: example

            **Example 3.** This example adds one extra thirty-second note to
            every other division. The durations of the divisions remain the
            same as in the previous example. But now every other division is
            tupletted:

            ::

                >>> rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
                ...     talea=rhythmmakertools.Talea(
                ...         counts=[2],
                ...         denominator=32,
                ...         ),
                ...     split_divisions_by_counts=[17],
                ...     extra_counts_per_division=[0, 1],
                ...     )

            ::

                >>> divisions = [(3, 8), (3, 8), (3, 8), (3, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 3/8
                        {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    }
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/6 {
                            c'16 [
                            c'16
                            c'16 ]
                        }
                        {
                            c'16 [
                            c'16
                            c'16
                            c'32 ~ ]
                        }
                    }
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/11 {
                            c'32 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                        {
                            c'16
                        }
                    }
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 12/13 {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'32 ]
                        }
                    }
                }

        Set to tuple of positive integers or none.

        Returns tuple of positive integers or none.
        '''
        return self._split_divisions_by_counts

    @property
    def talea(self):
        r'''Gets talea.

        ..  container:: example

            **Example 1.** No talea:

            ::

                >>> rhythm_maker = rhythmmakertools.TaleaRhythmMaker()

            ::

                >>> divisions = [(3, 8), (3, 8), (3, 8), (3, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 3/8
                        c'4.
                    }
                    {
                        c'4.
                    }
                    {
                        c'4.
                    }
                    {
                        c'4.
                    }
                }

        ..  container:: example

            **Example 2.** Talea equal to durations ``1/16``, ``2/16``,
            ``3/16``, ``4/16`` repeating indefinitely:

            ::

                >>> rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
                ...     talea=rhythmmakertools.Talea(
                ...         counts=[1, 2, 3, 4],
                ...         denominator=16,
                ...         ),
                ...     )

            ::

                >>> divisions = [(3, 8), (3, 8), (3, 8), (3, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 3/8
                        c'16 [
                        c'8
                        c'8. ]
                    }
                    {
                        c'4
                        c'16 [
                        c'16 ~ ]
                    }
                    {
                        c'16 [
                        c'8.
                        c'8 ~ ]
                    }
                    {
                        c'8 [
                        c'16
                        c'8
                        c'16 ]
                    }
                }

        Set to talea or none.

        Returns talea or none.
        '''
        return self._talea

    @property
    def tie_specifier(self):
        r'''Gets tie specifier.

        ..  container:: example

            **Example 1.** Does not tie across divisions:

            ::

                >>> rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
                ...     talea=rhythmmakertools.Talea(
                ...         counts=[5, 3, 3, 3],
                ...         denominator=16,
                ...         ),
                ...     )

            ::

                >>> divisions = [(4, 8), (3, 8), (4, 8), (3, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 4/8
                        c'4 ~
                        c'16 [
                        c'8. ]
                    }
                    {
                        \time 3/8
                        c'8. [
                        c'8. ]
                    }
                    {
                        \time 4/8
                        c'4 ~
                        c'16 [
                        c'8. ]
                    }
                    {
                        \time 3/8
                        c'8. [
                        c'8. ]
                    }
                }

            This is default behavior.

        ..  container:: example

            **Example 2.** Ties across divisions:

            ::

                >>> rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
                ...     talea=rhythmmakertools.Talea(
                ...         counts=[5, 3, 3, 3],
                ...         denominator=16,
                ...         ),
                ...     tie_specifier=rhythmmakertools.TieSpecifier(
                ...         tie_across_divisions=True,
                ...         ),
                ...     )

            ::

                >>> divisions = [(4, 8), (3, 8), (4, 8), (3, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 4/8
                        c'4 ~
                        c'16 [
                        c'8. ~ ]
                    }
                    {
                        \time 3/8
                        c'8. [
                        c'8. ~ ]
                    }
                    {
                        \time 4/8
                        c'4 ~
                        c'16 [
                        c'8. ~ ]
                    }
                    {
                        \time 3/8
                        c'8. [
                        c'8. ]
                    }
                }

        ..  container:: example

            **Example 3.** Patterns ties across divisions:

            ::

                >>> pattern = patterntools.Pattern(
                ...     indices=[0],
                ...     period=2,
                ...     )
                >>> rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
                ...     talea=rhythmmakertools.Talea(
                ...         counts=[5, 3, 3, 3],
                ...         denominator=16,
                ...         ),
                ...     tie_specifier=rhythmmakertools.TieSpecifier(
                ...         tie_across_divisions=pattern,
                ...         ),
                ...     )

            ::

                >>> divisions = [(4, 8), (3, 8), (4, 8), (3, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 4/8
                        c'4 ~
                        c'16 [
                        c'8. ~ ]
                    }
                    {
                        \time 3/8
                        c'8. [
                        c'8. ]
                    }
                    {
                        \time 4/8
                        c'4 ~
                        c'16 [
                        c'8. ~ ]
                    }
                    {
                        \time 3/8
                        c'8. [
                        c'8. ]
                    }
                }

        ..  container:: example

            **Example 4.** Uses Messiaen-style ties:

            ::

                >>> rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
                ...     talea=rhythmmakertools.Talea(
                ...         counts=[5, 3, 3, 3],
                ...         denominator=16,
                ...         ),
                ...     tie_specifier=rhythmmakertools.TieSpecifier(
                ...         tie_across_divisions=True,
                ...         use_messiaen_style_ties=True,
                ...         ),
                ...     )

            ::

                >>> divisions = [(4, 8), (3, 8), (4, 8), (3, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 4/8
                        c'4
                        c'16 \repeatTie [
                        c'8. ]
                    }
                    {
                        \time 3/8
                        c'8. \repeatTie [
                        c'8. ]
                    }
                    {
                        \time 4/8
                        c'4 \repeatTie
                        c'16 \repeatTie [
                        c'8. ]
                    }
                    {
                        \time 3/8
                        c'8. \repeatTie [
                        c'8. ]
                    }
                }

        ..  container:: example

            **Example 5.** Ties consecutive notes:

            ::

                >>> rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
                ...     talea=rhythmmakertools.Talea(
                ...         counts=[5, -3, 3, 3],
                ...         denominator=16,
                ...         ),
                ...     tie_specifier=rhythmmakertools.TieSpecifier(
                ...         tie_consecutive_notes=True,
                ...         ),
                ...     )

            ::

                >>> divisions = [(4, 8), (3, 8), (4, 8), (3, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 4/8
                        c'4 ~
                        c'16
                        r8.
                    }
                    {
                        \time 3/8
                        c'8. ~ [
                        c'8. ~ ]
                    }
                    {
                        \time 4/8
                        c'4 ~
                        c'16
                        r8.
                    }
                    {
                        \time 3/8
                        c'8. ~ [
                        c'8. ]
                    }
                }

        Set to tie specifier or none.

        Returns tie specifier.
        '''
        superclass = super(TaleaRhythmMaker, self)
        return superclass.tie_specifier

    @property
    def tie_split_notes(self):
        r'''Is true when talea rhythm-maker should tie split notes.
        Otherwise false.

        ..  todo:: Add examples.

        Set to true or false.

        Returns true or false.
        '''
        return self._tie_split_notes

    @property
    def tuplet_spelling_specifier(self):
        r'''Gets tuplet spelling specifier.

        ..  container:: example

            **Example 1.** Redudant tuplets with no tuplet spelling specifier:

            ::

                >>> rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
                ...     extra_counts_per_division=[0, 4],
                ...     talea=rhythmmakertools.Talea(
                ...         counts=[3, 3, 6, 6],
                ...         denominator=16,
                ...         ),
                ...     )

            ::

                >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 3/8
                        {
                            c'8. [
                            c'8. ]
                        }
                    }
                    {
                        \time 4/8
                        \times 2/3 {
                            c'4.
                            c'4.
                        }
                    }
                    {
                        \time 3/8
                        {
                            c'8. [
                            c'8. ]
                        }
                    }
                    {
                        \time 4/8
                        \times 2/3 {
                            c'4.
                            c'4.
                        }
                    }
                }

        ..  container:: example

            **Example 2.** Simplifies redundant tuplets:

            ::

                >>> rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
                ...     extra_counts_per_division=[0, 4],
                ...     talea=rhythmmakertools.Talea(
                ...         counts=[3, 3, 6, 6],
                ...         denominator=16,
                ...         ),
                ...     tuplet_spelling_specifier=rhythmmakertools.TupletSpellingSpecifier(
                ...         simplify_redundant_tuplets=True,
                ...         ),
                ...     )

            ::

                >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 3/8
                        {
                            c'8. [
                            c'8. ]
                        }
                    }
                    {
                        \time 4/8
                        {
                            c'4
                            c'4
                        }
                    }
                    {
                        \time 3/8
                        {
                            c'8. [
                            c'8. ]
                        }
                    }
                    {
                        \time 4/8
                        {
                            c'4
                            c'4
                        }
                    }
                }

        ..  container:: example

            **Example 3.** Rest-filled tuplets with no tuplet spelling
            specifier:

            ::

                >>> rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
                ...     extra_counts_per_division=[1, 0],
                ...     talea=rhythmmakertools.Talea(
                ...         counts=[3, 3, -6, -6],
                ...         denominator=16,
                ...         ),
                ...     )

            ::

                >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 3/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 6/7 {
                            c'8. [
                            c'8. ]
                            r16
                        }
                    }
                    {
                        \time 4/8
                        {
                            r4
                            r16
                            r8.
                        }
                    }
                    {
                        \time 3/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 6/7 {
                            r8.
                            c'8. [
                            c'16 ~ ]
                        }
                    }
                    {
                        \time 4/8
                        {
                            c'8
                            r4.
                        }
                    }
                }

        ..  container:: example

            **Example 4.** Rewrites rest-filled tuplets:

            ::

                >>> rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
                ...     extra_counts_per_division=[1, 0],
                ...     talea=rhythmmakertools.Talea(
                ...         counts=[3, 3, -6, -6],
                ...         denominator=16,
                ...         ),
                ...     tuplet_spelling_specifier=rhythmmakertools.TupletSpellingSpecifier(
                ...         rewrite_rest_filled_tuplets=True,
                ...         ),
                ...     )

            ::

                >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 3/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 6/7 {
                            c'8. [
                            c'8. ]
                            r16
                        }
                    }
                    {
                        \time 4/8
                        {
                            r2
                        }
                    }
                    {
                        \time 3/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 6/7 {
                            r8.
                            c'8. [
                            c'16 ~ ]
                        }
                    }
                    {
                        \time 4/8
                        {
                            c'8
                            r4.
                        }
                    }
                }

        Set to tuplet spelling specifier or none.

        Returns tuplet spelling specifier or none.
        '''
        superclass = super(TaleaRhythmMaker, self)
        return superclass.tuplet_spelling_specifier
