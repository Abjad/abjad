from abjad import *


def test_Container___imul___01():

    t = Voice("c'8 d'8")
    beamtools.BeamSpanner(t[:])
    t *= 2

    r'''
    \new Voice {
        c'8 [
        d'8 ]
        c'8 [
        d'8 ]
    }
    '''

    assert wellformednesstools.is_well_formed_component(t)
    assert t.lilypond_format == "\\new Voice {\n\tc'8 [\n\td'8 ]\n\tc'8 [\n\td'8 ]\n}"


def test_Container___imul___02():

    t = Voice("c'8 d'8")
    beamtools.BeamSpanner(t[:])
    t *= 1

    r'''
    \new Voice {
        c'8 [
        d'8 ]
    }
    '''

    assert wellformednesstools.is_well_formed_component(t)
    assert t.lilypond_format == "\\new Voice {\n\tc'8 [\n\td'8 ]\n}"


def test_Container___imul___03():

    t = Voice("c'8 d'8")
    beamtools.BeamSpanner(t[:])
    t *= 0

    r'''
    \new Voice {
    }
    '''

    assert wellformednesstools.is_well_formed_component(t)
    assert t.lilypond_format == '\\new Voice {\n}'
