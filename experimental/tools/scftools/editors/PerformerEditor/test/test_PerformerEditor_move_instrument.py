from experimental import *
from abjad.tools.scoretools import Performer
from abjad.tools.instrumenttools import *


def test_PerformerEditor_move_instrument_01():
    '''Quit, back, studio, score & junk all work.
    '''

    studio = scftools.studio.Studio()
    studio.run(user_input="l'arch setup performers flutist move q")
    assert studio.ts == (11,)

    studio.run(user_input="l'arch setup performers flutist move b q")
    assert studio.ts == (13, (8, 11))

    studio.run(user_input="l'arch setup performers flutist move studio q")
    assert studio.ts == (13, (0, 11))

    studio.run(user_input="l'arch setup performers flutist move score q")
    assert studio.ts == (13, (2, 11))

    studio.run(user_input="l'arch setup performers flutist move foo q")
    assert studio.ts == (13,)


def test_PerformerEditor_move_instrument_02():
    '''Add two instruments. Move them.
    '''

    editor = scftools.editors.PerformerEditor()
    editor.run(user_input='add 1 add 2 move 1 2 q')
    assert editor.target == Performer(instruments=[AltoFlute(), Accordion()])
