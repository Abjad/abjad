from abjad.tools.leaftools._construct_tied_leaf import _construct_tied_leaf


def _construct_tied_rest(dur, direction='big-endian', tied=False):
    '''Returns a list of rests to fill given duration.
        Rests returned are Tie spanned.
    '''
    from abjad.tools.resttools.Rest import Rest

    return _construct_tied_leaf(Rest, dur, direction, None, tied)
