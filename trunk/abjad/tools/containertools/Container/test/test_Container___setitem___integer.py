from abjad import *
import py.test


def test_Container___setitem___integer_01():
    '''Spanned leaves exchange correctly.'''

    t = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(t[:2])
    spannertools.GlissandoSpanner(t.leaves)

    r'''
    \new Voice {
        c'8 [ \glissando
        d'8 ] \glissando
        e'8 \glissando
        f'8
    }
    '''

    t[1] = Note(12, (1, 8))

    r'''
    \new Voice {
        c'8 [ \glissando
        c''8 ] \glissando
        e'8 \glissando
        f'8
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\tc'8 [ \\glissando\n\tc''8 ] \\glissando\n\te'8 \\glissando\n\tf'8\n}"


def test_Container___setitem___integer_02():
    '''Spanned leaf hands position over to container correctly.'''

    t = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(t[:2])
    spannertools.GlissandoSpanner(t.leaves)

    r'''
    \new Voice {
        c'8 [ \glissando
        d'8 ] \glissando
        e'8 \glissando
        f'8
    }
    '''

    t[1] = Container(notetools.make_repeated_notes(3, Duration(1, 16)))

    r'''
    \new Voice {
        c'8 [ \glissando
        {
            c'16 \glissando
            c'16 \glissando
            c'16 ] \glissando
        }
        e'8 \glissando
        f'8
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\tc'8 [ \\glissando\n\t{\n\t\tc'16 \\glissando\n\t\tc'16 \\glissando\n\t\tc'16 ] \\glissando\n\t}\n\te'8 \\glissando\n\tf'8\n}"


def test_Container___setitem___integer_03():
    '''Directly spanned contains hand over correctly to a single leaf.
        Note here that only the sequentials are initially spanned.'''

    t = Voice(Container(notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    spannertools.BeamSpanner(t[:])
    spannertools.GlissandoSpanner(t[:])

    r'''
    \new Voice {
        {
            c'8 [ \glissando
            d'8 \glissando
        }
        {
            e'8 \glissando
            f'8 ]
        }
    }
    '''

    t[1] = Note(12, (1, 8))

    r'''
    \new Voice {
        {
            c'8 [ \glissando
            d'8 \glissando
        }
        c''8 ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [ \\glissando\n\t\td'8 \\glissando\n\t}\n\tc''8 ]\n}"


def test_Container___setitem___integer_04():
    '''Indirectly spanned containers hand over correctly to a single leaf.
        Notice here that only LEAVES are initially spanned.'''

    t = Voice(Container(notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    spannertools.BeamSpanner(t.leaves)
    spannertools.GlissandoSpanner(t.leaves)

    r'''
    \new Voice {
        {
            c'8 [ \glissando
            d'8 \glissando
        }
        {
            e'8 \glissando
            f'8 ]
        }
    }
    '''

    t[1] = Note(12, (1, 8))

    r'''
    \new Voice {
        {
            c'8 [ \glissando
            d'8 \glissando
        }
        c''8 ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [ \\glissando\n\t\td'8 \\glissando\n\t}\n\tc''8 ]\n}"


def test_Container___setitem___integer_05():
    '''Directly spanned containers hand over to other containers correctly.'''

    t = Voice(Container(notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    spannertools.BeamSpanner(t[:])
    spannertools.GlissandoSpanner(t[:])

    r'''
    \new Voice {
        {
            c'8 [ \glissando
            d'8 \glissando
        }
        {
            e'8 \glissando
            f'8 ]
        }
    }
    '''

    t[1] = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")

    r'''
    \new Voice {
        {
            c'8 [ \glissando
            d'8 \glissando
        }
        \times 2/3 {
            c'8 \glissando
            d'8 \glissando
            e'8 ]
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [ \\glissando\n\t\td'8 \\glissando\n\t}\n\t\\times 2/3 {\n\t\tc'8 \\glissando\n\t\td'8 \\glissando\n\t\te'8 ]\n\t}\n}"


def test_Container___setitem___integer_06():
    '''Indirectly spanned containers hand over correctly to a single leaf.'''

    t = Voice(Container(notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    spannertools.BeamSpanner(t.leaves)
    spannertools.GlissandoSpanner(t.leaves)

    r'''
    \new Voice {
        {
            c'8 [ \glissando
            d'8 \glissando
        }
        {
            e'8 \glissando
            f'8 ]
        }
    }
    '''

    t[1] = Note(12, (1, 8))

    r'''
    \new Voice {
        {
            c'8 [ \glissando
            d'8 \glissando
        }
        c''8 ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [ \\glissando\n\t\td'8 \\glissando\n\t}\n\tc''8 ]\n}"


def test_Container___setitem___integer_07():
    '''Indirectly HALF-spanned containers hand over correctly to a
    single leaf. WOW!'''

    t = Voice(Container(notetools.make_repeated_notes(4)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    spannertools.BeamSpanner(t.leaves[0:6])
    r'''
    \new Voice {
        {
            c'8 [
            d'8
            e'8
            f'8
        }
        {
            g'8
            a'8 ]
            b'8
            c''8
        }
    }
    '''

    t[1] = Rest((1, 2))

    r'''
    \new Voice {
        {
            c'8 [
            d'8
            e'8
            f'8 ]
        }
        r2
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [\n\t\td'8\n\t\te'8\n\t\tf'8 ]\n\t}\n\tr2\n}"


def test_Container___setitem___integer_08():
    '''Take spanned leaf from donor container
        and insert into recipient container.
        Both donor and recipient check after set item.'''

    notes = [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8"), Note("g'8"), Note("a'8")]

    t = Voice(notes[:3])
    spannertools.BeamSpanner(t[:])

    r'''
    \new Voice {
        c'8 [
        d'8
        e'8 ]
    }
    '''

    u = Voice(notes[3:])
    spannertools.BeamSpanner(u[:])

    r'''
    \new Voice {
        f'8 [
        g'8
        a'8 ]
    }
    '''

    t[1] = u[1]

    "Modified t:"

    r'''
    \new Voice {
        c'8 [
        g'8
        e'8 ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\tc'8 [\n\tg'8\n\te'8 ]\n}"

    "Modified u:"

    r'''
    \new Voice {
        f'8 [
        a'8 ]
    }
    '''

    assert componenttools.is_well_formed_component(u)
    assert u.format == "\\new Voice {\n\tf'8 [\n\ta'8 ]\n}"


def test_Container___setitem___integer_09():
    '''Take down-spanned container with completely covered spanner
        from donor container and insert into recipient container.
        Both donor and recipient check after set item.'''

    notes = [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8"), Note("g'8"), Note("a'8"), Note("b'8")]

    t = Voice(notes[:3])
    spannertools.BeamSpanner(t[:])

    r'''
    \new Voice {
        c'8 [
        d'8
        e'8 ]
    }
    '''

    u = Voice(notes[3:])
    Container(u[1:3])
    spannertools.GlissandoSpanner(u.leaves)
    spannertools.SlurSpanner(u[1].leaves)

    r'''
    \new Voice {
        f'8 \glissando
        {
            g'8 \glissando (
            a'8 \glissando )
        }
        b'8
    }
    '''

    t[1] = u[1]

    "Voice t is now ..."

    r'''
    \new Voice {
        c'8 [
        {
            g'8 (
            a'8 )
        }
        e'8 ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\tc'8 [\n\t{\n\t\tg'8 (\n\t\ta'8 )\n\t}\n\te'8 ]\n}"

    "Voice u is now ..."

    r'''
    \new Voice {
        f'8 \glissando
        b'8
    }
    '''

    assert componenttools.is_well_formed_component(u)
    assert u.format == "\\new Voice {\n\tf'8 \\glissando\n\tb'8\n}"
