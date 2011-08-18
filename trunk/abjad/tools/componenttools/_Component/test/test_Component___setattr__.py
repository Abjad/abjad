from abjad import *
from abjad.tools.componenttools._Component import _Component
import py.test


def test_Component___setattr___01():
    '''Slots constrain component attributes.
    '''

    component = _Component()

    assert py.test.raises(AttributeError, "component.foo = 'bar'")
