# -*- coding: utf-8 -*-
import operator
from abjad.tools import mathtools
from abjad.tools.sievetools.BaseResidueClass import BaseResidueClass


class Sieve(BaseResidueClass):
    r'''Sieve.

    Due to Xenakis.

    ..  container:: example

        **Example 1.** Sieve from the opening of Xenakis's *Psappha* for solo 
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

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_logical_operator',
        '_residue_classes',
        )

    logical_operator_dictionary = {
        'and': '&',
        'or': '|',
        'xor': '^',
        }

    ### INITIALIZER ###

    def __init__(self, residue_classes=None, logical_operator='or'):
        from abjad.tools import sievetools
        if isinstance(residue_classes, type(self)):
            self._residue_classes = residue_classes.residue_classes[:]
            self._logical_operator = residue_classes.logical_operator
        elif residue_classes is None:
            residue_classes = [sievetools.ResidueClass()]
            self._residue_classes = residue_classes
            self._logical_operator = logical_operator
        else:
            self._residue_classes = residue_classes[:]
            self._logical_operator = logical_operator
        self._sort_residue_classes()

    ### PRIVATE METHODS ###

    @staticmethod
    def _cycle_token_to_sieve(cycle_token):
        from abjad.tools import sievetools
        if isinstance(cycle_token, Sieve):
            return Sieve(cycle_token)
        period = cycle_token[0]
        residues = cycle_token[1]
        try:
            offset = cycle_token[2]
        except IndexError:
            offset = 0
        residue_classes = []
        for residue in residues:
            adjusted_residue = (residue + offset) % period
            residue_class = sievetools.ResidueClass(period, adjusted_residue)
            residue_classes.append(residue_class)
        residue_classes.sort(key=lambda x: x.offset)
        sieve = Sieve(residue_classes, logical_operator='or')
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

    def _sort_residue_classes(self):
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

            **Example 1.** Gets boolean train:

            ::

                >>> residue_class_1 = sievetools.ResidueClass(2, 0)
                >>> residue_class_2 = sievetools.ResidueClass(3, 0)
                >>> sieve = residue_class_1 | residue_class_2
                >>> sieve.boolean_train
                [1, 0, 1, 1, 1, 0]

        Returns list.
        '''
        result = []
        congruent_bases = self.congruent_bases
        for i in range(0, self.period):
            if i % self.period in congruent_bases:
                result.append(1)
            else:
                result.append(0)
        return result

    @property
    def congruent_bases(self):
        r'''Gets congruent bases.
        
        ..  container::

            **Example 1.** Gets congruent bases of sieve with period 6:

            ::

                >>> residue_class_1 = sievetools.ResidueClass(2, 0)
                >>> residue_class_2 = sievetools.ResidueClass(3, 0)
                >>> sieve = residue_class_1 | residue_class_2
                >>> sieve.congruent_bases
                [0, 2, 3, 4]

        Returns list.
        '''
        if self.logical_operator == 'or':
            return self._get_congruent_bases(operator.ior)
        elif self.logical_operator == 'xor':
            return self._get_congruent_bases(operator.ixor)
        elif self.logical_operator == 'and':
            return self._get_congruent_bases(operator.iand)

    @property
    def logical_operator(self):
        r'''Gets logical operator of sieve.

        Returns string.
        '''
        return self._logical_operator

    @property
    def period(self):
        r'''Gets period of sieve.

        Returns positive integer.
        '''
        periods = []
        for residue_class in self.residue_classes:
            periods.append(residue_class.period)
        if periods:
            period = mathtools.least_common_multiple(*periods)
        else:
            period = 1
        return period

    @property
    def residue_classes(self):
        r'''Gets residue classes of sieve.

        Returns list.
        '''
        return self._residue_classes

    ### PUBLIC METHODS ###

    # TODO: reimplement as Sieve.from_boolean_patterns()
#    @staticmethod
#    def from_cycle_tokens(*cycle_tokens):
#        '''Initializes sieve from `cycle_tokens`.
#
#        ..  container:: example
#
#            **Example 1.** Initializes sieve from two cycle tokens:
#
#            ::
#
#                >>> cycle_token_1 = (6, [0, 4, 5])
#                >>> cycle_token_2 = (10, [0, 1, 2], 6)
#                >>> cycle_tokens = [cycle_token_1, cycle_token_2]
#
#            ::
#
#                >>> sieve = sievetools.Sieve.from_cycle_tokens(*cycle_tokens)
#                >>> print(format(sieve))
#                sievetools.Sieve(
#                    residue_classes=[
#                        sievetools.ResidueClass(period=6, offset=0, ),
#                        sievetools.ResidueClass(period=6, offset=4, ),
#                        sievetools.ResidueClass(period=6, offset=5, ),
#                        sievetools.ResidueClass(period=10, offset=6, ),
#                        sievetools.ResidueClass(period=10, offset=7, ),
#                        sievetools.ResidueClass(period=10, offset=8, ),
#                        ],
#                    logical_operator='or',
#                    )
#
#        Cycle token comprises `period`, `residues` and optional `offset`.
#        '''
#        sieves = []
#        for cycle_token in cycle_tokens:
#            sieve = Sieve._cycle_token_to_sieve(cycle_token)
#            sieves.append(sieve)
#        if sieves:
#            current_sieve = sieves[0]
#            for sieve in sieves[1:]:
#                current_sieve = current_sieve | sieve
#        else:
#            current_sieve = Sieve([])
#        return current_sieve