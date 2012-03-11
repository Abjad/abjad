from abjad import *
from abjad.tools.componenttools.Component import Component
import py.test


def testComponent___setattr___01():
    '''Slots constrain component attributes.
    '''

    component = Component()

    assert py.test.raises(AttributeError, "component.foo = 'bar'")
