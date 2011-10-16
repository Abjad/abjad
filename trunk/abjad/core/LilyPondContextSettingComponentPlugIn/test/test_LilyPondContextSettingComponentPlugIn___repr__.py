from abjad import *
from abjad.core import LilyPondContextSettingComponentPlugIn


def test_LilyPondContextSettingComponentPlugIn___repr___01():
    '''LilyPond context setting component plug-in repr is evaluable.
    '''

    note = Note("c'4")
    note.set.staff.tuplet_full_length = True

    context_setting_component_plug_in_1 = note.set
    context_setting_component_plug_in_2 = eval(repr(context_setting_component_plug_in_1))

    assert isinstance(context_setting_component_plug_in_1, LilyPondContextSettingComponentPlugIn)
    assert isinstance(context_setting_component_plug_in_2, LilyPondContextSettingComponentPlugIn)


def test_LilyPondContextSettingComponentPlugIn___repr___02():
    '''LilyPond context setting component plug-in looks like this.
    '''

    note = Note("c'4")
    note.set.staff.tuplet_full_length = True

    assert repr(note.set) == \
        'LilyPondContextSettingComponentPlugIn(staff__tuplet_full_length = True)'
