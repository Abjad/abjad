from abjad import *


def test_LilyPondComment_opening_01():
    '''Opening comments in container.'''

    t = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(t[:])
    marktools.LilyPondComment('Voice opening comments here.', 'opening')(t)
    marktools.LilyPondComment('More voice opening comments.', 'opening')(t)

    r'''
    \new Voice {
        % Voice opening comments here.
        % More voice opening comments.
        c'8 [
        d'8
        e'8
        f'8 ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\t% Voice opening comments here.\n\t% More voice opening comments.\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n}"


def test_LilyPondComment_opening_02():
    '''Opening comments on leaf.'''

    t = Note(0, (1, 8))
    t.override.beam.thickness = 3
    marktools.LilyPondComment('Leaf opening comments here.', 'opening')(t)
    marktools.LilyPondComment('More leaf opening comments.', 'opening')(t)

    r'''
    \once \override Beam #'thickness = #3
    % Leaf opening comments here.
    % More leaf opening comments.
    c'8
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\once \\override Beam #'thickness = #3\n% Leaf opening comments here.\n% More leaf opening comments.\nc'8"
