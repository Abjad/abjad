from abjad import *
from abjad.tools import abctools
import py


def test_NonsortingIdEqualityAbjadObject___cmp___01():
    '''Mutable strict comparator.
    '''

    class Foo(abctools.NonsortingIdEqualityAbjadObject):
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


def test_NonsortingIdEqualityAbjadObject___cmp___02():
    '''ImmutableAbjadObject strict comparator.
    '''

    class Foo(abctools.ImmutableAbjadObject, abctools.NonsortingIdEqualityAbjadObject):
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
