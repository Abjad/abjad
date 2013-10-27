# -*- encoding: utf-8 -*-
from abjad import *



def test_componenttools_Component__has_mark_01():

    staff = Staff("c'2 d'2")
    marktools.Annotation('name', 'value')(staff[0])

    assert staff[0]._has_mark(marktools.Annotation)
    assert not staff[1]._has_mark(marktools.Annotation)


def test_componenttools_Component__has_mark_02():

    staff = Staff("c'2 d'2")
    marktools.Articulation('staccato')(staff[0])

    staff[0]._has_mark(marktools.Articulation)
    assert not staff[1]._has_mark(marktools.Articulation)


def test_componenttools_Component__has_mark_03():

    staff = Staff("c'8 d'8 e'8 f'8")
    marktools.LilyPondCommandMark('break', 'closing')(staff[-1])

    assert not staff[0]._has_mark(marktools.LilyPondCommandMark)
    assert not staff[1]._has_mark(marktools.LilyPondCommandMark)
    assert not staff[2]._has_mark(marktools.LilyPondCommandMark)
    assert     staff[3]._has_mark(marktools.LilyPondCommandMark)



def test_componenttools_Component__has_mark_04():

    staff = Staff("c'2 d'2")
    marktools.LilyPondComment('comment')(staff[0])

    assert staff[0]._has_mark(marktools.LilyPondComment)
    assert not staff[1]._has_mark(marktools.LilyPondComment)


def test_componenttools_Component__has_mark_05():

    staff = Staff("c'2 d'2")
    marktools.Mark()(staff[0])

    assert staff[0]._has_mark()
    assert not staff[1]._has_mark()


def test_componenttools_Component__has_mark_06():

    staff = Staff("c'2 d'2")
    marktools.StemTremolo(16)(staff[0])

    assert staff[0]._has_mark(marktools.StemTremolo)
    assert not staff[1]._has_mark(marktools.StemTremolo)


def test_componenttools_Component__has_mark_07():

    staff = Staff("c'8 d'8 e'8 f'8")
    contexttools.TimeSignatureMark((4, 8))(staff[0])

    assert staff[0]._has_mark(contexttools.ContextMark)
    assert not staff[1]._has_mark(contexttools.ContextMark)
    assert not staff[2]._has_mark(contexttools.ContextMark)
    assert not staff[3]._has_mark(contexttools.ContextMark)
    assert not staff._has_mark(contexttools.ContextMark)
