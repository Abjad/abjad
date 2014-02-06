# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadObject


class Sequence(AbjadObject):
    r'''A sequence.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_elements',
        )

    ### INITIALIZER ###

    def __init__(self, *args):
        args = args or ()
        elements = tuple(args)
        self._elements = elements

    ### SPECIAL METHODS ###

    def __len__(self):
        r'''Gets length of sequence.

        Returns nonnegative integer.
        '''
        return len(self._elements)

    def __getitem__(self, i):
        r'''Gets item `i` from sequence.

        Return item.
        '''
        return self._elements.__getitem__(i)

    ### PRIVATE PROPERTIES ###

    @property
    def _repr_specification(self):
        return self._storage_format_specification

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        positional_argument_values = tuple(self._elements)
        return systemtools.StorageFormatSpecification(
            self,
            is_indented=False,
            positional_argument_values=positional_argument_values,
            )
