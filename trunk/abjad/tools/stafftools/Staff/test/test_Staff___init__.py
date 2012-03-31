from abjad import *


def test_Staff___init___01():
    '''Initialize with context name.
    '''

    staff = Staff(context_name='BlueStaff')
    assert staff.context_name == 'BlueStaff'


def test_Staff___init___02():
    '''Initialize with name.
    '''

    staff = Staff(name='FirstBlueStaff')
    assert staff.name == 'FirstBlueStaff'


def test_Staff___init___03():
    '''Initialize with both context name and name.
    '''

    staff = Staff(context_name='BlueStaff', name='FirstBlueStaff')
    assert staff.context_name == 'BlueStaff'
    assert staff.name == 'FirstBlueStaff'
