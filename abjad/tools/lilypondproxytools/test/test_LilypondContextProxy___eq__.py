# -*- encoding: utf-8 -*-
import copy
from abjad import *


def test_LilypondContextProxy___eq___01():

    note_1 = Note("c'4")
    setting(note_1).voice.auto_beaming = False
    setting(note_1).voice.tuplet_full_length = True

    note_2 = Note("c'4")
    setting(note_2).voice.auto_beaming = False
    setting(note_2).voice.tuplet_full_length = True

    note_3 = Note("c'4")
    setting(note_3).voice.auto_beaming = True

    context_proxy_1 = setting(note_1).voice
    context_proxy_2 = setting(note_2).voice
    context_proxy_3 = setting(note_3).voice

    assert      context_proxy_1 == context_proxy_1
    assert      context_proxy_1 == context_proxy_2
    assert not context_proxy_1 == context_proxy_3
    assert      context_proxy_2 == context_proxy_1
    assert      context_proxy_2 == context_proxy_2
    assert not context_proxy_2 == context_proxy_3
    assert not context_proxy_3 == context_proxy_1
    assert not context_proxy_3 == context_proxy_2
    assert      context_proxy_3 == context_proxy_3
