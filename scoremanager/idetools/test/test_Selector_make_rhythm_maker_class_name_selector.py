# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
session = scoremanager.idetools.Session(is_test=True)


def test_Selector_make_rhythm_maker_class_name_selector_01():

    selector = scoremanager.idetools.Selector(session=session)
    selector = selector.make_rhythm_maker_class_name_selector()
    selector._session._is_test = True
    selector._session._pending_input = 'note'

    result = selector._run()
    assert result == 'NoteRhythmMaker'