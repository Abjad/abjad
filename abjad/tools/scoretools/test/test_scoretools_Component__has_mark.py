# -*- encoding: utf-8 -*-
from abjad import *


def test_scoretools_Component__has_mark_01():

    staff = Staff("c'2 d'2")
    annotation = marktools.Annotation('name', 'value')
    attach(annotation, staff[0])

    assert staff[0]._has_indicator(marktools.Annotation)
    assert not staff[1]._has_indicator(marktools.Annotation)


def test_scoretools_Component__has_mark_02():

    staff = Staff("c'2 d'2")
    articulation = Articulation('staccato')
    attach(articulation, staff[0])

    staff[0]._has_mark(Articulation)
    assert not staff[1]._has_mark(Articulation)


def test_scoretools_Component__has_mark_03():

    staff = Staff("c'8 d'8 e'8 f'8")
    command = marktools.LilyPondCommand('break', 'closing')
    attach(command, staff[-1])

    assert not staff[0]._has_indicator(marktools.LilyPondCommand)
    assert not staff[1]._has_indicator(marktools.LilyPondCommand)
    assert not staff[2]._has_indicator(marktools.LilyPondCommand)
    assert     staff[3]._has_indicator(marktools.LilyPondCommand)


def test_scoretools_Component__has_mark_04():

    staff = Staff("c'2 d'2")
    comment = marktools.LilyPondComment('comment')
    attach(comment, staff[0])

    assert staff[0]._has_indicator(marktools.LilyPondComment)
    assert not staff[1]._has_indicator(marktools.LilyPondComment)


def test_scoretools_Component__has_mark_05():

    staff = Staff("c'2 d'2")
    stem_tremolo = marktools.StemTremolo(16)
    attach(stem_tremolo, staff[0])

    assert staff[0]._has_indicator(marktools.StemTremolo)
    assert not staff[1]._has_indicator(marktools.StemTremolo)


def test_scoretools_Component__has_mark_06():

    staff = Staff("c'8 d'8 e'8 f'8")
    time_signature = TimeSignature((4, 8))
    attach(time_signature, staff[0])

    assert staff[0]._has_mark(marktools.ContextMark)
    assert not staff[1]._has_mark(marktools.ContextMark)
    assert not staff[2]._has_mark(marktools.ContextMark)
    assert not staff[3]._has_mark(marktools.ContextMark)
    assert not staff._has_mark(marktools.ContextMark)
