from abjad.tools import abctools
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
