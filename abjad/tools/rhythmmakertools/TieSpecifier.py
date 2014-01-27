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
