# -*- coding: utf-8 -*-
import functools
from abjad.tools.sievetools.BaseResidueClass import BaseResidueClass


@functools.total_ordering
class ResidueClass(BaseResidueClass):
    r'''Residue class.

    A residue class is a simple periodic sequence.

    Residue classes can be combined with logical operators.

    Residue classes form the basis of Xenakis sieves.

    ..  container:: example

        **Example 1.** A residue class:

        ::

            >>> residue_class = sievetools.ResidueClass(2, 0)

        ::

            >>> residue_class
            ResidueClass(period=2, offset=0)

        ::

            >>> print(format(residue_class))
            sievetools.ResidueClass(period=2, offset=0, )

    ..  container:: example

        **Example 2.** Sieve from the opening of Xenakis's *Psappha* for solo 
        percussion:

        ::

            >>> RC = sievetools.ResidueClass

        ::

            >>> sieve_1 = (RC(8, 0) | RC(8, 1) | RC(8, 7)) & (RC(5, 1) | RC(5, 3))
            >>> sieve_2 = (RC(8, 0) | RC(8, 1) | RC(8, 2)) & RC(5, 0)
            >>> sieve_3 = RC(8, 3)
            >>> sieve_4 = RC(8, 4)
            >>> sieve_5 = (RC(8, 5) | RC(8, 6)) & (RC(5, 2) | RC(5, 3) | RC(5, 4))
            >>> sieve_6 = (RC(8, 1) & RC(5, 2))
            >>> sieve_7 = (RC(8, 6) & RC(5, 1))

        ::

            >>> sieve = sieve_1 | sieve_2 | sieve_3 | sieve_4 | sieve_5 | sieve_6 | sieve_7

        ::

            >>> sieve.get_congruent_bases()
                [0, 1, 3, 4, 6, 8, 10, 11, 12, 13, 14, 16, 17, 19, 20, 22,
                23, 25, 27, 28, 29, 31, 33, 35, 36, 37, 38, 40]

        ::

            >>> sieve.get_boolean_train()
                [1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1,
                1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0]


    '''

    ### CLASS VARIABLES ###

    __slots__ = (
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

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        r'''Is true when `expr` is a residue class with module and residue
        equal to those of this residue class. Otherwise false.

        Returns true or false.
        '''
        if not isinstance(expr, type(self)):
            return False
        if self.period == expr.period:
            if self.offset == expr.offset:
                return True

    def __hash__(self):
        r'''Hashes residue class.

        Required to be explicitly re-defined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(ResidueClass, self).__hash__()

    def __lt__(self, expr):
        r'''Is true when `expr` is a residue class with module greater than 
        that of this residue class. Also true when `expr` is a residue class
        with period equal to that of this residue class and with residue 
        greater than that of this residue class. Otherwise false.

        Returns true or false.
        '''
        if not isinstance(expr, type(self)):
            return False
        if self.period == expr.period:
            return self.offset < expr.offset
        return self.period < expr.period

    def __ne__(self, expr):
        r'''Is true when `expr` is not equal to this residue class. Otherwise
        false.

        Return boolean.
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
    def offset(self):
        r'''Gets offset of residue class.

        Returns nonnegative integer.
        '''
        return self._offset

    @property
    def period(self):
        r'''Gets period of residue class.

        Returns positive integer.
        '''
        return self._period

    ### PUBLIC METHODS ###

    def get_boolean_train(self, start=0, stop=None):
        r'''Gets boolean train.

        ..  container:: example

            **Example 1.** Gets first eight values of boolean train:

                ::

                    >>> residue_class = RC(2, 0)
                    >>> residue_class.get_boolean_train(stop=8)
                    [1, 0, 1, 0, 1, 0, 1, 0]

        ..  container:: example

            **Example 2.** Gets first eight values of boolean train:

                ::

                    >>> residue_class = RC(3, 0)
                    >>> residue_class.get_boolean_train(stop=8)
                    [1, 0, 0, 1, 0, 0, 1, 0]

        Boolean train is defined equal to a list of ones and zeros: ones map to
        integers included in the residue class while zeroes map to integers not
        included in the residue class.

        Sets `stop` to period of residue class when `stop` is none.

        Returns list.
        '''
        stop = stop or self.period
        result = []
        for i in range(start, stop):
            if i % self.period == self.offset:
                result.append(1)
            else:
                result.append(0)
        return result

    def get_congruent_bases(self, start=0, stop=None):
        r'''Gets congruent bases.
        
        ..  container:: example

            **Example 1.** Gets congruent bases:

                ::

                    >>> residue_class = RC(2, 0)
                    >>> residue_class.get_congruent_bases(stop=8)
                    [0, 2, 4, 6, 8]

        ..  container:: example

            **Example 2.** Gets congruent bases:

                ::

                    >>> residue_class = RC(3, 0)
                    >>> residue_class.get_congruent_bases(stop=8)
                    [0, 3, 6]

        Sets `stop` to period of residue class when `stop` is none.

        Returns list.
        '''
        stop = stop or self.period
        result = []
        for i in range(start, stop + 1):
            if i % self.period == self.offset:
                result.append(i)
        return result