from abjad.tools import leaftools


def make_tied_rest(duration, decrease_durations_monotonically=True, tie_parts=False):
    '''Returns a list of rests to fill given duration.
    
    Tie rest parts when ``tie_parts=True``.
    '''
    from abjad.tools import resttools

    return leaftools.make_tied_leaf(
        resttools.Rest, duration, 
        decrease_durations_monotonically=decrease_durations_monotonically, 
        pitches=None, tie_parts=tie_parts)
