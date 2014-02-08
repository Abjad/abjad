# -*- encoding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools import sequencetools
from abjad.tools import spannertools
from abjad.tools.abctools import AbjadObject
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import inspect_
from abjad.tools.topleveltools import iterate


class TieSpecifier(AbjadObject):
    r'''Tie specifier.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_tie_across_divisions',
        '_tie_split_notes',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        tie_across_divisions=False,
        tie_split_notes=True,
        ):
        assert isinstance(tie_across_divisions, bool)
        assert isinstance(tie_split_notes, bool)
        self._tie_across_divisions = tie_across_divisions
        self._tie_split_notes = tie_split_notes

    ### SPECIAL METHODS ###

    def __eq__(self, arg):
        r'''Is true when `arg` is a tie specifier with values of
        `tie_across_divisions` and `tie_split_notes` equal to those of this tie
        specifier. Otherwise false.

        Returns boolean.
        '''
        if isinstance(arg, type(self)):
            if self.tie_across_divisions == arg.tie_across_divisions and \
                self.tie_split_notes == arg.tie_split_notes:
                return True
        return False

    ### PRIVATE METHODS ###

    def _make_ties(self, music):
        if self.tie_across_divisions:
            self._make_ties_across_divisions(music)

    @staticmethod
    def _make_ties_across_divisions(music):
        for division_one, division_two in \
            sequencetools.iterate_sequence_nwise(music):
            leaf_one = iterate(division_one).by_class(
                prototype=scoretools.Leaf,
                reverse=True,
                ).next()
            leaf_two = iterate(division_two).by_class(
                prototype=scoretools.Leaf,
                ).next()
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
            attach(spannertools.Tie(), combined_logical_tie)

    ### PUBLIC PROPERTIES ###

    @property
    def tie_across_divisions(self):
        r'''Is true when rhythm-maker should tie across divisons.
        Otherwise false.

        Returns boolean.
        '''
        return self._tie_across_divisions

    @property
    def tie_split_notes(self):
        r'''Is true when rhythm-maker should tie split notes.
        Otherwise false.

        Returns boolean.
        '''
        return self._tie_split_notes
