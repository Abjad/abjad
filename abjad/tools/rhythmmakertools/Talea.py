# -*- encoding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools.abctools import AbjadValueObject


class Talea(AbjadValueObject):
    '''Talea.

    ..  container:: example

        ::

            >>> talea = rhythmmakertools.Talea(
            ...    counts=(2, 1, 3, 2, 4, 1, 1),
            ...    denominator=16,
            ...    )

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_counts',
        '_denominator',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        counts=(1,),
        denominator=16,
        ):
        counts = self._to_tuple(counts)
        assert isinstance(counts, tuple)
        assert all(isinstance(x, int) for x in counts)
        self._counts = counts
        assert mathtools.is_nonnegative_integer_power_of_two(denominator)
        self._denominator = denominator

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        r'''Is true when `expr` is a talea with `counts` and `denominator`
        equal to those of this talea. Otherwise false.

        Returns boolean.
        '''
        from abjad.tools import systemtools
        return systemtools.StorageFormatManager.compare(self, expr)

    def __hash__(self):
        r'''Hashes talea.

        Returns integer.
        '''
        from abjad.tools import systemtools
        hash_values = systemtools.StorageFormatManager.get_hash_values(self)
        return hash(hash_values)

    ### PRIVATE PROPERTIES ###

    @property
    def _attribute_manifest(self):
        from abjad.tools import systemtools
        from scoremanager import idetools
        return systemtools.AttributeManifest(
            systemtools.AttributeDetail(
                name='counts',
                command='c',
                editor=idetools.getters.get_nonzero_integers,
                ),
            systemtools.AttributeDetail(
                name='denominator',
                command='d',
                editor=idetools.getters.get_positive_integer_power_of_two,
                ),
            )

    ### PRIVATE METHODS ###

    @staticmethod
    def _to_tuple(expr):
        if isinstance(expr, list):
            expr = tuple(expr)
        return expr

    ### PUBLIC PROPERTIES ###

    @property
    def counts(self):
        r'''Gets counts of talea.

        Returns tuple.
        '''
        return self._counts

    @property
    def denominator(self):
        r'''Gets denominator of talea.

        Returns nonnegative integer power of two.
        '''
        return self._denominator

    ### PUBLIC METHODS ###

    def reverse(self):
        r'''Reverses talea.

        ..  container:: example

            ::

                >>> reversed_talea = talea.reverse()
                >>> print(format(reversed_talea))
                rhythmmakertools.Talea(
                    counts=(1, 1, 4, 2, 3, 1, 2),
                    denominator=16,
                    )

        Returns new talea.
        '''
        counts = tuple(reversed(self.counts))
        result = type(self)(
            counts=counts,
            denominator=self.denominator,
            )
        return result

    def rotate(self, n=0):
        r'''Rotates talea by `n`.

        ..  container:: example

            ::

                >>> rotated_talea = talea.rotate(1)
                >>> print(format(rotated_talea))
                rhythmmakertools.Talea(
                    counts=(1, 2, 1, 3, 2, 4, 1),
                    denominator=16,
                    )

        Returns new talea.
        '''
        counts = tuple(sequencetools.rotate_sequence(self.counts, n))
        result = type(self)(
            counts=counts,
            denominator=self.denominator,
            )
        return result