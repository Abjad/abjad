# -*- encoding: utf-8 -*-
from abjad import *



def test_scoretools_Component__has_mark_01():

    staff = Staff("c'2 d'2")
    annotation = marktools.Annotation('name', 'value')
    attach(annotation, staff[0])

    assert staff[0]._has_mark(marktools.Annotation)
    assert not staff[1]._has_mark(marktools.Annotation)


def test_scoretools_Component__has_mark_02():

    staff = Staff("c'2 d'2")
    articulation = marktools.Articulation('staccato')
    attach(articulation, staff[0])

    staff[0]._has_mark(marktools.Articulation)
    assert not staff[1]._has_mark(marktools.Articulation)


def test_scoretools_Component__has_mark_03():

    staff = Staff("c'8 d'8 e'8 f'8")
    command = marktools.LilyPondCommandMark('break', 'closing')
    attach(command, staff[-1])

    assert not staff[0]._has_mark(marktools.LilyPondCommandMark)
    assert not staff[1]._has_mark(marktools.LilyPondCommandMark)
    assert not staff[2]._has_mark(marktools.LilyPondCommandMark)
    assert     staff[3]._has_mark(marktools.LilyPondCommandMark)



def test_scoretools_Component__has_mark_04():

    staff = Staff("c'2 d'2")
    comment = marktools.LilyPondComment('comment')
    attach(comment, staff[0])

    assert staff[0]._has_mark(marktools.LilyPondComment)
    assert not staff[1]._has_mark(marktools.LilyPondComment)


def test_scoretools_Component__has_mark_05():

    staff = Staff("c'2 d'2")
    mark = marktools.Mark()
    attach(mark, staff[0])

    assert staff[0]._has_mark()
    assert not staff[1]._has_mark()


def test_scoretools_Component__has_mark_06():

    staff = Staff("c'2 d'2")
    stem_tremolo = marktools.StemTremolo(16)
    attach(stem_tremolo, staff[0])

    assert staff[0]._has_mark(marktools.StemTremolo)
    assert not staff[1]._has_mark(marktools.StemTremolo)


def test_scoretools_Component__has_mark_07():

    staff = Staff("c'8 d'8 e'8 f'8")
    time_signature = contexttools.TimeSignatureMark((4, 8))
    attach(time_signature, staff[0])

    assert staff[0]._has_mark(contexttools.ContextMark)
    assert not staff[1]._has_mark(contexttools.ContextMark)
    assert not staff[2]._has_mark(contexttools.ContextMark)
    assert not staff[3]._has_mark(contexttools.ContextMark)
    assert not staff._has_mark(contexttools.ContextMark)
