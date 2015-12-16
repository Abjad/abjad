# -*- coding: utf-8 -*-
import operator
from abjad.tools import mathtools
from abjad.tools.sievetools.BaseResidueClass import BaseResidueClass


class CompoundSieve(BaseResidueClass):
    r'''CompoundSieve.

    ..  container:: example

        **Example 1.** CompoundSieve from the opening of Xenakis's *Psappha* for solo 
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
                residue_classes=[
                    sievetools.CompoundSieve(
                        residue_classes=[
                            sievetools.CompoundSieve(
                                residue_classes=[
                                    sievetools.ResidueClass(period=8, offset=0, ),
                                    sievetools.ResidueClass(period=8, offset=1, ),
                                    sievetools.ResidueClass(period=8, offset=7, ),
                                    ],
                                logical_operator='or',
                                ),
                            sievetools.CompoundSieve(
                                residue_classes=[
                                    sievetools.ResidueClass(period=5, offset=1, ),
                                    sievetools.ResidueClass(period=5, offset=3, ),
                                    ],
                                logical_operator='or',
                                ),
                            ],
                        logical_operator='and',
                        ),
                    sievetools.CompoundSieve(
                        residue_classes=[
                            sievetools.CompoundSieve(
                                residue_classes=[
                                    sievetools.ResidueClass(period=8, offset=0, ),
                                    sievetools.ResidueClass(period=8, offset=1, ),
                                    sievetools.ResidueClass(period=8, offset=2, ),
                                    ],
                                logical_operator='or',
                                ),
                            sievetools.ResidueClass(period=5, offset=0, ),
                            ],
                        logical_operator='and',
                        ),
                    sievetools.ResidueClass(period=8, offset=3, ),
                    sievetools.ResidueClass(period=8, offset=4, ),
                    sievetools.CompoundSieve(
                        residue_classes=[
                            sievetools.CompoundSieve(
                                residue_classes=[
                                    sievetools.ResidueClass(period=8, offset=5, ),
                                    sievetools.ResidueClass(period=8, offset=6, ),
                                    ],
                                logical_operator='or',
                                ),
                            sievetools.CompoundSieve(
                                residue_classes=[
                                    sievetools.ResidueClass(period=5, offset=2, ),
                                    sievetools.ResidueClass(period=5, offset=3, ),
                                    sievetools.ResidueClass(period=5, offset=4, ),
                                    ],
                                logical_operator='or',
                                ),
                            ],
                        logical_operator='and',
                        ),
                    sievetools.CompoundSieve(
                        residue_classes=[
                            sievetools.ResidueClass(period=5, offset=2, ),
                            sievetools.ResidueClass(period=8, offset=1, ),
                            ],
                        logical_operator='and',
                        ),
                    sievetools.CompoundSieve(
                        residue_classes=[
                            sievetools.ResidueClass(period=5, offset=1, ),
                            sievetools.ResidueClass(period=8, offset=6, ),
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
        '_residue_classes',
        )

    ### INITIALIZER ###

    def __init__(self, residue_classes=None, logical_operator='or'):
        from abjad.tools import sievetools
        residue_classes = residue_classes or []
        self._residue_classes = residue_classes[:]
        self._logical_operator = logical_operator
        self._sort_sieves()
        periods = []
        for residue_class in self.residue_classes:
            periods.append(residue_class.period)
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

    ### PRIVATE METHODS ###

    @staticmethod
    def _boolean_pattern_to_sieve(boolean_pattern):
        from abjad.tools import sievetools
        if isinstance(boolean_pattern, CompoundSieve):
            return CompoundSieve(boolean_pattern)
        period = boolean_pattern.period
        residues = boolean_pattern.indices or []
        offset = 0
        residue_classes = []
        for residue in residues:
            adjusted_residue = (residue + offset) % period
            residue_class = sievetools.ResidueClass(period, adjusted_residue)
            residue_classes.append(residue_class)
        residue_classes.sort(key=lambda x: x.offset)
        sieve = CompoundSieve(residue_classes, logical_operator='or')
        return sieve

    def _get_congruent_bases(self, logical_operator):
        if logical_operator is operator.iand:
            result = set(range(0, self.period))
        else:
            result = set()
        for residue_class in self.residue_classes:
            bases_ = set()
            for i in range(0, self.period):
                congruent_bases = residue_class.congruent_bases
                if i % residue_class.period in congruent_bases:
                    bases_.add(i)
            logical_operator(result, bases_)
        return sorted(result)

    def _sort_sieves(self):
        from abjad.tools import sievetools
        if all(
            isinstance(residue_class, sievetools.ResidueClass) 
            for residue_class in self.residue_classes
            ):
            self.residue_classes.sort()

    ### PUBLIC PROPERTIES ###

    @property
    def boolean_train(self):
        r'''Gets boolean train.
        
        ..  container::

            **Example 1.** With period equal to 6:

            ::

                >>> residue_class_1 = sievetools.ResidueClass(2, 0)
                >>> residue_class_2 = sievetools.ResidueClass(3, 0)
                >>> sieve = residue_class_1 | residue_class_2
                >>> sieve.boolean_train
                [1, 0, 1, 1, 1, 0]

        ..  container::

            **Example 2.** With period equal to 10:

            ::

                >>> residue_class_1 = sievetools.ResidueClass(2, 0)
                >>> residue_class_2 = sievetools.ResidueClass(5, 0)
                >>> sieve = residue_class_1 | residue_class_2
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

                >>> residue_class_1 = sievetools.ResidueClass(2, 0)
                >>> residue_class_2 = sievetools.ResidueClass(3, 0)
                >>> sieve = residue_class_1 | residue_class_2
                >>> sieve.congruent_bases
                [0, 2, 3, 4]
                
        ..  container::

            **Example 2.** With period equal to 10:

            ::

                >>> residue_class_1 = sievetools.ResidueClass(2, 0)
                >>> residue_class_2 = sievetools.ResidueClass(5, 0)
                >>> sieve = residue_class_1 | residue_class_2
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

                >>> residue_class_1 = sievetools.ResidueClass(2, 0)
                >>> residue_class_2 = sievetools.ResidueClass(3, 0)
                >>> sieve = residue_class_1 | residue_class_2
                >>> sieve.logical_operator
                'or'

        ..  container::

            **Example 2.** With period equal to 10:

            ::

                >>> residue_class_1 = sievetools.ResidueClass(2, 0)
                >>> residue_class_2 = sievetools.ResidueClass(5, 0)
                >>> sieve = residue_class_1 | residue_class_2
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

                >>> residue_class_1 = sievetools.ResidueClass(2, 0)
                >>> residue_class_2 = sievetools.ResidueClass(3, 0)
                >>> sieve = residue_class_1 | residue_class_2
                >>> sieve.period
                6
                
        ..  container::

            **Example 2.** With period equal to 10:

            ::

                >>> residue_class_1 = sievetools.ResidueClass(2, 0)
                >>> residue_class_2 = sievetools.ResidueClass(5, 0)
                >>> sieve = residue_class_1 | residue_class_2
                >>> sieve.period
                10

        Returns positive integer.
        '''
        return self._period

    @property
    def residue_classes(self):
        r'''Gets residue classes of sieve.

        ..  container::

            **Example 1.** With period equal to 6:

            ::

                >>> residue_class_1 = sievetools.ResidueClass(2, 0)
                >>> residue_class_2 = sievetools.ResidueClass(3, 0)
                >>> sieve = residue_class_1 | residue_class_2
                >>> for residue_class in sieve.residue_classes:
                ...     residue_class
                ResidueClass(period=2, offset=0)
                ResidueClass(period=3, offset=0)

        ..  container::

            **Example 2.** With period equal to 10:

            ::

                >>> residue_class_1 = sievetools.ResidueClass(2, 0)
                >>> residue_class_2 = sievetools.ResidueClass(5, 0)
                >>> sieve = residue_class_1 | residue_class_2
                >>> for residue_class in sieve.residue_classes:
                ...     residue_class
                ResidueClass(period=2, offset=0)
                ResidueClass(period=5, offset=0)

        Returns list.
        '''
        return self._residue_classes

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
                    residue_classes=[
                        sievetools.ResidueClass(period=6, offset=0, ),
                        sievetools.ResidueClass(period=6, offset=4, ),
                        sievetools.ResidueClass(period=6, offset=5, ),
                        sievetools.ResidueClass(period=10, offset=6, ),
                        sievetools.ResidueClass(period=10, offset=7, ),
                        sievetools.ResidueClass(period=10, offset=8, ),
                        ],
                    logical_operator='or',
                    )

            ::

                >>> sieve.congruent_bases
                [0, 4, 5, 6, 7, 8, 10, 11, 12, 16, 17, 18, 22, 23, 24, 26, 27, 28, 29]

        '''
        sieves = []
        for boolean_pattern in boolean_patterns:
            sieve = CompoundSieve._boolean_pattern_to_sieve(boolean_pattern)
            sieves.append(sieve)
        if sieves:
            current_sieve = sieves[0]
            for sieve in sieves[1:]:
                current_sieve = current_sieve | sieve
        else:
            current_sieve = CompoundSieve([])
        return current_sieve