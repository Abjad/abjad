from abjad import *


def test_marktools_is_component_with_lilypond_command_mark_attached_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    marktools.LilyPondCommandMark('break', 'closing')(staff[-1])
    f(staff)

    assert not marktools.is_component_with_lilypond_command_mark_attached(staff[0])
    assert not marktools.is_component_with_lilypond_command_mark_attached(staff[1])
    assert not marktools.is_component_with_lilypond_command_mark_attached(staff[2])
    assert      marktools.is_component_with_lilypond_command_mark_attached(staff[3])


def test_marktools_is_component_with_lilypond_command_mark_attached_02():

    staff = Staff("c'8 d'8 e'8 f'8")
    marktools.LilyPondCommandMark('break', 'closing')(staff[-1])
    f(staff)

    assert not marktools.is_component_with_lilypond_command_mark_attached(staff[0], 'break')
    assert not marktools.is_component_with_lilypond_command_mark_attached(staff[1], 'break')
    assert not marktools.is_component_with_lilypond_command_mark_attached(staff[2], 'break')
    assert      marktools.is_component_with_lilypond_command_mark_attached(staff[3], 'break')


def test_marktools_is_component_with_lilypond_command_mark_attached_03():

    staff = Staff("c'8 d'8 e'8 f'8")
    marktools.LilyPondCommandMark('break', 'closing')(staff[-1])
    f(staff)

    assert not marktools.is_component_with_lilypond_command_mark_attached(staff[0], 'foo')
    assert not marktools.is_component_with_lilypond_command_mark_attached(staff[1], 'foo')
    assert not marktools.is_component_with_lilypond_command_mark_attached(staff[2], 'foo')
    assert not marktools.is_component_with_lilypond_command_mark_attached(staff[3], 'foo')
