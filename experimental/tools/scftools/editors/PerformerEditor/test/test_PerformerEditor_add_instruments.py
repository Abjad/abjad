from experimental import *
from abjad.tools.scoretools import Performer
from abjad.tools.instrumenttools import *


def test_PerformerEditor_add_instruments_01():
    '''Quit, back, studio, score & junk all work.
    '''

    studio = scftools.studio.Studio()
    studio.run(user_input='1 setup perf 1 add q')
    assert studio.ts == (12, (1, 7))

    studio.run(user_input='1 setup perf 1 add b q')
    assert studio.ts == (14, (1, 7), (8, 12))

    studio.run(user_input='1 setup perf 1 add studio q')
    assert studio.ts == (14, (0, 12), (1, 7))

    studio.run(user_input='1 setup perf 1 add score q')
    assert studio.ts == (14, (1, 7), (2, 12))

    studio.run(user_input='1 setup perf 1 add foo q')
    assert studio.ts == (14, (1, 7), (10, 12))


def test_PerformerEditor_add_instruments_02():
    '''Add two instruments.
    '''

    editor = scftools.editors.PerformerEditor()
    editor.run(user_input='add 1 add 2 q')
    assert editor.target == Performer(instruments=[Accordion(), AltoFlute()])


def test_PerformerEditor_add_instruments_03():
    '''Range handling.
    '''

    editor = scftools.editors.PerformerEditor()
    editor.run(user_input='add 1-2 q')
    assert editor.target == Performer(instruments=[Accordion(), AltoFlute()])
