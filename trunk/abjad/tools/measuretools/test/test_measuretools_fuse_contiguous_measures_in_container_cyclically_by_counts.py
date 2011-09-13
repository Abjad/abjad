from abjad import *


def test_measuretools_fuse_contiguous_measures_in_container_cyclically_by_counts_01():
    '''Docs.'''

    t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 5)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)

    r'''
    \new Staff {
        {
            \time 2/8
            c'8
            d'8
        }
        {
            \time 2/8
            e'8
            f'8
        }
        {
            \time 2/8
            g'8
            a'8
        }
        {
            \time 2/8
            b'8
            c''8
        }
        {
            \time 2/8
            d''8
            e''8
        }
    }
    '''

    part_counts = (2, 1)
    measuretools.fuse_contiguous_measures_in_container_cyclically_by_counts(t, part_counts)

    r'''
    \new Staff {
        {
            \time 4/8
            c'8
            d'8
            e'8
            f'8
        }
        {
            \time 2/8
            g'8
            a'8
        }
        {
            \time 4/8
            b'8
            c''8
            d''8
            e''8
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\t{\n\t\t\\time 4/8\n\t\tc'8\n\t\td'8\n\t\te'8\n\t\tf'8\n\t}\n\t{\n\t\t\\time 2/8\n\t\tg'8\n\t\ta'8\n\t}\n\t{\n\t\t\\time 4/8\n\t\tb'8\n\t\tc''8\n\t\td''8\n\t\te''8\n\t}\n}"


def test_measuretools_fuse_contiguous_measures_in_container_cyclically_by_counts_02():
    '''Docs.'''

    t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 5)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)

    r'''
    \new Staff {
        {
            \time 2/8
            c'8
            d'8
        }
        {
            \time 2/8
            e'8
            f'8
        }
        {
            \time 2/8
            g'8
            a'8
        }
        {
            \time 2/8
            b'8
            c''8
        }
        {
            \time 2/8
            d''8
            e''8
        }
    }
    '''

    part_counts = (3, )
    measuretools.fuse_contiguous_measures_in_container_cyclically_by_counts(t, part_counts)

    r'''
    \new Staff {
        {
            \time 6/8
            c'8
            d'8
            e'8
            f'8
            g'8
            a'8
        }
        {
            \time 4/8
            b'8
            c''8
            d''8
            e''8
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\t{\n\t\t\\time 6/8\n\t\tc'8\n\t\td'8\n\t\te'8\n\t\tf'8\n\t\tg'8\n\t\ta'8\n\t}\n\t{\n\t\t\\time 4/8\n\t\tb'8\n\t\tc''8\n\t\td''8\n\t\te''8\n\t}\n}"
