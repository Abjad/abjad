from abjad import *
import handlers


def test_NoteAndChordHairpinHandler___eq___01():

    handler_1 = handlers.dynamics.NoteAndChordHairpinHandler(
        hairpin_token=('p', '<', 'f'),
        minimum_prolated_duration=Duration(1, 8))

    handler_2 = handlers.dynamics.NoteAndChordHairpinHandler(
        hairpin_token=('p', '<', 'f'),
        minimum_prolated_duration=Duration(1, 8))

    handler_3 = handlers.dynamics.NoteAndChordHairpinHandler(
        hairpin_token=('pp', '<', 'p'),
        minimum_prolated_duration=Duration(1, 8))

    assert handler_1 == handler_1
    assert handler_1 == handler_2
    assert not handler_1 == handler_3
    assert handler_2 == handler_1
    assert handler_2 == handler_2
    assert not handler_2 == handler_3
    assert not handler_3 == handler_1
    assert not handler_3 == handler_2
    assert handler_3 == handler_3
