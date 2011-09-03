from abjad import *
import py.test


def test_Container___cmp___01():
    '''Compare container to itself.
    '''

    container = Container([])

    assert container == container
    assert not container != container

    comparison_string = 'container <  container'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'container <= container'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'container >  container'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'container >= container'
    assert py.test.raises(NotImplementedError, comparison_string)


def test_Container___cmp___02():
    '''Compare containers.
    '''

    container_1 = Container([])
    container_2 = Container([])

    assert not container_1 == container_2
    assert      container_1 != container_2

    comparison_string = 'container_1 <  container_2'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'container_1 <= container_2'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'container_1 >  container_2'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'container_1 >= container_2'
    assert py.test.raises(NotImplementedError, comparison_string)


def test_Container___cmp___03():
    '''Compare container to foreign type.
    '''

    container = Container([])

    assert not container == 'foo'
    assert      container != 'foo'

    comparison_string = "container <  'foo'"
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = "container <= 'foo'"
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = "container >  'foo'"
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = "container >= 'foo'"
    assert py.test.raises(NotImplementedError, comparison_string)


def test_Container___cmp___04():
    '''Compare nonempty containers.
    '''

    container_1 = Container("c'8 d'8 e'8")
    container_2 = Container("c'8 d'8 e'8")

    assert not container_1 == container_2
    assert      container_1 != container_2

    comparison_string = 'container_1 <  container_2'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'container_1 <= container_2'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'container_1 >  container_2'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'container_1 >= container_2'
    assert py.test.raises(NotImplementedError, comparison_string)


def test_Container___cmp___05():
    '''Compare nonempty containers.
    '''

    container_1 = Container("c'8 d'8 e'8")
    container_2 = Container("f'8 g'8 a'8")

    assert not container_1 == container_2
    assert      container_1 != container_2

    comparison_string = 'container_1 <  container_2'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'container_1 <= container_2'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'container_1 >  container_2'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'container_1 >= container_2'
    assert py.test.raises(NotImplementedError, comparison_string)
