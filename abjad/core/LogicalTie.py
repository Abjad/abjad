import itertools

from abjad import exceptions
from abjad.indicators.RepeatTie import RepeatTie
from abjad.indicators.Tie import Tie
from abjad.mathtools import Ratio
from abjad.top.detach import detach
from abjad.top.inspect import inspect
from abjad.top.mutate import mutate
from abjad.top.select import select
from abjad.utilities.Duration import Duration

from .Selection import Selection


class LogicalTie(Selection):
    """
    Logical tie of a component.

    ..  container:: example

        >>> staff = abjad.Staff("c' d' e' ~ e'")
        >>> abjad.show(staff) # doctest: +SKIP

        >>> abjad.select(staff[2]).logical_tie()
        LogicalTie([Note("e'4"), Note("e'4")])

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __getitem__(self, argument):
        """
        Gets ``argument``.

        Returns component or vanilla selection (not logical tie).
        """
        result = self.items.__getitem__(argument)
        if isinstance(result, tuple):
            result = Selection(result)
        return result

    ### PRIVATE METHODS ###

    def _add_or_remove_notes_to_achieve_written_duration(self, new_written_duration):
        from abjad.spanners import tie as abjad_tie
        from .NoteMaker import NoteMaker
        from .Tuplet import Tuplet

        new_written_duration = Duration(new_written_duration)
        maker = NoteMaker()
        if new_written_duration.is_assignable:
            self[0].written_duration = new_written_duration
            for leaf in self[1:]:
                mutate(leaf).extract()
            detach(Tie, self[0])
            detach(RepeatTie, self[0])
        elif new_written_duration.has_power_of_two_denominator:
            durations = maker(0, [new_written_duration])
            for leaf, token in zip(self, durations):
                leaf.written_duration = token.written_duration
            if len(self) == len(durations):
                pass
            elif len(durations) < len(self):
                for leaf in self[len(durations) :]:
                    mutate(leaf).extract()
            elif len(self) < len(durations):
                # detach(Tie, self[0])
                detach(Tie, self[0])
                detach(RepeatTie, self[0])
                difference = len(durations) - len(self)
                extra_leaves = self[0] * difference
                for extra_leaf in extra_leaves:
                    # detach(Tie, extra_leaf)
                    detach(Tie, extra_leaf)
                    detach(RepeatTie, extra_leaf)
                extra_tokens = durations[len(self) :]
                for leaf, token in zip(extra_leaves, extra_tokens):
                    leaf.written_duration = token.written_duration
                parent = inspect(self[-1]).parentage().parent
                index = parent.index(self[-1])
                next_ = index + 1
                parent[next_:next_] = extra_leaves
                leaves = self.leaves + extra_leaves
                # attach(Tie(), leaves)
                abjad_tie(leaves)
        else:
            components = maker(0, new_written_duration)
            assert isinstance(components[0], Tuplet)
            tuplet = components[0]
            logical_tie = tuplet[0]._get_logical_tie()
            duration = logical_tie._get_preprolated_duration()
            leaves_ = self._add_or_remove_notes_to_achieve_written_duration(duration)
            multiplier = tuplet.multiplier
            tuplet = Tuplet(multiplier, [])
            # mutate(self.leaves).wrap(tuplet)
            mutate(leaves_).wrap(tuplet)

        return self[0]._get_logical_tie()

    def _fuse_leaves_by_immediate_parent(self):
        result = []
        parts = self._get_leaves_grouped_by_immediate_parents()
        for part in parts:
            result.append(part._fuse())
        return result

    def _get_leaves_grouped_by_immediate_parents(self):
        result = []
        pairs_generator = itertools.groupby(self, lambda x: id(x._parent))
        for key, values_generator in pairs_generator:
            group = select(list(values_generator))
            result.append(group)
        return result

    def _scale(self, multiplier):
        new_duration = multiplier * self.written_duration
        return self._add_or_remove_notes_to_achieve_written_duration(new_duration)

    ### PUBLIC PROPERTIES ###

    @property
    def head(self):
        """
        Reference to element ``0`` in logical tie.

        Returns component.
        """
        if self.items:
            return self.items[0]

    @property
    def is_pitched(self):
        """
        Is true when logical tie head is a note or chord.

        Returns true or false.
        """
        from .Chord import Chord
        from .Note import Note

        return isinstance(self.head, (Chord, Note))

    @property
    def is_trivial(self):
        """
        Is true when length of logical tie is less than or equal to ``1``.

        Returns true or false.
        """
        return len(self) <= 1

    @property
    def leaves(self):
        """
        Gets leaves in logical tie.

        Returns selection.
        """
        return Selection(self)

    @property
    def tail(self):
        """
        Gets last leaf in logical tie.

        Returns leaf.
        """
        if self.items:
            return self.items[-1]

    @property
    def written_duration(self):
        """
        Sum of written duration of all components in logical tie.

        Returns duration.
        """
        return sum([_.written_duration for _ in self])

    ### PUBLIC METHODS ###

    def to_tuplet(self, proportions):
        r"""
        Changes logical tie to tuplet.

        ..  container:: example

            >>> staff = abjad.Staff(r"df'8 c'8 ~ c'16 cqs''4")
            >>> abjad.attach(abjad.Dynamic('p'), staff[0])
            >>> abjad.attach(abjad.StartHairpin('<'), staff[0])
            >>> abjad.attach(abjad.Dynamic('f'), staff[-1])
            >>> abjad.override(staff).dynamic_line_spanner.staff_padding = 3
            >>> time_signature = abjad.TimeSignature((9, 16))
            >>> abjad.attach(time_signature, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    \override DynamicLineSpanner.staff-padding = #3
                }
                {
                    \time 9/16
                    df'8
                    \p
                    \<
                    c'8
                    ~
                    c'16
                    cqs''4
                    \f
                }

            >>> logical_tie = abjad.select(staff[1]).logical_tie()
            >>> logical_tie.to_tuplet([2, 1, 1, 1])
            Tuplet(Multiplier(3, 5), "c'8 c'16 c'16 c'16")

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    \override DynamicLineSpanner.staff-padding = #3
                }
                {
                    \time 9/16
                    df'8
                    \p
                    \<
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 3/5 {
                        c'8
                        c'16
                        c'16
                        c'16
                    }
                    cqs''4
                    \f
                }

            >>> abjad.show(staff) # doctest: +SKIP

        ..  container:: example

            >>> staff = abjad.Staff(r"c'8 ~ c'16 cqs''4")
            >>> abjad.hairpin('p < f', staff[:])
            >>> abjad.override(staff).dynamic_line_spanner.staff_padding = 3
            >>> time_signature = abjad.TimeSignature((7, 16))
            >>> abjad.attach(time_signature, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    \override DynamicLineSpanner.staff-padding = #3
                }
                {
                    \time 7/16
                    c'8
                    \p
                    \<
                    ~
                    c'16
                    cqs''4
                    \f
                }

        Returns tuplet.
        """
        from .Note import Note
        from .Note import Note
        from .NoteMaker import NoteMaker
        from .Tuplet import Tuplet

        proportions = Ratio(proportions)
        target_duration = self._get_preprolated_duration()
        prolated_duration = target_duration / sum(proportions.numbers)
        basic_written_duration = prolated_duration.equal_or_greater_power_of_two
        written_durations = [_ * basic_written_duration for _ in proportions.numbers]
        maker = NoteMaker()
        try:
            notes = [Note(0, _) for _ in written_durations]
        except exceptions.AssignabilityError:
            denominator = target_duration._denominator
            note_durations = [Duration(_, denominator) for _ in proportions.numbers]
            notes = maker(0, note_durations)
        tuplet = Tuplet.from_duration(target_duration, notes)
        for leaf in self:
            detach(Tie, leaf)
            detach(RepeatTie, leaf)
        mutate(self).replace(tuplet)
        return tuplet
