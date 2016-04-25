# -*- coding: utf-8 -*-
import copy
from abjad import *


def test_lilypondproxytools_LilyPondGrobNameManager___eq___01():

    note_1 = Note("c'4")
    override(note_1).note_head.color = 'red'
    override(note_1).stem.color = 'red'

    note_2 = Note("c'4")
    override(note_2).note_head.color = 'red'
    override(note_2).stem.color = 'red'

    note_3 = Note("c'4")
    override(note_3).note_head.color = 'red'

    grob_override_component_plug_in_1 = override(note_1)
    grob_override_component_plug_in_2 = override(note_2)
    grob_override_component_plug_in_3 = override(note_3)

    assert      grob_override_component_plug_in_1 == grob_override_component_plug_in_1
    assert      grob_override_component_plug_in_1 == grob_override_component_plug_in_2
    assert not grob_override_component_plug_in_1 == grob_override_component_plug_in_3
    assert      grob_override_component_plug_in_2 == grob_override_component_plug_in_1
    assert      grob_override_component_plug_in_2 == grob_override_component_plug_in_2
    assert not grob_override_component_plug_in_2 == grob_override_component_plug_in_3
    assert not grob_override_component_plug_in_3 == grob_override_component_plug_in_1
    assert not grob_override_component_plug_in_3 == grob_override_component_plug_in_2
    assert      grob_override_component_plug_in_3 == grob_override_component_plug_in_3
