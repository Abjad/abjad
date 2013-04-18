from abjad import *
from experimental import *


def test_PerformerEditor_name_01():
    '''Quit, back and studio all work.
    '''

    studio = scoremanagementtools.studio.Studio()
    studio.run(user_input='example~score~i setup performers hornist name q')
    assert studio.ts == (11,)

    studio.run(user_input='example~score~i setup performers hornist name b q')
    assert studio.ts == (13, (8, 11))

    studio.run(user_input='example~score~i setup performers hornist name studio q')
    assert studio.ts == (13, (0, 11))


def test_PerformerEditor_name_02():
    '''String input only.
    '''

    studio = scoremanagementtools.studio.Studio()
    studio.run(user_input='example~score~i setup performers hornist name -99 q')
    assert studio.ts == (13,)


def test_PerformerEditor_name_03():
    '''Create, name and rename performer.
    '''

    editor = scoremanagementtools.editors.PerformerEditor()
    editor.run(user_input='name foo name bar q')
    assert editor.target == scoretools.Performer(name='bar')
