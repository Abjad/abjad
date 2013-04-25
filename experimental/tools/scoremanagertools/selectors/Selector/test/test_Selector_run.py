from experimental import *


def test_Selector_run_01():

    selector = scoremanagertools.selectors.Selector()
    selector.items = ['apple', 'banana', 'cherry']

    assert selector.run(user_input='apple') == 'apple'
    assert selector.run(user_input='banana') == 'banana'
    assert selector.run(user_input='cherry') == 'cherry'
