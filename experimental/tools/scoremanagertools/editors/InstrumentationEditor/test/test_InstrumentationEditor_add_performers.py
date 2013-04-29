from abjad import *
from experimental import *


def test_InstrumentationEditor_add_performers_01():
    '''Quit, back, home, score & junk all work.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager.run(user_input='example~score~i setup performers add q')
    assert score_manager.transcript_signature == (10,)

    score_manager.run(user_input='example~score~i setup performers add b q')
    assert score_manager.transcript_signature == (12, (6, 10))

    score_manager.run(user_input='example~score~i setup performers add home q')
    assert score_manager.transcript_signature == (12, (0, 10))

    score_manager.run(user_input='example~score~i setup performers add score q')
    assert score_manager.transcript_signature == (12, (2, 10))

    score_manager.run(user_input='example~score~i setup performers add foo q')
    assert score_manager.transcript_signature == (12, (8, 10))


def test_InstrumentationEditor_add_performers_02():
    '''Add three performers.
    '''

    editor = scoremanagertools.editors.InstrumentationEditor()
    editor.run(user_input='add accordionist default add bassoonist default add cellist default q')
    assert editor.target == scoretools.InstrumentationSpecifier([
        scoretools.Performer(name='accordionist', instruments=[instrumenttools.Accordion()]),
        scoretools.Performer(name='bassoonist', instruments=[instrumenttools.Bassoon()]),
        scoretools.Performer(name='cellist', instruments=[instrumenttools.Cello()])])


def test_InstrumentationEditor_add_performers_03():
    '''Range handling.
    '''

    editor = scoremanagertools.editors.InstrumentationEditor()
    editor.run(user_input='add 1-3 default default default q')
    assert editor.target == scoretools.InstrumentationSpecifier([
        scoretools.Performer(name='accordionist', instruments=[instrumenttools.Accordion()]),
        scoretools.Performer(name='baritone', instruments=[instrumenttools.BaritoneVoice()]),
        scoretools.Performer(name='bass', instruments=[instrumenttools.BassVoice()])])
