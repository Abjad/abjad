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

    ### PUBLIC METHODS ###

    def is_monotonically_decreasing(self):
        r'''Is true when elements decrease monotonically.

        ..  container:: example

            Is true when elements decrease monotonically:

            ::

                >>> Sequence(5, 4, 3, 2, 1, 0).is_monotonically_decreasing()
                True

            ::

                >>> Sequence(3, 3, 3, 2, 1, 0).is_monotonically_decreasing()
                True

            ::

                >>> Sequence(3, 3, 3, 3, 3, 3).is_monotonically_decreasing()
                True

        ..  container:: example

            False when elements do not decrease monotonically:

            ::

                >>> Sequence(0, 1, 2, 3, 4, 5).is_monotonically_decreasing()
                False

            ::

                >>> Sequence(0, 1, 2, 3, 3, 3).is_monotonically_decreasing()
                False

        ..  container:: example

            Is true when empty:

            ::

                >>> Sequence().is_monotonically_decreasing()
                True

        Returns boolean.
        '''
        try:
            previous = None
            for current in self:
                if previous is not None:
                    if not current <= previous:
                        return False
                previous = current
            return True
        except TypeError:
            return False

    def is_monotonically_increasing(self):
        r'''Is true when elements increase monotonically.

        ..  container:: example

            Is true when elements increasing monotonically:

            ::

                >>> Sequence(0, 1, 2, 3, 4, 5).is_monotonically_increasing()
                True

            ::

                >>> Sequence(0, 1, 2, 3, 3, 3).is_monotonically_increasing()
                True

            ::

                >>> Sequence(3, 3, 3, 3, 3, 3).is_monotonically_increasing()
                True

        ..  container:: example

            Is false when elements do not increase monotonically:

            ::

                >>> Sequence(5, 4, 3, 2, 1, 0).is_monotonically_increasing()
                False

            ::

                >>> Sequence(3, 3, 3, 2, 1, 0).is_monotonically_increasing()
                False

        ..  container:: example

            Is true when empty:

            ::

                >>> Sequence().is_monotonically_increasing()
                True

        Returns boolean.
        '''
        try:
            previous = None
            for current in self:
                if previous is not None:
                    if not previous <= current:
                        return False
                previous = current
            return True
        except TypeError:
            return False
