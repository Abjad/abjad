# -*- coding: utf-8 -*-
from __future__ import print_function
import collections
import itertools
from abjad.tools import datastructuretools
from abjad.tools import scoretools
from abjad.tools import spannertools
from abjad.tools.abctools import AbjadValueObject
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import detach
from abjad.tools.topleveltools import inspect
from abjad.tools.topleveltools import iterate
from abjad.tools.topleveltools import select


class TieSpecifier(AbjadValueObject):
    r'''Tie specifier.

    ::

        >>> import abjad
        >>> from abjad.tools import rhythmmakertools

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_strip_ties',
        '_tie_across_divisions',
        '_tie_consecutive_notes',
        '_use_messiaen_style_ties',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        strip_ties=None,
        tie_across_divisions=None,
        tie_consecutive_notes=None,
        use_messiaen_style_ties=None,
        ):
        if strip_ties is not None:
            strip_ties = bool(strip_ties)
        self._strip_ties = strip_ties
        prototype = (
            type(None),
            bool,
            collections.Sequence,
            datastructuretools.Pattern,
            datastructuretools.PatternList,
            )
        assert isinstance(tie_across_divisions, prototype)
        self._tie_across_divisions = tie_across_divisions
        if tie_consecutive_notes is not None:
            tie_consecutive_notes = bool(tie_consecutive_notes)
        self._tie_consecutive_notes = tie_consecutive_notes
        if self.tie_consecutive_notes and self.strip_ties:
            message = 'can not tie leaves and strip ties at same time.'
            raise Exception(message)
        if use_messiaen_style_ties is not None:
            use_messiaen_style_ties = bool(use_messiaen_style_ties)
        self._use_messiaen_style_ties = use_messiaen_style_ties

    ### SPECIAL METHODS ###

    def __call__(self, divisions):
        r'''Calls tie specifier on `divisions`.

        Returns none.
        '''
        self._do_tie_across_divisions(divisions)
        self._do_tie_consecutive_notes(divisions)
        self._do_strip_ties(divisions)
        self._configure_messiaen_style_ties(divisions)

    ### PRIVATE METHODS ###

    def _configure_messiaen_style_ties(self, divisions):
        if not self.use_messiaen_style_ties:
            return
        tie_spanners = set()
        for leaf in iterate(divisions).by_leaf():
            tie_spanners_ = inspect(leaf).get_spanners(
                prototype=spannertools.Tie,
                in_parentage=True,
                )
            tie_spanners.update(tie_spanners_)
        for tie_spanner in tie_spanners:
            tie_spanner._use_messiaen_style_ties = True

    def _do_strip_ties(self, divisions):
        if not self.strip_ties:
            return
        for division in divisions:
            for leaf in iterate(division).by_leaf():
                detach(spannertools.Tie, leaf)

    def _do_tie_across_divisions(self, divisions):
        import abjad
        if not self.tie_across_divisions:
            return
        if self.strip_ties:
            return
        if self.tie_consecutive_notes:
            return
        length = len(divisions)
        tie_across_divisions = self.tie_across_divisions
        if isinstance(tie_across_divisions, bool):
            tie_across_divisions = [tie_across_divisions]
        if not isinstance(tie_across_divisions, abjad.Pattern):
            tie_across_divisions = abjad.Pattern.from_vector(
                tie_across_divisions)
        pairs = abjad.Sequence(divisions).nwise()
        rest_prototype = (abjad.Rest, abjad.MultimeasureRest)
        for i, pair in enumerate(pairs):
            if not tie_across_divisions.matches_index(i, length):
                continue
            division_one, division_two = pair
            leaf_one = next(iterate(division_one).by_leaf(reverse=True))
            leaf_two = next(iterate(division_two).by_leaf())
            leaves = [leaf_one, leaf_two]
            if isinstance(leaf_one, rest_prototype):
                continue
            if isinstance(leaf_two, rest_prototype):
                continue
            pitched_prototype = (abjad.Note, abjad.Chord)
            if not all(isinstance(_, pitched_prototype) for _ in leaves):
                continue
            logical_tie_one = inspect(leaf_one).get_logical_tie()
            logical_tie_two = inspect(leaf_two).get_logical_tie()
            if logical_tie_one == logical_tie_two:
                continue
            combined_logical_tie = logical_tie_one + logical_tie_two
            for leaf in combined_logical_tie:
                abjad.detach(abjad.Tie, leaf)
            tie = abjad.Tie(
                use_messiaen_style_ties=self.use_messiaen_style_ties,
                )
            tie._unconstrain_contiguity()
            if tie._attachment_test_all(combined_logical_tie):
                try:
                    attach(tie, combined_logical_tie)
                except:
                    raise Exception(tie, combined_logical_tie)
            tie._constrain_contiguity()

    def _do_tie_consecutive_notes(self, divisions):
        import abjad
        if not self.tie_consecutive_notes:
            return
        leaves = abjad.select(divisions).by_leaf()
        for leaf in leaves:
            abjad.detach(abjad.Tie, leaf)
        pairs = itertools.groupby(leaves, lambda _: _.__class__)
        def _get_pitches(component):
            if isinstance(component, abjad.Note):
                return component.written_pitch
            elif isinstance(component, abjad.Chord):
                return component.written_pitches
            else:
                raise TypeError(component)
        for class_, group in pairs:
            group = list(group)
            if not isinstance(group[0], (abjad.Note, abjad.Chord)):
                continue
            subpairs = itertools.groupby(group, lambda _: _get_pitches(_))
            for pitches, subgroup in subpairs:
                subgroup = list(subgroup)
                if len(subgroup) == 1:
                    continue
                tie = abjad.Tie()
                assert tie._attachment_test_all(subgroup)
                abjad.attach(tie, abjad.select(subgroup))

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
    def tie_consecutive_notes(self):
        r'''Is true when rhythm-maker should tie consecutive notes.
        Otherwise false.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._tie_consecutive_notes

    @property
    def use_messiaen_style_ties(self):
        r'''Is true when ties should be Messiaen-style with the LilyPond
        ``\repeatTie`` command. Otherwise false.

        Set to true, false or none.
        '''
        return self._use_messiaen_style_ties
