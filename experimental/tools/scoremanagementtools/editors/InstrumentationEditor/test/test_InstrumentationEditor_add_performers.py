from abjad import *
from experimental import *


def test_InstrumentationEditor_add_performers_01():
    '''Quit, back, studio, score & junk all work.
    '''

    studio = scoremanagementtools.studio.Studio()
    studio.run(user_input='example~score~i setup performers add q')
    assert studio.ts == (10,)

    studio.run(user_input='example~score~i setup performers add b q')
    assert studio.ts == (12, (6, 10))

    studio.run(user_input='example~score~i setup performers add studio q')
    assert studio.ts == (12, (0, 10))

    studio.run(user_input='example~score~i setup performers add score q')
    assert studio.ts == (12, (2, 10))

    studio.run(user_input='example~score~i setup performers add foo q')
    assert studio.ts == (12, (8, 10))


def test_InstrumentationEditor_add_performers_02():
    '''Add three performers.
    '''

    editor = scoremanagementtools.editors.InstrumentationEditor()
    editor.run(user_input='add accordionist default add bassoonist default add cellist default q')
    assert editor.target == scoretools.InstrumentationSpecifier([
        scoretools.Performer(name='accordionist', instruments=[instrumenttools.Accordion()]),
        scoretools.Performer(name='bassoonist', instruments=[instrumenttools.Bassoon()]),
        scoretools.Performer(name='cellist', instruments=[instrumenttools.Cello()])])


def test_InstrumentationEditor_add_performers_03():
    '''Range handling.
    '''

    editor = scoremanagementtools.editors.InstrumentationEditor()
    editor.run(user_input='add 1-3 default default default q')
    assert editor.target == scoretools.InstrumentationSpecifier([
        scoretools.Performer(name='accordionist', instruments=[instrumenttools.Accordion()]),
        scoretools.Performer(name='baritone', instruments=[instrumenttools.BaritoneVoice()]),
        scoretools.Performer(name='bass', instruments=[instrumenttools.BassVoice()])])
