from abjad.core import _Immutable
from abjad.tools import mathtools
from abjad.tools.sievetools._BaseResidueClass import _BaseResidueClass
from abjad.tools.sievetools._process_min_max_attribute import _process_min_max_attribute
import operator


# TODO: change name to Sieve
class ResidueClassExpression(_BaseResidueClass, _Immutable):

    def __init__(self, rcs, operator = 'or'):
        # init from other rc expression
        if isinstance(rcs, ResidueClassExpression):
            #self.rcs = rcs.rcs[:]
            #self.operator = rcs.operator
            object.__setattr__(self, '_rcs', rcs.rcs[:])
            object.__setattr__(self, '_operator', rcs.operator)
        # init from rcs and operator
        else:
            #self.rcs = rcs[:]
            #self.operator = operator
            object.__setattr__(self, '_rcs', rcs[:])
            object.__setattr__(self, '_operator', operator)
        # sort rcs
        self._sort_rcs()

    ### OVERLOADS ###

    def __repr__(self):
        opdic = {'and':' & ', 'or':' | ', 'xor':' ^ '}
        result = opdic[self.operator].join([str(rc) for rc in self.rcs])
        return '{%s}' % result

    ### PRIVATE METHODS ###

    # TB: _get_congruent_bases() might implement more cleanly
    # if the min and max parameters behaved more like the
    # start and stop parameters passed to slice() objects in
    # list slicing.
    # That is, ResidueClassExpression.get_congruent_bases(8) currently
    # returns a list of up to *nine* items; should probably
    # return a list of up to only *eight* items.
    def _get_congruent_bases(self, minimum, maximum, op):
        if op is operator.iand:
            result = set(range(minimum, maximum + 1))
        else:
            result = set([])
        for rc in self.rcs:
            op(result, set(rc.get_congruent_bases(minimum, maximum)))
        return sorted(result)

    def _sort_rcs(self):
        from abjad.tools.sievetools.ResidueClass import ResidueClass
        if all([isinstance(rc, ResidueClass) for rc in self.rcs]):
            self.rcs.sort()

    ### PUBLIC ATTRIBUTES ###

    @property
    def operator(self):
        '''Operator of residue class expression.
        '''
        return self._operator

    @property
    def period(self):
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
        '''Residue classes of expression.
        '''
        return self._rcs

    @property
    def representative_boolean_train(self):
        return self.get_boolean_train(self.period)

    @property
    def representative_congruent_bases(self):
        congruent_bases = self.get_congruent_bases(self.period)
        # remove redundant last element from get_congruent_bases()
        congruent_bases = congruent_bases[:-1]
        return congruent_bases

    ### PUBLIC METHODS ###

    def get_boolean_train(self, *min_max):
        '''Returns a boolean train with 0s mapped to the integers
        that are not congruent bases of the RC expression and 1s mapped
        to those that are.
        The method takes one or two integer arguments.
        If only one is given, it is taken as the max range
        and min is assumed to be 0.

        Example::

            abjad> from abjad.tools.sievetools import ResidueClass as RC

        ::

            abjad> e = RC(3, 0) | RC(2, 0)
            abjad> e.get_boolean_train(6)
            [1, 0, 1, 1, 1, 0]
            abjad> e.get_congruent_bases(-6, 6)
            [-6, -4, -3, -2, 0, 2, 3, 4, 6]

        Return list.
        '''

        minimum, maximum = _process_min_max_attribute(*min_max)
        result = []
        cb = self.get_congruent_bases(minimum, maximum)
        for i in range(minimum, maximum ):
            if i in cb:
                result.append(1)
            else:
                result.append(0)
        return result

    def get_congruent_bases(self, *min_max):
        '''Returns all the congruent bases of this RC expression
        within the given range.
        The method takes one or two integer arguments.
        If only one it given, it is taken as the max range
        and min is assumed to be 0.

        Example::

            abjad> from abjad.tools.sievetools import ResidueClass as RC

        ::

            abjad> e = RC(3, 0) | RC(2, 0)
            abjad> e.get_congruent_bases(6)
            [0, 2, 3, 4, 6]
            abjad> e.get_congruent_bases(-6, 6)
            [-6, -4, -3, -2, 0, 2, 3, 4, 6]

        Return list.
        '''

        minimum, maximum = _process_min_max_attribute(*min_max)
        if self.operator == 'or':
            return self._get_congruent_bases(minimum, maximum, operator.ior)
        elif self.operator == 'xor':
            return self._get_congruent_bases(minimum, maximum, operator.ixor)
        elif self.operator == 'and':
            return self._get_congruent_bases(minimum, maximum, operator.iand)

    # TB: the +1 adjustment is necessary here because of
    # _process_min_max_attribute() demands min strictly less than max;
    # that is, self.get_congruent_bases(0, 0) raises an exception;
    # so we workaround this with self.get_congruent_bases(-1, 1) instead.
    def is_congruent_base(self, integer):
        tmp_min, tmp_max = -(abs(integer) + 1), abs(integer) + 1
        return integer in self.get_congruent_bases(tmp_min, tmp_max)
