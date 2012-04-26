from abjad.tools.abctools.ScoreSelection import ScoreSelection


class TieChain(ScoreSelection):
    '''.. versionadded:: 2.9

    All the notes in a tie chain::

        abjad> staff = Staff("c' d' e' ~ e'")

    ::

        abjad> tietools.get_tie_chain(staff[2])
        TieChain((Note("e'4"), Note("e'4")))

    Tie chains are immutable score selections.
    '''

    def __init__(self, music):
        ScoreSelection.__init__(self, music)

    ### READ-ONLY PROPERTIES ###

    @property
    def duration_in_seconds(self):
        '''Read-only duration in seconds of components in tie chain.

        Return duration.
        '''
        return sum([x.duration_in_seconds for x in self])

    @property
    def head(self):
        '''Read-only reference to element ``0`` in tie chain.
        '''
        if self.music:
            return self.music[0]

    @property
    def is_trivial(self):
        '''True when length of tie chain is less than or equal to ``1``.

        Return boolean.
        '''
        return len(self) <= 1

    @property
    def leaves(self):
        '''Read-only tuple of leaves in tie spanner.
        '''
        from abjad.tools import spannertools
        from abjad.tools import tietools
        try:
            tie_spanner = spannertools.get_the_only_spanner_attached_to_component(self[0], tietools.TieSpanner)
            return tie_spanner.leaves
        except MissingSpannerError:
            assert self.is_trivial
            return (self[0], )

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
