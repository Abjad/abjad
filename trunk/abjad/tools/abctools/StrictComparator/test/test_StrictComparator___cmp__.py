from abjad import *
from abjad.tools import abctools
import py


def test_StrictComparator___cmp___01():
    '''Mutable strict comparator.
    '''

    class Foo(abctools.MutableAbjadObject, abctools.StrictComparator):
        pass

    foo_1 = Foo()
    foo_2 = Foo() 

    foo_1.color = 'red'
    foo_2.color = 'red'

    assert not foo_1 == foo_2
    assert foo_1 != foo_2

    assert py.test.raises(Exception, 'foo_1 < foo_2')
    assert py.test.raises(Exception, 'foo_1 <= foo_2')
    assert py.test.raises(Exception, 'foo_1 > foo_2')
    assert py.test.raises(Exception, 'foo_1 >= foo_2')


def test_StrictComparator___cmp___02():
    '''Immutable strict comparator.
    '''

    class Foo(abctools.Immutable, abctools.StrictComparator):
        pass

    foo_1 = Foo()
    foo_2 = Foo() 

    assert py.test.raises(Exception, "foo_1.color = 'red'")
    assert py.test.raises(Exception, "foo_2.color = 'red'")

    assert not foo_1 == foo_2
    assert foo_1 != foo_2

    assert py.test.raises(Exception, 'foo_1 < foo_2')
    assert py.test.raises(Exception, 'foo_1 <= foo_2')
    assert py.test.raises(Exception, 'foo_1 > foo_2')
    assert py.test.raises(Exception, 'foo_1 >= foo_2')
