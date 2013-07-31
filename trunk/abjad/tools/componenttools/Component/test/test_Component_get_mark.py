# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_Component_get_mark_01():

    note = Note("c'8")
    annotation = marktools.Annotation('special information')(note)

    assert note.get_mark(marktools.Annotation) is annotation


def test_Component_get_mark_02():

    note = Note("c'8")

    assert py.test.raises(MissingMarkError,
        'note.get_mark(marktools.Annotation)')


def test_Component_get_mark_03():

    note = Note("c'8")
    marktools.Annotation('special information')(note)
    marktools.Annotation('more special information')(note)

    assert py.test.raises(ExtraMarkError, 
        'note.get_mark(marktools.Annotation)')


def test_Component_get_mark_04():

    note = Note("c'8")
    articulation = marktools.Articulation('staccato')(note)

    assert note.get_mark(marktools.Articulation) is articulation


def test_Component_get_mark_05():

    note = Note("c'8")

    assert py.test.raises(MissingMarkError,
        'note.get_mark(marktools.Articulation)')


def test_Component_get_mark_06():

    note = Note("c'8")
    marktools.Articulation('staccato')(note)
    marktools.Articulation('marcato')(note)

    assert py.test.raises(ExtraMarkError,
        'note.get_mark(marktools.Articulation)')


def test_Component_get_mark_07():

    note = Note("c'8")
    lilypond_command_mark = marktools.LilyPondCommandMark('stemUp')(note)

    assert note.get_mark(marktools.LilyPondCommandMark) is \
        lilypond_command_mark


def test_Component_get_mark_08():

    note = Note("c'8")

    assert py.test.raises(MissingMarkError,
        'note.get_mark(marktools.LilyPondCommandMark)')


def test_Component_get_mark_09():

    note = Note("c'8")
    marktools.LilyPondCommandMark('stemUp')(note)
    marktools.LilyPondCommandMark('slurUp')(note)

    assert py.test.raises(ExtraMarkError,
        'note.get_mark(marktools.LilyPondCommandMark)')


def test_Component_get_mark_10():

    staff = Staff("c'8 d'8 e'8 f'8")
    slur = spannertools.SlurSpanner(staff.select_leaves())
    lilypond_command_mark_1 = marktools.LilyPondCommandMark('slurDotted')(staff[0])
    lilypond_command_mark_2 = marktools.LilyPondCommandMark('slurUp')(staff[0])

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

    marks = staff[0].get_marks(marktools.LilyPondCommandMark)

    assert lilypond_command_mark_1 in marks
    assert lilypond_command_mark_2 in marks
    assert len(marks) == 2


def test_Component_get_mark_11():

    note = Note("c'8")
    lilypond_comment = marktools.LilyPondComment('comment')(note)

    assert note.get_mark(marktools.LilyPondComment) is lilypond_comment


def test_Component_get_mark_12():

    note = Note("c'8")

    assert py.test.raises(MissingMarkError,
        'note.get_mark(marktools.LilyPondComment)')


def test_Component_get_mark_13():

    note = Note("c'8")
    marktools.LilyPondComment('comment')(note)
    marktools.LilyPondComment('another comment')(note)

    assert py.test.raises(ExtraMarkError,
        'note.get_mark(marktools.LilyPondComment)')


def test_Component_get_mark_14():

    note = Note("c'8")
    mark = marktools.Mark()(note)

    assert note.get_mark() is mark


def test_Component_get_mark_15():

    note = Note("c'8")

    assert py.test.raises(MissingMarkError, 'note.get_mark()')


def test_Component_get_mark_16():

    note = Note("c'8")
    marktools.Mark()(note)
    marktools.Mark()(note)

    assert py.test.raises(ExtraMarkError, 'note.get_mark()')


def test_Component_get_mark_17():

    note = Note("c'4")
    stem_tremolo = marktools.StemTremolo(16)(note)
    stem_tremolo = note.get_mark(marktools.StemTremolo)

    assert stem_tremolo is stem_tremolo


def test_Component_get_mark_18():

    staff = Staff("c'8 d'8 e'8 f'8")
    instrument_mark = contexttools.InstrumentMark('Violin ', 'Vn. ')
    instrument_mark.attach(staff)

    found_instrument_mark = staff.get_mark(contexttools.InstrumentMark)

    assert found_instrument_mark is instrument_mark


def test_Component_get_mark_19():

    measure = Measure((4, 8), "c'8 d'8 e'8 f'8")
    time_signature_mark = measure.get_mark(contexttools.TimeSignatureMark)

    assert time_signature_mark == contexttools.TimeSignatureMark((4, 8))
