import itertools
from abjad.tools.exceptiontools import MissingSpannerError, AssignabilityError
from .Selection import Selection


class LogicalTie(Selection):
    r'''Logical tie of a component.

    ..  container:: example

        >>> staff = abjad.Staff("c' d' e' ~ e'")
        >>> abjad.show(staff) # doctest: +SKIP

        >>> abjad.inspect(staff[2]).get_logical_tie()
        LogicalTie([Note("e'4"), Note("e'4")])

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __getitem__(self, argument):
        r'''Gets `argument`.

        Returns component or vanilla selection (not logical tie).
        '''
        result = self.items.__getitem__(argument)
        if isinstance(result, tuple):
            result = Selection(result)
        return result

    ### PRIVATE METHODS ###

    def _add_or_remove_notes_to_achieve_written_duration(
        self, new_written_duration):
        import abjad
        new_written_duration = abjad.Duration(new_written_duration)
        maker = abjad.NoteMaker()
        if new_written_duration.is_assignable:
            self[0].written_duration = new_written_duration
            for leaf in self[1:]:
                parent = leaf._parent
                if parent:
                    index = parent.index(leaf)
                    del(parent[index])
            first = self[0]
            for spanner in first._get_spanners(abjad.Tie):
                spanner._sever_all_leaves()
            #detach(abjad.Tie, first)
        elif new_written_duration.has_power_of_two_denominator:
            durations = maker(0, [new_written_duration])
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
                for spanner in self[0]._get_spanners(abjad.Tie):
                    spanner._sever_all_leaves()
                #detach(abjad.Tie, self[0])
                difference = len(durations) - len(self)
                extra_leaves = self[0] * difference
                for extra_leaf in extra_leaves:
                    for spanner in extra_leaf._get_spanners():
                        spanner._remove(extra_leaf)
                extra_tokens = durations[len(self):]
                for leaf, token in zip(extra_leaves, extra_tokens):
                    leaf.written_duration = token.written_duration
                ties = self[-1]._get_spanners(abjad.Tie)
                if not ties:
                    tie = abjad.Tie()
                    if all(tie._attachment_test(_) for _ in self):
                        abjad.attach(tie, self.leaves)
                self[-1]._splice(extra_leaves, grow_spanners=True)
        else:
            durations = maker(0, new_written_duration)
            assert isinstance(durations[0], abjad.Tuplet)
            tuplet = durations[0]
            logical_tie = tuplet[0]._get_logical_tie()
            duration = logical_tie._get_preprolated_duration()
            self._add_or_remove_notes_to_achieve_written_duration(duration)
            multiplier = tuplet.multiplier
            tuplet = abjad.Tuplet(multiplier, [])
            abjad.mutate(self.leaves).wrap(tuplet)
        return self[0]._get_logical_tie()

    def _fuse_leaves_by_immediate_parent(self):
        result = []
        parts = self._get_leaves_grouped_by_immediate_parents()
        for part in parts:
            result.append(part._fuse())
        return result

    def _get_leaves_grouped_by_immediate_parents(self):
        import abjad
        result = []
        pairs_generator = itertools.groupby(self, lambda x: id(x._parent))
        for key, values_generator in pairs_generator:
            group = abjad.select(list(values_generator))
            result.append(group)
        return result

    def _scale(self, multiplier):
        new_duration = multiplier * self.written_duration
        return self._add_or_remove_notes_to_achieve_written_duration(
            new_duration)

    ### PUBLIC PROPERTIES ###

    @property
    def head(self):
        r'''Reference to element ``0`` in logical tie.

        Returns component.
        '''
        if self.items:
            return self.items[0]

    @property
    def is_pitched(self):
        r'''Is true when logical tie head is a note or chord.

        Returns true or false.
        '''
        import abjad
        return isinstance(self.head, (abjad.Note, abjad.Chord))

    @property
    def is_trivial(self):
        r'''Is true when length of logical tie is less than or equal to ``1``.

        Returns true or false.
        '''
        return len(self) <= 1

    @property
    def leaves(self):
        r'''Gets leaves in logical tie.

        Returns selection.
        '''
        import abjad
        try:
            tie = self[0]._get_spanner(prototype=abjad.Tie)
        except MissingSpannerError:
            assert self.is_trivial
            return abjad.select(self[0])
        selection = tie.leaves
        assert isinstance(selection, abjad.Selection)
        return selection

    @property
    def tail(self):
        r'''Gets last leaf in logical tie.

        Returns leaf.
        '''
        if self.items:
            return self.items[-1]

    @property
    def tie_spanner(self):
        r'''Gets tie spanner governing logical tie.

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

    ### PUBLIC METHODS ###

    def to_tuplet(
        self,
        proportions,
        dotted=False,
        is_diminution=True,
        ):
        r'''Changes logical tie to tuplet.

        ..  container:: example

            Changes logical tie to diminished tuplet:

            >>> staff = abjad.Staff(r"c'8 ~ c'16 cqs''4")
            >>> crescendo = abjad.Hairpin('p < f')
            >>> abjad.attach(crescendo, staff[:])
            >>> abjad.override(staff).dynamic_line_spanner.staff_padding = 3
            >>> time_signature = abjad.TimeSignature((7, 16))
            >>> abjad.attach(time_signature, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    \override DynamicLineSpanner.staff-padding = #3
                } {
                    \time 7/16
                    c'8 ~ \< \p
                    c'16
                    cqs''4 \f
                }

            >>> logical_tie = abjad.inspect(staff[0]).get_logical_tie()
            >>> logical_tie.to_tuplet([2, 1, 1, 1], is_diminution=True)
            Tuplet(Multiplier(3, 5), "c'8 c'16 c'16 c'16")

            >>> time_signature = abjad.TimeSignature((7, 16))
            >>> leaf = abjad.inspect(staff).get_leaf(0)
            >>> abjad.attach(time_signature, leaf)

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    \override DynamicLineSpanner.staff-padding = #3
                } {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 3/5 {
                        \time 7/16
                        c'8 \< \p
                        c'16
                        c'16
                        c'16
                    }
                    cqs''4 \f
                }

            >>> abjad.show(staff) # doctest: +SKIP

        ..  container:: example

            Changes logical tie to augmented tuplet:

            >>> staff = abjad.Staff(r"c'8 ~ c'16 cqs''4")
            >>> crescendo = abjad.Hairpin(descriptor='p < f')
            >>> abjad.attach(crescendo, staff[:])
            >>> abjad.override(staff).dynamic_line_spanner.staff_padding = 3
            >>> time_signature = abjad.TimeSignature((7, 16))
            >>> abjad.attach(time_signature, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    \override DynamicLineSpanner.staff-padding = #3
                } {
                    \time 7/16
                    c'8 ~ \< \p
                    c'16
                    cqs''4 \f
                }

            >>> logical_tie = abjad.inspect(staff[0]).get_logical_tie()
            >>> tuplet = logical_tie.to_tuplet(
            ...     [2, 1, 1, 1],
            ...     is_diminution=False,
            ...     )
            >>> time_signature = abjad.TimeSignature((7, 16))
            >>> leaf = abjad.inspect(staff).get_leaf(0)
            >>> abjad.attach(time_signature, leaf)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    \override DynamicLineSpanner.staff-padding = #3
                } {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 6/5 {
                        \time 7/16
                        c'16 \< \p
                        c'32
                        c'32
                        c'32
                    }
                    cqs''4 \f
                }

        Returns tuplet.
        '''
        import abjad
        # coerce input
        proportions = abjad.Ratio(proportions)
        # find target duration of tuplet
        target_duration = self._get_preprolated_duration()
        # find duration of each note in tuplet
        prolated_duration = target_duration / sum(proportions.numbers)
        # find written duration of each note in tuplet
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
        maker = abjad.NoteMaker()
        try:
            notes = [abjad.Note(0, _) for _ in written_durations]
        except AssignabilityError:
            denominator = target_duration._denominator
            note_durations = [
                abjad.Duration(_, denominator)
                for _ in proportions.numbers
                ]
            notes = maker(0, note_durations)
        # make tuplet
        tuplet = abjad.Tuplet.from_duration(target_duration, notes)
        # remove tie spanner from leaves
        for leaf in self:
            for spanner in leaf._get_spanners(abjad.Tie):
                spanner._sever_all_leaves()
        # replace leaves with tuplet
        abjad.mutate(self).replace(tuplet)
        return tuplet
