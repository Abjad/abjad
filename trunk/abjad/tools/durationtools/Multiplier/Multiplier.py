from abjad.tools import abctools
from abjad.tools import mathtools
from abjad.tools.durationtools.Duration import Duration


class Multiplier(Duration):
    '''.. versionadded:: 2.11

    Multiplier.
    '''

    ### SPECIAL METHODS ###

    # multiplier times duration gives duration
    def __mul__(self, *args):
        if len(args) == 1 and args[0].__class__.__name__ == 'Duration':
            return Duration(Duration.__mul__(self, *args))
        else:
            return Duration.__mul__(self, *args)

    ### PUBLIC PROPERTIES ###

#    @property
#    def implied_prolation(self):
#        r'''.. versionadded:: 2.11
#
#        Implied prolation of multiplier::
#
#            >>> for denominator in range(1, 16 + 1):
#            ...     multiplier = Multiplier(1, denominator)
#            ...     print '{}\t{}'.format(multiplier, multiplier.implied_prolation)
#            ... 
#            1       1
#            1/2     1
#            1/3     2/3
#            1/4     1
#            1/5     4/5
#            1/6     2/3
#            1/7     4/7
#            1/8     1
#            1/9     8/9
#            1/10    4/5
#            1/11    8/11
#            1/12    2/3
#            1/13    8/13
#            1/14    4/7
#            1/15    8/15
#            1/16    1
#
#        Return new multipler.
#        '''
#        numerator = mathtools.greatest_power_of_two_less_equal(self.denominator)
#        return type(self)(numerator, self.denominator)

    @property
    def is_proper_tuplet_multiplier(self):
        '''.. versionadded:: 2.11

        True when mutliplier is greater than ``1/2`` and less than ``2``.
        Otherwise false::

            >>> Multiplier(3, 2).is_proper_tuplet_multiplier
            True

        Return boolean.
        '''
        return type(self)(1, 2) < self < type(self)(2)
