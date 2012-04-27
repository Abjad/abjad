from abjad import *


def test_Component_id_string_01():
    '''Return component name if it exists, otherwise Python ID.'''

    t = Staff("c'8 d'8 e'8 f'8")
    assert t._id_string.startswith('Staff-')


def test_Component_id_string_02():
    '''Return component name if it exists, otherwise Python ID.'''

    t = Staff("c'8 d'8 e'8 f'8")
    t.name = 'foo'
    assert t._id_string == "Staff-'foo'"
