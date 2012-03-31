from abjad import *


def test_Staff___init___01():
    '''Initialize with context name.
    '''

    staff = Staff(context_name='BlueStaff')

    assert staff.context_name == 'BlueStaff'
