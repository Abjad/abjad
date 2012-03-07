from abjad import *
import copy


def test_LilypondContextProxy___eq___01():

    note_1 = Note("c'4")
    note_1.set.voice.auto_beaming = False
    note_1.set.voice.tuplet_full_length = True

    note_2 = Note("c'4")
    note_2.set.voice.auto_beaming = False
    note_2.set.voice.tuplet_full_length = True

    note_3 = Note("c'4")
    note_3.set.voice.auto_beaming = True

    context_proxy_1 = note_1.set.voice
    context_proxy_2 = note_2.set.voice
    context_proxy_3 = note_3.set.voice

    assert      context_proxy_1 == context_proxy_1
    assert      context_proxy_1 == context_proxy_2
    assert not context_proxy_1 == context_proxy_3
    assert      context_proxy_2 == context_proxy_1
    assert      context_proxy_2 == context_proxy_2
    assert not context_proxy_2 == context_proxy_3
    assert not context_proxy_3 == context_proxy_1
    assert not context_proxy_3 == context_proxy_2
    assert      context_proxy_3 == context_proxy_3
