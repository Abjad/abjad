from experimental import *
from abjad.tools.scoretools import Performer
from abjad.tools.instrumenttools import *


def test_PerformerEditor_delete_instruments_01():
    '''Quit, back, studio, score & junk all work.
    '''

    studio = scoremanagementtools.studio.Studio()
    studio.run(user_input='1 setup perf 1 rm q')
    assert studio.ts == (11, (1, 7))

    studio.run(user_input='1 setup perf 1 rm b q')
    assert studio.ts == (13, (1, 7), (8, 11))

    studio.run(user_input='1 setup perf 1 rm studio q')
    assert studio.ts == (13, (0, 11), (1, 7))

    studio.run(user_input='1 setup perf 1 rm score q')
    assert studio.ts == (13, (1, 7), (2, 11))

    studio.run(user_input='1 setup perf 1 rm foo q')
    transcript = studio.transcript
    assert studio.ts == (13, (1, 7))


def test_PerformerEditor_delete_instruments_02():
    '''Add two instruments. Delete one.
    '''

    editor = scoremanagementtools.editors.PerformerEditor()
    editor.run(user_input='add flute add acc rm flute q')
    assert editor.target == Performer(instruments=[Accordion()])


def test_PerformerEditor_delete_instruments_03():
    '''Numeric range handling.
    '''

    editor = scoremanagementtools.editors.PerformerEditor()
    editor.run(user_input='add 1-3 rm 1,3 q')
    assert editor.target == Performer(instruments=[AltoFlute()])
