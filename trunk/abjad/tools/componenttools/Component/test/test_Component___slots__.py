from abjad import *
from abjad.tools.componenttools.Component import Component
import py.test


def test_Component___slots___01():
    '''Slots constraint component attributes.
    '''

    _component = Component()

    assert py.test.raises(AttributeError, "_component.foo = 'bar'")
