# -*- encoding: utf-8 -*-
from abjad.tools import datastructuretools
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
        assert isinstance(tie_across_divisions, (bool, tuple, list))
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

    def __hash__(self):
        r'''Hashes tie specifier.

        Required to be explicitely re-defined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(TieSpecifier, self).__hash__()

    ### PRIVATE PROPERTIES ###

    @property
    def _attribute_manifest(self):
        from abjad.tools import systemtools
        from scoremanager import idetools
        return systemtools.AttributeManifest(
            systemtools.AttributeDetail(
                name='tie_across_divisions',
                command='tad',
                editor=idetools.getters.get_boolean,
                ),
            systemtools.AttributeDetail(
                name='tie_split_notes',
                command='tsn',
                editor=idetools.getters.get_boolean,
                ),
            )

    ### PRIVATE METHODS ###

    def _make_ties_across_divisions(self, music):
        if not self.tie_across_divisions:
            return
        if self.tie_across_divisions == True:
            for division_one, division_two in \
                sequencetools.iterate_sequence_nwise(music):
                leaf_one = next(iterate(division_one).by_class(
                    prototype=scoretools.Leaf,
                    reverse=True))
                leaf_two = next(iterate(division_two).by_class(
                    prototype=scoretools.Leaf))
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
        elif isinstance(self.tie_across_divisions, (tuple, list)):
            tie_across_divisions = datastructuretools.CyclicTuple(
                self.tie_across_divisions
                )
            pairs = sequencetools.iterate_sequence_nwise(music)
            for i, pair in enumerate(pairs):
                indicator = tie_across_divisions[i]
                if not bool(indicator):
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
                attach(spannertools.Tie(), combined_logical_tie)
        else:
            raise TypeError(self.tie_across_divisions)

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