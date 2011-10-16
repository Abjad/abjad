from abjad import *
from abjad.core.LilyPondGrobProxy import LilyPondGrobProxy


def test_LilyPondGrobProxy___repr___01():
    '''LilyPond grob proxy repr is evaluable.
    '''

    note = Note("c'4")
    note.override.note_head.color = 'red'

    grob_proxy_1 = note.override.note_head
    grob_proxy_2 = eval(repr(grob_proxy_1))

    assert isinstance(grob_proxy_1, LilyPondGrobProxy)
    assert isinstance(grob_proxy_2, LilyPondGrobProxy)
