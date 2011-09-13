from abjad import *


def test_tietools_get_tie_chain_01():
    '''Return tuple of all leaves in spanner, if spanned;
    otherwise return 1-tuple of client.
    '''

    t = Staff(notetools.make_repeated_notes(4))
    tietools.TieSpanner(t[2:])

    r'''
    \new Staff {
        c'8
        d'8
        e'8 ~
        f'8
    }
    '''

    assert tietools.get_tie_chain(t[0]) == (t[0], )
    assert tietools.get_tie_chain(t[1]) == (t[1], )
    assert tietools.get_tie_chain(t[2]) == (t[2], t[3])
    assert tietools.get_tie_chain(t[3]) == (t[2], t[3])
