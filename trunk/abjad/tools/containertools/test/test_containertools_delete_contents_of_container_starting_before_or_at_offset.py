# -*- encoding: utf-8 -*-
from abjad import *


def test_containertools_delete_contents_of_container_starting_before_or_at_offset_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(staff.select_leaves())
    containertools.delete_contents_of_container_starting_before_or_at_offset(staff, Duration(1, 8))

    r'''
    \new Staff {
        e'8 [
        f'8 ]
    }
    '''

    assert select(staff).is_well_formed()
    assert testtools.compare(
        staff.lilypond_format,
        r'''
        \new Staff {
            e'8 [
            f'8 ]
        }
        '''
        )


def test_containertools_delete_contents_of_container_starting_before_or_at_offset_02():

    staff = Staff("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(staff.select_leaves())
    containertools.delete_contents_of_container_starting_before_or_at_offset(staff, Duration(3, 16))

    r'''
    \new Staff {
        e'8 [
        f'8 ]
    }
    '''

    assert select(staff).is_well_formed()
    assert testtools.compare(
        staff.lilypond_format,
        r'''
        \new Staff {
            e'8 [
            f'8 ]
        }
        '''
        )


def test_containertools_delete_contents_of_container_starting_before_or_at_offset_03():
    r'''Delete nothing when no contents start after prolated offset.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(staff.select_leaves())
    containertools.delete_contents_of_container_starting_before_or_at_offset(staff, -99)

    r'''
    \new Staff {
        c'8 [
        d'8
        e'8
        f'8 ]
    }
    '''

    assert select(staff).is_well_formed()
    assert testtools.compare(
        staff.lilypond_format,
        r'''
        \new Staff {
            c'8 [
            d'8
            e'8
            f'8 ]
        }
        '''
        )


def test_containertools_delete_contents_of_container_starting_before_or_at_offset_04():
    r'''Delete everything when all contents start after prolated offset.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(staff.select_leaves())
    containertools.delete_contents_of_container_starting_before_or_at_offset(staff, 99)

    r'''
    \new Staff {
    }
    '''

    assert select(staff).is_well_formed()
    assert testtools.compare(
        staff.lilypond_format,
        '\\new Staff {\n}'
        )
