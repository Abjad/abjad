from abjad import *
import copy


def test_LilyPondGrobProxy___eq___01():

    note_1 = Note("c'4")
    note_1.override.note_head.color = 'red'
    note_1.override.note_head.thickness = 2

    note_2 = Note("c'4")
    note_2.override.note_head.color = 'red'
    note_2.override.note_head.thickness = 2

    note_3 = Note("c'4")
    note_3.override.note_head.color = 'blue'

    grob_proxy_1 = note_1.override.note_head
    grob_proxy_2 = note_2.override.note_head
    grob_proxy_3 = note_3.override.note_head

    assert      grob_proxy_1 == grob_proxy_1
    assert      grob_proxy_1 == grob_proxy_2
    assert not grob_proxy_1 == grob_proxy_3
    assert      grob_proxy_2 == grob_proxy_1
    assert      grob_proxy_2 == grob_proxy_2
    assert not grob_proxy_2 == grob_proxy_3
    assert not grob_proxy_3 == grob_proxy_1
    assert not grob_proxy_3 == grob_proxy_2
    assert      grob_proxy_3 == grob_proxy_3
