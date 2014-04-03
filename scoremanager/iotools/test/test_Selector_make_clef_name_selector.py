# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_Selector_make_clef_name_selector_01():

    selector = scoremanager.iotools.Selector()
    selector = selector.make_clef_name_selector()
    selector._session._is_test = True

    input_ = 'tre'
    assert selector._run(pending_user_input=input_) == 'treble'