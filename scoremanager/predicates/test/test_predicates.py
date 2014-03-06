# -*- encoding: utf-8 -*-
from scoremanager.predicates import predicates


def test_predicates_01():

    assert predicates.is_boolean(True)
    assert predicates.is_boolean(False)

    assert not predicates.is_boolean(None)
    assert not predicates.is_boolean('')
    assert not predicates.is_boolean(0)
    assert not predicates.is_boolean(1)
