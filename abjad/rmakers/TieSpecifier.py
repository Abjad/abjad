import collections
import itertools
import typing
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class TieSpecifier(AbjadValueObject):
    """
    Tie specifier.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_repeat_ties',
        '_strip_ties',
        '_tie_across_divisions',
        '_tie_consecutive_notes',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        repeat_ties=None,
        strip_ties=None,
        tie_across_divisions=None,
        tie_consecutive_notes=None,
        ):
        import abjad
        if repeat_ties is not None:
            repeat_ties = bool(repeat_ties)
        self._repeat_ties = repeat_ties
        if strip_ties is not None:
            strip_ties = bool(strip_ties)
        self._strip_ties = strip_ties
        prototype = (
            type(None),
            bool,
            collections.Sequence,
            abjad.Pattern,
            abjad.PatternTuple,
            )
        assert isinstance(tie_across_divisions, prototype)
        self._tie_across_divisions = tie_across_divisions
        if tie_consecutive_notes is not None:
            tie_consecutive_notes = bool(tie_consecutive_notes)
        self._tie_consecutive_notes = tie_consecutive_notes
        if self.tie_consecutive_notes and self.strip_ties:
            message = 'can not tie leaves and strip ties at same time.'
            raise Exception(message)

    ### SPECIAL METHODS ###

    def __call__(self, divisions):
        """
        Calls tie specifier on ``divisions``.

        Returns none.
        """
        self._tie_across_divisions_(divisions)
        self._tie_consecutive_notes_(divisions)
        self._strip_ties_(divisions)
        self._configure_repeat_ties(divisions)

    ### PRIVATE METHODS ###

    def _configure_repeat_ties(self, divisions):
        import abjad
        if not self.repeat_ties:
            return
        ties = set()
        for leaf in abjad.iterate(divisions).leaves():
            ties_ = abjad.inspect(leaf).get_spanners(abjad.Tie)
            ties.update(ties_)
        for tie in ties:
            tie._repeat = True

    def _strip_ties_(self, divisions):
        import abjad
        if not self.strip_ties:
            return
        for division in divisions:
            for leaf in abjad.iterate(division).leaves():
                abjad.detach(abjad.Tie, leaf)

    def _tie_across_divisions_(self, divisions):
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
        pairs = abjad.sequence(divisions).nwise()
        rest_prototype = (abjad.Rest, abjad.MultimeasureRest)
        for i, pair in enumerate(pairs):
            if not tie_across_divisions.matches_index(i, length):
                continue
            division_one, division_two = pair
            leaf_one = next(abjad.iterate(division_one).leaves(reverse=True))
            leaf_two = next(abjad.iterate(division_two).leaves())
            leaves = [leaf_one, leaf_two]
            if isinstance(leaf_one, rest_prototype):
                continue
            if isinstance(leaf_two, rest_prototype):
                continue
            pitched_prototype = (abjad.Note, abjad.Chord)
            if not all(isinstance(_, pitched_prototype) for _ in leaves):
                continue
            logical_tie_one = abjad.inspect(leaf_one).get_logical_tie()
            logical_tie_two = abjad.inspect(leaf_two).get_logical_tie()
            if logical_tie_one == logical_tie_two:
                continue
            combined_logical_tie = logical_tie_one + logical_tie_two
            for leaf in combined_logical_tie:
                abjad.detach(abjad.Tie, leaf)
            tie = abjad.Tie(repeat=self.repeat_ties)
            tie._unconstrain_contiguity()
            if tie._attachment_test_all(combined_logical_tie) is True:
                try:
                    abjad.attach(tie, combined_logical_tie)
                except:
                    raise Exception(tie, combined_logical_tie)
            tie._constrain_contiguity()

    def _tie_consecutive_notes_(self, divisions):
        import abjad
        if not self.tie_consecutive_notes:
            return
        leaves = list(abjad.iterate(divisions).leaves())
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
                assert tie._attachment_test_all(subgroup) is True
                abjad.attach(tie, abjad.select(subgroup))

    ### PUBLIC PROPERTIES ###

    @property
    def repeat_ties(self) -> typing.Optional[bool]:
        r"""
        Is true when ties should format with LilyPond ``\repeatTie``.
        """
        return self._repeat_ties

    @property
    def strip_ties(self):
        """
        Is true when rhythm-maker should strip all ties from all leaves in
        each division.

        Set to true, false or none.
        """
        return self._strip_ties

    @property
    def tie_across_divisions(self):
        """
        Is true or is a boolean vector when rhythm-maker should tie across
        divisons.

        Set to true, false or to a boolean vector.
        """
        return self._tie_across_divisions

    @property
    def tie_consecutive_notes(self):
        """
        Is true when rhythm-maker should tie consecutive notes.

        Set to true, false or none.

        Returns true, false or none.
        """
        return self._tie_consecutive_notes
