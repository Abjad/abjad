# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import handlertools
import scoremanager


def test_NoteAndChordsHairpinHandler_autoedit_01():
    r'''Edits hairpins handler.
    '''

    session = scoremanager.idetools.Session(is_test=True)
    session._autoadvance_depth = 1
    target = handlertools.NoteAndChordHairpinsHandler()
    autoeditor = scoremanager.idetools.Autoeditor(
        session=session,
        target=target,
        )
    input_ = "[('p', '<', 'f')] Duration(1, 8) done"
    autoeditor._session._pending_input = input_
    autoeditor._run()

    handler = handlertools.NoteAndChordHairpinsHandler(
        hairpin_tokens=[('p', '<', 'f')],
        minimum_duration=Duration(1, 8),
        )

    assert autoeditor.target == handler