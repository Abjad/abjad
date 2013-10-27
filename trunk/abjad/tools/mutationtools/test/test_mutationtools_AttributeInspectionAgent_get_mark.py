# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_mutationtools_AttributeInspectionAgent_get_mark_01():

    note = Note("c'8")
    annotation = marktools.Annotation('special information')
    annotation.attach(note)

    assert inspect(note).get_mark(marktools.Annotation) is annotation


def test_mutationtools_AttributeInspectionAgent_get_mark_02():

    note = Note("c'8")

    assert py.test.raises(
        MissingMarkError,
        'inspect(note).get_mark(marktools.Annotation)',
        )


def test_mutationtools_AttributeInspectionAgent_get_mark_03():

    note = Note("c'8")
    annotation = marktools.Annotation('special information')
    annotation.attach(note)
    annotation = marktools.Annotation('more special information')
    annotation.attach(note)

    assert py.test.raises(
        ExtraMarkError, 
        'inspect(note).get_mark(marktools.Annotation)',
        )


def test_mutationtools_AttributeInspectionAgent_get_mark_04():

    note = Note("c'8")
    articulation = marktools.Articulation('staccato')
    articulation.attach(note)

    assert inspect(note).get_mark(marktools.Articulation) is articulation


def test_mutationtools_AttributeInspectionAgent_get_mark_05():

    note = Note("c'8")

    assert py.test.raises(
        MissingMarkError,
        'inspect(note).get_mark(marktools.Articulation)',
        )


def test_mutationtools_AttributeInspectionAgent_get_mark_06():

    note = Note("c'8")
    articulation = marktools.Articulation('staccato')
    articulation.attach(note)
    articulation = marktools.Articulation('marcato')
    articulation.attach(note)

    assert py.test.raises(
        ExtraMarkError,
        'inspect(note).get_mark(marktools.Articulation)',
        )


def test_mutationtools_AttributeInspectionAgent_get_mark_07():

    note = Note("c'8")
    command = marktools.LilyPondCommandMark('stemUp')
    command.attach(note)

    assert inspect(note).get_mark(marktools.LilyPondCommandMark) is command


def test_mutationtools_AttributeInspectionAgent_get_mark_08():

    note = Note("c'8")

    assert py.test.raises(
        MissingMarkError,
        'inspect(note).get_mark(marktools.LilyPondCommandMark)',
        )


def test_mutationtools_AttributeInspectionAgent_get_mark_09():

    note = Note("c'8")
    command = marktools.LilyPondCommandMark('stemUp')
    command.attach(note)
    command = marktools.LilyPondCommandMark('slurUp')
    command.attach(note)

    assert py.test.raises(
        ExtraMarkError,
        'inspect(note).get_mark(marktools.LilyPondCommandMark)',
        )


def test_mutationtools_AttributeInspectionAgent_get_mark_10():

    staff = Staff("c'8 d'8 e'8 f'8")
    slur = spannertools.SlurSpanner()
    slur.attach(staff.select_leaves())
    command_1 = marktools.LilyPondCommandMark('slurDotted')
    command_1.attach(staff[0])
    command_2 = marktools.LilyPondCommandMark('slurUp')
    command_2.attach(staff[0])

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

    assert command_1 in marks
    assert command_2 in marks
    assert len(marks) == 2


def test_mutationtools_AttributeInspectionAgent_get_mark_11():

    note = Note("c'8")
    comment = marktools.LilyPondComment('comment')
    comment.attach(note)

    mark = inspect(note).get_mark(marktools.LilyPondComment) 
    assert mark is comment


def test_mutationtools_AttributeInspectionAgent_get_mark_12():

    note = Note("c'8")

    assert py.test.raises(
        MissingMarkError,
        'inspect(note).get_mark(marktools.LilyPondComment)',
        )


def test_mutationtools_AttributeInspectionAgent_get_mark_13():

    note = Note("c'8")
    comment = marktools.LilyPondComment('comment')
    comment.attach(note)
    comment = marktools.LilyPondComment('another comment')
    comment.attach(note)

    assert py.test.raises(
        ExtraMarkError,
        'inspect(note).get_mark(marktools.LilyPondComment)',
        )


def test_mutationtools_AttributeInspectionAgent_get_mark_14():

    note = Note("c'8")
    mark = marktools.Mark()
    mark.attach(note)

    assert inspect(note).get_mark() is mark


def test_mutationtools_AttributeInspectionAgent_get_mark_15():

    note = Note("c'8")

    assert py.test.raises(MissingMarkError, 'inspect(note).get_mark()')


def test_mutationtools_AttributeInspectionAgent_get_mark_16():

    note = Note("c'8")
    mark = marktools.Mark()
    mark.attach(note)
    mark = marktools.Mark()
    mark.attach(note)

    assert py.test.raises(ExtraMarkError, 'inspect(note).get_mark()')


def test_mutationtools_AttributeInspectionAgent_get_mark_17():

    note = Note("c'4")
    stem_tremolo = marktools.StemTremolo(16)
    stem_tremolo.attach(note)
    stem_tremolo = inspect(note).get_mark(marktools.StemTremolo)

    assert stem_tremolo is stem_tremolo


def test_mutationtools_AttributeInspectionAgent_get_mark_18():

    staff = Staff("c'8 d'8 e'8 f'8")
    violin = instrumenttools.Violin()
    violin.attach(staff)

    found_instrument_mark = inspect(staff).get_mark(instrumenttools.Instrument)

    assert found_instrument_mark is violin


def test_mutationtools_AttributeInspectionAgent_get_mark_19():

    measure = Measure((4, 8), "c'8 d'8 e'8 f'8")
    time_signature = inspect(measure).get_mark(contexttools.TimeSignatureMark)

    assert time_signature == contexttools.TimeSignatureMark((4, 8))
