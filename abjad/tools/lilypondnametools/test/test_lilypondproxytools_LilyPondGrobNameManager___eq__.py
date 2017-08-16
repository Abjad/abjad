import copy
import abjad


def test_lilypondproxytools_LilyPondGrobNameManager___eq___01():

    note_1 = abjad.Note("c'4")
    abjad.override(note_1).note_head.color = 'red'
    abjad.override(note_1).stem.color = 'red'

    note_2 = abjad.Note("c'4")
    abjad.override(note_2).note_head.color = 'red'
    abjad.override(note_2).stem.color = 'red'

    note_3 = abjad.Note("c'4")
    abjad.override(note_3).note_head.color = 'red'

    grob_override_component_plug_in_1 = abjad.override(note_1)
    grob_override_component_plug_in_2 = abjad.override(note_2)
    grob_override_component_plug_in_3 = abjad.override(note_3)

    assert      grob_override_component_plug_in_1 == grob_override_component_plug_in_1
    assert      grob_override_component_plug_in_1 == grob_override_component_plug_in_2
    assert not grob_override_component_plug_in_1 == grob_override_component_plug_in_3
    assert      grob_override_component_plug_in_2 == grob_override_component_plug_in_1
    assert      grob_override_component_plug_in_2 == grob_override_component_plug_in_2
    assert not grob_override_component_plug_in_2 == grob_override_component_plug_in_3
    assert not grob_override_component_plug_in_3 == grob_override_component_plug_in_1
    assert not grob_override_component_plug_in_3 == grob_override_component_plug_in_2
    assert      grob_override_component_plug_in_3 == grob_override_component_plug_in_3
