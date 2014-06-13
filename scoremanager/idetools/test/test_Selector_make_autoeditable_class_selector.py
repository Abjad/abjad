# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
session = scoremanager.idetools.Session(is_test=True)


def test_Selector_make_autoeditable_class_selector_01():

    selector = scoremanager.idetools.Selector(session=session)
    selector = selector.make_autoeditable_class_selector()
    selector._session._pending_input = 'MarkupInventory'
    result = selector._run()

    assert result == markuptools.MarkupInventory