from abjad.tools import leaftools


def make_tied_rest(duration, decrease_durations_monotonically=True, tied=False):
    '''Returns a list of rests to fill given duration.
    
    Rests returned are tie-spanned when ``tied=True``.
    '''
    from abjad.tools import resttools

    return leaftools.make_tied_leaf(resttools.Rest, duration, decrease_durations_monotonically=decrease_durations_monotonically, pitches=None, tied=tied)
