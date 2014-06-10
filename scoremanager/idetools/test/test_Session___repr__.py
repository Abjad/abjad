# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_Session___repr___01():

    session = scoremanager.idetools.Session(input_='foo')
    string = "Session(initial_input_='foo',"
    string += " input_='foo')"
    assert repr(session) == string