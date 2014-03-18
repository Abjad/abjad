# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_Selector_make_rhythm_maker_class_name_selector_01():

    session = scoremanager.core.Session(is_test=True)
    selector = scoremanager.iotools.Selector
    selector = selector.make_rhythm_maker_class_name_selector(session=session)
    selector._session._is_test = True

    input_ = 'note'
    result = selector._run(pending_user_input=input_)
    assert result == 'NoteRhythmMaker'
