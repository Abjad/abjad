# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_Editor__run_01():

    session = scoremanager.core.Session(is_test=True)
    clef = Clef('alto')
    editor = scoremanager.editors.Editor(
        session=session,
        target=clef,
        )
    input_ = 'nm tenor done'
    editor._run(pending_user_input=input_)

    assert editor.target == Clef('tenor')