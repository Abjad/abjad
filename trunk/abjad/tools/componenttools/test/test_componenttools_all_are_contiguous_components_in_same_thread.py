from abjad import *
import py.test


def test_componenttools_all_are_contiguous_components_in_same_thread_01():
    '''True for strictly contiguous leaves in same staff.'''

    t = Staff("c'8 d'8 e'8 f'8")
    assert componenttools.all_are_contiguous_components_in_same_thread(t[:])


def test_componenttools_all_are_contiguous_components_in_same_thread_02():
    '''True for orphan components when allow_orphans is True.
        False for orphan components when allow_orphans is False.'''

    notes = [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8")]
    assert componenttools.all_are_contiguous_components_in_same_thread(notes)
    assert not componenttools.all_are_contiguous_components_in_same_thread(notes, allow_orphans = False)


def test_componenttools_all_are_contiguous_components_in_same_thread_03():
    '''False for time reordered leaves in staff.'''

    t = Staff("c'8 d'8 e'8 f'8")
    assert not componenttools.all_are_contiguous_components_in_same_thread(t[2:] + t[:2],
        )


def test_componenttools_all_are_contiguous_components_in_same_thread_04():
    '''False for unincorporated component.'''

    assert componenttools.all_are_contiguous_components_in_same_thread([Staff("c'8 d'8 e'8 f'8")],
        )


def test_componenttools_all_are_contiguous_components_in_same_thread_05():
    '''True for empty list.'''

    assert componenttools.all_are_contiguous_components_in_same_thread([])
