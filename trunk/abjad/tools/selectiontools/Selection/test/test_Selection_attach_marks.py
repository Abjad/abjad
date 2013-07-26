from abjad import *


def test_Selection_attach_marks_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    annotation = marktools.Annotation('foo', 'bar')
    staff[:].attach_marks(annotation)

    for leaf in staff.select_leaves():
        new_annotation = leaf.get_marks(marktools.Annotation)[0]
        assert new_annotation == annotation
        assert new_annotation is not annotation


def test_Selection_attach_marks_02():

    staff = Staff("c'8 d'8 e'8 f'8")
    lilypond_comment = marktools.LilyPondComment('foo', 'right')
    staff[:].attach_marks(lilypond_comment)

    r'''
    \new Staff {
        c'8 % foo
        d'8 % foo
        e'8 % foo
        f'8 % foo
    }
    '''

    assert staff.lilypond_format == "\\new Staff {\n\tc'8 % foo\n\td'8 % foo\n\te'8 % foo\n\tf'8 % foo\n}"


def test_Selection_attach_marks_03():

    staff = Staff("c'8 d'8 e'8 f'8")
    lilypond_command_mark = marktools.LilyPondCommandMark('stemUp')
    staff[:].attach_marks(lilypond_command_mark)


    r'''
    \new Staff {
        \stemUp
        c'8
        \stemUp
        d'8
        \stemUp
        e'8
        \stemUp
        f'8
    }
    '''

    for leaf in staff.select_leaves():
        new_lilypond_command_mark = \
            leaf.get_marks(marktools.LilyPondCommandMark)[0]
        assert new_lilypond_command_mark == lilypond_command_mark
        assert new_lilypond_command_mark is not lilypond_command_mark

    assert staff.lilypond_format == "\\new Staff {\n\t\\stemUp\n\tc'8\n\t\\stemUp\n\td'8\n\t\\stemUp\n\te'8\n\t\\stemUp\n\tf'8\n}"
