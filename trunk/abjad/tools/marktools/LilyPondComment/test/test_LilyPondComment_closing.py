from abjad import *


def test_LilyPondComment_closing_01():
    '''Test container comments closing.'''

    t = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(t[:])
    marktools.LilyPondComment('Voice closing comments here.', 'closing')(t)
    marktools.LilyPondComment('More voice closing comments.', 'closing')(t)

    r'''
    \new Voice {
        c'8 [
        d'8
        e'8
        f'8 ]
        % Voice closing comments here.
        % More voice closing comments.
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n\t% Voice closing comments here.\n\t% More voice closing comments.\n}"


def test_LilyPondComment_closing_02():
    '''Test leaf comments closing.'''

    t = Note(0, (1, 8))
    t.override.beam.thickness = 3
    marktools.LilyPondComment('Leaf closing comments here.', 'closing')(t)
    marktools.LilyPondComment('More leaf closing comments.', 'closing')(t)

    r'''
    \once \override Beam #'thickness = #3
    c'8
    % Leaf closing comments here.
    % More leaf closing comments.
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\once \\override Beam #'thickness = #3\nc'8\n% Leaf closing comments here.\n% More leaf closing comments."
