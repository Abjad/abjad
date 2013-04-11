from experimental import *


def test_Selector_run_01():

    selector = scftools.selectors.Selector()
    selector.items = ['apple', 'banana', 'cherry']

    assert selector.run(user_input='1') == 'apple'
    assert selector.run(user_input='2') == 'banana'
    assert selector.run(user_input='3') == 'cherry'
