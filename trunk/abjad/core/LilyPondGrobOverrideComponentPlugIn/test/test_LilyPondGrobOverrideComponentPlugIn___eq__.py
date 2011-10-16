from abjad import *
import copy


def test_LilyPondGrobOverrideComponentPlugIn___eq___01():

    note_1 = Note("c'4")
    note_1.override.note_head.color = 'red'
    note_1.override.stem.color = 'red'

    note_2 = Note("c'4")
    note_2.override.note_head.color = 'red'
    note_2.override.stem.color = 'red'

    note_3 = Note("c'4")
    note_3.override.note_head.color = 'red'

    grob_override_component_plug_in_1 = note_1.override
    grob_override_component_plug_in_2 = note_2.override
    grob_override_component_plug_in_3 = note_3.override

    assert      grob_override_component_plug_in_1 == grob_override_component_plug_in_1
    assert      grob_override_component_plug_in_1 == grob_override_component_plug_in_2
    assert not grob_override_component_plug_in_1 == grob_override_component_plug_in_3
    assert      grob_override_component_plug_in_2 == grob_override_component_plug_in_1
    assert      grob_override_component_plug_in_2 == grob_override_component_plug_in_2
    assert not grob_override_component_plug_in_2 == grob_override_component_plug_in_3
    assert not grob_override_component_plug_in_3 == grob_override_component_plug_in_1
    assert not grob_override_component_plug_in_3 == grob_override_component_plug_in_2
    assert      grob_override_component_plug_in_3 == grob_override_component_plug_in_3
