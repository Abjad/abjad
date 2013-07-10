import itertools
from abjad.tools import chordtools
from abjad.tools import componenttools
from abjad.tools import notetools
from abjad.tools import sequencetools
from abjad.tools import spannertools
from abjad.tools.selectiontools.Selection import Selection


class TieChain(Selection):
    '''.. versionadded:: 2.9

    All the notes in a tie chain:

    ::

        >>> staff = Staff("c' d' e' ~ e'")

    ::

        >>> tietools.get_tie_chain(staff[2])
        TieChain(Note("e'4"), Note("e'4"))

    Tie chains are immutable score selections.
    '''

    ### INITIALIZER ###

    def __init__(self, music=None):
        if isinstance(music, Selection):
            Selection.__init__(self, music.music)
        else:
            Selection.__init__(self, music)

    ### PUBLIC PROPERTIES ###

    @property
    def all_leaves_are_in_same_parent(self):
        '''True when all leaves in tie chain are in same parent.

        Return boolean.
        '''
        return sequencetools.all_are_equal(
            [leaf.parent for leaf in self.leaves])

    @property
    def duration_in_seconds(self):
        '''Duration in seconds of components in tie chain.

        Return duration.
        '''
        return sum([x.duration_in_seconds for x in self])

    @property
    def head(self):
        '''Reference to element ``0`` in tie chain.
        '''
        if self.music:
            return self.music[0]

    @property
    def is_pitched(self):
        '''True when tie chain head is a note or chord.

        Return boolean.
        '''
        return isinstance(self.head, (notetools.Note, chordtools.Chord))

    @property
    def is_trivial(self):
        '''True when length of tie chain is less than or equal to ``1``.

        Return boolean.
        '''
        return len(self) <= 1

    @property
    def leaves(self):
        '''Tuple of leaves in tie spanner.
        '''
        from abjad.tools import tietools
        spanner_classes = (tietools.TieSpanner, )
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
        '''List of leaves in tie chain grouped 
        by immediate parents of leaves.

        Return list of lists.
        '''
        result = []
        pairs_generator = itertools.groupby(self, lambda x: id(x.parent))
        for key, values_generator in pairs_generator:
            result.append(list(values_generator))
        return result

    @property
    def preprolated_duration(self):
        '''Sum of preprolated durations of all components in tie chain.
        '''
        return sum([x.preprolated_duration for x in self])

    @property
    def prolated_duration(self):
        '''Sum of prolated durations of all components in tie chain.
        '''
        return sum([x.prolated_duration for x in self])

    @property
    def written_duration(self):
        '''Sum of written duration of all components in tie chain.
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

            >>> tie_chain = tietools.get_tie_chain(staff[0])
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

            >>> tie_chain = tietools.get_tie_chain(staff[0])
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
        from abjad.tools import durationtools
        from abjad.tools import mathtools
        from abjad.tools import notetools
        from abjad.tools import spannertools
        from abjad.tools import tietools
        from abjad.tools import tuplettools

        # coerce input
        proportions = mathtools.Ratio(proportions)

        # find target duration of fixed-duration tuplet
        target_duration = self.preprolated_duration

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
        spannertools.destroy_spanners_attached_to_component(
            tuplet, tietools.TieSpanner)

        # return tuplet
        return tuplet
