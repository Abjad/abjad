from abjad import *
import copy


def test_LilyPondContextSettingComponentPlugIn___eq___01():

    note_1 = Note("c'4")
    note_1.set.voice.auto_beaming = False
    note_1.set.staff.tuplet_full_length = True

    note_2 = Note("c'4")
    note_2.set.voice.auto_beaming = False
    note_2.set.staff.tuplet_full_length = True

    note_3 = Note("c'4")
    note_3.set.voice.auto_beaming = True

    context_setting_component_plug_in_1 = note_1.set
    context_setting_component_plug_in_2 = note_2.set
    context_setting_component_plug_in_3 = note_3.set

    assert      context_setting_component_plug_in_1 == context_setting_component_plug_in_1
    assert      context_setting_component_plug_in_1 == context_setting_component_plug_in_2
    assert not context_setting_component_plug_in_1 == context_setting_component_plug_in_3
    assert      context_setting_component_plug_in_2 == context_setting_component_plug_in_1
    assert      context_setting_component_plug_in_2 == context_setting_component_plug_in_2
    assert not context_setting_component_plug_in_2 == context_setting_component_plug_in_3
    assert not context_setting_component_plug_in_3 == context_setting_component_plug_in_1
    assert not context_setting_component_plug_in_3 == context_setting_component_plug_in_2
    assert      context_setting_component_plug_in_3 == context_setting_component_plug_in_3
