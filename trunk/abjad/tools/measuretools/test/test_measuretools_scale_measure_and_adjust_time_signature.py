from abjad import *
import py.test


def test_measuretools_scale_measure_and_adjust_time_signature_01():
    '''Scale power-of-two to non-power-of-two.
    No note head rewriting necessary.
    '''

    t = Measure((3, 8), "c'8 d'8 e'8")
    measuretools.scale_measure_and_adjust_time_signature(t, Duration(2, 3))

    r'''
    {
        \time 3/12
        \scaleDurations #'(2 . 3) {
            c'8
            d'8
            e'8
        }
    }
    '''

    assert wellformednesstools.is_well_formed_component(t)
    assert t.lilypond_format == "{\n\t\\time 3/12\n\t\\scaleDurations #'(2 . 3) {\n\t\tc'8\n\t\td'8\n\t\te'8\n\t}\n}"



def test_measuretools_scale_measure_and_adjust_time_signature_02():
    '''Scale non-power-of-two time signature to power-of-two.
    No note head rewriting necessary.
    '''

    t = Measure((3, 12), "c'8 d'8 e'8")
    measuretools.scale_measure_and_adjust_time_signature(t, Duration(3, 2))

    r'''
    {
        \time 3/8
        c'8
        d'8
        e'8
    }
    '''

    assert wellformednesstools.is_well_formed_component(t)
    assert t.lilypond_format == "{\n\t\\time 3/8\n\tc'8\n\td'8\n\te'8\n}"


def test_measuretools_scale_measure_and_adjust_time_signature_03():
    '''Scale power-of-two time signature to power-of-two time signature.
    Noteheads rewrite with dots.
    '''

    t = Measure((3, 8), "c'8 d'8 e'8")
    measuretools.scale_measure_and_adjust_time_signature(t, Duration(3, 2))

    r'''
    {
        \time 9/16
        c'8.
        d'8.
        e'8.
    }
    '''

    assert wellformednesstools.is_well_formed_component(t)
    assert t.lilypond_format == "{\n\t\\time 9/16\n\tc'8.\n\td'8.\n\te'8.\n}"


def test_measuretools_scale_measure_and_adjust_time_signature_04():
    '''Scale power-of-two time signature to power-of-two time signature.
    Noteheads rewrite without dots.
    '''

    t = Measure((9, 16), "c'8. d'8. e'8.")
    measuretools.scale_measure_and_adjust_time_signature(t, Duration(2, 3))

    r'''
    {
        \time 3/8
        c'8
        d'8
        e'8
    }
    '''

    assert wellformednesstools.is_well_formed_component(t)
    assert t.lilypond_format == "{\n\t\\time 3/8\n\tc'8\n\td'8\n\te'8\n}"


def test_measuretools_scale_measure_and_adjust_time_signature_05():
    '''Scale power-of-two time signature to non-power-of-two time signature.
    No note head rewriting necessary.
    '''

    t = Measure((9, 16), "c'16 d'16 e'16 f'16 g'16 a'16 b'16 c''16 d''16")
    measuretools.scale_measure_and_adjust_time_signature(t, Duration(2, 3))

    r'''
    {
        \time 9/24
        \scaleDurations #'(2 . 3) {
            c'16
            d'16
            e'16
            f'16
            g'16
            a'16
            b'16
            c''16
            d''16
        }
    }
    '''

    assert wellformednesstools.is_well_formed_component(t)
    assert t.lilypond_format == "{\n\t\\time 9/24\n\t\\scaleDurations #'(2 . 3) {\n\t\tc'16\n\t\td'16\n\t\te'16\n\t\tf'16\n\t\tg'16\n\t\ta'16\n\t\tb'16\n\t\tc''16\n\t\td''16\n\t}\n}"


def test_measuretools_scale_measure_and_adjust_time_signature_06():
    '''Scale non-power-of-two time signature to power-of-two time signature.
    Noteheads rewrite with double duration.
    '''

    t = Measure((3, 12), "c'8 d'8 e'8")
    measuretools.scale_measure_and_adjust_time_signature(t, Duration(3))

    r'''
    {
        \time 3/4
        c'4
        d'4
        e'4
    }
    '''

    assert wellformednesstools.is_well_formed_component(t)
    assert t.lilypond_format == "{\n\t\\time 3/4\n\tc'4\n\td'4\n\te'4\n}"


def test_measuretools_scale_measure_and_adjust_time_signature_07():
    '''Scale power-of-two time signature by one half.
    Noteheads rewrite with half duration.
    Time signature rewrites with double denominator.
    '''

    t = Measure((6, 16), "c'16 d'16 e'16 f'16 g'16 a'16")
    measuretools.scale_measure_and_adjust_time_signature(t, Duration(1, 2))

    r'''
    {
        \time 6/32
        c'32
        d'32
        e'32
        f'32
        g'32
        a'32
    }
    '''

    assert wellformednesstools.is_well_formed_component(t)
    assert t.lilypond_format == "{\n\t\\time 6/32\n\tc'32\n\td'32\n\te'32\n\tf'32\n\tg'32\n\ta'32\n}"


def test_measuretools_scale_measure_and_adjust_time_signature_08():
    '''Scale power-of-two time signature by one quarter.
    Noteheads rewrite with quarter duration.
    Time signature rewrites with quadruple denominator.
    '''

    t = Measure((6, 16), "c'16 d'16 e'16 f'16 g'16 a'16")
    measuretools.scale_measure_and_adjust_time_signature(t, Duration(1, 4))

    r'''
    {
        \time 6/64
        c'64
        d'64
        e'64
        f'64
        g'64
        a'64
    }
    '''

    assert wellformednesstools.is_well_formed_component(t)
    assert t.lilypond_format == "{\n\t\\time 6/64\n\tc'64\n\td'64\n\te'64\n\tf'64\n\tg'64\n\ta'64\n}"


def test_measuretools_scale_measure_and_adjust_time_signature_09():
    '''Scale power-of-two time signature by two.
    Noteheads rewrite with double duration.
    Time signature rewrites with half denominator.
    '''

    t = Measure((6, 16), "c'16 d'16 e'16 f'16 g'16 a'16")
    measuretools.scale_measure_and_adjust_time_signature(t, Duration(2))

    r'''
    {
        \time 6/8
        c'8
        d'8
        e'8
        f'8
        g'8
        a'8
    }
    '''

    assert wellformednesstools.is_well_formed_component(t)
    assert t.lilypond_format == "{\n\t\\time 6/8\n\tc'8\n\td'8\n\te'8\n\tf'8\n\tg'8\n\ta'8\n}"


def test_measuretools_scale_measure_and_adjust_time_signature_10():
    '''Scale power-of-two time signature by four.
    Noteheads rewrite with quadruple duration.
    Time signature rewrites with quarter denominator.
    '''

    t = Measure((6, 16), "c'16 d'16 e'16 f'16 g'16 a'16")
    measuretools.scale_measure_and_adjust_time_signature(t, Duration(4))

    r'''
    {
        \time 6/4
        c'4
        d'4
        e'4
        f'4
        g'4
        a'4
    }
    '''

    assert wellformednesstools.is_well_formed_component(t)
    assert t.lilypond_format == "{\n\t\\time 6/4\n\tc'4\n\td'4\n\te'4\n\tf'4\n\tg'4\n\ta'4\n}"


def test_measuretools_scale_measure_and_adjust_time_signature_11():
    '''Raise ZeroDivisionError when multiplier equals zero.
    '''

    t = Measure((6, 16), "c'16 d'16 e'16 f'16 g'16 a'16")
    py.test.raises(ZeroDivisionError, 'measuretools.scale_measure_and_adjust_time_signature(t, 0)')
