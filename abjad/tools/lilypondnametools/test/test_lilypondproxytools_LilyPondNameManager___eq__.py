# -*- coding: utf-8 -*-
import copy
from abjad import *


def test_lilypondproxytools_LilyPondNameManager___eq___01():

    note_1 = Note("c'4")
    set_(note_1).voice.auto_beaming = False
    set_(note_1).voice.tuplet_full_length = True

    note_2 = Note("c'4")
    set_(note_2).voice.auto_beaming = False
    set_(note_2).voice.tuplet_full_length = True

    note_3 = Note("c'4")
    set_(note_3).voice.auto_beaming = True

    context_proxy_1 = set_(note_1).voice
    context_proxy_2 = set_(note_2).voice
    context_proxy_3 = set_(note_3).voice

    assert      context_proxy_1 == context_proxy_1
    assert      context_proxy_1 == context_proxy_2
    assert not context_proxy_1 == context_proxy_3
    assert      context_proxy_2 == context_proxy_1
    assert      context_proxy_2 == context_proxy_2
    assert not context_proxy_2 == context_proxy_3
    assert not context_proxy_3 == context_proxy_1
    assert not context_proxy_3 == context_proxy_2
    assert      context_proxy_3 == context_proxy_3


def test_lilypondproxytools_LilyPondNameManager___eq___02():

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
