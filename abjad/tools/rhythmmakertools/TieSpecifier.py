# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadObject


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
        tie_split_notes=False,
        ):
        assert isinstance(tie_across_divisions, bool)
        assert isinstance(tie_split_notes, bool)
        self._tie_across_divisions = tie_across_divisions
        self._tie_split_notes = tie_split_notes
