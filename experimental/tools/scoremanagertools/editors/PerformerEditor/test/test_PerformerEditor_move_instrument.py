from experimental import *
from abjad.tools.scoretools import Performer
from abjad.tools.instrumenttools import *


def test_PerformerEditor_move_instrument_01():
    '''Quit, back, home, score & junk all work.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager.run(user_input="l'arch setup performers flutist move q")
    assert score_manager.ts == (11,)

    score_manager.run(user_input="l'arch setup performers flutist move b q")
    assert score_manager.ts == (13, (8, 11))

    score_manager.run(user_input="l'arch setup performers flutist move home q")
    assert score_manager.ts == (13, (0, 11))

    score_manager.run(user_input="l'arch setup performers flutist move score q")
    assert score_manager.ts == (13, (2, 11))

    score_manager.run(user_input="l'arch setup performers flutist move foo q")
    assert score_manager.ts == (13,)


def test_PerformerEditor_move_instrument_02():
    '''Add two instruments. Move them.
    '''

    editor = scoremanagertools.editors.PerformerEditor()
    editor.run(user_input='add 1 add 2 move 1 2 q')
    assert editor.target == Performer(instruments=[AltoFlute(), Accordion()])
