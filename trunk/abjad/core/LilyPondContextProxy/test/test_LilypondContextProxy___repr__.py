from abjad import *
from abjad.core.LilyPondContextProxy import LilyPondContextProxy


def test_LilypondContextProxy___repr___01():
    '''LilyPond component proxy repr is evaluable.
    '''

    note = Note("c'4")
    note.set.staff.tuplet_full_length = True

    context_proxy_1 = note.set.staff
    context_proxy_2 = eval(repr(context_proxy_1))

    assert isinstance(context_proxy_1, LilyPondContextProxy)
    assert isinstance(context_proxy_2, LilyPondContextProxy)
