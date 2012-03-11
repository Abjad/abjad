from abjad import *
from abjad.tools.componenttools.Component import Component
import py.test


def test_Component___cmp___01():
    '''Compare component to itself.
    '''

    component = Component()

    assert component == component
    assert not component != component

    comparison_string = 'component <  component'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'component <= component'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'component >  component'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'component >= component'
    assert py.test.raises(NotImplementedError, comparison_string)


def test_Component___cmp___02():
    '''Compare components.
    '''

    component_1 = Component()
    component_2 = Component()

    assert not component_1 == component_2
    assert      component_1 != component_2

    comparison_string = 'component_1 <  component_2'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'component_1 <= component_2'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'component_1 >  component_2'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'component_1 >= component_2'
    assert py.test.raises(NotImplementedError, comparison_string)


def test_Component___cmp___03():
    '''Compare component to foreign type.
    '''

    component = Component()

    assert not component == 'foo'
    assert      component != 'foo'

    comparison_string = "component <  'foo'"
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = "component <= 'foo'"
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = "component >  'foo'"
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = "component >= 'foo'"
    assert py.test.raises(NotImplementedError, comparison_string)
