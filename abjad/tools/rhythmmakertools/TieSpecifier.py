# -*- encoding: utf-8 -*-
from __future__ import print_function
import collections
from abjad.tools import scoretools
from abjad.tools import sequencetools
from abjad.tools import spannertools
from abjad.tools.abctools import AbjadValueObject
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import detach
from abjad.tools.topleveltools import inspect_
from abjad.tools.topleveltools import iterate


class TieSpecifier(AbjadValueObject):
    r'''Tie specifier.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_strip_ties',
        '_tie_across_divisions',
        '_use_messiaen_style_ties',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        strip_ties=None,
        tie_across_divisions=None,
        use_messiaen_style_ties=None,
        ):
        from abjad.tools import rhythmmakertools
        if strip_ties is not None:
            strip_ties = bool(strip_ties)
        self._strip_ties = strip_ties
        prototype = (
            type(None),
            bool,
            collections.Sequence,
            rhythmmakertools.BooleanPattern,
            rhythmmakertools.BooleanPatternInventory,
            )
        assert isinstance(tie_across_divisions, prototype)
        self._tie_across_divisions = tie_across_divisions
        if use_messiaen_style_ties is not None:
            use_messiaen_style_ties = bool(use_messiaen_style_ties)
        self._use_messiaen_style_ties = use_messiaen_style_ties

    ### SPECIAL METHODS ###

    def __call__(self, divisions):
        r'''Processes `divisions`.

        Returns none.
        '''
        if not self.strip_ties:
            self._make_ties_across_divisions(divisions)
        self._strip_ties_from_divisions(divisions)

    ### PRIVATE METHODS ###

    def _make_ties_across_divisions(self, divisions):
        from abjad.tools import rhythmmakertools
        if not self.tie_across_divisions:
            return
        length = len(divisions)
        tie_across_divisions = self.tie_across_divisions
        if isinstance(tie_across_divisions, bool):
            tie_across_divisions = [tie_across_divisions]
        if not isinstance(tie_across_divisions,
            rhythmmakertools.BooleanPattern):
            tie_across_divisions = \
                rhythmmakertools.BooleanPattern.from_sequence(
                    tie_across_divisions)
        pairs = sequencetools.iterate_sequence_nwise(divisions)
        for i, pair in enumerate(pairs):
            if not tie_across_divisions.matches_index(i, length):
                continue
            division_one, division_two = pair
            leaf_one = next(iterate(division_one).by_class(
                prototype=scoretools.Leaf,
                reverse=True,
                ))
            leaf_two = next(iterate(division_two).by_class(
                prototype=scoretools.Leaf,
                ))
            leaves = [leaf_one, leaf_two]
            prototype = (scoretools.Note, scoretools.Chord)
            if not all(isinstance(x, prototype) for x in leaves):
                continue
            logical_tie_one = inspect_(leaf_one).get_logical_tie()
            logical_tie_two = inspect_(leaf_two).get_logical_tie()
            for tie in inspect_(leaf_one).get_spanners(spannertools.Tie):
                detach(tie, leaf_one)
            for tie in inspect_(leaf_two).get_spanners(spannertools.Tie):
                detach(tie, leaf_two)
            combined_logical_tie = logical_tie_one + logical_tie_two
            tie_spanner = spannertools.Tie(
                use_messiaen_style_ties=self.use_messiaen_style_ties,
                )
            tie_spanner._unconstrain_contiguity()
            attach(tie_spanner, combined_logical_tie)
            tie_spanner._constrain_contiguity()

    def _strip_ties_from_divisions(self, divisions):
        if not self.strip_ties:
            return
        for division in divisions:
            for leaf in iterate(division).by_class(scoretools.Leaf):
                detach(spannertools.Tie, leaf)

    ### PUBLIC PROPERTIES ###

    @property
    def strip_ties(self):
        r'''Is true when rhythm-maker should strip all ties from all leaves in
        each division.

        Set to true, false or none.
        '''
        return self._strip_ties

    @property
    def tie_across_divisions(self):
        r'''Is true or is a boolean vector when rhythm-maker should tie across
        divisons. Otherwise false.

        Set to true, false or to a boolean vector.
        '''
        return self._tie_across_divisions

    @property
    def use_messiaen_style_ties(self):
        r'''Is true when ties should be Messiaen-style with the LilyPond
        ``\repeatTie`` command. Otherwise false.

        Set to true, false or none.
        '''
        return self._use_messiaen_style_ties