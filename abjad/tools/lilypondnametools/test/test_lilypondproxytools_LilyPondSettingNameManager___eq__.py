# -*- coding: utf-8 -*-
import copy
from abjad import *


def test_lilypondproxytools_LilyPondSettingNameManager___eq___01():

    note_1 = Note("c'4")
    set_(note_1).voice.auto_beaming = False
    set_(note_1).staff.tuplet_full_length = True

    note_2 = Note("c'4")
    set_(note_2).voice.auto_beaming = False
    set_(note_2).staff.tuplet_full_length = True

    note_3 = Note("c'4")
    set_(note_3).voice.auto_beaming = True

    context_setting_component_plug_in_1 = set_(note_1)
    context_setting_component_plug_in_2 = set_(note_2)
    context_setting_component_plug_in_3 = set_(note_3)

    assert      context_setting_component_plug_in_1 == context_setting_component_plug_in_1
    assert      context_setting_component_plug_in_1 == context_setting_component_plug_in_2
    assert not context_setting_component_plug_in_1 == context_setting_component_plug_in_3
    assert      context_setting_component_plug_in_2 == context_setting_component_plug_in_1
    assert      context_setting_component_plug_in_2 == context_setting_component_plug_in_2
    assert not context_setting_component_plug_in_2 == context_setting_component_plug_in_3
    assert not context_setting_component_plug_in_3 == context_setting_component_plug_in_1
    assert not context_setting_component_plug_in_3 == context_setting_component_plug_in_2
    assert      context_setting_component_plug_in_3 == context_setting_component_plug_in_3
