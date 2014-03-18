# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_Selector_make_clef_name_selector_01():

    Selector = scoremanager.iotools.Selector
    selector = Selector.make_clef_name_selector()
    selector._session._is_test = True

    input_ = 'tre'
    assert selector._run(pending_user_input=input_) == 'treble'
