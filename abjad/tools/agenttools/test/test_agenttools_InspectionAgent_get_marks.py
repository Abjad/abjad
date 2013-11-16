# -*- encoding: utf-8 -*-
from abjad import *


def test_agenttools_InspectionAgent_get_marks_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    slur = Slur()
    attach(slur, staff.select_leaves())
    command_1 = indicatortools.LilyPondCommand('slurDotted')
    attach(command_1, staff[0])
    command_2 = indicatortools.LilyPondCommand('slurUp')
    attach(command_2, staff[0])

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            \slurDotted
            \slurUp
            c'8 (
            d'8
            e'8
            f'8 )
        }
        '''
        )

    marks = inspect(staff[0]).get_indicators(indicatortools.LilyPondCommand)
    assert command_1 in marks
    assert command_2 in marks
    assert len(marks) == 2


def test_agenttools_InspectionAgent_get_marks_02():

    staff = Staff("c'8 d'8 e'8 f'8")
    slur = Slur()
    attach(slur, staff.select_leaves())
    comment = indicatortools.LilyPondComment('beginning of note content')
    attach(comment, staff[0])
    command = indicatortools.LilyPondCommand('slurDotted')
    attach(command, staff[0])

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            % beginning of note content
            \slurDotted
            c'8 (
            d'8
            e'8
            f'8 )
        }
        '''
        )

    items = inspect(staff[0]).get_indicators()
    assert comment in items
    assert command in items
    assert len(items) == 2


def test_agenttools_InspectionAgent_get_marks_03():

    staff = Staff("c'8 d'8 e'8 f'8")
    clef = Clef('treble')
    attach(clef, staff)
    dynamic = Dynamic('p')
    attach(dynamic, staff[0])

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            \clef "treble"
            c'8 \p
            d'8
            e'8
            f'8
        }
        '''
        )

    context_marks = inspect(staff[0]).get_marks(indicatortools.ContextMark)
    assert dynamic in context_marks
    assert len(context_marks) == 1


def test_agenttools_InspectionAgent_get_marks_04():

    staff = Staff("c'8 d'8 e'8 f'8")
    clef = Clef('treble')
    attach(clef, staff)
    dynamic = Dynamic('p')
    attach(dynamic, staff[0])

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            \clef "treble"
            c'8 \p
            d'8
            e'8
            f'8
        }
        '''
        )

    dynamics = inspect(staff[0]).get_marks(Dynamic)
    assert dynamic in dynamics
    assert len(dynamics) == 1


def test_agenttools_InspectionAgent_get_marks_05():

    staff = Staff("c'8 d'8 e'8 f'8")
    annotation_1 = indicatortools.Annotation('annotation 1')
    attach(annotation_1, staff[0])
    annotation_2 = indicatortools.Annotation('annotation 2')
    attach(annotation_2, staff[0])

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            c'8
            d'8
            e'8
            f'8
        }
        '''
        )

    annotations = inspect(staff[0]).get_indicators(indicatortools.Annotation)
    assert annotations == (annotation_1, annotation_2)


def test_agenttools_InspectionAgent_get_marks_06():

    staff = Staff("c'8 d'8 e'8 f'8")
    comment_1 = indicatortools.LilyPondComment('comment 1')
    attach(comment_1, staff[0])
    comment_2 = indicatortools.LilyPondComment('comment 2')
    attach(comment_2, staff[0])

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            % comment 1
            % comment 2
            c'8
            d'8
            e'8
            f'8
        }
        '''
        )

    marks = inspect(staff[0]).get_indicators(indicatortools.LilyPondComment)
    assert comment_1 in marks
    assert comment_2 in marks
    assert len(marks) == 2


def test_agenttools_InspectionAgent_get_marks_07():

    note = Note("c'4")
    stem_tremolo = indicatortools.StemTremolo(16)
    attach(stem_tremolo, note)
    stem_tremolos = inspect(note).get_indicators(indicatortools.StemTremolo)

    assert stem_tremolos[0] is stem_tremolo
