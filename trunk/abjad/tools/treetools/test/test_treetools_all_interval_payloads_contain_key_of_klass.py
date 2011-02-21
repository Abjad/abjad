import py.test
from fractions import Fraction
from abjad.tools.treetools import *
from abjad.tools.treetools._make_test_blocks import _make_test_blocks


def test_treetools_all_interval_payloads_contain_key_of_klass_01( ):
    a = BoundedInterval(0, 10, data = 1)
    b = BoundedInterval(5, 15, data = 'hello')
    c = BoundedInterval(10, 20, data = {'dog': 'cat'})
    tree = IntervalTree([a, b, c])
    assert not all_interval_payloads_contain_key_of_klass(tree, 'fish', int)

def test_treetools_all_interval_payloads_contain_key_of_klass_02( ):
    tree = IntervalTree([ ])
    a = BoundedInterval(0, 10, data = {'fish': 1})
    b = BoundedInterval(5, 15, data = {'frog': Fraction(2, 3)})
    c = BoundedInterval(10, 20, data = {'dog': 'cat'})
    tree = IntervalTree([a, b, c])
    assert not all_interval_payloads_contain_key_of_klass(tree, 'fish', int)

def test_treetools_all_interval_payloads_contain_key_of_klass_03( ):
    tree = IntervalTree([ ])
    a = BoundedInterval(0, 10, data = {'fish': 1})
    b = BoundedInterval(5, 15, data = {'fish': Fraction(2, 3)})
    c = BoundedInterval(10, 20, data = {'fish': 'cat'})
    tree = IntervalTree([a, b, c])
    assert not all_interval_payloads_contain_key_of_klass(tree, 'fish', int)

def test_treetools_all_interval_payloads_contain_key_of_klass_04( ):
    tree = IntervalTree([ ])
    a = BoundedInterval(0, 10, data = {'fish': 1})
    b = BoundedInterval(5, 15, data = {'fish': 2})
    c = BoundedInterval(10, 20, data = {'fish': 3})
    tree = IntervalTree([a, b, c])
    assert not not all_interval_payloads_contain_key_of_klass(tree, 'fish', int)
