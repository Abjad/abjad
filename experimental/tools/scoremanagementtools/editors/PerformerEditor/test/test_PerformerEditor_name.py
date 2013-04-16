from experimental import *
from abjad import *


def test_PerformerEditor_name_01():
    '''Quit, back and studio all work.
    '''

    studio = scoremanagementtools.studio.Studio()
    studio.run(user_input='1 setup performers 1 name q')
    assert studio.ts == (11, (1, 7))

    studio.run(user_input='1 setup performers 1 name b q')
    assert studio.ts == (13, (1, 7), (8, 11))

    studio.run(user_input='1 setup performers 1 name studio q')
    assert studio.ts == (13, (0, 11), (1, 7))


def test_PerformerEditor_name_02():
    '''String input only.
    '''

    studio = scoremanagementtools.studio.Studio()
    studio.run(user_input='1 setup performers 1 name -99 q')
    assert studio.ts == (13, (1, 7))


def test_PerformerEditor_name_03():
    '''Create, name and rename performer.
    '''

    editor = scoremanagementtools.editors.PerformerEditor()
    editor.run(user_input='name foo name bar q')
    assert editor.target == scoretools.Performer(name='bar')
