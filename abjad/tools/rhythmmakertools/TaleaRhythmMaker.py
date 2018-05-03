import typing
from abjad.tools.datastructuretools.Duration import Duration
from abjad.tools.datastructuretools.OrderedDict import OrderedDict
from abjad.tools.datastructuretools.Pattern import Pattern
from .BeamSpecifier import BeamSpecifier
from .DurationSpecifier import DurationSpecifier
from .BurnishSpecifier import BurnishSpecifier
from .RhythmMaker import RhythmMaker
from .Talea import Talea
from .TieSpecifier import TieSpecifier
from .TupletSpecifier import TupletSpecifier


class TaleaRhythmMaker(RhythmMaker):
    r'''Talea rhythm-maker.

    ..  container:: example

        Repeats talea of 1/16, 2/16, 3/16, 4/16:

        >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
        ...     talea=abjad.rhythmmakertools.Talea(
        ...         counts=[1, 2, 3, 4],
        ...         denominator=16,
        ...         ),
        ...     )

        >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
        >>> selections = rhythm_maker(divisions)
        >>> lilypond_file = abjad.LilyPondFile.rhythm(
        ...     selections,
        ...     divisions,
        ...     )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff])
            \new RhythmicStaff
            {
                {   % measure
                    \time 3/8
                    c'16
                    [
                    c'8
                    c'8.
                    ]
                }   % measure
                {   % measure
                    \time 4/8
                    c'4
                    c'16
                    [
                    c'8
                    c'16
                    ~
                    ]
                }   % measure
                {   % measure
                    \time 3/8
                    c'8
                    c'4
                }   % measure
                {   % measure
                    \time 4/8
                    c'16
                    [
                    c'8
                    c'8.
                    c'8
                    ]
                }   % measure
            }

    Follows the configure-once / call-repeatedly pattern shown here.

    Object model of a partially evaluated function. Function accepts a list of
    divisions as input. Function returns a list of selections as output. Length
    of input equals length of output.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Rhythm-makers'

    __slots__ = (
        '_burnish_specifier',
        '_extra_counts_per_division',
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
        duration_specifier=None,
        extra_counts_per_division=None,
        logical_tie_masks=None,
        read_talea_once_only=None,
        rest_tied_notes=None,
        split_divisions_by_counts=None,
        tie_specifier=None,
        tie_split_notes=True,
        tuplet_specifier=None,
        ):
        import abjad
        from abjad.tools import rhythmmakertools
        RhythmMaker.__init__(
            self,
            beam_specifier=beam_specifier,
            duration_specifier=duration_specifier,
            division_masks=division_masks,
            logical_tie_masks=logical_tie_masks,
            tie_specifier=tie_specifier,
            tuplet_specifier=tuplet_specifier,
            )
        prototype = (rhythmmakertools.Talea, type(None))
        assert isinstance(talea, prototype)
        assert isinstance(read_talea_once_only, (bool, type(None)))
        self._read_talea_once_only = read_talea_once_only
        self._talea = talea
        if tie_split_notes is not None:
            assert isinstance(tie_split_notes, bool), repr(tie_split_notes)
        self._tie_split_notes = tie_split_notes
        prototype = (rhythmmakertools.BurnishSpecifier, type(None))
        assert isinstance(burnish_specifier, prototype)
        self._burnish_specifier = burnish_specifier
        if split_divisions_by_counts is not None:
            split_divisions_by_counts = tuple(split_divisions_by_counts)
        assert extra_counts_per_division is None or \
            abjad.mathtools.all_are_integer_equivalent_numbers(
                extra_counts_per_division)
        assert split_divisions_by_counts is None or \
            abjad.mathtools.all_are_nonnegative_integer_equivalent_numbers(
                split_divisions_by_counts)
        self._extra_counts_per_division = extra_counts_per_division
        self._split_divisions_by_counts = split_divisions_by_counts
        assert isinstance(rest_tied_notes, (bool, type(None))), rest_tied_notes
        self._rest_tied_notes = rest_tied_notes

    ### SPECIAL METHODS ###

    def __call__(self, divisions, previous_state=None):
        r'''Calls talea rhythm-maker on `divisions`.

        ..  container:: example

                >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
                ...     talea=abjad.rhythmmakertools.Talea(
                ...         counts=[1, 2, 3, 4],
                ...         denominator=16,
                ...         ),
                ...     )

            >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
            >>> selections = rhythm_maker(divisions)

            >>> for selection in selections:
            ...     selection
            Selection([Note("c'16"), Note("c'8"), Note("c'8.")])
            Selection([Note("c'4"), Note("c'16"), Note("c'8"), Note("c'16")])
            Selection([Note("c'8"), Note("c'4")])
            Selection([Note("c'16"), Note("c'8"), Note("c'8."), Note("c'8")])

        Returns list of of selections.
        '''
        return RhythmMaker.__call__(
            self,
            divisions,
            previous_state=previous_state,
            )

    def __format__(self, format_specification=''):
        r'''Formats talea rhythm-maker.

        Set `format_specification` to `''` or `'storage'`.

        ..  container:: example

            Formats talea rhythm-maker:

                >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
                ...     talea=abjad.rhythmmakertools.Talea(
                ...         counts=[1, 2, 3, 4],
                ...         denominator=16,
                ...         ),
                ...     )

            >>> abjad.f(rhythm_maker)
            abjad.rhythmmakertools.TaleaRhythmMaker(
                talea=abjad.rhythmmakertools.Talea(
                    counts=[1, 2, 3, 4],
                    denominator=16,
                    ),
                )

        ..  container:: example

            Storage formats talea rhythm-maker:

                >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
                ...     talea=abjad.rhythmmakertools.Talea(
                ...         counts=[1, 2, 3, 4],
                ...         denominator=16,
                ...         ),
                ...     )

            >>> abjad.f(rhythm_maker)
            abjad.rhythmmakertools.TaleaRhythmMaker(
                talea=abjad.rhythmmakertools.Talea(
                    counts=[1, 2, 3, 4],
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

            >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
            ...     talea=abjad.rhythmmakertools.Talea(
            ...         counts=[1, 2, 3, 4],
            ...         denominator=16,
            ...         ),
            ...     )
            >>> abjad.show(rhythm_maker) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = rhythm_maker.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 3/8
                        c'16
                        [
                        c'8
                        c'8.
                        ]
                    }   % measure
                    {   % measure
                        \time 4/8
                        c'4
                        c'16
                        [
                        c'8
                        c'16
                        ~
                        ]
                    }   % measure
                    {   % measure
                        \time 3/16
                        c'8
                        [
                        c'16
                        ~
                        ]
                    }   % measure
                    {   % measure
                        \time 4/16
                        c'8.
                        [
                        c'16
                        ]
                    }   % measure
                }

        Defaults `divisions` to ``3/8``, ``4/8``, ``3/16``, ``4/16``.

        Returns LilyPond file.
        '''
        return RhythmMaker.__illustrate__(self, divisions=divisions)

    def __repr__(self):
        r'''Gets interpreter representation.

        ..  container:: example

            >>> abjad.rhythmmakertools.TaleaRhythmMaker(
            ...     talea=abjad.rhythmmakertools.Talea(
            ...         counts=[1, 2, 3, 4],
            ...         denominator=16,
            ...         ),
            ...     )
            TaleaRhythmMaker(talea=Talea(counts=[1, 2, 3, 4], denominator=16))

        Returns string.
        '''
        return super(TaleaRhythmMaker, self).__repr__()

    ### PRIVATE METHODS ###

    def _apply_burnish_specifier(self, divisions):
        burnish_specifier = self._get_burnish_specifier()
        return burnish_specifier(divisions)

    def _apply_ties_to_split_notes(
        self,
        result,
        unscaled_preamble,
        unscaled_talea,
        ):
        import abjad
        if not self.tie_split_notes:
            return
        leaves = abjad.select(result).leaves()
        written_durations = [leaf.written_duration for leaf in leaves]
        written_durations = abjad.sequence(written_durations)
        total_duration = written_durations.weight()
        if unscaled_preamble is None:
            preamble_weights = []
        else:
            preamble_weights = []
            for numerator in unscaled_preamble:
                pair = (numerator, self.talea.denominator)
                duration = Duration(*pair)
                weight = abs(duration)
                preamble_weights.append(weight)
        preamble_duration = sum(preamble_weights)
        if total_duration <= preamble_duration:
            preamble_parts = written_durations.partition_by_weights(
                weights=preamble_weights,
                allow_part_weights=abjad.More,
                cyclic=True,
                overhang=True,
                )
            talea_parts = []
        else:
            assert preamble_duration < total_duration
            preamble_parts = written_durations.partition_by_weights(
                weights=preamble_weights,
                allow_part_weights=abjad.Exact,
                cyclic=False,
                overhang=False,
                )
            talea_weights = []
            for numerator in unscaled_talea:
                pair = (numerator, self.talea.denominator)
                weight = abs(Duration(*pair))
                talea_weights.append(weight)
            preamble_length = len(preamble_parts.flatten())
            talea_written_durations = written_durations[preamble_length:]
            talea_parts = talea_written_durations.partition_by_weights(
                weights=talea_weights,
                allow_part_weights=abjad.More,
                cyclic=True,
                overhang=True,
                )
        parts = preamble_parts + talea_parts
        part_durations = parts.flatten()
        assert part_durations == abjad.sequence(written_durations)
        counts = [len(part) for part in parts]
        parts = abjad.sequence(leaves).partition_by_counts(counts)
        prototype = (abjad.Tie,)
        for part in parts:
            if any(isinstance(_, abjad.Rest) for _ in part):
                continue
            part = abjad.select(part)
            tie_spanner = abjad.Tie()
            # voodoo to temporarily neuter the contiguity constraint
            tie_spanner._unconstrain_contiguity()
            for component in part:
                # TODO: make top-level abjad.detach() work here
                for spanner in component._get_spanners(prototype=prototype):
                    spanner._sever_all_leaves()
                #abjad.detach(prototype, component)
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
        agent = systemtools.StorageFormatManager(self)
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
        import abjad
        if not self.rest_tied_notes:
            return selections
        # wrap every selection in a temporary container;
        # this allows the call to abjad.mutate().replace() to work
        containers = []
        for selection in selections:
            container = abjad.Container(selection)
            abjad.attach('temporary container', container)
            containers.append(container)
        for logical_tie in abjad.iterate(selections).logical_ties():
            if not logical_tie.is_trivial:
                for note in logical_tie[1:]:
                    rest = abjad.Rest(note)
                    abjad.mutate(note).replace(rest)
                abjad.detach(abjad.Tie, logical_tie.head)
        # remove every temporary container and recreate selections
        new_selections = []
        for container in containers:
            inspection = abjad.inspect(container)
            assert inspection.get_indicator(str) == 'temporary container'
            new_selection = abjad.mutate(container).eject_contents()
            new_selections.append(new_selection)
        return new_selections

    def _make_leaf_lists(self, numeric_map, talea_denominator):
        leaf_lists = []
        specifier = self._get_duration_specifier()
        for map_division in numeric_map:
            leaf_list = self._make_leaves_from_talea(
                map_division,
                talea_denominator,
                decrease_monotonic=specifier.decrease_monotonic,
                forbidden_duration=specifier.forbidden_duration,
                spell_metrically=specifier.spell_metrically,
                )
            leaf_lists.append(leaf_list)
        return leaf_lists

    @staticmethod
    def _make_leaves_from_talea(
        talea,
        talea_denominator,
        decrease_monotonic=True,
        forbidden_duration=None,
        spell_metrically=None,
        repeat_ties=False,
        ):
        import abjad
        assert all(x != 0 for x in talea), repr(talea)
        result = []
        leaf_maker = abjad.LeafMaker(
            decrease_monotonic=decrease_monotonic,
            forbidden_duration=forbidden_duration,
            repeat_ties=repeat_ties,
            )
        for note_value in talea:
            if 0 < note_value:
                pitches = [0]
            else:
                pitches = [None]
            division = abjad.Duration(
                abs(note_value),
                talea_denominator,
                )
            if (spell_metrically is True or
                (spell_metrically == 'unassignable' and
                not abjad.mathtools.is_assignable_integer(
                    division.numerator))):
                meter = abjad.Meter(division)
                rhythm_tree_container = meter.root_node
                durations = [_.duration for _ in rhythm_tree_container]
            else:
                durations = [division]
            leaves = leaf_maker(pitches, durations)
            if (1 < len(leaves) and
                not leaves[0]._has_spanner(abjad.Tie) and
                not isinstance(leaves[0], abjad.Rest)):
                tie = abjad.Tie(repeat=repeat_ties)
                abjad.attach(tie, leaves[:])
            result.extend(leaves)
        result = abjad.select(result)
        return result

    def _make_music(self, divisions):
        import abjad
        input_divisions = divisions[:]
        input_ = self._prepare_input()
        preamble = input_['preamble']
        talea = input_['talea']
        if talea:
            advanced_talea = Talea(
                counts=talea,
                denominator=self.talea.denominator,
                preamble=preamble,
                )
        else:
            advanced_talea = None
        extra_counts_per_division = input_['extra_counts_per_division']
        unscaled_preamble = tuple(preamble)
        unscaled_talea = tuple(talea)
        split_divisions_by_counts = input_['split_divisions_by_counts']
        counts = {
            'preamble': preamble,
            'talea': talea,
            'extra_counts_per_division': extra_counts_per_division,
            'split_divisions_by_counts': split_divisions_by_counts,
            }
        if self.talea is not None:
            talea_denominator = self.talea.denominator
        else:
            talea_denominator = None
        result = self._scale_counts(divisions, talea_denominator, counts)
        divisions = result['divisions']
        lcd = result['lcd']
        counts = result['counts']
        preamble = counts['preamble']
        secondary_divisions = self._make_secondary_divisions(
            divisions,
            counts['split_divisions_by_counts'],
            )
        if counts['talea']:
            numeric_map = self._make_numeric_map(
                secondary_divisions,
                counts['preamble'],
                counts['talea'],
                counts['extra_counts_per_division'],
                )
            talea_weight_consumed = sum(_.weight() for _ in numeric_map)
            leaf_lists = self._make_leaf_lists(numeric_map, lcd)
            if not counts['extra_counts_per_division']:
                result = leaf_lists
            else:
                tuplets = self._make_tuplets(secondary_divisions, leaf_lists)
                result = tuplets
            selections = [abjad.select(_) for _ in result]
        else:
            talea_weight_consumed = 0
            leaf_maker = abjad.LeafMaker()
            selections = []
            for division in secondary_divisions:
                selection = leaf_maker([0], [division])
                selections.append(selection)
        beam_specifier = self._get_beam_specifier()
        beam_specifier(selections)
        if counts['talea']:
            self._apply_ties_to_split_notes(
                selections,
                unscaled_preamble,
                unscaled_talea,
                )
        selections = self._handle_rest_tied_notes(selections)
        if self.tuplet_specifier:
            diminution = self.tuplet_specifier.diminution
        else:
            diminution = None
        if diminution is not None:
            for tuplet in abjad.iterate(selections).components(abjad.Tuplet):
                if tuplet.multiplier == 1:
                    continue
                if diminution is True and not tuplet.diminution():
                    tuplet.toggle_prolation()
                elif diminution is False and tuplet.diminution():
                    tuplet.toggle_prolation()
        selections = self._apply_division_masks(selections)
        specifier = self._get_duration_specifier()
        if specifier.rewrite_meter:
            selections = specifier._rewrite_meter_(selections, input_divisions)
        string = 'divisions_consumed'
        self.state[string] = self.previous_state.get(string, 0)
        self.state[string] += len(divisions)
        if talea and talea_weight_consumed not in advanced_talea:
            last_leaf = abjad.inspect(selections).get_leaf(-1)
            if isinstance(last_leaf, abjad.Note):
                self.state['incomplete_last_note'] = True
        previous_logical_ties_produced = self._previous_logical_ties_produced()
        logical_ties_produced = len(abjad.select(selections).logical_ties())
        logical_ties_produced += previous_logical_ties_produced
        if self._previous_incomplete_last_note():
            logical_ties_produced -= 1
        self.state['logical_ties_produced'] = logical_ties_produced
        string = 'talea_weight_consumed'
        self.state[string] = self.previous_state.get(string, 0)
        self.state[string] += talea_weight_consumed
        items = self.state.items()
        state = OrderedDict(sorted(items))
        self._state = state
        return selections

    def _make_numeric_map(
        self,
        divisions,
        preamble,
        talea,
        extra_counts_per_division,
        ):
        import abjad
        assert all(isinstance(_, int) for _ in preamble), repr(preamble)
        assert all(isinstance(_, int) for _ in talea), repr(talea)
        prolated_divisions = self._make_prolated_divisions(
            divisions,
            extra_counts_per_division,
            )
        prolated_divisions = [
            abjad.NonreducedFraction(_) for _ in prolated_divisions
            ]
        if not preamble and not talea:
            return prolated_divisions
        prolated_numerators = [_.numerator for _ in prolated_divisions]
        result = self._split_talea_extended_to_weights(
            preamble,
            talea,
            prolated_numerators,
            )
        for list_ in result:
            assert all(isinstance(_, int) for _ in list_), repr(list_)
        if self.burnish_specifier is not None:
            result = self._apply_burnish_specifier(result)
        return result

    def _make_prolated_divisions(self, divisions, extra_counts_per_division):
        prolated_divisions = []
        for i, division in enumerate(divisions):
            if not extra_counts_per_division:
                prolated_divisions.append(division)
                continue
            prolation_addendum = extra_counts_per_division[i]
            try:
                numerator = division.numerator
            except AttributeError:
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

    def _prepare_input(self):
        import abjad
        talea_weight_consumed = self.previous_state.get(
            'talea_weight_consumed',
            0,
            )
        if self.talea is None:
            preamble = ()
            talea = ()
        else:
            talea = self.talea.advance(talea_weight_consumed)
            preamble = talea.preamble or ()
            talea = talea.counts or ()
        talea = abjad.CyclicTuple(talea)
        extra_counts_per_division = self.extra_counts_per_division or ()
        extra_counts_per_division = abjad.sequence(
            extra_counts_per_division
            )
        divisions_consumed = self.previous_state.get('divisions_consumed', 0)
        extra_counts_per_division = extra_counts_per_division.rotate(
            -divisions_consumed
            )
        extra_counts_per_division = abjad.CyclicTuple(
            extra_counts_per_division
            )
        split_divisions_by_counts = self.split_divisions_by_counts or ()
        split_divisions_by_counts = abjad.CyclicTuple(
            split_divisions_by_counts)
        return {
            'extra_counts_per_division': extra_counts_per_division,
            'preamble': preamble,
            'split_divisions_by_counts': split_divisions_by_counts,
            'talea': talea,
            }

    def _split_talea_extended_to_weights(self, preamble, talea, weights):
        import abjad
        assert abjad.mathtools.all_are_positive_integers(weights)
        preamble_weight = abjad.mathtools.weight(preamble)
        talea_weight = abjad.mathtools.weight(talea)
        weight = abjad.mathtools.weight(weights)
        if (self.read_talea_once_only and
            preamble_weight + talea_weight < weight):
            message = f'{preamble!s} + {talea!s} is too short'
            message += f' to read {weights} once.'
            raise Exception(message)
        if weight <= preamble_weight:
            talea = abjad.sequence(preamble)
            talea = talea.truncate(weight=weight)
        else:
            weight -= preamble_weight
            talea = abjad.sequence(talea).repeat_to_weight(weight)
            talea = preamble + talea
        talea = talea.split(weights, cyclic=True)
        return talea

    ### PUBLIC PROPERTIES ###

    @property
    def beam_specifier(self) -> typing.Optional[BeamSpecifier]:
        r'''Gets beam specifier.

        ..  container:: example

            Beams each division:

            >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
            ...     talea=abjad.rhythmmakertools.Talea(
            ...         counts=[1],
            ...         denominator=16,
            ...         ),
            ...     beam_specifier=abjad.rhythmmakertools.BeamSpecifier(
            ...         beam_each_division=True,
            ...         ),
            ...     )

            >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 3/8
                        c'16
                        [
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        ]
                    }   % measure
                    {   % measure
                        \time 4/8
                        c'16
                        [
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        ]
                    }   % measure
                    {   % measure
                        \time 3/8
                        c'16
                        [
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        ]
                    }   % measure
                    {   % measure
                        \time 4/8
                        c'16
                        [
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        ]
                    }   % measure
                }

        ..  container:: example

            Beams divisions together:

            >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
            ...     talea=abjad.rhythmmakertools.Talea(
            ...         counts=[1],
            ...         denominator=16,
            ...         ),
            ...     beam_specifier=abjad.rhythmmakertools.BeamSpecifier(
            ...         beam_divisions_together=True,
            ...         ),
            ...     )

            >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 3/8
                        \set stemLeftBeamCount = 0
                        \set stemRightBeamCount = 2
                        c'16
                        [
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        c'16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        c'16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        c'16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        c'16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 1
                        c'16
                    }   % measure
                    {   % measure
                        \time 4/8
                        \set stemLeftBeamCount = 1
                        \set stemRightBeamCount = 2
                        c'16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        c'16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        c'16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        c'16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        c'16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        c'16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        c'16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 1
                        c'16
                    }   % measure
                    {   % measure
                        \time 3/8
                        \set stemLeftBeamCount = 1
                        \set stemRightBeamCount = 2
                        c'16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        c'16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        c'16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        c'16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        c'16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 1
                        c'16
                    }   % measure
                    {   % measure
                        \time 4/8
                        \set stemLeftBeamCount = 1
                        \set stemRightBeamCount = 2
                        c'16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        c'16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        c'16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        c'16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        c'16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        c'16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        c'16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 0
                        c'16
                        ]
                    }   % measure
                }

        ..  container:: example

            Beams nothing:

            >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
            ...     talea=abjad.rhythmmakertools.Talea(
            ...         counts=[1],
            ...         denominator=16,
            ...         ),
            ...     beam_specifier=abjad.rhythmmakertools.BeamSpecifier(
            ...         beam_each_division=False,
            ...         beam_divisions_together=False,
            ...         ),
            ...     )

            >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 3/8
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                    }   % measure
                    {   % measure
                        \time 4/8
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                    }   % measure
                    {   % measure
                        \time 3/8
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                    }   % measure
                    {   % measure
                        \time 4/8
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                    }   % measure
                }

        ..  container:: example

            Does not beam rests:

            >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
            ...     talea=abjad.rhythmmakertools.Talea(
            ...         counts=[1, 1, 1, -1],
            ...         denominator=16,
            ...         ),
            ...     beam_specifier=abjad.rhythmmakertools.BeamSpecifier(
            ...         beam_each_division=True,
            ...         ),
            ...     )

            >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 3/8
                        c'16
                        [
                        c'16
                        c'16
                        ]
                        r16
                        c'16
                        [
                        c'16
                        ]
                    }   % measure
                    {   % measure
                        \time 4/8
                        c'16
                        r16
                        c'16
                        [
                        c'16
                        c'16
                        ]
                        r16
                        c'16
                        [
                        c'16
                        ]
                    }   % measure
                    {   % measure
                        \time 3/8
                        c'16
                        r16
                        c'16
                        [
                        c'16
                        c'16
                        ]
                        r16
                    }   % measure
                    {   % measure
                        \time 4/8
                        c'16
                        [
                        c'16
                        c'16
                        ]
                        r16
                        c'16
                        [
                        c'16
                        c'16
                        ]
                        r16
                    }   % measure
                }

        ..  container:: example

            Does beam rests:

            >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
            ...     talea=abjad.rhythmmakertools.Talea(
            ...         counts=[1, 1, 1, -1],
            ...         denominator=16,
            ...         ),
            ...     beam_specifier=abjad.rhythmmakertools.BeamSpecifier(
            ...         beam_each_division=True,
            ...         beam_rests=True,
            ...         ),
            ...     )

            >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 3/8
                        c'16
                        [
                        c'16
                        c'16
                        r16
                        c'16
                        c'16
                        ]
                    }   % measure
                    {   % measure
                        \time 4/8
                        c'16
                        [
                        r16
                        c'16
                        c'16
                        c'16
                        r16
                        c'16
                        c'16
                        ]
                    }   % measure
                    {   % measure
                        \time 3/8
                        c'16
                        [
                        r16
                        c'16
                        c'16
                        c'16
                        r16
                        ]
                    }   % measure
                    {   % measure
                        \time 4/8
                        c'16
                        [
                        c'16
                        c'16
                        r16
                        c'16
                        c'16
                        c'16
                        r16
                        ]
                    }   % measure
                }

        ..  container:: example

            Beams rests with stemlets:

            >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
            ...     talea=abjad.rhythmmakertools.Talea(
            ...         counts=[1, 1, 1, -1],
            ...         denominator=16,
            ...         ),
            ...     beam_specifier=abjad.rhythmmakertools.BeamSpecifier(
            ...         beam_each_division=True,
            ...         beam_rests=True,
            ...         stemlet_length=0.75,
            ...         ),
            ...     )

            >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 3/8
                        \override RhythmicStaff.Stem.stemlet-length = 0.75
                        c'16
                        [
                        c'16
                        c'16
                        r16
                        c'16
                        \revert RhythmicStaff.Stem.stemlet-length
                        c'16
                        ]
                    }   % measure
                    {   % measure
                        \time 4/8
                        \override RhythmicStaff.Stem.stemlet-length = 0.75
                        c'16
                        [
                        r16
                        c'16
                        c'16
                        c'16
                        r16
                        c'16
                        \revert RhythmicStaff.Stem.stemlet-length
                        c'16
                        ]
                    }   % measure
                    {   % measure
                        \time 3/8
                        \override RhythmicStaff.Stem.stemlet-length = 0.75
                        c'16
                        [
                        r16
                        c'16
                        c'16
                        c'16
                        \revert RhythmicStaff.Stem.stemlet-length
                        r16
                        ]
                    }   % measure
                    {   % measure
                        \time 4/8
                        \override RhythmicStaff.Stem.stemlet-length = 0.75
                        c'16
                        [
                        c'16
                        c'16
                        r16
                        c'16
                        c'16
                        c'16
                        \revert RhythmicStaff.Stem.stemlet-length
                        r16
                        ]
                    }   % measure
                }

        '''
        return super(TaleaRhythmMaker, self).beam_specifier

    @property
    def burnish_specifier(self) -> typing.Optional[BurnishSpecifier]:
        r'''Gets burnish specifier.

        ..  container:: example

            Forces the first leaf and the last two leaves to be rests:

            >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
            ...     talea=abjad.rhythmmakertools.Talea(
            ...         counts=[1, 2, 3, 4],
            ...         denominator=16,
            ...         ),
            ...     burnish_specifier=abjad.rhythmmakertools.BurnishSpecifier(
            ...         left_classes=[abjad.Rest],
            ...         left_counts=[1],
            ...         right_classes=[abjad.Rest],
            ...         right_counts=[2],
            ...         outer_divisions_only=True,
            ...         ),
            ...     )

            >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 3/8
                        r16
                        c'8
                        [
                        c'8.
                        ]
                    }   % measure
                    {   % measure
                        \time 4/8
                        c'4
                        c'16
                        [
                        c'8
                        c'16
                        ~
                        ]
                    }   % measure
                    {   % measure
                        \time 3/8
                        c'8
                        c'4
                    }   % measure
                    {   % measure
                        \time 4/8
                        c'16
                        [
                        c'8
                        ]
                        r8.
                        r8
                    }   % measure
                }

        ..  container:: example

            Forces the first leaf of every division to be a rest:

            >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
            ...     talea=abjad.rhythmmakertools.Talea(
            ...         counts=[1, 2, 3, 4],
            ...         denominator=16,
            ...         ),
            ...     burnish_specifier=abjad.rhythmmakertools.BurnishSpecifier(
            ...         left_classes=[abjad.Rest],
            ...         left_counts=[1],
            ...         ),
            ...     )

            >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 3/8
                        r16
                        c'8
                        [
                        c'8.
                        ]
                    }   % measure
                    {   % measure
                        \time 4/8
                        r4
                        c'16
                        [
                        c'8
                        c'16
                        ]
                    }   % measure
                    {   % measure
                        \time 3/8
                        r8
                        c'4
                    }   % measure
                    {   % measure
                        \time 4/8
                        r16
                        c'8
                        [
                        c'8.
                        c'8
                        ]
                    }   % measure
                }

        '''
        return self._burnish_specifier

    @property
    def division_masks(self) -> typing.Optional[typing.List[Pattern]]:
        r'''Gets division masks.

        ..  container:: example

            No division masks:

            >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
            ...     talea=abjad.rhythmmakertools.Talea(
            ...         counts=[1, 2, 3, 4],
            ...         denominator=16,
            ...         ),
            ...     )

            >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 3/8
                        c'16
                        [
                        c'8
                        c'8.
                        ]
                    }   % measure
                    {   % measure
                        \time 4/8
                        c'4
                        c'16
                        [
                        c'8
                        c'16
                        ~
                        ]
                    }   % measure
                    {   % measure
                        \time 3/8
                        c'8
                        c'4
                    }   % measure
                    {   % measure
                        \time 4/8
                        c'16
                        [
                        c'8
                        c'8.
                        c'8
                        ]
                    }   % measure
                }

        ..  container:: example

            Silences every other output division:

            >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
            ...     talea=abjad.rhythmmakertools.Talea(
            ...         counts=[1, 2, 3, 4],
            ...         denominator=16,
            ...         ),
            ...     division_masks=[
            ...         abjad.rhythmmakertools.SilenceMask(
            ...             pattern=abjad.index([1], 2),
            ...             ),
            ...         ],
            ...     )

            >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 3/8
                        c'16
                        [
                        c'8
                        c'8.
                        ]
                    }   % measure
                    {   % measure
                        \time 4/8
                        r2
                    }   % measure
                    {   % measure
                        \time 3/8
                        c'8
                        c'4
                    }   % measure
                    {   % measure
                        \time 4/8
                        r2
                    }   % measure
                }

        ..  container:: example

            Sustains every other output division:

            >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
            ...     talea=abjad.rhythmmakertools.Talea(
            ...         counts=[1, 2, 3, 4],
            ...         denominator=16,
            ...         ),
            ...     division_masks=[
            ...         abjad.sustain([1], 2),
            ...         ],
            ...     )

            >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 3/8
                        c'16
                        [
                        c'8
                        c'8.
                        ]
                    }   % measure
                    {   % measure
                        \time 4/8
                        c'2
                    }   % measure
                    {   % measure
                        \time 3/8
                        c'8
                        c'4
                    }   % measure
                    {   % measure
                        \time 4/8
                        c'2
                    }   % measure
                }

        ..  container:: example

            Silences every other secondary output division:

            >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
            ...     talea=abjad.rhythmmakertools.Talea(
            ...         counts=[1],
            ...         denominator=16,
            ...         ),
            ...     split_divisions_by_counts=[9],
            ...     division_masks=[
            ...         abjad.rhythmmakertools.SilenceMask(
            ...             pattern=abjad.index([1], 2),
            ...             ),
            ...         ],
            ...     )

            >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 3/8
                        c'16
                        [
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        ]
                    }   % measure
                    {   % measure
                        \time 4/8
                        r8.
                        c'16
                        [
                        c'16
                        c'16
                        c'16
                        c'16
                        ]
                    }   % measure
                    {   % measure
                        \time 3/8
                        r4
                        c'16
                        [
                        c'16
                        ]
                    }   % measure
                    {   % measure
                        \time 4/8
                        r4..
                        c'16
                    }   % measure
                }

        ..  container:: example

            Sustains every other secondary output division:

            >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
            ...     talea=abjad.rhythmmakertools.Talea(
            ...         counts=[1],
            ...         denominator=16,
            ...         ),
            ...     split_divisions_by_counts=[9],
            ...     division_masks=[
            ...         abjad.sustain([1], 2),
            ...         ],
            ...     )

            >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 3/8
                        c'16
                        [
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        ]
                    }   % measure
                    {   % measure
                        \time 4/8
                        c'8.
                        c'16
                        [
                        c'16
                        c'16
                        c'16
                        c'16
                        ]
                    }   % measure
                    {   % measure
                        \time 3/8
                        c'4
                        c'16
                        [
                        c'16
                        ]
                    }   % measure
                    {   % measure
                        \time 4/8
                        c'4..
                        c'16
                    }   % measure
                }

        ..  container:: example

            REGRESSION. Nonperiodic division masks respect state.

            Only divisions 0 and 2 are masked here:

            >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
            ...     extra_counts_per_division=[0, 1, 2],
            ...     division_masks=[abjad.silence([0, 2, 7])],
            ...     talea=abjad.rhythmmakertools.Talea(
            ...         counts=[4],
            ...         denominator=16,
            ...         ),
            ...     tuplet_specifier=abjad.rhythmmakertools.TupletSpecifier(
            ...         extract_trivial=True,
            ...         ),
            ...     )

            >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 3/8
                        r4.
                    }   % measure
                    {   % measure
                        \time 4/8
                        \times 8/9 {
                            c'8
                            c'4
                            c'8.
                        }
                    }   % measure
                    {   % measure
                        \time 3/8
                        r4.
                    }   % measure
                    {   % measure
                        \time 4/8
                        c'16
                        c'4
                        c'8.
                    }   % measure
                }

            >>> state = rhythm_maker.state
            >>> abjad.f(state)
            abjad.OrderedDict(
                [
                    ('divisions_consumed', 4),
                    ('incomplete_last_note', True),
                    ('logical_ties_produced', 8),
                    ('talea_weight_consumed', 31),
                    ]
                )

            Only division 7 is masked here:

            >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
            >>> selections = rhythm_maker(divisions, previous_state=state)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 3/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 6/7 {
                            c'16
                            c'4
                            c'8
                            ~
                        }
                    }   % measure
                    {   % measure
                        \time 4/8
                        \times 4/5 {
                            c'8
                            c'4
                            c'4
                        }
                    }   % measure
                    {   % measure
                        \time 3/8
                        c'4
                        c'8
                    }   % measure
                    {   % measure
                        \time 4/8
                        r2
                    }   % measure
                }

            >>> state = rhythm_maker.state
            >>> abjad.f(state)
            abjad.OrderedDict(
                [
                    ('divisions_consumed', 8),
                    ('incomplete_last_note', True),
                    ('logical_ties_produced', 15),
                    ('talea_weight_consumed', 63),
                    ]
                )

        ..  container:: example

            REGRESSION. Periodic division masks also respect state.

            >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
            ...     extra_counts_per_division=[0, 1, 2],
            ...     division_masks=[abjad.silence([2], period=3)],
            ...     talea=abjad.rhythmmakertools.Talea(
            ...         counts=[4],
            ...         denominator=16,
            ...         ),
            ...     tuplet_specifier=abjad.rhythmmakertools.TupletSpecifier(
            ...         extract_trivial=True,
            ...         ),
            ...     )

            >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 3/8
                        c'4
                        c'8
                        ~
                    }   % measure
                    {   % measure
                        \time 4/8
                        \times 8/9 {
                            c'8
                            c'4
                            c'8.
                        }
                    }   % measure
                    {   % measure
                        \time 3/8
                        r4.
                    }   % measure
                    {   % measure
                        \time 4/8
                        c'16
                        c'4
                        c'8.
                    }   % measure
                }

            >>> state = rhythm_maker.state
            >>> abjad.f(state)
            abjad.OrderedDict(
                [
                    ('divisions_consumed', 4),
                    ('incomplete_last_note', True),
                    ('logical_ties_produced', 8),
                    ('talea_weight_consumed', 31),
                    ]
                )

            Incomplete first note is masked here:

            >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
            >>> selections = rhythm_maker(divisions, previous_state=state)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 3/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 6/7 {
                            c'16
                            c'4
                            c'8
                        }
                    }   % measure
                    {   % measure
                        \time 4/8
                        r2
                    }   % measure
                    {   % measure
                        \time 3/8
                        c'4
                        c'8
                        ~
                    }   % measure
                    {   % measure
                        \time 4/8
                        \times 8/9 {
                            c'8
                            c'4
                            c'8.
                        }
                    }   % measure
                }

            >>> state = rhythm_maker.state
            >>> abjad.f(state)
            abjad.OrderedDict(
                [
                    ('divisions_consumed', 8),
                    ('incomplete_last_note', True),
                    ('logical_ties_produced', 15),
                    ('talea_weight_consumed', 63),
                    ]
                )

        '''
        return super(TaleaRhythmMaker, self).division_masks

    @property
    def duration_specifier(self) -> typing.Optional[DurationSpecifier]:
        r'''Gets duration specifier.

        Several duration specifier configurations are available.

        ..  container:: example

            Spells nonassignable durations with monontonically decreasing
            durations:

            >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
            ...     talea=abjad.rhythmmakertools.Talea(
            ...         counts=[5],
            ...         denominator=16,
            ...         ),
            ...     duration_specifier=abjad.rhythmmakertools.DurationSpecifier(
            ...         decrease_monotonic=True,
            ...         ),
            ...     )

            >>> divisions = [(5, 8), (5, 8), (5, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 5/8
                        c'4
                        ~
                        c'16
                        c'4
                        ~
                        c'16
                    }   % measure
                    {   % measure
                        c'4
                        ~
                        c'16
                        c'4
                        ~
                        c'16
                    }   % measure
                    {   % measure
                        c'4
                        ~
                        c'16
                        c'4
                        ~
                        c'16
                    }   % measure
                }

        ..  container:: example

            Spells nonassignable durations with monontonically increasing
            durations:

            >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
            ...     talea=abjad.rhythmmakertools.Talea(
            ...         counts=[5],
            ...         denominator=16,
            ...         ),
            ...     duration_specifier=abjad.rhythmmakertools.DurationSpecifier(
            ...         decrease_monotonic=False,
            ...         ),
            ...     )

            >>> divisions = [(5, 8), (5, 8), (5, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 5/8
                        c'16
                        ~
                        c'4
                        c'16
                        ~
                        c'4
                    }   % measure
                    {   % measure
                        c'16
                        ~
                        c'4
                        c'16
                        ~
                        c'4
                    }   % measure
                    {   % measure
                        c'16
                        ~
                        c'4
                        c'16
                        ~
                        c'4
                    }   % measure
                }

        ..  container:: example

            Forbids no durations:

            >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
            ...     talea=abjad.rhythmmakertools.Talea(
            ...         counts=[1, 1, 1, 1, 4, 4],
            ...         denominator=16,
            ...         ),
            ...     duration_specifier=abjad.rhythmmakertools.DurationSpecifier(
            ...         forbidden_duration=None,
            ...         ),
            ...     )

            >>> divisions = [(3, 4), (3, 4)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 3/4
                        c'16
                        [
                        c'16
                        c'16
                        c'16
                        ]
                        c'4
                        c'4
                    }   % measure
                    {   % measure
                        c'16
                        [
                        c'16
                        c'16
                        c'16
                        ]
                        c'4
                        c'4
                    }   % measure
                }

        ..  container:: example

            Forbids durations equal to ``1/4`` or greater:

                >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
                ...     talea=abjad.rhythmmakertools.Talea(
                ...         counts=[1, 1, 1, 1, 4, 4],
                ...         denominator=16,
                ...         ),
                ...     duration_specifier=abjad.rhythmmakertools.DurationSpecifier(
                ...         forbidden_duration=(1, 4),
                ...         ),
                ...     )

            >>> divisions = [(3, 4), (3, 4)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 3/4
                        c'16
                        [
                        c'16
                        c'16
                        c'16
                        c'8
                        ~
                        c'8
                        c'8
                        ~
                        c'8
                        ]
                    }   % measure
                    {   % measure
                        c'16
                        [
                        c'16
                        c'16
                        c'16
                        c'8
                        ~
                        c'8
                        c'8
                        ~
                        c'8
                        ]
                    }   % measure
                }

            Rewrites forbidden durations with smaller durations tied together.

        ..  container:: example

            Spells all durations metrically:

                >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
                ...     talea=abjad.rhythmmakertools.Talea(
                ...         counts=[5, 4],
                ...         denominator=16,
                ...         ),
                ...     duration_specifier=abjad.rhythmmakertools.DurationSpecifier(
                ...         spell_metrically=True,
                ...         ),
                ...     )

            >>> divisions = [(3, 4), (3, 4), (3, 4)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 3/4
                        c'8.
                        ~
                        [
                        c'8
                        ]
                        c'4
                        c'16
                        ~
                        [
                        c'16
                        ~
                        c'16
                        ~
                        ]
                    }   % measure
                    {   % measure
                        c'8
                        c'4
                        c'8.
                        ~
                        [
                        c'8
                        c'16
                        ~
                        ]
                    }   % measure
                    {   % measure
                        c'16
                        ~
                        [
                        c'16
                        ~
                        c'16
                        c'8.
                        ~
                        c'8
                        ]
                        c'4
                    }   % measure
                }

        ..  container:: example

            Spells unassignable durations metrically:

                >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
                ...     talea=abjad.rhythmmakertools.Talea(
                ...         counts=[5, 4],
                ...         denominator=16,
                ...         ),
                ...     duration_specifier=abjad.rhythmmakertools.DurationSpecifier(
                ...         spell_metrically='unassignable',
                ...         ),
                ...     )

            >>> divisions = [(3, 4), (3, 4), (3, 4)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 3/4
                        c'8.
                        ~
                        [
                        c'8
                        ]
                        c'4
                        c'8.
                        ~
                    }   % measure
                    {   % measure
                        c'8
                        c'4
                        c'8.
                        ~
                        [
                        c'8
                        c'16
                        ~
                        ]
                    }   % measure
                    {   % measure
                        c'8.
                        [
                        c'8.
                        ~
                        c'8
                        ]
                        c'4
                    }   % measure
                }

        ..  container:: example

            Rewrites meter:

                >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
                ...     talea=abjad.rhythmmakertools.Talea(
                ...         counts=[5, 4],
                ...         denominator=16,
                ...         ),
                ...     duration_specifier=abjad.rhythmmakertools.DurationSpecifier(
                ...         rewrite_meter=True,
                ...         ),
                ...     )

            >>> divisions = [(3, 4), (3, 4), (3, 4)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 3/4
                        c'4
                        ~
                        c'16
                        [
                        c'8.
                        ~
                        c'16
                        c'8.
                        ~
                        ]
                    }   % measure
                    {   % measure
                        c'8
                        [
                        c'8
                        ~
                        c'8
                        c'8
                        ~
                        c'8.
                        c'16
                        ~
                        ]
                    }   % measure
                    {   % measure
                        c'8.
                        [
                        c'16
                        ~
                        ]
                        c'4
                        c'4
                    }   % measure
                }

        '''
        return super(TaleaRhythmMaker, self).duration_specifier

    @property
    def extra_counts_per_division(self) -> typing.Optional[typing.List[int]]:
        r'''Gets extra counts per division.

        ..  container:: example

            No extra counts per division:

            >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
            ...     talea=abjad.rhythmmakertools.Talea(
            ...         counts=[1, 2, 3, 4],
            ...         denominator=16,
            ...         ),
            ...     )

            >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 3/8
                        c'16
                        [
                        c'8
                        c'8.
                        ]
                    }   % measure
                    {   % measure
                        \time 4/8
                        c'4
                        c'16
                        [
                        c'8
                        c'16
                        ~
                        ]
                    }   % measure
                    {   % measure
                        \time 3/8
                        c'8
                        c'4
                    }   % measure
                    {   % measure
                        \time 4/8
                        c'16
                        [
                        c'8
                        c'8.
                        c'8
                        ]
                    }   % measure
                }

        ..  container:: example

            Adds one extra count to every other division:

            >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
            ...     talea=abjad.rhythmmakertools.Talea(
            ...         counts=[1, 2, 3, 4],
            ...         denominator=16,
            ...         ),
            ...     extra_counts_per_division=[0, 1],
            ...     )

            >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 3/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 1/1 {
                            c'16
                            [
                            c'8
                            c'8.
                            ]
                        }
                    }   % measure
                    {   % measure
                        \time 4/8
                        \times 8/9 {
                            c'4
                            c'16
                            [
                            c'8
                            c'8
                            ~
                            ]
                        }
                    }   % measure
                    {   % measure
                        \time 3/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 1/1 {
                            c'16
                            c'4
                            c'16
                        }
                    }   % measure
                    {   % measure
                        \time 4/8
                        \times 8/9 {
                            c'8
                            [
                            c'8.
                            ]
                            c'4
                        }
                    }   % measure
                }

        ..  container:: example

            Adds two extra counts to every other division:

            >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
            ...     talea=abjad.rhythmmakertools.Talea(
            ...         counts=[1, 2, 3, 4],
            ...         denominator=16,
            ...         ),
            ...     extra_counts_per_division=[0, 2],
            ...     )

            >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 3/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 1/1 {
                            c'16
                            [
                            c'8
                            c'8.
                            ]
                        }
                    }   % measure
                    {   % measure
                        \time 4/8
                        \times 4/5 {
                            c'4
                            c'16
                            [
                            c'8
                            c'8.
                            ]
                        }
                    }   % measure
                    {   % measure
                        \time 3/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 1/1 {
                            c'4
                            c'16
                            [
                            c'16
                            ~
                            ]
                        }
                    }   % measure
                    {   % measure
                        \time 4/8
                        \times 4/5 {
                            c'16
                            [
                            c'8.
                            ]
                            c'4
                            c'16
                            [
                            c'16
                            ]
                        }
                    }   % measure
                }

            The duration of each added count equals the duration
            of each count in the rhythm-maker's input talea.

        ..  container:: example

            Removes one count from every other division:

            >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
            ...     talea=abjad.rhythmmakertools.Talea(
            ...         counts=[1, 2, 3, 4],
            ...         denominator=16,
            ...         ),
            ...     extra_counts_per_division=[0, -1],
            ...     )

            >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 3/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 1/1 {
                            c'16
                            [
                            c'8
                            c'8.
                            ]
                        }
                    }   % measure
                    {   % measure
                        \time 4/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 8/7 {
                            c'4
                            c'16
                            [
                            c'8
                            ]
                        }
                    }   % measure
                    {   % measure
                        \time 3/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 1/1 {
                            c'8.
                            [
                            c'8.
                            ~
                            ]
                        }
                    }   % measure
                    {   % measure
                        \time 4/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 8/7 {
                            c'16
                            [
                            c'16
                            c'8
                            c'8.
                            ]
                        }
                    }   % measure
                }

        '''
        if self._extra_counts_per_division:
            return list(self._extra_counts_per_division)
        else:
            return None

    @property
    def logical_tie_masks(self) -> typing.Optional[typing.List[Pattern]]:
        r'''Gets logical tie masks.

        ..  container:: example

            Silences every third logical tie:

            >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
            ...     logical_tie_masks=[
            ...         abjad.silence([2], 3),
            ...         ],
            ...     talea=abjad.rhythmmakertools.Talea(
            ...         counts=[1, 2, 3, 4],
            ...         denominator=16,
            ...         ),
            ...     )

            >>> divisions = [(3, 8), (3, 8), (3, 8), (3, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 3/8
                        c'16
                        [
                        c'8
                        ]
                        r8.
                    }   % measure
                    {   % measure
                        c'4
                        c'16
                        r16
                    }   % measure
                    {   % measure
                        r16
                        c'8.
                        [
                        c'8
                        ~
                        ]
                    }   % measure
                    {   % measure
                        c'8
                        r16
                        c'8
                        [
                        c'16
                        ]
                    }   % measure
                }

            Silences the first and last logical ties:

            >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
            ...     logical_tie_masks=[
            ...         abjad.silence([0]),
            ...         abjad.silence([-1]),
            ...         ],
            ...     talea=abjad.rhythmmakertools.Talea(
            ...         counts=[1, 2, 3, 4],
            ...         denominator=16,
            ...         ),
            ...     )

            >>> divisions = [(3, 8), (3, 8), (3, 8), (3, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 3/8
                        r16
                        c'8
                        [
                        c'8.
                        ]
                    }   % measure
                    {   % measure
                        c'4
                        c'16
                        [
                        c'16
                        ~
                        ]
                    }   % measure
                    {   % measure
                        c'16
                        [
                        c'8.
                        c'8
                        ~
                        ]
                    }   % measure
                    {   % measure
                        c'8
                        [
                        c'16
                        c'8
                        ]
                        r16
                    }   % measure
                }

        ..  container:: example

            REGRESSION. Nonperiodic logical tie masks respect state.

            Only logical ties 0 and 2 are masked here:

            >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
            ...     extra_counts_per_division=[0, 1, 2],
            ...     logical_tie_masks=[abjad.silence([0, 2, 12])],
            ...     talea=abjad.rhythmmakertools.Talea(
            ...         counts=[4],
            ...         denominator=16,
            ...         ),
            ...     tuplet_specifier=abjad.rhythmmakertools.TupletSpecifier(
            ...         extract_trivial=True,
            ...         ),
            ...     )

            >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 3/8
                        r4
                        c'8
                        ~
                    }   % measure
                    {   % measure
                        \time 4/8
                        \times 8/9 {
                            c'8
                            r4
                            c'8.
                            ~
                        }
                    }   % measure
                    {   % measure
                        \time 3/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/4 {
                            c'16
                            c'4
                            c'8.
                            ~
                        }
                    }   % measure
                    {   % measure
                        \time 4/8
                        c'16
                        c'4
                        c'8.
                    }   % measure
                }

            >>> state = rhythm_maker.state
            >>> abjad.f(state)
            abjad.OrderedDict(
                [
                    ('divisions_consumed', 4),
                    ('incomplete_last_note', True),
                    ('logical_ties_produced', 8),
                    ('talea_weight_consumed', 31),
                    ]
                )

            Only logical tie 12 is masked here:

            >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
            >>> selections = rhythm_maker(divisions, previous_state=state)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 3/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 6/7 {
                            c'16
                            c'4
                            c'8
                            ~
                        }
                    }   % measure
                    {   % measure
                        \time 4/8
                        \times 4/5 {
                            c'8
                            c'4
                            c'4
                        }
                    }   % measure
                    {   % measure
                        \time 3/8
                        r4
                        c'8
                        ~
                    }   % measure
                    {   % measure
                        \time 4/8
                        \times 8/9 {
                            c'8
                            c'4
                            c'8.
                        }
                    }   % measure
                }
            
            >>> state = rhythm_maker.state
            >>> abjad.f(state)
            abjad.OrderedDict(
                [
                    ('divisions_consumed', 8),
                    ('incomplete_last_note', True),
                    ('logical_ties_produced', 16),
                    ('talea_weight_consumed', 63),
                    ]
                )

        ..  container:: example

            REGRESSION. Periodic logical tie masks also respect state.

            >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
            ...     extra_counts_per_division=[0, 1, 2],
            ...     logical_tie_masks=[
            ...         abjad.silence([3], period=4),
            ...     ],
            ...     talea=abjad.rhythmmakertools.Talea(
            ...         counts=[4],
            ...         denominator=16,
            ...         ),
            ...     tuplet_specifier=abjad.rhythmmakertools.TupletSpecifier(
            ...         extract_trivial=True,
            ...         ),
            ...     )

            Incomplete last note is masked here:

            >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 3/8
                        c'4
                        c'8
                        ~
                    }   % measure
                    {   % measure
                        \time 4/8
                        \times 8/9 {
                            c'8
                            c'4
                            r8.
                        }
                    }   % measure
                    {   % measure
                        \time 3/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/4 {
                            r16
                            c'4
                            c'8.
                            ~
                        }
                    }   % measure
                    {   % measure
                        \time 4/8
                        c'16
                        c'4
                        r8.
                    }   % measure
                }

            >>> state = rhythm_maker.state
            >>> abjad.f(state)
            abjad.OrderedDict(
                [
                    ('divisions_consumed', 4),
                    ('incomplete_last_note', True),
                    ('logical_ties_produced', 8),
                    ('talea_weight_consumed', 31),
                    ]
                )

            Incomplete first note is masked here:

            >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
            >>> selections = rhythm_maker(divisions, previous_state=state)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 3/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 6/7 {
                            r16
                            c'4
                            c'8
                            ~
                        }
                    }   % measure
                    {   % measure
                        \time 4/8
                        \times 4/5 {
                            c'8
                            c'4
                            r4
                        }
                    }   % measure
                    {   % measure
                        \time 3/8
                        c'4
                        c'8
                        ~
                    }   % measure
                    {   % measure
                        \time 4/8
                        \times 8/9 {
                            c'8
                            c'4
                            r8.
                        }
                    }   % measure
                }

            >>> state = rhythm_maker.state
            >>> abjad.f(state)
            abjad.OrderedDict(
                [
                    ('divisions_consumed', 8),
                    ('incomplete_last_note', True),
                    ('logical_ties_produced', 16),
                    ('talea_weight_consumed', 63),
                    ]
                )

        '''
        return super(TaleaRhythmMaker, self).logical_tie_masks

    @property
    def read_talea_once_only(self) -> typing.Optional[bool]:
        r'''Is true when rhythm-maker should read talea once only.

        ..  container:: example

            Reads talea cyclically:

            >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
            ...     talea=abjad.rhythmmakertools.Talea(
            ...         counts=[1, 2, 3, 4],
            ...         denominator=16,
            ...         ),
            ...     )

            >>> divisions = [(3, 8), (3, 8), (3, 8), (3, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 3/8
                        c'16
                        [
                        c'8
                        c'8.
                        ]
                    }   % measure
                    {   % measure
                        c'4
                        c'16
                        [
                        c'16
                        ~
                        ]
                    }   % measure
                    {   % measure
                        c'16
                        [
                        c'8.
                        c'8
                        ~
                        ]
                    }   % measure
                    {   % measure
                        c'8
                        [
                        c'16
                        c'8
                        c'16
                        ]
                    }   % measure
                }

        ..  container:: example

            Reads talea once only:

            >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
            ...     read_talea_once_only=True,
            ...     talea=abjad.rhythmmakertools.Talea(
            ...         counts=[1, 2, 3, 4],
            ...         denominator=16,
            ...         ),
            ...     )

            Calling rhythm_maker on these divisions raises an exception because talea
            is too short to read once only:

            >>> divisions = [(3, 8), (3, 8), (3, 8), (3, 8)]
            >>> rhythm_maker(divisions)
            Traceback (most recent call last):
                ...
            Exception: () + (1, 2, 3, 4) is too short to read [6, 6, 6, 6] once.

        Set to true to ensure talea is long enough to cover all divisions
        without repeating.

        Provides way of using talea noncyclically when, for example,
        interpolating from short durations to long durations.
        '''
        return self._read_talea_once_only

    @property
    def rest_tied_notes(self) -> typing.Optional[bool]:
        r'''Is true when rhythm-maker should leave the head of each logical
        tie but change tied notes to rests and remove ties.

        ..  container:: example

            Does not rest tied notes:

            >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
            ...     talea=abjad.rhythmmakertools.Talea(
            ...         counts=[1, 2, 3, 4],
            ...         denominator=16,
            ...         ),
            ...     )

            >>> divisions = [(3, 8), (3, 8), (3, 8), (3, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 3/8
                        c'16
                        [
                        c'8
                        c'8.
                        ]
                    }   % measure
                    {   % measure
                        c'4
                        c'16
                        [
                        c'16
                        ~
                        ]
                    }   % measure
                    {   % measure
                        c'16
                        [
                        c'8.
                        c'8
                        ~
                        ]
                    }   % measure
                    {   % measure
                        c'8
                        [
                        c'16
                        c'8
                        c'16
                        ]
                    }   % measure
                }

        ..  container:: example

            Rests tied notes:

            >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
            ...     rest_tied_notes=True,
            ...     talea=abjad.rhythmmakertools.Talea(
            ...         counts=[1, 2, 3, 4],
            ...         denominator=16,
            ...         ),
            ...     )

            >>> divisions = [(3, 8), (3, 8), (3, 8), (3, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 3/8
                        c'16
                        [
                        c'8
                        c'8.
                        ]
                    }   % measure
                    {   % measure
                        c'4
                        c'16
                        [
                        c'16
                        ]
                    }   % measure
                    {   % measure
                        r16
                        c'8.
                        [
                        c'8
                        ]
                    }   % measure
                    {   % measure
                        r8
                        c'16
                        [
                        c'8
                        c'16
                        ]
                    }   % measure
                }

        '''
        return self._rest_tied_notes

    @property
    def split_divisions_by_counts(self) -> typing.Optional[int]:
        r'''Gets secondary divisions.

        Secondary divisions impose a cyclic split operation on divisions.

        ..  container:: example

            Here's a talea equal to two thirty-second notes repeating
            indefinitely. Output equals four divisions of 12 thirty-second
            notes each:

            >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
            ...     talea=abjad.rhythmmakertools.Talea(
            ...         counts=[2],
            ...         denominator=32,
            ...         ),
            ...     )

            >>> divisions = [(3, 8), (3, 8), (3, 8), (3, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 3/8
                        c'16
                        [
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        ]
                    }   % measure
                    {   % measure
                        c'16
                        [
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        ]
                    }   % measure
                    {   % measure
                        c'16
                        [
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        ]
                    }   % measure
                    {   % measure
                        c'16
                        [
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        ]
                    }   % measure
                }

        ..  container:: example

            Here's the same talea with secondary divisions set to split the
            divisions every 17 thirty-second notes. The rhythm_maker makes six
            divisions with durations equal, respectively, to 12, 5, 7, 10, 2
            and 12 thirty-second notes.

            Note that ``12 + 5 = 17`` and ``7 + 10 = 17``:

            >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
            ...     talea=abjad.rhythmmakertools.Talea(
            ...         counts=[2],
            ...         denominator=32,
            ...         ),
            ...     split_divisions_by_counts=[17],
            ...     )

            >>> divisions = [(3, 8), (3, 8), (3, 8), (3, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 3/8
                        c'16
                        [
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        ]
                    }   % measure
                    {   % measure
                        c'16
                        [
                        c'16
                        c'32
                        ~
                        ]
                        c'32
                        [
                        c'16
                        c'16
                        c'16
                        ]
                    }   % measure
                    {   % measure
                        c'16
                        [
                        c'16
                        c'16
                        c'16
                        c'16
                        ]
                        c'16
                    }   % measure
                    {   % measure
                        c'16
                        [
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        ]
                    }   % measure
                }

            Additional divisions created when using `split_divisions_by_counts`
            are subject to `extra_counts_per_division` just like other
            divisions.

        ..  container:: example

            This example adds one extra thirty-second note to every other
            division. The durations of the divisions remain the same as in the
            previous example. But now every other division is tupletted:

            >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
            ...     talea=abjad.rhythmmakertools.Talea(
            ...         counts=[2],
            ...         denominator=32,
            ...         ),
            ...     split_divisions_by_counts=[17],
            ...     extra_counts_per_division=[0, 1],
            ...     )

            >>> divisions = [(3, 8), (3, 8), (3, 8), (3, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 3/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 1/1 {
                            c'16
                            [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            ]
                        }
                    }   % measure
                    {   % measure
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/6 {
                            c'16
                            [
                            c'16
                            c'16
                            ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 1/1 {
                            c'16
                            [
                            c'16
                            c'16
                            c'32
                            ~
                            ]
                        }
                    }   % measure
                    {   % measure
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/11 {
                            c'32
                            [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 1/1 {
                            c'16
                        }
                    }   % measure
                    {   % measure
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 12/13 {
                            c'16
                            [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'32
                            ]
                        }
                    }   % measure
                }

        '''
        return self._split_divisions_by_counts

    @property
    def state(self) -> OrderedDict:
        r'''Gets state dictionary.

        ..  container:: example

            Consumes 4 divisions and 31 counts:

            >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
            ...     extra_counts_per_division=[0, 1, 2],
            ...     talea=abjad.rhythmmakertools.Talea(
            ...         counts=[4],
            ...         denominator=16,
            ...         ),
            ...     tuplet_specifier=abjad.rhythmmakertools.TupletSpecifier(
            ...         extract_trivial=True,
            ...         ),
            ...     )

            >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 3/8
                        c'4
                        c'8
                        ~
                    }   % measure
                    {   % measure
                        \time 4/8
                        \times 8/9 {
                            c'8
                            c'4
                            c'8.
                            ~
                        }
                    }   % measure
                    {   % measure
                        \time 3/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/4 {
                            c'16
                            c'4
                            c'8.
                            ~
                        }
                    }   % measure
                    {   % measure
                        \time 4/8
                        c'16
                        c'4
                        c'8.
                    }   % measure
                }

            >>> state = rhythm_maker.state
            >>> abjad.f(state)
            abjad.OrderedDict(
                [
                    ('divisions_consumed', 4),
                    ('incomplete_last_note', True),
                    ('logical_ties_produced', 8),
                    ('talea_weight_consumed', 31),
                    ]
                )

            Advances 4 divisions and 31 counts; then consumes another 4
            divisions and 31 counts:

            >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
            >>> selections = rhythm_maker(divisions, previous_state=state)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 3/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 6/7 {
                            c'16
                            c'4
                            c'8
                            ~
                        }
                    }   % measure
                    {   % measure
                        \time 4/8
                        \times 4/5 {
                            c'8
                            c'4
                            c'4
                        }
                    }   % measure
                    {   % measure
                        \time 3/8
                        c'4
                        c'8
                        ~
                    }   % measure
                    {   % measure
                        \time 4/8
                        \times 8/9 {
                            c'8
                            c'4
                            c'8.
                        }
                    }   % measure
                }

            >>> state = rhythm_maker.state
            >>> abjad.f(state)
            abjad.OrderedDict(
                [
                    ('divisions_consumed', 8),
                    ('incomplete_last_note', True),
                    ('logical_ties_produced', 16),
                    ('talea_weight_consumed', 63),
                    ]
                )

            Advances 8 divisions and 62 counts; then consumes 4 divisions and
            31 counts:

            >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
            >>> selections = rhythm_maker(divisions, previous_state=state)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 3/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/4 {
                            c'16
                            c'4
                            c'8.
                            ~
                        }
                    }   % measure
                    {   % measure
                        \time 4/8
                        c'16
                        c'4
                        c'8.
                        ~
                    }   % measure
                    {   % measure
                        \time 3/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 6/7 {
                            c'16
                            c'4
                            c'8
                            ~
                        }
                    }   % measure
                    {   % measure
                        \time 4/8
                        \times 4/5 {
                            c'8
                            c'4
                            c'4
                        }
                    }   % measure
                }

            >>> state = rhythm_maker.state
            >>> abjad.f(state)
            abjad.OrderedDict(
                [
                    ('divisions_consumed', 12),
                    ('incomplete_last_note', True),
                    ('logical_ties_produced', 24),
                    ('talea_weight_consumed', 96),
                    ]
                )


        '''
        return super(TaleaRhythmMaker, self).state

    @property
    def talea(self) -> Talea:
        r'''Gets talea.

        ..  container:: example

            No talea:

            >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker()

            >>> divisions = [(3, 8), (3, 8), (3, 8), (3, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 3/8
                        c'4.
                    }   % measure
                    {   % measure
                        c'4.
                    }   % measure
                    {   % measure
                        c'4.
                    }   % measure
                    {   % measure
                        c'4.
                    }   % measure
                }

        ..  container:: example

            Working with ``preamble``.

            Preamble less than total duration:

            >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
            ...     talea=abjad.rhythmmakertools.Talea(
            ...         counts=[8, -4, 8],
            ...         denominator=32,
            ...         preamble=[1, 1, 1, 1],
            ...         ),
            ...     )

            >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 3/8
                        c'32
                        [
                        c'32
                        c'32
                        c'32
                        ]
                        c'4
                    }   % measure
                    {   % measure
                        \time 4/8
                        r8
                        c'4
                        c'8
                        ~
                    }   % measure
                    {   % measure
                        \time 3/8
                        c'8
                        r8
                        c'8
                        ~
                    }   % measure
                    {   % measure
                        \time 4/8
                        c'8
                        c'4
                        r8
                    }   % measure
                }

            Preamble more than total duration; ignores counts:

            >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
            ...     talea=abjad.rhythmmakertools.Talea(
            ...         counts=[8, -4, 8],
            ...         denominator=32,
            ...         preamble=[32, 32, 32, 32],
            ...         ),
            ...     )

            >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 3/8
                        c'4.
                        ~
                    }   % measure
                    {   % measure
                        \time 4/8
                        c'2
                        ~
                    }   % measure
                    {   % measure
                        \time 3/8
                        c'8
                        c'4
                        ~
                    }   % measure
                    {   % measure
                        \time 4/8
                        c'2
                    }   % measure
                }

        '''
        return self._talea

    @property
    def tie_specifier(self) -> typing.Optional[TieSpecifier]:
        r'''Gets tie specifier.

        ..  container:: example

            Does not tie across divisions:

            >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
            ...     talea=abjad.rhythmmakertools.Talea(
            ...         counts=[5, 3, 3, 3],
            ...         denominator=16,
            ...         ),
            ...     )

            >>> divisions = [(4, 8), (3, 8), (4, 8), (3, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 4/8
                        c'4
                        ~
                        c'16
                        [
                        c'8.
                        ]
                    }   % measure
                    {   % measure
                        \time 3/8
                        c'8.
                        [
                        c'8.
                        ]
                    }   % measure
                    {   % measure
                        \time 4/8
                        c'4
                        ~
                        c'16
                        [
                        c'8.
                        ]
                    }   % measure
                    {   % measure
                        \time 3/8
                        c'8.
                        [
                        c'8.
                        ]
                    }   % measure
                }

        ..  container:: example

            Ties across divisions:

            >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
            ...     talea=abjad.rhythmmakertools.Talea(
            ...         counts=[5, 3, 3, 3],
            ...         denominator=16,
            ...         ),
            ...     tie_specifier=abjad.rhythmmakertools.TieSpecifier(
            ...         tie_across_divisions=True,
            ...         ),
            ...     )

            >>> divisions = [(4, 8), (3, 8), (4, 8), (3, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 4/8
                        c'4
                        ~
                        c'16
                        [
                        c'8.
                        ~
                        ]
                    }   % measure
                    {   % measure
                        \time 3/8
                        c'8.
                        [
                        c'8.
                        ~
                        ]
                    }   % measure
                    {   % measure
                        \time 4/8
                        c'4
                        ~
                        c'16
                        [
                        c'8.
                        ~
                        ]
                    }   % measure
                    {   % measure
                        \time 3/8
                        c'8.
                        [
                        c'8.
                        ]
                    }   % measure
                }

        ..  container:: example

            Patterns ties across divisions:

            >>> pattern = abjad.Pattern(
            ...     indices=[0],
            ...     period=2,
            ...     )
            >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
            ...     talea=abjad.rhythmmakertools.Talea(
            ...         counts=[5, 3, 3, 3],
            ...         denominator=16,
            ...         ),
            ...     tie_specifier=abjad.rhythmmakertools.TieSpecifier(
            ...         tie_across_divisions=pattern,
            ...         ),
            ...     )

            >>> divisions = [(4, 8), (3, 8), (4, 8), (3, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 4/8
                        c'4
                        ~
                        c'16
                        [
                        c'8.
                        ~
                        ]
                    }   % measure
                    {   % measure
                        \time 3/8
                        c'8.
                        [
                        c'8.
                        ]
                    }   % measure
                    {   % measure
                        \time 4/8
                        c'4
                        ~
                        c'16
                        [
                        c'8.
                        ~
                        ]
                    }   % measure
                    {   % measure
                        \time 3/8
                        c'8.
                        [
                        c'8.
                        ]
                    }   % measure
                }

        ..  container:: example

            Uses repeat ties:

            >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
            ...     talea=abjad.rhythmmakertools.Talea(
            ...         counts=[5, 3, 3, 3],
            ...         denominator=16,
            ...         ),
            ...     tie_specifier=abjad.rhythmmakertools.TieSpecifier(
            ...         tie_across_divisions=True,
            ...         repeat_ties=True,
            ...         ),
            ...     )

            >>> divisions = [(4, 8), (3, 8), (4, 8), (3, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 4/8
                        c'4
                        c'16
                        \repeatTie
                        [
                        c'8.
                        ]
                    }   % measure
                    {   % measure
                        \time 3/8
                        c'8.
                        \repeatTie
                        [
                        c'8.
                        ]
                    }   % measure
                    {   % measure
                        \time 4/8
                        c'4
                        \repeatTie
                        c'16
                        \repeatTie
                        [
                        c'8.
                        ]
                    }   % measure
                    {   % measure
                        \time 3/8
                        c'8.
                        \repeatTie
                        [
                        c'8.
                        ]
                    }   % measure
                }

        ..  container:: example

            Ties consecutive notes:

            >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
            ...     talea=abjad.rhythmmakertools.Talea(
            ...         counts=[5, -3, 3, 3],
            ...         denominator=16,
            ...         ),
            ...     tie_specifier=abjad.rhythmmakertools.TieSpecifier(
            ...         tie_consecutive_notes=True,
            ...         ),
            ...     )

            >>> divisions = [(4, 8), (3, 8), (4, 8), (3, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 4/8
                        c'4
                        ~
                        c'16
                        r8.
                    }   % measure
                    {   % measure
                        \time 3/8
                        c'8.
                        ~
                        [
                        c'8.
                        ~
                        ]
                    }   % measure
                    {   % measure
                        \time 4/8
                        c'4
                        ~
                        c'16
                        r8.
                    }   % measure
                    {   % measure
                        \time 3/8
                        c'8.
                        ~
                        [
                        c'8.
                        ]
                    }   % measure
                }

        '''
        return super(TaleaRhythmMaker, self).tie_specifier

    @property
    def tie_split_notes(self) -> typing.Optional[bool]:
        r'''Is true when talea rhythm-maker should tie split notes.
        Otherwise false.

        ..  todo:: Add examples.

        '''
        return self._tie_split_notes

    @property
    def tuplet_specifier(self) -> typing.Optional[TupletSpecifier]:
        r'''Gets tuplet specifier.

        ..  container:: example

            Working with ``diminution``.
            
            Makes diminished tuplets when ``diminution`` is true (or when no
            tuplet specifier is given):

            >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
            ...     extra_counts_per_division=[0, -1],
            ...     talea=abjad.rhythmmakertools.Talea(
            ...         counts=[1],
            ...         denominator=16,
            ...         ),
            ...     tuplet_specifier=abjad.rhythmmakertools.TupletSpecifier(
            ...         extract_trivial=True,
            ...         ),
            ...     )

            >>> divisions = [(1, 4), (1, 4), (1, 4), (1, 4), (1, 4), (1, 4)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 1/4
                        c'16
                        [
                        c'16
                        c'16
                        c'16
                        ]
                    }   % measure
                    {   % measure
                        \times 2/3 {
                            c'8
                            [
                            c'8
                            c'8
                            ]
                        }
                    }   % measure
                    {   % measure
                        c'16
                        [
                        c'16
                        c'16
                        c'16
                        ]
                    }   % measure
                    {   % measure
                        \times 2/3 {
                            c'8
                            [
                            c'8
                            c'8
                            ]
                        }
                    }   % measure
                    {   % measure
                        c'16
                        [
                        c'16
                        c'16
                        c'16
                        ]
                    }   % measure
                    {   % measure
                        \times 2/3 {
                            c'8
                            [
                            c'8
                            c'8
                            ]
                        }
                    }   % measure
                }

            Makes augmented tuplets when ``diminution`` is set to false:

            >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
            ...     extra_counts_per_division=[0, -1],
            ...     talea=abjad.rhythmmakertools.Talea(
            ...         counts=[1],
            ...         denominator=16,
            ...         ),
            ...     tuplet_specifier=abjad.rhythmmakertools.TupletSpecifier(
            ...         diminution=False,
            ...         extract_trivial=True,
            ...         ),
            ...     )

            >>> divisions = [(1, 4), (1, 4), (1, 4), (1, 4), (1, 4), (1, 4)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 1/4
                        c'16
                        [
                        c'16
                        c'16
                        c'16
                        ]
                    }   % measure
                    {   % measure
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 4/3 {
                            c'16
                            [
                            c'16
                            c'16
                            ]
                        }
                    }   % measure
                    {   % measure
                        c'16
                        [
                        c'16
                        c'16
                        c'16
                        ]
                    }   % measure
                    {   % measure
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 4/3 {
                            c'16
                            [
                            c'16
                            c'16
                            ]
                        }
                    }   % measure
                    {   % measure
                        c'16
                        [
                        c'16
                        c'16
                        c'16
                        ]
                    }   % measure
                    {   % measure
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 4/3 {
                            c'16
                            [
                            c'16
                            c'16
                            ]
                        }
                    }   % measure
                }

        ..  container:: example

            Working with ``trivialize``.

            Leaves trivializable tuplets as-is when no tuplet specifier is
            given. The tuplets in measures 2 and 4 can be written as trivial
            tuplets, but they are not:

            >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
            ...     extra_counts_per_division=[0, 4],
            ...     talea=abjad.rhythmmakertools.Talea(
            ...         counts=[3, 3, 6, 6],
            ...         denominator=16,
            ...         ),
            ...     )

            >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 3/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 1/1 {
                            c'8.
                            [
                            c'8.
                            ]
                        }
                    }   % measure
                    {   % measure
                        \time 4/8
                        \times 2/3 {
                            c'4.
                            c'4.
                        }
                    }   % measure
                    {   % measure
                        \time 3/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 1/1 {
                            c'8.
                            [
                            c'8.
                            ]
                        }
                    }   % measure
                    {   % measure
                        \time 4/8
                        \times 2/3 {
                            c'4.
                            c'4.
                        }
                    }   % measure
                }

            Rewrites trivializable tuplets as trivial (1:1) tuplets when
            ``trivialize`` is true:

            >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
            ...     extra_counts_per_division=[0, 4],
            ...     talea=abjad.rhythmmakertools.Talea(
            ...         counts=[3, 3, 6, 6],
            ...         denominator=16,
            ...         ),
            ...     tuplet_specifier=abjad.rhythmmakertools.TupletSpecifier(
            ...         trivialize=True,
            ...         ),
            ...     )

            >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 3/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 1/1 {
                            c'8.
                            [
                            c'8.
                            ]
                        }
                    }   % measure
                    {   % measure
                        \time 4/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 1/1 {
                            c'4
                            c'4
                        }
                    }   % measure
                    {   % measure
                        \time 3/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 1/1 {
                            c'8.
                            [
                            c'8.
                            ]
                        }
                    }   % measure
                    {   % measure
                        \time 4/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 1/1 {
                            c'4
                            c'4
                        }
                    }   % measure
                }

            REGRESSION #907a. Rewrites trivializable tuplets even when
            tuplets contain multiple ties:

            >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
            ...     extra_counts_per_division=[0, 4],
            ...     talea=abjad.rhythmmakertools.Talea(
            ...         counts=[3, 3, 6, 6],
            ...         denominator=16,
            ...         ),
            ...     tie_specifier=abjad.rhythmmakertools.TieSpecifier(
            ...         tie_across_divisions=True,
            ...         ),
            ...     tuplet_specifier=abjad.rhythmmakertools.TupletSpecifier(
            ...         trivialize=True,
            ...         ),
            ...     )

            >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 3/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 1/1 {
                            c'8.
                            [
                            c'8.
                            ~
                            ]
                        }
                    }   % measure
                    {   % measure
                        \time 4/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 1/1 {
                            c'4
                            c'4
                            ~
                        }
                    }   % measure
                    {   % measure
                        \time 3/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 1/1 {
                            c'8.
                            [
                            c'8.
                            ~
                            ]
                        }
                    }   % measure
                    {   % measure
                        \time 4/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 1/1 {
                            c'4
                            c'4
                        }
                    }   % measure
                }

            REGRESSION #907b. Rewrites trivializable tuplets even when
            tuplets contain very long ties:

            >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
            ...     extra_counts_per_division=[0, 4],
            ...     talea=abjad.rhythmmakertools.Talea(
            ...         counts=[3, 3, 6, 6],
            ...         denominator=16,
            ...         ),
            ...     tie_specifier=abjad.rhythmmakertools.TieSpecifier(
            ...         tie_across_divisions=True,
            ...         tie_consecutive_notes=True,
            ...         ),
            ...     tuplet_specifier=abjad.rhythmmakertools.TupletSpecifier(
            ...         trivialize=True,
            ...         ),
            ...     )

            >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 3/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 1/1 {
                            c'8.
                            ~
                            [
                            c'8.
                            ~
                            ]
                        }
                    }   % measure
                    {   % measure
                        \time 4/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 1/1 {
                            c'4
                            ~
                            c'4
                            ~
                        }
                    }   % measure
                    {   % measure
                        \time 3/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 1/1 {
                            c'8.
                            ~
                            [
                            c'8.
                            ~
                            ]
                        }
                    }   % measure
                    {   % measure
                        \time 4/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 1/1 {
                            c'4
                            ~
                            c'4
                        }
                    }   % measure
                }

        ..  container:: example

            Working with ``rewrite_rest_filled``.

            Makes rest-filled tuplets when ``rewrite_rest_filled`` is false (or
            when no tuplet specifier is given):

            >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
            ...     extra_counts_per_division=[1, 0],
            ...     talea=abjad.rhythmmakertools.Talea(
            ...         counts=[3, 3, -6, -6],
            ...         denominator=16,
            ...         ),
            ...     )

            >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 3/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 6/7 {
                            c'8.
                            [
                            c'8.
                            ]
                            r16
                        }
                    }   % measure
                    {   % measure
                        \time 4/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 1/1 {
                            r4
                            r16
                            r8.
                        }
                    }   % measure
                    {   % measure
                        \time 3/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 6/7 {
                            r8.
                            c'8.
                            [
                            c'16
                            ~
                            ]
                        }
                    }   % measure
                    {   % measure
                        \time 4/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 1/1 {
                            c'8
                            r4.
                        }
                    }   % measure
                }

            Rewrites rest-filled tuplets when ``rewrite_rest_filled`` is true:

            >>> rhythm_maker = abjad.rhythmmakertools.TaleaRhythmMaker(
            ...     extra_counts_per_division=[1, 0],
            ...     talea=abjad.rhythmmakertools.Talea(
            ...         counts=[3, 3, -6, -6],
            ...         denominator=16,
            ...         ),
            ...     tuplet_specifier=abjad.rhythmmakertools.TupletSpecifier(
            ...         rewrite_rest_filled=True,
            ...         ),
            ...     )

            >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 3/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 6/7 {
                            c'8.
                            [
                            c'8.
                            ]
                            r16
                        }
                    }   % measure
                    {   % measure
                        \time 4/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 1/1 {
                            r2
                        }
                    }   % measure
                    {   % measure
                        \time 3/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 6/7 {
                            r8.
                            c'8.
                            [
                            c'16
                            ~
                            ]
                        }
                    }   % measure
                    {   % measure
                        \time 4/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 1/1 {
                            c'8
                            r4.
                        }
                    }   % measure
                }

        '''
        return super(TaleaRhythmMaker, self).tuplet_specifier
