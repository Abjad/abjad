# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.lilypondproxytools import LilyPondGrobManager


def test_lilypondproxytools_LilyPondGrobManager___repr___01():
    r'''LilyPond grob override component plug-in repr is evaluable.
    '''

    note = Note("c'4")
    override(note).note_head.color = 'red'

    grob_override_component_plug_in_1 = override(note)
    grob_override_component_plug_in_2 = eval(repr(grob_override_component_plug_in_1))

    assert isinstance(grob_override_component_plug_in_1, LilyPondGrobManager)
    assert isinstance(grob_override_component_plug_in_2, LilyPondGrobManager)


def test_lilypondproxytools_LilyPondGrobManager___repr___02():
    r'''LilyPond grob override component plug-in repr does not truncate override strings.
    '''

    note = Note("c'8")
    override(note).beam.breakable = True
    override(note).note_head.color = 'red'

    assert repr(override(note)) == \
        "LilyPondGrobManager(beam__breakable=True, note_head__color='red')"
