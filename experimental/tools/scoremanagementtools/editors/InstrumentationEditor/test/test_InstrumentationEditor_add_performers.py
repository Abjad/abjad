from abjad.tools.instrumenttools import *
from abjad.tools.scoretools import InstrumentationSpecifier
from abjad.tools.scoretools import Performer
from experimental import *


def test_InstrumentationEditor_add_performers_01():
    '''Quit, back, studio, score & junk all work.
    '''

    studio = scoremanagementtools.studio.Studio()
    studio.run(user_input='1 setup performers add q')
    assert studio.ts == (10,)

    studio.run(user_input='1 setup performers add b q')
    assert studio.ts == (12, (6, 10))

    studio.run(user_input='1 setup performers add studio q')
    assert studio.ts == (12, (0, 10))

    studio.run(user_input='1 setup performers add score q')
    assert studio.ts == (12, (2, 10))

    studio.run(user_input='1 setup performers add foo q')
    assert studio.ts == (12, (8, 10))


def test_InstrumentationEditor_add_performers_02():
    '''Add three performers.
    '''

    editor = scoremanagementtools.editors.InstrumentationEditor()
    editor.run(user_input='add accordionist default add bassoonist default add cellist default q')
    assert editor.target == InstrumentationSpecifier([
        Performer(name='accordionist', instruments=[Accordion()]),
        Performer(name='bassoonist', instruments=[Bassoon()]),
        Performer(name='cellist', instruments=[Cello()])])


def test_InstrumentationEditor_add_performers_03():
    '''Range handling.
    '''

    editor = scoremanagementtools.editors.InstrumentationEditor()
    editor.run(user_input='add 1-3 default default default q')
    assert editor.target == InstrumentationSpecifier([
        Performer(name='accordionist', instruments=[Accordion()]),
        Performer(name='baritone', instruments=[BaritoneVoice()]),
        Performer(name='bass', instruments=[BassVoice()])])
