from abjad import *
import py.test


def test_containertools_delete_contents_of_container_01():
    '''Eject container contents.'''

    t = Staff("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(t)

    contents = containertools.delete_contents_of_container(t)

    assert len(t) == 0
    assert len(contents) == 4
    assert t.format == '\\new Staff {\n}'


def test_containertools_delete_contents_of_container_02():
    '''Eject container contents.'''

    t = Staff([])
    contents = containertools.delete_contents_of_container(t)

    assert len(t) == 0
    assert contents == []


def test_containertools_delete_contents_of_container_03():
    '''Raise type error on noncontainer.'''

    assert py.test.raises(TypeError, '''containertools.delete_contents_of_container(Note("c'4"))''')
