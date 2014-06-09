# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
session = scoremanager.iotools.Session(is_test=True)


def test_Selector__run_01():

    items=['apple', 'banana', 'cherry']
    selector = scoremanager.iotools.Selector(
        items=items,
        session=session,
        )
    selector._session._is_test = True

    assert selector._run(input_='apple') == 'apple'
    assert selector._run(input_='banana') == 'banana'
    assert selector._run(input_='cherry') == 'cherry'


def test_Selector__run_02():

    items = instrumenttools.UntunedPercussion.known_untuned_percussion[:]
    selector = scoremanager.iotools.Selector(
        items=items,
        session=session,
        )
    selector._session._is_test = True

    assert selector._run(input_='cax') == 'caxixi'