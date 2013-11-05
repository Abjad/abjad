# -*- encoding: utf-8 -*-
import copy
from abjad import *


def test_lilypondproxytools_LilyPondGrobProxy___eq___01():

    note_1 = Note("c'4")
    override(note_1).note_head.color = 'red'
    override(note_1).note_head.thickness = 2

    note_2 = Note("c'4")
    override(note_2).note_head.color = 'red'
    override(note_2).note_head.thickness = 2

    note_3 = Note("c'4")
    override(note_3).note_head.color = 'blue'

    grob_proxy_1 = override(note_1).note_head
    grob_proxy_2 = override(note_2).note_head
    grob_proxy_3 = override(note_3).note_head

    assert      grob_proxy_1 == grob_proxy_1
    assert      grob_proxy_1 == grob_proxy_2
    assert not grob_proxy_1 == grob_proxy_3
    assert      grob_proxy_2 == grob_proxy_1
    assert      grob_proxy_2 == grob_proxy_2
    assert not grob_proxy_2 == grob_proxy_3
    assert not grob_proxy_3 == grob_proxy_1
    assert not grob_proxy_3 == grob_proxy_2
    assert      grob_proxy_3 == grob_proxy_3
