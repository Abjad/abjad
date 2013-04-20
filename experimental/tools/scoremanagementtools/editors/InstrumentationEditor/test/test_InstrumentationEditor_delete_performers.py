from abjad import *
from experimental import *


def test_InstrumentationEditor_delete_performers_01():
    '''Quit, back, studio, score & junk all work.
    '''

    studio = scoremanagementtools.studio.ScoreManager()
    studio.run(user_input='example~score~i setup performers rm q')
    assert studio.ts == (9,)

    studio.run(user_input='example~score~i setup performers rm b q')
    assert studio.ts == (11, (6, 9))

    studio.run(user_input='example~score~i setup performers rm studio q')
    assert studio.ts == (11, (0, 9))

    studio.run(user_input='example~score~i setup performers rm score q')
    assert studio.ts == (11, (2, 9))

    studio.run(user_input='example~score~i setup performers rm foo q')
    assert studio.ts == (11,)


def test_InstrumentationEditor_delete_performers_02():
    '''Add three performers. Delete two.
    '''

    editor = scoremanagementtools.editors.InstrumentationEditor()
    editor.run(user_input='add acc default add bass default add bassoon default rm 3 rm 2 q')
    assert editor.target == scoretools.InstrumentationSpecifier(
        [scoretools.Performer('accordionist', instruments=[instrumenttools.Accordion()])])


def test_InstrumentationEditor_delete_performers_03():
    '''Range handling.
    '''

    editor = scoremanagementtools.editors.InstrumentationEditor()
    editor.run(user_input='add 1-3 default default default rm 3-2 q')
    assert editor.target == scoretools.InstrumentationSpecifier(
        [scoretools.Performer('accordionist', instruments=[instrumenttools.Accordion()])])
