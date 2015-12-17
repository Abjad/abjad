# -*- coding: utf-8 -*-
import operator
from abjad.tools import mathtools
from abjad.tools.abctools.AbjadObject import AbjadObject


class CompoundSieve(AbjadObject):
    r'''Compound sieve.

    ..  container:: example

        **Example 1.** Compound sieve from the opening of Xenakis's *Psappha*
        for solo percussion:

        ::

            >>> Sieve = sievetools.Sieve

        ::

            >>> sieve_1 = (Sieve(8, 0) | Sieve(8, 1) | Sieve(8, 7)) 
            >>> sieve_1 = sieve_1 & (Sieve(5, 1) | Sieve(5, 3))
            >>> sieve_2 = (Sieve(8, 0) | Sieve(8, 1) | Sieve(8, 2)) 
            >>> sieve_2 = sieve_2 & Sieve(5, 0)
            >>> sieve_3 = Sieve(8, 3)
            >>> sieve_4 = Sieve(8, 4)
            >>> sieve_5 = (Sieve(8, 5) | Sieve(8, 6)) 
            >>> sieve_5 = sieve_5 & (Sieve(5, 2) | Sieve(5, 3) | Sieve(5, 4))
            >>> sieve_6 = (Sieve(8, 1) & Sieve(5, 2))
            >>> sieve_7 = (Sieve(8, 6) & Sieve(5, 1))

        ::

            >>> sieve = (
            ...     sieve_1 | sieve_2 | sieve_3 | 
            ...     sieve_4 | sieve_5 | sieve_6 | sieve_7
            ...     )

        ::

            >>> sieve.congruent_bases
                [0, 1, 3, 4, 6, 8, 10, 11, 12, 13, 14, 16, 17, 19, 20, 22,
                23, 25, 27, 28, 29, 31, 33, 35, 36, 37, 38]

        ::

            >>> sieve.boolean_train
                [1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1,
                1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0]

        ::

            >>> print(format(sieve))
            sievetools.CompoundSieve(
                sieves=[
                    sievetools.CompoundSieve(
                        sieves=[
                            sievetools.CompoundSieve(
                                sieves=[
                                    sievetools.Sieve(period=8, offset=0, ),
                                    sievetools.Sieve(period=8, offset=1, ),
                                    sievetools.Sieve(period=8, offset=7, ),
                                    ],
                                logical_operator='or',
                                ),
                            sievetools.CompoundSieve(
                                sieves=[
                                    sievetools.Sieve(period=5, offset=1, ),
                                    sievetools.Sieve(period=5, offset=3, ),
                                    ],
                                logical_operator='or',
                                ),
                            ],
                        logical_operator='and',
                        ),
                    sievetools.CompoundSieve(
                        sieves=[
                            sievetools.CompoundSieve(
                                sieves=[
                                    sievetools.Sieve(period=8, offset=0, ),
                                    sievetools.Sieve(period=8, offset=1, ),
                                    sievetools.Sieve(period=8, offset=2, ),
                                    ],
                                logical_operator='or',
                                ),
                            sievetools.Sieve(period=5, offset=0, ),
                            ],
                        logical_operator='and',
                        ),
                    sievetools.Sieve(period=8, offset=3, ),
                    sievetools.Sieve(period=8, offset=4, ),
                    sievetools.CompoundSieve(
                        sieves=[
                            sievetools.CompoundSieve(
                                sieves=[
                                    sievetools.Sieve(period=8, offset=5, ),
                                    sievetools.Sieve(period=8, offset=6, ),
                                    ],
                                logical_operator='or',
                                ),
                            sievetools.CompoundSieve(
                                sieves=[
                                    sievetools.Sieve(period=5, offset=2, ),
                                    sievetools.Sieve(period=5, offset=3, ),
                                    sievetools.Sieve(period=5, offset=4, ),
                                    ],
                                logical_operator='or',
                                ),
                            ],
                        logical_operator='and',
                        ),
                    sievetools.CompoundSieve(
                        sieves=[
                            sievetools.Sieve(period=5, offset=2, ),
                            sievetools.Sieve(period=8, offset=1, ),
                            ],
                        logical_operator='and',
                        ),
                    sievetools.CompoundSieve(
                        sieves=[
                            sievetools.Sieve(period=5, offset=1, ),
                            sievetools.Sieve(period=8, offset=6, ),
                            ],
                        logical_operator='and',
                        ),
                    ],
                logical_operator='or',
                )

    Due to Xenakis.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_boolean_train',
        '_congruent_bases',
        '_logical_operator',
        '_period',
        '_sieves',
        )

    ### INITIALIZER ###

    def __init__(self, sieves=None, logical_operator='or'):
        from abjad.tools import sievetools
        sieves = sieves or []
        self._sieves = sieves[:]
        self._logical_operator = logical_operator
        self._sort_sieves()
        periods = []
        for sieve in self.sieves:
            periods.append(sieve.period)
        if periods:
            period = mathtools.least_common_multiple(*periods)
        else:
            period = 1
        self._period = period
        if self.logical_operator == 'or':
            congruent_bases = self._get_congruent_bases(operator.ior)
        elif self.logical_operator == 'xor':
            congruent_bases = self._get_congruent_bases(operator.ixor)
        elif self.logical_operator == 'and':
            congruent_bases = self._get_congruent_bases(operator.iand)
        self._congruent_bases = congruent_bases
        boolean_train = []
        congruent_bases = self.congruent_bases
        for i in range(0, self.period):
            if i % self.period in congruent_bases:
                boolean_train.append(1)
            else:
                boolean_train.append(0)
        self._boolean_train = boolean_train

    ### SPECIAL METHODS ###

    def __and__(self, arg):
        r'''Logical AND of compound sieve and `arg`.

        Returns new compound sieve.
        '''
        return self._operate(arg, 'and')

    def __or__(self, arg):
        r'''Logical OR of compound sieve and `arg`.

        Returns new compound sieve.
        '''
        return self._operate(arg, 'or')

    def __xor__(self, arg):
        r'''Logical XOR of compound sieve and `arg`.

        Returns new compound sieve.
        '''
        return self._operate(arg, 'xor')

    ### PRIVATE METHODS ###

    @staticmethod
    def _boolean_pattern_to_compound_sieve(boolean_pattern):
        from abjad.tools import sievetools
        if isinstance(boolean_pattern, CompoundSieve):
            return CompoundSieve(boolean_pattern)
        period = boolean_pattern.period
        indices = boolean_pattern.indices or []
        offset = 0
        sieves = []
        for index in indices:
            adjusted_index = (index + offset) % period
            sieve = sievetools.Sieve(period, adjusted_index)
            sieves.append(sieve)
        sieves.sort(key=lambda x: x.offset)
        sieve = CompoundSieve(sieves, logical_operator='or')
        return sieve

    def _get_congruent_bases(self, logical_operator):
        if logical_operator is operator.iand:
            result = set(range(0, self.period))
        else:
            result = set()
        for sieve in self.sieves:
            bases_ = set()
            for i in range(0, self.period):
                congruent_bases = sieve.congruent_bases
                if i % sieve.period in congruent_bases:
                    bases_.add(i)
            logical_operator(result, bases_)
        return sorted(result)

    def _operate(self, arg, operator):
        from abjad.tools import sievetools
        if (isinstance(self, sievetools.CompoundSieve) and 
            self.logical_operator == operator):
            argument_a = self.sieves
        else:
            argument_a = [self]
        if (isinstance(arg, sievetools.CompoundSieve) and 
            arg.logical_operator == operator):
            argument_b = arg.sieves
        else:
            argument_b = [arg]
        sieve = sievetools.CompoundSieve(argument_a + argument_b, operator)
        return sieve

    def _sort_sieves(self):
        from abjad.tools import sievetools
        if all(
            isinstance(sieve, sievetools.Sieve) 
            for sieve in self.sieves
            ):
            self.sieves.sort()

    ### PUBLIC PROPERTIES ###

    @property
    def boolean_train(self):
        r'''Gets boolean train.
        
        ..  container::

            **Example 1.** With period equal to 6:

            ::

                >>> sieve_1 = sievetools.Sieve(2, 0)
                >>> sieve_2 = sievetools.Sieve(3, 0)
                >>> sieve = sieve_1 | sieve_2
                >>> sieve.boolean_train
                [1, 0, 1, 1, 1, 0]

        ..  container::

            **Example 2.** With period equal to 10:

            ::

                >>> sieve_1 = sievetools.Sieve(2, 0)
                >>> sieve_2 = sievetools.Sieve(5, 0)
                >>> sieve = sieve_1 | sieve_2
                >>> sieve.boolean_train
                [1, 0, 1, 0, 1, 1, 1, 0, 1, 0]

        Returns list of ones and zeroes.
        '''
        return self._boolean_train

    @property
    def congruent_bases(self):
        r'''Gets congruent bases.
        
        ..  container::

            **Example 1.** With period equal to 6:

            ::

                >>> sieve_1 = sievetools.Sieve(2, 0)
                >>> sieve_2 = sievetools.Sieve(3, 0)
                >>> sieve = sieve_1 | sieve_2
                >>> sieve.congruent_bases
                [0, 2, 3, 4]
                
        ..  container::

            **Example 2.** With period equal to 10:

            ::

                >>> sieve_1 = sievetools.Sieve(2, 0)
                >>> sieve_2 = sievetools.Sieve(5, 0)
                >>> sieve = sieve_1 | sieve_2
                >>> sieve.congruent_bases
                [0, 2, 4, 5, 6, 8]

        Returns list.
        '''
        return self._congruent_bases

    @property
    def logical_operator(self):
        r'''Gets logical operator of sieve.

        ..  container::

            **Example 1.** With period equal to 6:

            ::

                >>> sieve_1 = sievetools.Sieve(2, 0)
                >>> sieve_2 = sievetools.Sieve(3, 0)
                >>> sieve = sieve_1 | sieve_2
                >>> sieve.logical_operator
                'or'

        ..  container::

            **Example 2.** With period equal to 10:

            ::

                >>> sieve_1 = sievetools.Sieve(2, 0)
                >>> sieve_2 = sievetools.Sieve(5, 0)
                >>> sieve = sieve_1 | sieve_2
                >>> sieve.logical_operator
                'or'

        Returns string.
        '''
        return self._logical_operator

    @property
    def period(self):
        r'''Gets period of sieve.

        ..  container::

            **Example 1.** With period equal to 6:

            ::

                >>> sieve_1 = sievetools.Sieve(2, 0)
                >>> sieve_2 = sievetools.Sieve(3, 0)
                >>> sieve = sieve_1 | sieve_2
                >>> sieve.period
                6
                
        ..  container::

            **Example 2.** With period equal to 10:

            ::

                >>> sieve_1 = sievetools.Sieve(2, 0)
                >>> sieve_2 = sievetools.Sieve(5, 0)
                >>> sieve = sieve_1 | sieve_2
                >>> sieve.period
                10

        Returns positive integer.
        '''
        return self._period

    @property
    def sieves(self):
        r'''Gets sieves of compound sieve.

        ..  container::

            **Example 1.** With period equal to 6:

            ::

                >>> sieve_1 = sievetools.Sieve(2, 0)
                >>> sieve_2 = sievetools.Sieve(3, 0)
                >>> sieve = sieve_1 | sieve_2
                >>> for sieve in sieve.sieves:
                ...     sieve
                Sieve(period=2, offset=0)
                Sieve(period=3, offset=0)

        ..  container::

            **Example 2.** With period equal to 10:

            ::

                >>> sieve_1 = sievetools.Sieve(2, 0)
                >>> sieve_2 = sievetools.Sieve(5, 0)
                >>> sieve = sieve_1 | sieve_2
                >>> for sieve in sieve.sieves:
                ...     sieve
                Sieve(period=2, offset=0)
                Sieve(period=5, offset=0)

        Returns list.
        '''
        return self._sieves

    ### PUBLIC METHODS ###

    @staticmethod
    def from_boolean_patterns(boolean_patterns):
        '''Initializes sieve from `boolean_patterns`.

        ..  container:: example

            **Example 1.** From two boolean patterns:

            ::

                >>> pattern_1 = rhythmmakertools.BooleanPattern(
                ...     indices=[0, 4, 5],
                ...     period=6,
                ...     )
                >>> pattern_2 = rhythmmakertools.BooleanPattern(
                ...     indices=[6, 7, 8],
                ...     period=10,
                ...     )
                >>> patterns = [pattern_1, pattern_2]

            ::

                >>> sieve = sievetools.CompoundSieve.from_boolean_patterns(patterns)
                >>> print(format(sieve))
                sievetools.CompoundSieve(
                    sieves=[
                        sievetools.Sieve(period=6, offset=0, ),
                        sievetools.Sieve(period=6, offset=4, ),
                        sievetools.Sieve(period=6, offset=5, ),
                        sievetools.Sieve(period=10, offset=6, ),
                        sievetools.Sieve(period=10, offset=7, ),
                        sievetools.Sieve(period=10, offset=8, ),
                        ],
                    logical_operator='or',
                    )

            ::

                >>> sieve.congruent_bases
                [0, 4, 5, 6, 7, 8, 10, 11, 12, 16, 17, 18, 22, 23, 24, 26, 27, 28, 29]

        '''
        sieves = []
        for boolean_pattern in boolean_patterns:
            compound_sieve = CompoundSieve._boolean_pattern_to_compound_sieve(
                boolean_pattern)
            sieves.append(compound_sieve)
        if sieves:
            current_sieve = sieves[0]
            for sieve in sieves[1:]:
                current_sieve = current_sieve | sieve
        else:
            current_sieve = CompoundSieve([])
        return current_sieve