from abjad.tools.leaftools.make_tied_leaf import make_tied_leaf


def make_tied_rest(dur, direction='big-endian', tied=False):
    '''Returns a list of rests to fill given duration.
        Rests returned are Tie spanned.
    '''
    from abjad.tools.resttools.Rest import Rest

    return make_tied_leaf(Rest, dur, direction, None, tied)
