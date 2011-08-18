from abjad import *


def test_Component__ID_01():
    '''Return component name if it exists, otherwise Python ID.'''

    t = Staff("c'8 d'8 e'8 f'8")
    assert t._ID.startswith('Staff-')


def test_Component__ID_02():
    '''Return component name if it exists, otherwise Python ID.'''

    t = Staff("c'8 d'8 e'8 f'8")
    t.name = 'foo'
    assert t._ID == 'Staff-foo'
