# -*- coding: utf-8 -*-
import itertools
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import mutate
from abjad.tools.selectiontools.Selection import Selection


class LogicalTie(Selection):
    r'''A selection of components in a logical tie.

    ..  container:: example

        ::

            >>> staff = Staff("c' d' e' ~ e'")
            >>> show(staff) # doctest: +SKIP

        ::

            >>> inspect_(staff[2]).get_logical_tie()
            LogicalTie([Note("e'4"), Note("e'4")])

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### PRIVATE METHODS ###

    def _add_or_remove_notes_to_achieve_written_duration(
        self, new_written_duration):
        from abjad.tools import scoretools
        from abjad.tools import spannertools
        new_written_duration = durationtools.Duration(new_written_duration)
        if new_written_duration.is_assignable:
            self[0].written_duration = new_written_duration
            for leaf in self[1:]:
                parent = leaf._parent
                if parent:
                    index = parent.index(leaf)
                    del(parent[index])
            first = self[0]
            for spanner in first._get_spanners(spannertools.Tie):
                spanner._sever_all_components()
            #detach(spannertools.Tie, first)
        elif new_written_duration.has_power_of_two_denominator:
            durations = scoretools.make_notes(0, [new_written_duration])
            for leaf, token in zip(self, durations):
                leaf.written_duration = token.written_duration
            if len(self) == len(durations):
                pass
            elif len(durations) < len(self):
                for leaf in self[len(durations):]:
                    parent = leaf._parent
                    if parent:
                        index = parent.index(leaf)
                        del(parent[index])
            elif len(self) < len(durations):
                for spanner in self[0]._get_spanners(spannertools.Tie):
                    spanner._sever_all_components()
                #detach(spannertools.Tie, self[0])
                difference = len(durations) - len(self)
                extra_leaves = self[0] * difference
                for extra_leaf in extra_leaves:
                    for spanner in extra_leaf._get_spanners():
                        spanner._remove(extra_leaf)
                extra_tokens = durations[len(self):]
                for leaf, token in zip(extra_leaves, extra_tokens):
                    leaf.written_duration = token.written_duration
                ties = self[-1]._get_spanners(spannertools.Tie)
                if not ties:
                    tie = spannertools.Tie()
                    if all(tie._attachment_test(_) for _ in self):
                        attach(tie, list(self))
                self[-1]._splice(extra_leaves, grow_spanners=True)
        else:
            durations = scoretools.make_notes(0, new_written_duration)
            assert isinstance(durations[0], scoretools.Tuplet)
            fmtuplet = durations[0]
            new_logical_tie_written = \
                fmtuplet[0]._get_logical_tie()._preprolated_duration
            self._add_or_remove_notes_to_achieve_written_duration(
                new_logical_tie_written)
            multiplier = fmtuplet.multiplier
            scoretools.Tuplet(multiplier, self.leaves)
        return self[0]._get_logical_tie()

    def _fuse_leaves_by_immediate_parent(self):
        result = []
        parts = self.leaves_grouped_by_immediate_parents
        for part in parts:
            result.append(part._fuse())
        return result

    def _scale(self, multiplier):
        new_duration = multiplier * self.written_duration
        return self._add_or_remove_notes_to_achieve_written_duration(
            new_duration)

    ### PUBLIC METHODS ###

    def to_tuplet(
        self,
        proportions,
        dotted=False,
        is_diminution=True,
        ):
        r'''Change logical tie to tuplet.

        ..  container:: example

            **Example 1.** Change logical tie to diminished tuplet:

            ::

                >>> staff = Staff(r"c'8 ~ c'16 cqs''4")
                >>> crescendo = spannertools.Hairpin(descriptor='p < f')
                >>> attach(crescendo, staff[:])
                >>> override(staff).dynamic_line_spanner.staff_padding = 3
                >>> time_signature = TimeSignature((7, 16))
                >>> attach(time_signature, staff)

            ..  doctest::

                >>> print(format(staff))
                \new Staff \with {
                    \override DynamicLineSpanner.staff-padding = #3
                } {
                    \time 7/16
                    c'8 ~ \< \p
                    c'16
                    cqs''4 \f
                }

            ::

                >>> show(staff) # doctest: +SKIP

            ::

                >>> logical_tie = inspect_(staff[0]).get_logical_tie()
                >>> logical_tie.to_tuplet([2, 1, 1, 1], is_diminution=True)
                FixedDurationTuplet(Duration(3, 16), "c'8 c'16 c'16 c'16")

            ..  doctest::

                >>> print(format(staff))
                \new Staff \with {
                    \override DynamicLineSpanner.staff-padding = #3
                } {
                    \time 7/16
                    \tweak text #tuplet-number::calc-fraction-text
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

        ..  container:: example

            **Example 2.** Change logical tie to augmented tuplet:

            ::

                >>> staff = Staff(r"c'8 ~ c'16 cqs''4")
                >>> crescendo = spannertools.Hairpin(descriptor='p < f')
                >>> attach(crescendo, staff[:])
                >>> override(staff).dynamic_line_spanner.staff_padding = 3
                >>> time_signature = TimeSignature((7, 16))
                >>> attach(time_signature, staff)

            ..  doctest::

                >>> print(format(staff))
                \new Staff \with {
                    \override DynamicLineSpanner.staff-padding = #3
                } {
                    \time 7/16
                    c'8 ~ \< \p
                    c'16
                    cqs''4 \f
                }

            ::

                >>> show(staff) # doctest: +SKIP

            ::

                >>> logical_tie = inspect_(staff[0]).get_logical_tie()
                >>> logical_tie.to_tuplet([2, 1, 1, 1], is_diminution=False)
                FixedDurationTuplet(Duration(3, 16), "c'16 c'32 c'32 c'32")

            ..  doctest::

                >>> print(format(staff))
                \new Staff \with {
                    \override DynamicLineSpanner.staff-padding = #3
                } {
                    \time 7/16
                    \tweak text #tuplet-number::calc-fraction-text
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

        Returns tuplet.
        '''
        from abjad.tools import mathtools
        from abjad.tools import scoretools
        from abjad.tools import spannertools

        # coerce input
        proportions = mathtools.Ratio(proportions)

        # find target duration of fixed-duration tuplet
        target_duration = self._preprolated_duration

        # find duration of each note in tuplet
        prolated_duration = target_duration / sum(proportions.numbers)

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
        written_durations = [
            _ * basic_written_duration for _ in proportions.numbers
            ]

        # make tuplet notes
        try:
            notes = [scoretools.Note(0, x) for x in written_durations]
        except AssignabilityError:
            denominator = target_duration._denominator
            note_durations = [
                durationtools.Duration(_, denominator)
                for _ in proportions.numbers
                ]
            notes = scoretools.make_notes(0, note_durations)

        # make tuplet
        tuplet = scoretools.FixedDurationTuplet(target_duration, notes)

        # replace logical tie with tuplet
        mutate(self).replace(tuplet)

        # untie tuplet
        for spanner in tuplet._get_spanners(spannertools.Tie):
            spanner._sever_all_components()
        #detach(spannertools.Tie, tuplet)

        # return tuplet
        return tuplet

    ### PUBLIC PROPERTIES ###

    @property
    def all_leaves_are_in_same_parent(self):
        r'''Is true when all leaves in logical tie are in same parent.

        Returns true or false.
        '''
        return mathtools.all_are_equal(
            [leaf._parent for leaf in self.leaves])

    @property
    def head(self):
        r'''Reference to element ``0`` in logical tie.

        Returns component.
        '''
        if self._music:
            return self._music[0]

    @property
    def is_pitched(self):
        r'''Is true when logical tie head is a note or chord.

        Returns true or false.
        '''
        from abjad.tools import scoretools
        return isinstance(self.head, (scoretools.Note, scoretools.Chord))

    @property
    def is_trivial(self):
        r'''Is true when length of logical tie is less than or equal to ``1``.

        Returns true or false.
        '''
        return len(self) <= 1

    @property
    def leaves(self):
        r'''Leaves in logical tie.

        Returns tuple.
        '''
        from abjad.tools import spannertools
        prototype = (spannertools.Tie,)
        try:
            tie_spanner = self[0]._get_spanner(prototype=prototype)
            return tuple(tie_spanner._get_leaves())
        except MissingSpannerError:
            assert self.is_trivial
            return (self[0], )

    @property
    def leaves_grouped_by_immediate_parents(self):
        r'''Leaves in logical tie grouped by immediate parents of leaves.

        Returns list of lists.
        '''
        from abjad.tools import selectiontools
        result = []
        pairs_generator = itertools.groupby(self, lambda x: id(x._parent))
        for key, values_generator in pairs_generator:
            group = selectiontools.Selection(list(values_generator))
            result.append(group)
        return result

    @property
    def tail(self):
        r'''Reference to element ``-1`` in logical tie.

        Returns component.
        '''
        if self._music:
            return self._music[-1]

    @property
    def tie_spanner(self):
        r'''Tie spanner governing logical tie.

        Returns tie spanner.
        '''
        from abjad.tools import spannertools
        if 1 < len(self):
            prototype = (spannertools.Tie,)
            for component in self[0].parentage:
                try:
                    tie_spanner = component._get_spanner(prototype)
                    break
                except MissingSpannerError:
                    pass
            return tie_spanner

    @property
    def written_duration(self):
        r'''Sum of written duration of all components in logical tie.

        Returns duration.
        '''
        return sum([x.written_duration for x in self])
