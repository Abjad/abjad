# -*- encoding: utf-8 -*-
from experimental import *


def test_Selector_run_01():

    selector = scoremanager.iotools.Selector()
    selector.items = ['apple', 'banana', 'cherry']

    assert selector._run(pending_user_input='apple') == 'apple'
    assert selector._run(pending_user_input='banana') == 'banana'
    assert selector._run(pending_user_input='cherry') == 'cherry'


def test_Selector_run_02():

    selector = scoremanager.iotools.Selector()
    items = instrumenttools.UntunedPercussion.known_untuned_percussion[:]
    selector.items = items

    assert selector._run(pending_user_input='cax') == 'caxixi'
