# -*- encoding: utf-8 -*-
from abjad import *


def test_ComponentInspector_get_marks_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    slur = spannertools.SlurSpanner(staff.select_leaves())
    lilypond_command_mark_1 = \
        marktools.LilyPondCommandMark('slurDotted')(staff[0])
    lilypond_command_mark_2 = \
        marktools.LilyPondCommandMark('slurUp')(staff[0])

    assert testtools.compare(
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

    marks = inspect(staff[0]).get_marks(marktools.LilyPondCommandMark)
    assert lilypond_command_mark_1 in marks
    assert lilypond_command_mark_2 in marks
    assert len(marks) == 2


def test_ComponentInspector_get_marks_02():

    staff = Staff("c'8 d'8 e'8 f'8")
    slur = spannertools.SlurSpanner(staff.select_leaves())
    comment_mark = \
        marktools.LilyPondComment('beginning of note content')(staff[0])
    lilypond_command_mark = \
        marktools.LilyPondCommandMark('slurDotted')(staff[0])

    assert testtools.compare(
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

    marks = inspect(staff[0]).get_marks()
    assert comment_mark in marks
    assert lilypond_command_mark in marks
    assert len(marks) == 2


def test_ComponentInspector_get_marks_03():

    staff = Staff("c'8 d'8 e'8 f'8")
    clef_mark = contexttools.ClefMark('treble')(staff)
    dynamic_mark = contexttools.DynamicMark('p')(staff[0])

    assert testtools.compare(
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

    context_marks = inspect(staff[0]).get_marks(contexttools.ContextMark)
    assert dynamic_mark in context_marks
    assert len(context_marks) == 1


def test_ComponentInspector_get_marks_04():

    staff = Staff("c'8 d'8 e'8 f'8")
    clef_mark = contexttools.ClefMark('treble')(staff)
    dynamic_mark = contexttools.DynamicMark('p')(staff[0])

    assert testtools.compare(
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

    dynamic_marks = inspect(staff[0]).get_marks(contexttools.DynamicMark)
    assert dynamic_mark in dynamic_marks
    assert len(dynamic_marks) == 1


def test_ComponentInspector_get_marks_05():

    staff = Staff("c'8 d'8 e'8 f'8")
    annotation_1 = marktools.Annotation('annotation 1')(staff[0])
    annotation_2 = marktools.Annotation('annotation 2')(staff[0])

    assert testtools.compare(
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

    annotations = inspect(staff[0]).get_marks(marktools.Annotation)
    assert annotations == (annotation_1, annotation_2)


def test_ComponentInspector_get_marks_06():

    staff = Staff("c'8 d'8 e'8 f'8")
    comment_mark_1 = marktools.LilyPondComment('comment 1')(staff[0])
    comment_mark_2 = marktools.LilyPondComment('comment 2')(staff[0])

    assert testtools.compare(
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

    marks = inspect(staff[0]).get_marks(marktools.LilyPondComment)
    assert comment_mark_1 in marks
    assert comment_mark_2 in marks
    assert len(marks) == 2


def test_ComponentInspector_get_marks_07():

    note = Note("c'4")
    stem_tremolo = marktools.StemTremolo(16)(note)
    stem_tremolos = inspect(note).get_marks(marktools.StemTremolo)

    assert stem_tremolos[0] is stem_tremolo
