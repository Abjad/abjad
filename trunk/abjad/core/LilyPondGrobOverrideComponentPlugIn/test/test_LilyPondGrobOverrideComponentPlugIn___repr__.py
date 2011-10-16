from abjad import *
from abjad.core import LilyPondGrobOverrideComponentPlugIn


def test_LilyPondGrobOverrideComponentPlugIn___repr___01():
    '''LilyPond grob override component plug-in repr is evaluable.
    '''

    note = Note("c'4")
    note.override.note_head.color = 'red'

    grob_override_component_plug_in_1 = note.override
    grob_override_component_plug_in_2 = eval(repr(grob_override_component_plug_in_1))

    assert isinstance(grob_override_component_plug_in_1, LilyPondGrobOverrideComponentPlugIn)
    assert isinstance(grob_override_component_plug_in_2, LilyPondGrobOverrideComponentPlugIn)


def test_LilyPondGrobOverrideComponentPlugIn___repr___02():
    '''LilyPond grob override component plug-in repr does not truncate override strings.
    '''

    note = Note("c'8")
    note.override.beam.breakable = True
    note.override.note_head.color = 'red'

    assert repr(note.override) == \
        "LilyPondGrobOverrideComponentPlugIn(beam__breakable = True, note_head__color = 'red')"
