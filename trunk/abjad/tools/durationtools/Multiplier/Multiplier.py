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
