# -*- encoding: utf-8 -*-
import operator
from abjad.tools import mathtools
from abjad.tools.sievetools.BaseResidueClass import BaseResidueClass


class Sieve(BaseResidueClass):
    r'''A Xenakis sieve.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_logical_operator',
        '_rcs',
        )

    logical_operator_dictionary = {
        'and': '&',
        'or': '|',
        'xor': '^',
        }

    ### INITIALIZER ###

    def __init__(self, rcs=None, logical_operator='or'):
        from abjad.tools import sievetools
        if isinstance(rcs, type(self)):
            self._rcs = rcs.rcs[:]
            self._logical_operator = rcs.logical_operator
        elif rcs is None:
            rcs = [sievetools.ResidueClass()]
            self._rcs = rcs
            self._logical_operator = logical_operator
        else:
            self._rcs = rcs[:]
            self._logical_operator = logical_operator
        self._sort_rcs()

    ### PRIVATE METHODS ###

    @staticmethod
    def _cycle_token_to_sieve(cycle_token):
        from abjad.tools import sievetools
        if isinstance(cycle_token, Sieve):
            return Sieve(cycle_token)
        modulo = cycle_token[0]
        residues = cycle_token[1]
        try:
            offset = cycle_token[2]
        except IndexError:
            offset = 0
        residue_classes = []
        for residue in residues:
            adjusted_residue = (residue + offset) % modulo
            residue_class = sievetools.ResidueClass(modulo, adjusted_residue)
            residue_classes.append(residue_class)
        residue_classes.sort(key=lambda x: x.residue)
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
        for rc in self.rcs:
            logical_operator(
                result, set(rc.get_congruent_bases(minimum, maximum)))
        return sorted(result)

    def _sort_rcs(self):
        from abjad.tools import sievetools
        if all(isinstance(rc, sievetools.ResidueClass) for rc in self.rcs):
            self.rcs.sort()

    ### PUBLIC PROPERTIES ###

    @property
    def logical_operator(self):
        r'''Residue class expression logical operator.
        '''
        return self._logical_operator

    @property
    def period(self):
        r'''Residue class expression period.
        '''
        rc_periods = []
        for rc in self.rcs:
            rc_periods.append(rc.modulo)
        if rc_periods:
            period = mathtools.least_common_multiple(*rc_periods)
        else:
            period = 1
        return period

    @property
    def rcs(self):
        r'''Residue class expression residue classes.
        '''
        return self._rcs

    @property
    def representative_boolean_train(self):
        r'''Residue class expression representative boolean train.
        '''
        return self.get_boolean_train(self.period)

    @property
    def representative_congruent_bases(self):
        r'''Residue class expression representative congruent bases.
        '''
        congruent_bases = self.get_congruent_bases(self.period)
        # remove redundant last element from get_congruent_bases()
        congruent_bases = congruent_bases[:-1]
        return congruent_bases

    ### PUBLIC METHODS ###

    @staticmethod
    def from_cycle_tokens(*cycle_tokens):
        '''Makes Xenakis sieve from `cycle_tokens`.

        ::

            >>> cycle_token_1 = (6, [0, 4, 5])
            >>> cycle_token_2 = (10, [0, 1, 2], 6)
            >>> cycle_tokens = [cycle_token_1, cycle_token_2]

        ::

            >>> sieve = sievetools.Sieve.from_cycle_tokens(*cycle_tokens)
            >>> print format(sieve) 
            sievetools.Sieve(
                rcs=[
                    sievetools.ResidueClass(6, 0),
                    sievetools.ResidueClass(6, 4),
                    sievetools.ResidueClass(6, 5),
                    sievetools.ResidueClass(10, 6),
                    sievetools.ResidueClass(10, 7),
                    sievetools.ResidueClass(10, 8),
                    ],
                logical_operator='or',
                )

        Cycle token comprises `modulo`, `residues` and optional `offset`.
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
        r'''Returns a boolean train with 0s mapped to the integers that are not
        congruent bases of the residue class expression and 1s mapped to those
        that are.

        The method takes one or two integer arguments. If only one is given, it
        is taken as the max range and min is assumed to be 0.

        ..  container::

            ::

                >>> from abjad.tools.sievetools import ResidueClass

            ::

                >>> sieve = ResidueClass(3, 0) | ResidueClass(2, 0)
                >>> sieve.get_boolean_train(6)
                [1, 0, 1, 1, 1, 0]
                >>> sieve.get_congruent_bases(-6, 6)
                [-6, -4, -3, -2, 0, 2, 3, 4, 6]

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
        r'''Returns all the congruent bases of this residue class expression
        within the given range.

        The method takes one or two integer arguments. If only one it given, it
        is taken as the max range and min is assumed to be 0.

        ..  container:: example

            ::

                >>> sieve = ResidueClass(3, 0) | ResidueClass(2, 0)
                >>> sieve.get_congruent_bases(6)
                [0, 2, 3, 4, 6]
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
        r'''True when `integer` is congruent to base in sieve.
        Otherwise false.

            ::

                >>> sieve = ResidueClass(3, 0) | ResidueClass(2, 0)
                >>> sieve.get_congruent_bases(6)
                [0, 2, 3, 4, 6]
                >>> sieve.is_congruent_base(12)
                True

        Otherwise false:

            ::

                >>> sieve.is_congruent_base(13)
                False

        Returns boolean.
        '''
        tmp_min, tmp_max = -(abs(integer) + 1), abs(integer) + 1
        return integer in self.get_congruent_bases(tmp_min, tmp_max)
