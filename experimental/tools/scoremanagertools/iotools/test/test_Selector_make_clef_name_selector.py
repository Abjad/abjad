# -*- encoding: utf-8 -*-
from experimental import *


def test_Selector_make_clef_name_selector_01():

    Selector = scoremanagertools.iotools.Selector
    selector = Selector.make_clef_name_selector()

    assert selector._run(pending_user_input='tre') == 'treble'
