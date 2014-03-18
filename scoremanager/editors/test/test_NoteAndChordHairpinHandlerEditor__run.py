# -*- encoding: utf-8 -*-
from abjad import *
from experimental import *
import scoremanager


def test_NoteAndChordHairpinHandlerEditor__run_01():

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.NoteAndChordHairpinHandlerEditor
    editor = editor(session=session)
    input_ = "1 ('p', '<', 'f') Duration(1, 8) q"
    editor._run(pending_user_input=input_, is_autoadvancing=True)

    handler = handlertools.NoteAndChordHairpinHandler(
        hairpin_token=('p', '<', 'f'),
        minimum_duration=Duration(1, 8),
        )

    assert editor.target == handler
