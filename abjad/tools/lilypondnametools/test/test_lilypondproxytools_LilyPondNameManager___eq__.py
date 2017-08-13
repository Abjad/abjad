import copy
import abjad


def test_lilypondproxytools_LilyPondNameManager___eq___01():

    note_1 = abjad.Note("c'4")
    abjad.setting(note_1).voice.auto_beaming = False
    abjad.setting(note_1).voice.tuplet_full_length = True

    note_2 = abjad.Note("c'4")
    abjad.setting(note_2).voice.auto_beaming = False
    abjad.setting(note_2).voice.tuplet_full_length = True

    note_3 = abjad.Note("c'4")
    abjad.setting(note_3).voice.auto_beaming = True

    context_proxy_1 = abjad.setting(note_1).voice
    context_proxy_2 = abjad.setting(note_2).voice
    context_proxy_3 = abjad.setting(note_3).voice

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

    note_1 = abjad.Note("c'4")
    abjad.override(note_1).note_head.color = 'red'
    abjad.override(note_1).note_head.thickness = 2

    note_2 = abjad.Note("c'4")
    abjad.override(note_2).note_head.color = 'red'
    abjad.override(note_2).note_head.thickness = 2

    note_3 = abjad.Note("c'4")
    abjad.override(note_3).note_head.color = 'blue'

    grob_proxy_1 = abjad.override(note_1).note_head
    grob_proxy_2 = abjad.override(note_2).note_head
    grob_proxy_3 = abjad.override(note_3).note_head

    assert      grob_proxy_1 == grob_proxy_1
    assert      grob_proxy_1 == grob_proxy_2
    assert not grob_proxy_1 == grob_proxy_3
    assert      grob_proxy_2 == grob_proxy_1
    assert      grob_proxy_2 == grob_proxy_2
    assert not grob_proxy_2 == grob_proxy_3
    assert not grob_proxy_3 == grob_proxy_1
    assert not grob_proxy_3 == grob_proxy_2
    assert      grob_proxy_3 == grob_proxy_3
