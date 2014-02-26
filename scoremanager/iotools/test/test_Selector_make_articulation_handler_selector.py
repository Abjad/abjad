# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_Selector_make_articulation_handler_selector_01():

    selector = scoremanager.iotools.Selector
    selector = selector.make_articulation_handler_selector()
    string = 'scoremanager.materials.example_articulation_handler'
    result = selector._run(pending_user_input=string) 

    package = 'scoremanager.materials.example_articulation_handler'
    assert result == package
