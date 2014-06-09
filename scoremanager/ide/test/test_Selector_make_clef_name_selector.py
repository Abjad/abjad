# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
session = scoremanager.ide.Session(is_test=True)


def test_Selector_make_clef_name_selector_01():

    selector = scoremanager.ide.Selector(session=session)
    selector = selector.make_clef_name_selector()
    selector._session._is_test = True

    input_ = 'tre'
    assert selector._run(input_=input_) == 'treble'