# -*- coding: utf-8 -*-
import abjad


def test_scoretools_Staff___init___01():
    r'''Initialize with context name.
    '''

    staff = abjad.Staff(context_name='BlueStaff')
    assert staff.context_name == 'BlueStaff'


def test_scoretools_Staff___init___02():
    r'''Initialize with name.
    '''

    staff = abjad.Staff(name='FirstBlueStaff')
    assert staff.name == 'FirstBlueStaff'


def test_scoretools_Staff___init___03():
    r'''Initialize with both context name and name.
    '''

    staff = abjad.Staff(context_name='BlueStaff', name='FirstBlueStaff')
    assert staff.context_name == 'BlueStaff'
    assert staff.name == 'FirstBlueStaff'
