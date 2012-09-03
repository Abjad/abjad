from abjad.tools import leaftools


def make_tied_rest(duration, big_endian=True, tied=False):
    '''Returns a list of rests to fill given duration.
    
    Rests returned are tie-spanned when ``tied=True``.
    '''
    from abjad.tools import resttools

    return leaftools.make_tied_leaf(resttools.Rest, duration, big_endian=big_endian, pitches=None, tied=tied)
