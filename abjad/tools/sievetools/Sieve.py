# -*- coding: utf-8 -*-
import functools
from abjad.tools.sievetools.BaseResidueClass import BaseResidueClass


@functools.total_ordering
class Sieve(BaseResidueClass):
    r'''Sieve.

    ..  container:: example

        **Example 1.** Sieve without offset:

        ::

            >>> sieve = sievetools.Sieve(3, 0)
            >>> sieve
            Sieve(period=3, offset=0)

    ..  container:: example

        **Example 2.** Sieve with offset:

        ::

            >>> sieve = sievetools.Sieve(3, 1)
            >>> sieve
            Sieve(period=3, offset=1)

    A sieve is a simple periodic sequence.

    Sieves can be combined with logical operators.

    Sieves form the basis of Xenakis sieves.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_boolean_train',
        '_congruent_bases',
        '_offset',
        '_period',
        )

    ### INITIALIZER ##

    def __init__(self, period=1, offset=0):
        if not 0 < period:
            message = 'period must be positive: {!r}.'
            message = message.format(period)
            raise ValueError(message)
        if not 0 <= offset < period:
            message = 'abs(offset) must be < period.'
            raise ValueError(message)
        self._period = period
        self._offset = offset
        congruent_bases = []
        for i in range(0, self.period):
            if i % self.period == self.offset:
                congruent_bases.append(i)
        self._congruent_bases = congruent_bases

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        r'''Is true when `expr` is a sieve with period and residue
        equal to those of this sieve. Otherwise false.

        ..  container:: example

            **Example 1.** With equal period:

                >>> sieve_1 = sievetools.Sieve(6, 0)
                >>> sieve_2 = sievetools.Sieve(6, 1)

            ::

                >>> sieve_1 == sieve_1
                True

            ::

                >>> sieve_1 == sieve_2
                False

        ..  container:: example

            **Example 2.** With unequal period:

                >>> sieve_1 = sievetools.Sieve(6, 0)
                >>> sieve_2 = sievetools.Sieve(7, 0)

            ::

                >>> sieve_1 == sieve_1
                True

            ::

                >>> sieve_1 == sieve_2
                False

        Returns true or false.
        '''
        if not isinstance(expr, type(self)):
            return False
        if self.period == expr.period:
            if self.offset == expr.offset:
                return True
        return False

    def __hash__(self):
        r'''Hashes sieve.

        Required to be explicitly re-defined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(Sieve, self).__hash__()

    def __lt__(self, expr):
        r'''Is true when `expr` is a sieve with period greater than 
        that of this sieve.
        
        Is true when `expr` is a sieve with period equal to that of
        this sieve and with residue greater than that of this residue
        class.
        
        Otherwise false.

        ..  container:: example

            **Example 1.** With equal period and equal offset::

                >>> sieve_1 = sievetools.Sieve(6, 0)

            ::

                >>> sieve_1 == sieve_1
                True
                >>> sieve_1 != sieve_1
                False
                >>> sieve_1 < sieve_1
                False
                >>> sieve_1 <= sieve_1
                True
                >>> sieve_1 > sieve_1
                False
                >>> sieve_1 >= sieve_1
                True

        ..  container:: example

            **Example 2.** With equal period but unequal offset::

                >>> sieve_1 = sievetools.Sieve(6, 0)
                >>> sieve_2 = sievetools.Sieve(6, 1)

            ::

                >>> sieve_1 == sieve_2
                False
                >>> sieve_1 != sieve_2
                True
                >>> sieve_1 < sieve_2
                True
                >>> sieve_1 <= sieve_2
                True
                >>> sieve_1 > sieve_2
                False
                >>> sieve_1 >= sieve_2
                False

            ::

                >>> sieve_2 == sieve_1
                False
                >>> sieve_2 != sieve_1
                True
                >>> sieve_2 < sieve_1
                False
                >>> sieve_2 <= sieve_1
                False
                >>> sieve_2 > sieve_1
                True
                >>> sieve_2 >= sieve_1
                True

        ..  container:: example

            **Example 3.** With unequal period:

                >>> sieve_1 = sievetools.Sieve(6, 0)
                >>> sieve_2 = sievetools.Sieve(7, 0)

            ::

                >>> sieve_1 == sieve_2
                False
                >>> sieve_1 != sieve_2
                True
                >>> sieve_1 < sieve_2
                True
                >>> sieve_1 <= sieve_2
                True
                >>> sieve_1 > sieve_2
                False
                >>> sieve_1 >= sieve_2
                False

            ::

                >>> sieve_2 == sieve_1
                False
                >>> sieve_2 != sieve_1
                True
                >>> sieve_2 < sieve_1
                False
                >>> sieve_2 <= sieve_1
                False
                >>> sieve_2 > sieve_1
                True
                >>> sieve_2 >= sieve_1
                True

        Returns true or false.
        '''
        if not isinstance(expr, type(self)):
            return False
        if self.period == expr.period:
            return self.offset < expr.offset
        return self.period < expr.period

    def __ne__(self, expr):
        r'''Is true when `expr` is not equal to this sieve. Otherwise
        false.

        Returns true or false.
        '''
        return not self == expr

    ### PRIVATE PROPERTIES ###

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        return systemtools.StorageFormatSpecification(
            self,
            is_indented=False,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def boolean_train(self):
        r'''Gets boolean train.

        ..  container:: example

            **Example 1.** Gets boolean train:

                ::

                    >>> sieve = sievetools.Sieve(3, 0)
                    >>> sieve.boolean_train
                    [1, 0, 0]

        ..  container:: example

            **Example 2.** Gets boolean train:

                ::

                    >>> sieve = sievetools.Sieve(3, 1)
                    >>> sieve.boolean_train
                    [0, 1, 0]

        Returns list of ones and zeroes.
        '''
        result = []
        for i in range(0, self.period):
            if i % self.period == self.offset:
                result.append(1)
            else:
                result.append(0)
        return result

    @property
    def congruent_bases(self):
        r'''Gets congruent bases.
        
        ..  container:: example

            **Example 1.** Without offset:

                ::

                    >>> sieve = sievetools.Sieve(3, 0)
                    >>> sieve.congruent_bases
                    [0]

        ..  container:: example

            **Example 2.** With offset:

                ::

                    >>> sieve = sievetools.Sieve(3, 1)
                    >>> sieve.congruent_bases
                    [1]

        Returns list of nonnegative integers.
        '''
        return self._congruent_bases

    @property
    def offset(self):
        r'''Gets offset of sieve.

        ..  container:: example

            **Example 1.** Without offset:

                ::

                    >>> sieve = sievetools.Sieve(3, 0)
                    >>> sieve.offset
                    0

        ..  container:: example

            **Example 2.** With offset:

                ::

                    >>> sieve = sievetools.Sieve(3, 1)
                    >>> sieve.offset
                    1

        Returns nonnegative integer.
        '''
        return self._offset

    @property
    def period(self):
        r'''Gets period of sieve.

        ..  container:: example

            **Example 1.** Period equal to 3:

                ::

                    >>> sieve = sievetools.Sieve(3, 0)
                    >>> sieve.period
                    3

        ..  container:: example

            **Example 2.** Period equal to 99:

                ::

                    >>> sieve = sievetools.Sieve(99, 0)
                    >>> sieve.period
                    99

        Returns positive integer.
        '''
        return self._period