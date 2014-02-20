# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_Session___repr___01():

    _session = scoremanager.core.Session(pending_user_input='foo')
    string = "Session(initial_pending_user_input='foo',"
    string += " pending_user_input='foo')"
    assert repr(_session) == string
