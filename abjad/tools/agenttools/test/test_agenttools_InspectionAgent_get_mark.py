# -*- encoding: utf-8 -*-
from abjad import *
import pytest


def test_agenttools_InspectionAgent_get_mark_01():

    note = Note("c'8")
    annotation = marktools.Annotation('special information')
    attach(annotation, note)

    assert inspect(note).get_attached_item(marktools.Annotation) is annotation


def test_agenttools_InspectionAgent_get_mark_02():

    note = Note("c'8")

    statement = 'inspect(note).get_attached_item(marktools.Annotation)'
    assert pytest.raises(Exception, statement)


def test_agenttools_InspectionAgent_get_mark_03():

    note = Note("c'8")
    annotation = marktools.Annotation('special information')
    attach(annotation, note)
    annotation = marktools.Annotation('more special information')
    attach(annotation, note)

    statement = 'inspect(note).get_attached_item(marktools.Annotation)',
    assert pytest.raises(Exception, statement)


def test_agenttools_InspectionAgent_get_mark_04():

    note = Note("c'8")
    articulation = Articulation('staccato')
    attach(articulation, note)

    assert inspect(note).get_mark(Articulation) is articulation


def test_agenttools_InspectionAgent_get_mark_05():

    note = Note("c'8")

    statement = 'inspect(note).get_mark(Articulation)',
    assert pytest.raises(Exception, statement)


def test_agenttools_InspectionAgent_get_mark_06():

    note = Note("c'8")
    articulation = Articulation('staccato')
    attach(articulation, note)
    articulation = Articulation('marcato')
    attach(articulation, note)

    statement = 'inspect(note).get_mark(Articulation)',
    assert pytest.raises(Exception, statement)


def test_agenttools_InspectionAgent_get_mark_07():

    note = Note("c'8")
    command = marktools.LilyPondCommand('stemUp')
    attach(command, note)

    assert inspect(note).get_mark(marktools.LilyPondCommand) is command


def test_agenttools_InspectionAgent_get_mark_08():

    note = Note("c'8")

    statement = 'inspect(note).get_mark(marktools.LilyPondCommand)'
    assert pytest.raises(Exception, statement)


def test_agenttools_InspectionAgent_get_mark_09():

    note = Note("c'8")
    command = marktools.LilyPondCommand('stemUp')
    attach(command, note)
    command = marktools.LilyPondCommand('slurUp')
    attach(command, note)

    statement = 'inspect(note).get_mark(marktools.LilyPondCommand)'
    assert pytest.raises(Exception, statement)


def test_agenttools_InspectionAgent_get_mark_10():

    staff = Staff("c'8 d'8 e'8 f'8")
    slur = Slur()
    attach(slur, staff.select_leaves())
    command_1 = marktools.LilyPondCommand('slurDotted')
    attach(command_1, staff[0])
    command_2 = marktools.LilyPondCommand('slurUp')
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

    marks = inspect(staff[0]).get_marks(marktools.LilyPondCommand)

    assert command_1 in marks
    assert command_2 in marks
    assert len(marks) == 2


def test_agenttools_InspectionAgent_get_mark_11():

    note = Note("c'8")
    comment = marktools.LilyPondComment('comment')
    attach(comment, note)

    mark = inspect(note).get_mark(marktools.LilyPondComment) 
    assert mark is comment


def test_agenttools_InspectionAgent_get_mark_12():

    note = Note("c'8")

    statement = 'inspect(note).get_mark(marktools.LilyPondComment)'
    assert pytest.raises(Exception, statement)


def test_agenttools_InspectionAgent_get_mark_13():

    note = Note("c'8")
    comment = marktools.LilyPondComment('comment')
    attach(comment, note)
    comment = marktools.LilyPondComment('another comment')
    attach(comment, note)

    statement = 'inspect(note).get_mark(marktools.LilyPondComment)'
    assert pytest.raises(Exception, statement)


def test_agenttools_InspectionAgent_get_mark_14():

    note = Note("c'8")
    mark = marktools.Mark()
    attach(mark, note)

    assert inspect(note).get_mark() is mark


def test_agenttools_InspectionAgent_get_mark_15():

    note = Note("c'8")

    assert pytest.raises(Exception, 'inspect(note).get_mark()')


def test_agenttools_InspectionAgent_get_mark_16():

    note = Note("c'8")
    mark = marktools.Mark()
    attach(mark, note)
    mark = marktools.Mark()
    attach(mark, note)

    assert pytest.raises(Exception, 'inspect(note).get_mark()')


def test_agenttools_InspectionAgent_get_mark_17():

    note = Note("c'4")
    stem_tremolo = marktools.StemTremolo(16)
    attach(stem_tremolo, note)
    stem_tremolo = inspect(note).get_mark(marktools.StemTremolo)

    assert stem_tremolo is stem_tremolo


def test_agenttools_InspectionAgent_get_mark_18():

    staff = Staff("c'8 d'8 e'8 f'8")
    violin = instrumenttools.Violin()
    attach(violin, staff)

    found_instrument_mark = inspect(staff).get_mark(instrumenttools.Instrument)

    assert found_instrument_mark is violin


def test_agenttools_InspectionAgent_get_mark_19():

    measure = Measure((4, 8), "c'8 d'8 e'8 f'8")
    time_signature = inspect(measure).get_mark(TimeSignature)

    assert time_signature == TimeSignature((4, 8))
