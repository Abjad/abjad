# -*- coding: utf-8 -*-
import operator
from abjad.tools import mathtools
from abjad.tools.sievetools.BaseResidueClass import BaseResidueClass


class Sieve(BaseResidueClass):
    r'''Sieve.

    Due to Xenakis.
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
        self._sort_rcs()

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

    # _get_congruent_bases() might implement more cleanly
    # if the min and max parameters behaved more like the
    # start and stop parameters passed to slice() objects in
    # list slicing.
    # That is, Sieve.get_congruent_bases(8) currently
    # returns a list of up to *nine* items; should probably
    # return a list of up to only *eight* items.
    def _get_congruent_bases(self, minimum, maximum, logical_operator):
        if logical_operator is operator.iand:
            result = set(range(minimum, maximum + 1))
        else:
            result = set([])
        for rc in self.residue_classes:
            logical_operator(
                result, set(rc.get_congruent_bases(minimum, maximum)))
        return sorted(result)

    def _sort_rcs(self):
        from abjad.tools import sievetools
        if all(isinstance(rc, sievetools.ResidueClass) for rc in self.residue_classes):
            self.residue_classes.sort()

    ### PUBLIC PROPERTIES ###

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
        rc_periods = []
        for rc in self.residue_classes:
            rc_periods.append(rc.period)
        if rc_periods:
            period = mathtools.least_common_multiple(*rc_periods)
        else:
            period = 1
        return period

    @property
    def residue_classes(self):
        r'''Gets residue classes of sieve.

        Returns list.
        '''
        return self._residue_classes

    @property
    def representative_boolean_train(self):
        r'''Gets representative boolean train.

        Returns list.
        '''
        return self.get_boolean_train(self.period)

    @property
    def representative_congruent_bases(self):
        r'''Gets representative congruent bases.

        Returns list.
        '''
        congruent_bases = self.get_congruent_bases(self.period)
        # remove redundant last element from get_congruent_bases()
        congruent_bases = congruent_bases[:-1]
        return congruent_bases

    ### PUBLIC METHODS ###

    @staticmethod
    def from_cycle_tokens(*cycle_tokens):
        '''Initializes sieve from `cycle_tokens`.

        ..  container:: example

            **Example 1.** Initializes sieve from two cycle tokens:

            ::

                >>> cycle_token_1 = (6, [0, 4, 5])
                >>> cycle_token_2 = (10, [0, 1, 2], 6)
                >>> cycle_tokens = [cycle_token_1, cycle_token_2]

            ::

                >>> sieve = sievetools.Sieve.from_cycle_tokens(*cycle_tokens)
                >>> print(format(sieve))
                sievetools.Sieve(
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

        Cycle token comprises `period`, `residues` and optional `offset`.
        '''
        sieves = []
        for cycle_token in cycle_tokens:
            sieve = Sieve._cycle_token_to_sieve(cycle_token)
            sieves.append(sieve)
        if sieves:
            current_sieve = sieves[0]
            for sieve in sieves[1:]:
                current_sieve = current_sieve | sieve
        else:
            current_sieve = Sieve([])
        return current_sieve

    def get_boolean_train(self, *min_max):
        r'''Gets boolean train.
        
        ..  container::

            **Example 1.** Gets first six values of boolean train:

            ::

                >>> residue_class_1 = sievetools.ResidueClass(2, 0)
                >>> residue_class_2 = sievetools.ResidueClass(3, 0)
                >>> sieve = residue_class_1 | residue_class_2
                >>> sieve.get_boolean_train(6)
                [1, 0, 1, 1, 1, 0]

        Returns list.
        '''
        minimum, maximum = self._process_min_max_attribute(*min_max)
        result = []
        cb = self.get_congruent_bases(minimum, maximum)
        for i in range(minimum, maximum ):
            if i in cb:
                result.append(1)
            else:
                result.append(0)
        return result

    def get_congruent_bases(self, *min_max):
        r'''Gets congruent bases.
        
        ..  container::

            **Example 1.** Gets congruent bases from -6 to 6:

            ::

                >>> residue_class_1 = sievetools.ResidueClass(2, 0)
                >>> residue_class_2 = sievetools.ResidueClass(3, 0)
                >>> sieve = residue_class_1 | residue_class_2
                >>> sieve.get_congruent_bases(-6, 6)
                [-6, -4, -3, -2, 0, 2, 3, 4, 6]

        Returns list.
        '''
        minimum, maximum = self._process_min_max_attribute(*min_max)
        if self.logical_operator == 'or':
            return self._get_congruent_bases(minimum, maximum, operator.ior)
        elif self.logical_operator == 'xor':
            return self._get_congruent_bases(minimum, maximum, operator.ixor)
        elif self.logical_operator == 'and':
            return self._get_congruent_bases(minimum, maximum, operator.iand)

    # the +1 adjustment is necessary here because of
    # self._process_min_max_attribute() demands min strictly less than max;
    # that is, self.get_congruent_bases(0, 0) raises an exception;
    # so we work around this with self.get_congruent_bases(-1, 1) instead.
    def is_congruent_base(self, integer):
        r'''Is true when `integer` is congruent to base in sieve.

        ..  container:: example

            ::

                >>> residue_class_1 = sievetools.ResidueClass(2, 0)
                >>> residue_class_2 = sievetools.ResidueClass(3, 0)
                >>> sieve = residue_class_1 | residue_class_2
                >>> sieve.is_congruent_base(12)
                True

        Otherwise false:

        ..  container:: example

            ::

                >>> sieve.is_congruent_base(13)
                False

        Returns true or false.
        '''
        tmp_min, tmp_max = -(abs(integer) + 1), abs(integer) + 1
        return integer in self.get_congruent_bases(tmp_min, tmp_max)