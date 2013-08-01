# -*- encoding: utf-8 -*-
import itertools
from abjad.tools import durationtools
from abjad.tools import sequencetools
from abjad.tools.selectiontools.SequentialLeafSelection \
    import SequentialLeafSelection


class TieChain(SequentialLeafSelection):
    r'''All the notes in a tie chain:

    ::

        >>> staff = Staff("c' d' e' ~ e'")

    ::

        >>> staff[2].select_tie_chain()
        TieChain(Note("e'4"), Note("e'4"))

    Tie chains are immutable score selections.
    '''

    ### PRIVATE METHODS ###

    def _add_or_remove_notes_to_achieve_written_duration(
        self, new_written_duration):
        from abjad.tools import componenttools
        from abjad.tools import notetools
        from abjad.tools import spannertools
        from abjad.tools import tuplettools
        new_written_duration = durationtools.Duration(new_written_duration)
        if new_written_duration.is_assignable:
            self[0].written_duration = new_written_duration
            for leaf in self[1:]:
                componenttools.remove_component_subtree_from_score_and_spanners(
                    [leaf])
            first = self[0]
            spannertools.detach_spanners_attached_to_component(
                first, spannertools.TieSpanner)
        elif new_written_duration.has_power_of_two_denominator:
            durations = notetools.make_notes(0, [new_written_duration])
            for leaf, token in zip(self, durations):
                leaf.written_duration = token.written_duration
            if len(self) == len(durations):
                pass
            elif len(durations) < len(self):
                for leaf in self[len(durations):]:
                    componenttools.remove_component_subtree_from_score_and_spanners(
                        [leaf])
            elif len(self) < len(durations):
                spannertools.detach_spanners_attached_to_component(
                    self[0], spannertools.TieSpanner)
                difference = len(durations) - len(self)
                extra_leaves = self[0] * difference
                for extra_leaf in extra_leaves:
                    for spanner in extra_leaf.spanners:
                        spanner._remove(extra_leaf)
                extra_tokens = durations[len(self):]
                for leaf, token in zip(extra_leaves, extra_tokens):
                    leaf.written_duration = token.written_duration
                if not spannertools.is_component_with_spanner_attached(
                    self[-1], spannertools.TieSpanner):
                    spannertools.TieSpanner(list(self))
                self[-1].extend_in_parent(extra_leaves, grow_spanners=True)
        else:
            durations = notetools.make_notes(0, new_written_duration)
            assert isinstance(durations[0], tuplettools.Tuplet)
            fmtuplet = durations[0]
            new_chain_written = \
                fmtuplet[0].select_tie_chain()._preprolated_duration
            self._add_or_remove_notes_to_achieve_written_duration(
                new_chain_written)
            multiplier = fmtuplet.multiplier
            tuplettools.Tuplet(multiplier, self.leaves)
        return self[0].select_tie_chain()

    ### PUBLIC PROPERTIES ###

    @property
    def all_leaves_are_in_same_parent(self):
        r'''True when all leaves in tie chain are in same parent.

        Return boolean.
        '''
        return sequencetools.all_are_equal(
            [leaf._parent for leaf in self.leaves])

    @property
    def duration(self):
        r'''Sum of durations of all components in tie chain.

        Return duration.
        '''
        return sum([x.duration for x in self])

    @property
    def head(self):
        r'''Reference to element ``0`` in tie chain.

        Return component.
        '''
        if self.music:
            return self.music[0]

    @property
    def is_pitched(self):
        r'''True when tie chain head is a note or chord.

        Return boolean.
        '''
        from abjad.tools import chordtools
        from abjad.tools import notetools
        return isinstance(self.head, (notetools.Note, chordtools.Chord))

    @property
    def is_trivial(self):
        r'''True when length of tie chain is less than or equal to ``1``.

        Return boolean.
        '''
        return len(self) <= 1

    @property
    def leaves(self):
        r'''Leaves in tie chain.

        Return tuple.
        '''
        from abjad.tools import spannertools
        spanner_classes = (spannertools.TieSpanner, )
        try:
            tie_spanner = \
                spannertools.get_the_only_spanner_attached_to_component(
                    self[0], spanner_classes=spanner_classes)
            return tie_spanner.leaves
        except MissingSpannerError:
            assert self.is_trivial
            return (self[0], )

    @property
    def leaves_grouped_by_immediate_parents(self):
        r'''Leaves in tie chain grouped by immediate parents of leaves.

        Return list of lists.
        '''
        result = []
        pairs_generator = itertools.groupby(self, lambda x: id(x._parent))
        for key, values_generator in pairs_generator:
            result.append(list(values_generator))
        return result

    @property
    def tie_spanner(self):
        r'''Tie spanner governing tie chain.

        Return tie spanner.
        '''
        from abjad.tools import spannertools
        if 1 < len(self):
            spanner_classes = (spannertools.TieSpanner,)
            for component in self[0].parentage:
                try:
                    tie_spanner = component._get_spanner(spanner_classes)
                    break
                except MissingSpannerError:
                    pass
            return tie_spanner

    @property
    def written_duration(self):
        r'''Sum of written duration of all components in tie chain.

        Return duration.
        '''
        return sum([x.written_duration for x in self])

    ### PUBLIC METHODS ###

    def to_tuplet(
        self,
        proportions,
        dotted=False,
        is_diminution=True,
        ):
        r'''Change tie chain to tuplet.

        Example 1. Change tie chain to diminished tuplet:

        ::

            >>> staff = Staff(r"c'8 ~ c'16 cqs''4")
            >>> crescendo = spannertools.HairpinSpanner(staff[:], 'p < f')
            >>> staff.override.dynamic_line_spanner.staff_padding = 3
            >>> time_signature = contexttools.TimeSignatureMark((7, 16))
            >>> time_signature.attach(staff)
            TimeSignatureMark((7, 16))(Staff{3})
            
        ::

            >>> f(staff)
            \new Staff \with {
                \override DynamicLineSpanner #'staff-padding = #3
            } {
                \time 7/16
                c'8 \< \p ~
                c'16
                cqs''4 \f
            }

        ::

            >>> show(staff) # doctest: +SKIP

        ::

            >>> tie_chain = staff[0].select_tie_chain()
            >>> tie_chain.to_tuplet([2, 1, 1, 1], is_diminution=True)
            FixedDurationTuplet(3/16, [c'8, c'16, c'16, c'16])

        ::

            >>> f(staff)
            \new Staff \with {
                \override DynamicLineSpanner #'staff-padding = #3
            } {
                \time 7/16
                \tweak #'text #tuplet-number::calc-fraction-text
                \times 3/5 {
                    c'8 \< \p
                    c'16
                    c'16
                    c'16
                }
                cqs''4 \f
            }

        ::

            >>> show(staff) # doctest: +SKIP

        Example 2. Change tie chain to augmented tuplet:

        ::

            >>> staff = Staff(r"c'8 ~ c'16 cqs''4")
            >>> crescendo = spannertools.HairpinSpanner(staff[:], 'p < f')
            >>> staff.override.dynamic_line_spanner.staff_padding = 3
            >>> time_signature = contexttools.TimeSignatureMark((7, 16))
            >>> time_signature.attach(staff)
            TimeSignatureMark((7, 16))(Staff{3})
            
        ::

            >>> f(staff)
            \new Staff \with {
                \override DynamicLineSpanner #'staff-padding = #3
            } {
                \time 7/16
                c'8 \< \p ~
                c'16
                cqs''4 \f
            }

        ::

            >>> show(staff) # doctest: +SKIP

        ::

            >>> tie_chain = staff[0].select_tie_chain()
            >>> tie_chain.to_tuplet([2, 1, 1, 1], is_diminution=False)
            FixedDurationTuplet(3/16, [c'16, c'32, c'32, c'32])

        ::

            >>> f(staff)
            \new Staff \with {
                \override DynamicLineSpanner #'staff-padding = #3
            } {
                \time 7/16
                \tweak #'text #tuplet-number::calc-fraction-text
                \times 6/5 {
                    c'16 \< \p
                    c'32
                    c'32
                    c'32
                }
                cqs''4 \f
            }

        ::

            >>> show(staff) # doctest: +SKIP

        Return tuplet.
        '''
        from abjad.tools import componenttools
        from abjad.tools import mathtools
        from abjad.tools import notetools
        from abjad.tools import spannertools
        from abjad.tools import tuplettools

        # coerce input
        proportions = mathtools.Ratio(proportions)

        # find target duration of fixed-duration tuplet
        target_duration = self._preprolated_duration

        # find prolated duration of each note in tuplet
        prolated_duration = target_duration / sum(proportions)

        # find written duration of each notes in tuplet
        if is_diminution:
            if dotted:
                basic_written_duration = \
                    prolated_duration.equal_or_greater_assignable
            else:
                basic_written_duration = \
                    prolated_duration.equal_or_greater_power_of_two
        else:
            if dotted:
                basic_written_duration = \
                    prolated_duration.equal_or_lesser_assignable
            else:
                basic_written_duration = \
                    prolated_duration.equal_or_lesser_power_of_two

        # find written duration of each note in tuplet
        written_durations = [x * basic_written_duration for x in proportions]

        # make tuplet notes
        try:
            notes = [notetools.Note(0, x) for x in written_durations]
        except AssignabilityError:
            denominator = target_duration._denominator
            note_durations = [durationtools.Duration(x, denominator) 
                for x in proportions]
            notes = notetools.make_notes(0, note_durations)

        # make tuplet
        tuplet = tuplettools.FixedDurationTuplet(target_duration, notes)

        # replace tie chain with tuplet
        componenttools.move_parentage_and_spanners_from_components_to_components(
            list(self), [tuplet])

        # untie tuplet
        spannertools.detach_spanners_attached_to_component(
            tuplet, spannertools.TieSpanner)

        # return tuplet
        return tuplet
