# -*- coding: utf-8 -*-
import functools
from abjad.tools.sievetools.BaseResidueClass import BaseResidueClass


@functools.total_ordering
class ResidueClass(BaseResidueClass):
    r'''Residue class.

    ..  container:: example

        **Example 1.** Residue class without offset:

        ::

            >>> residue_class = sievetools.ResidueClass(3, 0)
            >>> residue_class
            ResidueClass(period=3, offset=0)

    ..  container:: example

        **Example 2.** Residue class with offset:

        ::

            >>> residue_class = sievetools.ResidueClass(3, 1)
            >>> residue_class
            ResidueClass(period=3, offset=1)

    A residue class is a simple periodic sequence.

    Residue classes can be combined with logical operators.

    Residue classes form the basis of Xenakis sieves.
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
        r'''Is true when `expr` is a residue class with period and residue
        equal to those of this residue class. Otherwise false.

        ..  container:: example

            **Example 1.** With equal period:

                >>> residue_class_1 = sievetools.ResidueClass(6, 0)
                >>> residue_class_2 = sievetools.ResidueClass(6, 1)

            ::

                >>> residue_class_1 == residue_class_1
                True

            ::

                >>> residue_class_1 == residue_class_2
                False

        ..  container:: example

            **Example 2.** With unequal period:

                >>> residue_class_1 = sievetools.ResidueClass(6, 0)
                >>> residue_class_2 = sievetools.ResidueClass(7, 0)

            ::

                >>> residue_class_1 == residue_class_1
                True

            ::

                >>> residue_class_1 == residue_class_2
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
        r'''Hashes residue class.

        Required to be explicitly re-defined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(ResidueClass, self).__hash__()

    def __lt__(self, expr):
        r'''Is true when `expr` is a residue class with period greater than 
        that of this residue class.
        
        Is true when `expr` is a residue class with period equal to that of
        this residue class and with residue greater than that of this residue
        class.
        
        Otherwise false.

        ..  container:: example

            **Example 1.** With equal period and equal offset::

                >>> residue_class_1 = sievetools.ResidueClass(6, 0)

            ::

                >>> residue_class_1 == residue_class_1
                True
                >>> residue_class_1 != residue_class_1
                False
                >>> residue_class_1 < residue_class_1
                False
                >>> residue_class_1 <= residue_class_1
                True
                >>> residue_class_1 > residue_class_1
                False
                >>> residue_class_1 >= residue_class_1
                True

        ..  container:: example

            **Example 2.** With equal period but unequal offset::

                >>> residue_class_1 = sievetools.ResidueClass(6, 0)
                >>> residue_class_2 = sievetools.ResidueClass(6, 1)

            ::

                >>> residue_class_1 == residue_class_2
                False
                >>> residue_class_1 != residue_class_2
                True
                >>> residue_class_1 < residue_class_2
                True
                >>> residue_class_1 <= residue_class_2
                True
                >>> residue_class_1 > residue_class_2
                False
                >>> residue_class_1 >= residue_class_2
                False

            ::

                >>> residue_class_2 == residue_class_1
                False
                >>> residue_class_2 != residue_class_1
                True
                >>> residue_class_2 < residue_class_1
                False
                >>> residue_class_2 <= residue_class_1
                False
                >>> residue_class_2 > residue_class_1
                True
                >>> residue_class_2 >= residue_class_1
                True

        ..  container:: example

            **Example 3.** With unequal period:

                >>> residue_class_1 = sievetools.ResidueClass(6, 0)
                >>> residue_class_2 = sievetools.ResidueClass(7, 0)

            ::

                >>> residue_class_1 == residue_class_2
                False
                >>> residue_class_1 != residue_class_2
                True
                >>> residue_class_1 < residue_class_2
                True
                >>> residue_class_1 <= residue_class_2
                True
                >>> residue_class_1 > residue_class_2
                False
                >>> residue_class_1 >= residue_class_2
                False

            ::

                >>> residue_class_2 == residue_class_1
                False
                >>> residue_class_2 != residue_class_1
                True
                >>> residue_class_2 < residue_class_1
                False
                >>> residue_class_2 <= residue_class_1
                False
                >>> residue_class_2 > residue_class_1
                True
                >>> residue_class_2 >= residue_class_1
                True

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

                    >>> residue_class = sievetools.ResidueClass(3, 0)
                    >>> residue_class.boolean_train
                    [1, 0, 0]

        ..  container:: example

            **Example 2.** Gets boolean train:

                ::

                    >>> residue_class = sievetools.ResidueClass(3, 1)
                    >>> residue_class.boolean_train
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

                    >>> residue_class = sievetools.ResidueClass(3, 0)
                    >>> residue_class.congruent_bases
                    [0]

        ..  container:: example

            **Example 2.** With offset:

                ::

                    >>> residue_class = sievetools.ResidueClass(3, 1)
                    >>> residue_class.congruent_bases
                    [1]

        Returns list of nonnegative integers.
        '''
        return self._congruent_bases

    @property
    def offset(self):
        r'''Gets offset of residue class.

        ..  container:: example

            **Example 1.** Without offset

                ::

                    >>> residue_class = sievetools.ResidueClass(3, 0)
                    >>> residue_class.offset
                    0

        ..  container:: example

            **Example 2.** With offset

                ::

                    >>> residue_class = sievetools.ResidueClass(3, 1)
                    >>> residue_class.offset
                    1

        Returns nonnegative integer.
        '''
        return self._offset

    @property
    def period(self):
        r'''Gets period of residue class.

        ..  container:: example

            **Example 1.** Period equal to 3:

                ::

                    >>> residue_class = sievetools.ResidueClass(3, 0)
                    >>> residue_class.period
                    3

        ..  container:: example

            **Example 2.** Period equal to 99:

                ::

                    >>> residue_class = sievetools.ResidueClass(99, 0)
                    >>> residue_class.period
                    99

        Returns positive integer.
        '''
        return self._period