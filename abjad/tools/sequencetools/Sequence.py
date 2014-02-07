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
        r'''Is true when sequence decreases monotonically.

        ..  container:: example

            Is true when sequence decreases monotonically:

            ::

                >>> Sequence(5, 4, 3, 2, 1, 0).is_monotonically_decreasing()
                True

            ::

                >>> Sequence(3, 3, 3, 2, 1, 0).is_monotonically_decreasing()
                True

            ::

                >>> Sequence(3, 3, 3, 3, 3, 3).is_monotonically_decreasing()
                True

            Is true when sequence is empty:

            ::

                >>> Sequence().is_monotonically_decreasing()
                True

        ..  container:: example

            Is false when sequence decreases monotonically:

            ::

                >>> Sequence(0, 1, 2, 3, 4, 5).is_monotonically_decreasing()
                False

            ::

                >>> Sequence(0, 1, 2, 3, 3, 3).is_monotonically_decreasing()
                False

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
        r'''Is true when sequence increases monotonically.

        ..  container:: example

            Is true when sequence increases monotonically:

            ::

                >>> Sequence(0, 1, 2, 3, 4, 5).is_monotonically_increasing()
                True

            ::

                >>> Sequence(0, 1, 2, 3, 3, 3).is_monotonically_increasing()
                True

            ::

                >>> Sequence(3, 3, 3, 3, 3, 3).is_monotonically_increasing()
                True

            Is true when sequence is empty:

            ::

                >>> Sequence().is_monotonically_increasing()
                True

        ..  container:: example

            Is false when sequence does not increase monotonically:

            ::

                >>> Sequence(5, 4, 3, 2, 1, 0).is_monotonically_increasing()
                False

            ::

                >>> Sequence(3, 3, 3, 2, 1, 0).is_monotonically_increasing()
                False

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


    def is_permutation(self, length=None):
        '''Is true when sequence is a permutation.

        ..  container:: example

            Is true when sequence is a permutation:

            ::

                >>> Sequence(4, 5, 0, 3, 2, 1).is_permutation()
                True

        ..  container:: example

            Is false when sequence is not a permutation:

            ::

                >>> Sequence(1, 1, 5, 3, 2, 1).is_permutation()
                False

        Returns boolean.
        '''
        return sorted(self) == range(len(self))

    def is_repetition_free(self):
        '''Is true when sequence is repetition-free.

        ..  container:: example

            Is true when sequence contains no repetitions:

            ::

                >>> Sequence(0, 1, 2, 6, 7, 8).is_repetition_free()
                True

            Is true when sequence is empty: 

            ::

                >>> Sequence().is_repetition_free()
                True

        ..  container:: example

            Is false when sequence contains repetitions:

            ::

                >>> Sequence(0, 1, 2, 2, 7, 8).is_repetition_free()
                False

        Returns boolean.
        '''
        from abjad.tools import sequencetools
        try:
            pairs = sequencetools.iterate_sequence_nwise(self)
            for left, right in pairs:
                if left == right:
                    return False
            return True
        except TypeError:
            return False

    def is_restricted_growth_function(self):
        '''Is true when sequence is a restricted growth function.

        ..  container:: example

            Is true when sequence is a restricted growth function:

            ::

                >>> Sequence(1, 1, 1, 1).is_restricted_growth_function()
                True

            ::


                >>> Sequence(1, 1, 1, 2).is_restricted_growth_function()
                True

            ::

                >>> Sequence(1, 1, 2, 1).is_restricted_growth_function()
                True

            ::

                >>> Sequence(1, 1, 2, 2).is_restricted_growth_function()
                True

        ..  container:: example

            Is false when sequence is not a restricted growth function:
            
            ::

                >>> Sequence(1, 1, 1, 3).is_restricted_growth_function()
                False

            ::

                >>> Sequence(17).is_restricted_growth_function()
                False

        A restricted growth function is a sequence ``l`` such that 
        ``l[0] == 1`` and such that ``l[i] <= max(l[:i]) + 1`` for 
        ``1 <= i <= len(l)``.

        Returns boolean.
        '''
        try:
            for i, n in enumerate(self):
                if i == 0:
                    if not n == 1:
                        return False
                else:
                    if not n <= max(self[:i]) + 1:
                        return False
            return True
        except TypeError:
            return False
