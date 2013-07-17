from abjad import *


def test_Component_detach_marks_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    clef_mark = contexttools.ClefMark('treble')(staff)
    dynamic_mark = contexttools.DynamicMark('p')(staff[0])

    r'''
    \new Staff {
        \clef "treble"
        c'8 \p
        d'8
        e'8
        f'8
    }
    '''

    contexttools.detach_context_marks_attached_to_component(staff[0])

    r'''
    \new Staff {
        \clef "treble"
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert wellformednesstools.is_well_formed_component(staff)
    assert staff.lilypond_format == '\\new Staff {\n\t\\clef "treble"\n\tc\'8\n\td\'8\n\te\'8\n\tf\'8\n}'


def test_Component_detach_marks_02():

    staff = Staff("c'4 d'4 e'4 f'4")
    instrument_mark = contexttools.InstrumentMark('Violin', 'Vn.')
    instrument_mark.attach(staff)

    detached_instrument_marks = contexttools.detach_instrument_marks_attached_to_component(staff)

    r'''
    \new Staff {
        c'4
        d'4
        e'4
        f'4
    }
    '''

    assert detached_instrument_marks[0] is instrument_mark
    assert staff.lilypond_format == "\\new Staff {\n\tc'4\n\td'4\n\te'4\n\tf'4\n}"


def test_Component_detach_marks_03():

    staff = Staff("c'4 d'4 e'4 f'4")
    time_signature_mark = contexttools.TimeSignatureMark((4, 4))(staff[0])

    result = contexttools.detach_time_signature_marks_attached_to_component(staff[0])

    r'''
    \new Staff {
        c'4
        d'4
        e'4
        f'4
    }
    '''

    assert result[0] is time_signature_mark
    assert staff.lilypond_format == "\\new Staff {\n\tc'4\n\td'4\n\te'4\n\tf'4\n}"


def test_Component_detach_marks_04():

    staff = Staff("c'8 d'8 e'8 f'8")
    slur = spannertools.SlurSpanner(staff.select_leaves())
    marktools.Annotation('comment 1')(staff[0])
    marktools.Annotation('comment 2')(staff[0])
    annotations = marktools.get_annotations_attached_to_component(staff[0])
    assert len(annotations) == 2

    marktools.detach_annotations_attached_to_component(staff[0])
    annotations = marktools.get_annotations_attached_to_component(staff[0])
    assert len(annotations) == 0


def test_Component_detach_marks_05():

    staff = Staff("c'8 d'8 e'8 f'8")
    slur = spannertools.SlurSpanner(staff.select_leaves())
    marktools.Articulation('^')(staff[0])
    marktools.Articulation('.')(staff[0])
    articulations = marktools.get_articulations_attached_to_component(staff[0])
    assert len(articulations) == 2

    marktools.detach_articulations_attached_to_component(staff[0])
    articulations = marktools.get_articulations_attached_to_component(staff[0])
    assert len(articulations) == 0


def test_Component_detach_marks_06():

    staff = Staff("c'8 d'8 e'8 f'8")
    slur = spannertools.SlurSpanner(staff.select_leaves())
    marktools.LilyPondCommandMark('slurDotted')(staff[0])
    marktools.LilyPondCommandMark('slurUp')(staff[0])

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

    marktools.detach_lilypond_command_marks_attached_to_component(staff[0])

    r'''
    \new Staff {
        c'8 (
        d'8
        e'8
        f'8 )
    }
    '''

    assert wellformednesstools.is_well_formed_component(staff)
    assert staff.lilypond_format == "\\new Staff {\n\tc'8 (\n\td'8\n\te'8\n\tf'8 )\n}"


def test_Component_detach_marks_07():

    staff = Staff("c'8 d'8 e'8 f'8")
    slur = spannertools.SlurSpanner(staff.select_leaves())
    marktools.LilyPondComment('comment 1')(staff[0])
    marktools.LilyPondComment('comment 2')(staff[0])

    r'''
    \new Staff {
        % comment 1
        % comment 2
        c'8 (
        d'8
        e'8
        f'8 )
    }
    '''

    marktools.detach_lilypond_comments_attached_to_component(staff[0])

    r'''
    \new Staff {
        c'8 (
        d'8
        e'8
        f'8 )
    }
    '''

    assert wellformednesstools.is_well_formed_component(staff)
    assert staff.lilypond_format == "\\new Staff {\n\tc'8 (\n\td'8\n\te'8\n\tf'8 )\n}"


def test_Component_detach_marks_08():

    staff = Staff("c'8 d'8 e'8 f'8")
    slur = spannertools.SlurSpanner(staff.select_leaves())
    marktools.Articulation('^')(staff[0])
    marktools.LilyPondComment('comment 1')(staff[0])
    marktools.LilyPondCommandMark('slurUp')(staff[0])
    marks = staff[0].get_marks()
    assert len(marks) == 3

    marktools.detach_marks_attached_to_component(staff[0])
    marks = staff[0].get_marks()
    assert len(marks) == 0


def test_Component_detach_marks_09():

    staff = Staff("c'4 \staccato d' \marcato e' \staccato f' \marcato")
    assert len(marktools.get_marks_attached_to_components_in_expr(staff)) == 4

    marks = marktools.detach_marks_attached_to_components_in_expr(staff)
    assert marks == (
        marktools.Articulation('staccato'),
        marktools.Articulation('marcato'),
        marktools.Articulation('staccato'),
        marktools.Articulation('marcato'))

    assert not len(staff.get_marks())


def test_Component_detach_marks_10():

    staff = Staff("c'8 d'8 e'8 f'8")
    contexttools.TimeSignatureMark((2, 4))(staff[0])
    marktools.Articulation('staccato')(staff[0])

    r'''
    \new Staff {
        \time 2/4
        c'8 -\staccato
        d'8
        e'8
        f'8
    }
    '''

    marktools.detach_noncontext_marks_attached_to_component(staff[0])

    r'''
    \new Staff {
        \time 2/4
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert staff.lilypond_format == "\\new Staff {\n\t\\time 2/4\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_Component_detach_marks_11():

    note = Note("c'4")
    stem_tremolo = marktools.StemTremolo(16)(note)

    attached_stem_tremolo = marktools.get_stem_tremolo_attached_to_component(note)
    assert attached_stem_tremolo is stem_tremolo

    stem_tremolos = marktools.detach_stem_tremolos_attached_to_component(note)
    assert len(stem_tremolos) == 1
    assert stem_tremolos[0] is stem_tremolo
